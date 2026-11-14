"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

studio_handler: "Edit in Studio" (owner decision C). Studio and Egeria are faked; what is tested is the Portal's
side: it asks as the user whose X-Egeria-Token came with the request (never the service user), it trades the
trellis SSO JWT at Studio once and caches the session per user and token, it trades again once on a 401, every
failure is "unknown" with its reason (never "no", never a guess), and the hand-off names the artifact and
carries the token only in the fragment.
"""
import asyncio
import base64
import json
import time

import pytest

import studio_handler


def _egeria_token(sub="peterprofile", ttl=3600):
    b = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    now = int(time.time())
    return f"{b({'alg': 'RS256'})}.{b({'sub': sub, 'iat': now, 'exp': now + ttl})}.sig"


class _Resp:
    def __init__(self, status, payload=None):
        self.status_code, self._payload = status, payload

    def json(self):
        return self._payload


class _FakeStudio:
    """Records calls; answers /api/auth/portal and /api/can-edit as told."""
    def __init__(self, exchange=200, answers=None):
        self.exchange, self.answers, self.calls = exchange, list(answers or []), []

    def client(self, *a, **k):
        studio = self

        class _C:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *exc):
                return False

            async def post(self, url, json=None):
                studio.calls.append(("post", url, json))
                if studio.exchange != 200:
                    return _Resp(studio.exchange, {})
                n = sum(1 for c in studio.calls if c[0] == "post")
                return _Resp(200, {"access_token": f"studio-session-{n}"})

            async def get(self, url, params=None, headers=None):
                studio.calls.append(("get", url, params, headers))
                status, body = studio.answers.pop(0)
                return _Resp(status, body)
        return _C()


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    studio_handler._sessions.clear()
    monkeypatch.setattr("demo_config.EGERIA_ADVISOR_SSO_SECRET", "test-secret-0123456789abcdef0123", raising=False)
    monkeypatch.setattr("demo_config.EGERIA_STUDIO_API_URL", "http://studio.test:8840", raising=False)
    monkeypatch.setattr("demo_config.EGERIA_STUDIO_URL", "https://studio.example/", raising=False)
    import trellis_sso
    monkeypatch.setattr(trellis_sso, "EGERIA_ADVISOR_SSO_SECRET", "test-secret-0123456789abcdef0123", raising=False)
    yield
    studio_handler._sessions.clear()


def _as(monkeypatch, token):
    import egeria_auth
    monkeypatch.setattr(egeria_auth, "get_request_token", lambda: token)
    monkeypatch.setattr(egeria_auth, "token_user", lambda: egeria_auth._token_sub(token) if token else None)


def _run(coro):
    return asyncio.run(coro)


def test_not_signed_in_is_unknown_and_studio_is_not_asked(monkeypatch):
    studio = _FakeStudio()
    monkeypatch.setattr(studio_handler.httpx, "AsyncClient", studio.client)
    _as(monkeypatch, None)
    out = _run(studio_handler.can_edit(kind="sheet", ref="catalog-health"))
    assert out["answer"] == "unknown" and "not signed in" in out["why"] and studio.calls == []


def test_yes_as_the_user_and_the_session_is_cached(monkeypatch):
    studio = _FakeStudio(answers=[(200, {"answer": "yes", "why": ""}), (200, {"answer": "no", "why": "not yours"})])
    monkeypatch.setattr(studio_handler.httpx, "AsyncClient", studio.client)
    tok = _egeria_token("peterprofile")
    _as(monkeypatch, tok)
    assert _run(studio_handler.can_edit(kind="sheet", ref="catalog-health")) == {"answer": "yes", "why": ""}
    assert _run(studio_handler.can_edit(kind="spec", ref="X")) == {"answer": "no", "why": "not yours"}
    posts = [c for c in studio.calls if c[0] == "post"]
    assert len(posts) == 1 and posts[0][1] == "http://studio.test:8840/api/auth/portal"
    from jose import jwt
    claims = jwt.get_unverified_claims(posts[0][2]["portal_token"])
    assert claims["sub"] == "peterprofile" and claims["egeria_token"] == tok   # the user's own token
    gets = [c for c in studio.calls if c[0] == "get"]
    assert gets[0][2] == {"kind": "sheet", "ref": "catalog-health"}
    assert gets[0][3] == {"Authorization": "Bearer studio-session-1"}


def test_a_401_trades_again_once(monkeypatch):
    studio = _FakeStudio(answers=[(401, {}), (200, {"answer": "yes"})])
    monkeypatch.setattr(studio_handler.httpx, "AsyncClient", studio.client)
    _as(monkeypatch, _egeria_token())
    assert _run(studio_handler.can_edit(kind="spec", ref="X"))["answer"] == "yes"
    assert [c[0] for c in studio.calls] == ["post", "get", "post", "get"]


@pytest.mark.parametrize("exchange,answers,words", [
    (503, [], "not configured on Studio"),
    (401, [], "refused the Portal sign-in"),
    (200, [(500, {})], "HTTP 500"),
    (200, [(200, {"answer": "probably"})], "not yes/no/unknown"),
])
def test_every_failure_is_unknown_with_its_reason(monkeypatch, exchange, answers, words):
    studio = _FakeStudio(exchange=exchange, answers=answers)
    monkeypatch.setattr(studio_handler.httpx, "AsyncClient", studio.client)
    _as(monkeypatch, _egeria_token())
    out = _run(studio_handler.can_edit(kind="spec", ref="X"))
    assert out["answer"] == "unknown" and words in out["why"]


def test_unreachable_studio_is_unknown(monkeypatch):
    import httpx

    def boom(*a, **k):
        raise httpx.ConnectError("refused")
    monkeypatch.setattr(studio_handler.httpx, "AsyncClient", boom)
    _as(monkeypatch, _egeria_token())
    out = _run(studio_handler.can_edit(kind="sheet", ref="x"))
    assert out["answer"] == "unknown" and "not reachable" in out["why"]


def test_no_sso_secret_is_unknown(monkeypatch):
    monkeypatch.setattr("demo_config.EGERIA_ADVISOR_SSO_SECRET", "", raising=False)
    _as(monkeypatch, _egeria_token())
    out = _run(studio_handler.can_edit(kind="sheet", ref="x"))
    assert out["answer"] == "unknown" and "SSO is not configured" in out["why"]


def test_bad_kind_is_400():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as e:
        _run(studio_handler.can_edit(kind="report", ref="x"))
    assert e.value.status_code == 400


class _Req:
    def __init__(self):
        self.headers = {"host": "portal.example"}

        class _U:
            hostname = "portal.example"
        self.url = _U()


def test_handoff_names_the_artifact_and_keeps_the_token_in_the_fragment(monkeypatch):
    tok = _egeria_token("peterprofile")
    _as(monkeypatch, tok)
    out = _run(studio_handler.handoff(_Req(), studio_handler.HandoffRequest(kind="sheet", label="catalog health")))
    url = out["studio_sso_url"]
    assert url.startswith("https://studio.example/?open=sheet:catalog%20health#pt=")
    from jose import jwt
    claims = jwt.get_unverified_claims(url.split("#pt=", 1)[1])
    assert claims["sub"] == "peterprofile" and claims["exp"] - claims["iat"] <= 120


def test_handoff_needs_a_signed_in_user(monkeypatch):
    from fastapi import HTTPException
    _as(monkeypatch, None)
    with pytest.raises(HTTPException) as e:
        _run(studio_handler.handoff(_Req(), studio_handler.HandoffRequest(kind="spec", label="X")))
    assert e.value.status_code == 401


def test_pages_show_the_link_only_on_yes():
    from pathlib import Path
    here = Path(__file__).resolve().parents[1]
    sheets = (here / "local-dashboards.html").read_text()
    assert "if (!v || v.answer !== 'yes') {" in sheets
    assert "studioEditLink('sheet', sheet.name" in sheets
    explorer = (here / "type-explorer.html").read_text()
    assert "if (answer !== 'yes') return null;" in explorer
    assert "if (spec.source !== 'egeria' || !label) return;" in explorer


def test_expired_sessions_are_pruned_on_insert(monkeypatch):
    studio = _FakeStudio(answers=[(200, {"answer": "yes"})])
    monkeypatch.setattr(studio_handler.httpx, "AsyncClient", studio.client)
    studio_handler._sessions[("old-user", "abc")] = ("stale", time.time() - 10)
    _as(monkeypatch, _egeria_token())
    _run(studio_handler.can_edit(kind="spec", ref="X"))
    assert ("old-user", "abc") not in studio_handler._sessions and len(studio_handler._sessions) == 1
