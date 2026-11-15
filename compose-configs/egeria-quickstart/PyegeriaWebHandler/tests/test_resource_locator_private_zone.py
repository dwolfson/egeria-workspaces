"""Resource Locator private notes use the Locator's own secured zone (PO-13, owner's decision "Dedicated zone",
DESIGN-PO13-RESOURCE-LOCATOR-PRIVATE-ZONE-2026-11-15 part 2).

- a new note is re-zoned to [resource-locator-private, <user>], never to RE's resource-explorer-private;
- reads mark a note protected when it carries either secured zone (migrated and unmigrated notes alike);
- a re-zone failure still says, in words, that other people may be able to read the note (502);
- a source guard: nothing in the Locator writes resource-explorer-private any more.
The add route is driven for real (its Egeria clients are fakes that record the calls)."""
import asyncio
import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import resource_browser_handler as rb  # noqa: E402


@pytest.fixture
def egeria(monkeypatch):
    calls = {"zoned": [], "linked": [], "rezone_fails": False}

    class Profile:
        async def _async_journal_my_activity(self, body):
            calls["journal"] = body
            return "note-guid-1"

    class Explorer:
        async def _async_add_zone_membership(self, guid, body):
            if calls["rezone_fails"]:
                raise RuntimeError("Egeria refused the classification")
            calls["zoned"].append((guid, body["properties"]["zoneMembership"]))

    class Expert:
        async def _async_create_related_elements(self, body):
            calls["linked"].append(body)

    async def profile():
        return Profile()

    async def explorer():
        return Explorer()

    async def expert():
        return Expert()

    async def notes(guid):
        return {"notes": []}

    monkeypatch.setattr(rb, "_my_profile_async", profile)
    monkeypatch.setattr(rb, "_explorer_async", explorer)
    monkeypatch.setattr(rb, "_expert_async", expert)
    monkeypatch.setattr(rb, "get_private_notes", notes)
    monkeypatch.setattr(rb, "_require_signed_in", lambda: "peterprofile")
    return calls


def _add(text="a private thought"):
    return asyncio.run(rb.add_private_note("res-1", rb.PrivateNoteBody(text=text, resourceName="Sales DB")))


def test_a_new_note_is_zoned_to_the_locators_own_zone_and_the_author(egeria):
    _add()
    assert egeria["zoned"] == [("note-guid-1", ["resource-locator-private", "peterprofile"])]
    assert rb._PRIVATE_ZONE == "resource-locator-private"


def test_a_rezone_failure_still_says_others_may_read_it(egeria):
    egeria["rezone_fails"] = True
    with pytest.raises(HTTPException) as ei:
        _add()
    assert ei.value.status_code == 502
    assert "other people may be able to read it" in ei.value.detail
    assert egeria["linked"] == []          # nothing linked to the resource after a failed re-zone


def _entry(zones):
    return {"elementHeader": {"guid": "n1", "zoneMembership": {"classificationProperties": {"zoneMembership": zones}}},
            "properties": {"description": "t", "additionalProperties": {"resourceGUID": "res-1"}}}


@pytest.mark.parametrize("zones,protected", [
    (["resource-locator-private", "peterprofile"], True),    # written by this code
    (["resource-explorer-private", "peterprofile"], True),   # written before PO-13, not yet migrated
    (["peterprofile"], False),                                # older notes: the userId zone alone
    ([], False),
])
def test_reads_mark_either_secured_zone_as_protected(zones, protected):
    rec = rb._private_note_record(_entry(zones))
    assert rec["protected"] is protected and rec["zones"] == zones and rec["private"] is True


def test_the_locator_never_writes_res_zone():
    src = (ROOT / "resource_browser_handler.py").read_text()
    # the old zone is named exactly once: in the read-side set of protected zones
    assert src.count('"resource-explorer-private"') == 1
    line = next(ln for ln in src.splitlines() if '"resource-explorer-private"' in ln)
    assert line.startswith("_PROTECTED_ZONES = frozenset(")
    assert '"zoneMembership": [_PRIVATE_ZONE, user]' in src


def test_the_stale_comment_is_gone():
    src = (ROOT / "resource_browser_handler.py").read_text()
    assert "everyone can still read the entry" not in src
    assert "e9fd817f4c" in src
