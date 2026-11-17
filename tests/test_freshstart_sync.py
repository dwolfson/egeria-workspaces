"""SHARE-3 drift check: freshstart's Portal files match quickstart's as compose-configs/freshstart-sync-manifest.json says.

Quickstart is the source. If this fails, edit the file in compose-configs/egeria-quickstart/PyegeriaWebHandler/ (not
freshstart's copy), run `python3 compose-configs/sync-freshstart.py --write`, and commit both. A new Portal file must
be classified in the manifest. The other tests here exercise the script on a throwaway tree.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "compose-configs" / "sync-freshstart.py"

_spec = importlib.util.spec_from_file_location("sync_freshstart", SCRIPT)
sync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sync)


def test_freshstart_is_in_sync_with_quickstart():
    r = subprocess.run([sys.executable, str(SCRIPT), "--check"], capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0, r.stdout + r.stderr


# ── the script itself, on a throwaway tree (no git: it walks the files) ──────────────────────────────────────────

def _tree(tmp_path: Path, files: dict[str, tuple[bytes | None, bytes | None]], manifest: dict) -> Path:
    for rel, (qs, fs) in files.items():
        for sub, data in ((sync.SOURCE, qs), (sync.TARGET, fs)):
            if data is not None:
                p = tmp_path / sub / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
    m = {"transforms": {"view-server": [["qs-view-server", "fs-view-server"]]}, **manifest}
    (tmp_path / "manifest.json").write_text(json.dumps(m))
    return tmp_path


def _check(root: Path):
    return sync.check(root, root / "manifest.json")


def test_in_sync_tree_passes(tmp_path):
    root = _tree(tmp_path, {"a.py": (b"x\n", b"x\n"), "b.py": (b"s='qs-view-server'\n", b"s='fs-view-server'\n"),
                            "only_qs.py": (b"q\n", None)},
                 {"identical": ["a.py"], "transformed": {"b.py": {"transforms": ["view-server"]}},
                  "by_design": {"only_qs.py": "quickstart-only"}})
    assert _check(root)[0] == []


def test_drift_is_reported_with_the_fix_and_write_fixes_it(tmp_path):
    root = _tree(tmp_path, {"a.py": (b"new\n", b"old\n"), "b.py": (b"s='qs-view-server'\n", b"s='qs-view-server'\n")},
                 {"identical": ["a.py"], "transformed": {"b.py": {"transforms": ["view-server"]}}})
    fail, _ = _check(root)
    assert len(fail) == 1 and "a.py" in fail[0] and "b.py" in fail[0] and sync.FIX in fail[0]
    assert sorted(sync.write([], root, root / "manifest.json")) == ["a.py", "b.py"]
    assert (root / sync.TARGET / "b.py").read_bytes() == b"s='fs-view-server'\n"
    assert (root / sync.SOURCE / "a.py").read_bytes() == b"new\n"          # quickstart is never written
    assert _check(root)[0] == []


def test_unclassified_and_stale_entries_fail(tmp_path):
    root = _tree(tmp_path, {"new.py": (b"n\n", None)}, {"identical": ["gone.py"], "not_yet": {"x/**": "row 9"}})
    fail = " | ".join(_check(root)[0])
    assert "unclassified (quickstart): new.py" in fail
    assert "stale identical entry" in fail and "gone.py" in fail
    assert "stale not_yet entry" in fail and "x/**" in fail


def test_pending_is_a_note_until_in_sync_then_fails(tmp_path):
    m = {"pending": {"p.py": {"after": "#999"}}}
    root = _tree(tmp_path, {"p.py": (b"new\n", b"old\n")}, m)
    fail, note = _check(root)
    assert fail == [] and any("#999" in n for n in note)
    (root / sync.TARGET / "p.py").write_bytes(b"new\n")
    fail, _ = _check(root)
    assert len(fail) == 1 and "move p.py to identical" in fail[0]


def test_not_yet_shrinks(tmp_path):
    root = _tree(tmp_path, {"n.py": (b"same\n", b"same\n"), "t/x.py": (b"same\n", b"same\n")},
                 {"not_yet": {"n.py": "row 6", "t/**": "tests"}})
    fail = " | ".join(_check(root)[0])
    assert "move n.py to identical" in fail
    assert "add t/x.py to identical" in fail


def test_fenced_freshstart_block_is_kept(tmp_path):
    qs = b"one\ntwo\nthree\n"
    fs = b"one\ntwo\n# FRESHSTART-ONLY BEGIN\nfs line\n# FRESHSTART-ONLY END\nthree\n"
    root = _tree(tmp_path, {"f.py": (qs, fs)}, {"transformed": {"f.py": {"transforms": ["fences"]}}})
    assert _check(root)[0] == []
    (root / sync.SOURCE / "f.py").write_bytes(b"one\ntwo\nthree\nfour\n")
    assert _check(root)[0]
    assert sync.write(["f.py"], root, root / "manifest.json") == ["f.py"]
    assert (root / sync.TARGET / "f.py").read_bytes() == \
        b"one\ntwo\n# FRESHSTART-ONLY BEGIN\nfs line\n# FRESHSTART-ONLY END\nthree\nfour\n"


def test_fence_without_a_unique_anchor_is_refused(tmp_path):
    root = _tree(tmp_path, {"f.py": (b"x\nx\n", b"x\n# FRESHSTART-ONLY BEGIN\nb\n# FRESHSTART-ONLY END\nx\n")},
                 {"transformed": {"f.py": {"transforms": ["fences"]}}})
    fail = _check(root)[0]
    assert fail and "no unique place" in fail[0]


def test_write_refuses_an_unsynced_entry(tmp_path):
    root = _tree(tmp_path, {"d.py": (b"q\n", b"f\n")}, {"by_design": {"d.py": "on purpose"}})
    with pytest.raises(sync.SyncError):
        sync.write(["d.py"], root, root / "manifest.json")
    assert (root / sync.TARGET / "d.py").read_bytes() == b"f\n"


def test_manifest_categories_do_not_overlap():
    m = json.loads(sync.MANIFEST.read_text())
    seen: dict[str, str] = {}
    for cat in sync.CATEGORIES:
        for p in sync._entries(m, cat):
            assert p not in seen, f"{p} is in both {seen[p]} and {cat}"
            seen[p] = cat
