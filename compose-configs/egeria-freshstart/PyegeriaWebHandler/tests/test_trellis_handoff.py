# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Freshstart's Portal -> trellis (Egeria Advisor, Resource Explorer) SSO handoff.

Freshstart hands off as the signed-in user, around that user's own Egeria token
from the portal session (no personas, no password handling). The shared parts
(trellis_sso.py and demo_config's URL helpers) stay identical to quickstart's.
"""
import ast
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

_REPO = _MODULE_DIR.parents[2]
_QS = _REPO / "compose-configs" / "egeria-quickstart" / "PyegeriaWebHandler"

SSO_SECRET = "test-sso-secret-not-real"
PORTAL_SECRET = "test-portal-jwt-secret-not-real"


def _fake_egeria_token(exp_offset: int) -> str:
    return jwt.encode({"sub": "erin", "exp": int(time.time()) + exp_offset}, "egeria-side", algorithm="HS256")


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("EGERIA_ADVISOR_SSO_SECRET", SSO_SECRET)
    monkeypatch.setenv("JWT_SECRET", PORTAL_SECRET)
    # test freshstart's own defaults, whatever the host container sets
    monkeypatch.delenv("EGERIA_ADVISOR_URL", raising=False)
    monkeypatch.delenv("EGERIA_RESOURCE_EXPLORER_URL", raising=False)
    for m in ("demo_config", "trellis_sso", "demo_auth_handler", "advisor_handler", "resource_explorer_handler"):
        sys.modules.pop(m, None)
    import advisor_handler
    import resource_explorer_handler
    import demo_auth_handler

    async def _up():
        return True
    monkeypatch.setattr(advisor_handler, "_advisor_reachable", _up)
    monkeypatch.setattr(resource_explorer_handler, "_resource_explorer_reachable", _up)
    a = FastAPI()
    a.include_router(advisor_handler.router)
    a.include_router(resource_explorer_handler.router)
    a.state.mods = (advisor_handler, resource_explorer_handler, demo_auth_handler)
    yield a
    for m in ("demo_config", "trellis_sso", "demo_auth_handler", "advisor_handler", "resource_explorer_handler"):
        sys.modules.pop(m, None)


def _session_cookie(app, egeria_token, user_id="erin", role="user", display="Erin Overview"):
    demo_auth_handler = app.state.mods[2]
    return {"demo_token": demo_auth_handler._make_jwt(user_id, role, display, egeria_token)}


@pytest.mark.parametrize("path,url_key,port", [
    ("/api/advisor/handoff", "advisor_sso_url", 7880),
    ("/api/resource-explorer/handoff", "resource_explorer_sso_url", 7810),
])
def test_handoff_carries_the_signed_in_users_own_token(app, path, url_key, port):
    egeria_token = _fake_egeria_token(600)
    c = TestClient(app, cookies=_session_cookie(app, egeria_token, role="admin"))
    r = c.post(path, json={}, headers={"x-forwarded-host": "fs.example.test:7843"})
    assert r.status_code == 200, r.text
    url = r.json()[url_key]
    assert url.startswith(f"http://fs.example.test:{port}/#pt=")
    claims = jwt.decode(url.split("#pt=", 1)[1], SSO_SECRET, algorithms=["HS256"])
    assert claims["sub"] == "erin"
    assert claims["role"] == "admin"
    assert claims["display_name"] == "Erin Overview"
    assert claims["egeria_token"] == egeria_token
    assert 0 < claims["exp"] - claims["iat"] <= 120
    assert "egeria_password" not in claims and "password" not in claims


@pytest.mark.parametrize("path", ["/api/advisor/handoff", "/api/resource-explorer/handoff"])
def test_handoff_needs_a_signed_in_user(app, path):
    r = TestClient(app).post(path, json={})
    assert r.status_code == 401


@pytest.mark.parametrize("path", ["/api/advisor/handoff", "/api/resource-explorer/handoff"])
def test_expired_egeria_session_token_is_refused_not_handed_on(app, path):
    c = TestClient(app, cookies=_session_cookie(app, _fake_egeria_token(-60)))
    r = c.post(path, json={})
    assert r.status_code == 401
    assert "sign in again" in r.json()["detail"]


@pytest.mark.parametrize("path", ["/api/advisor/handoff", "/api/resource-explorer/handoff"])
def test_handoff_is_503_without_the_shared_secret(app, monkeypatch, path):
    for mod in app.state.mods[:2]:
        monkeypatch.setattr(mod, "EGERIA_ADVISOR_SSO_SECRET", "")
    c = TestClient(app, cookies=_session_cookie(app, _fake_egeria_token(600)))
    assert c.post(path, json={}).status_code == 503


@pytest.mark.parametrize("path", ["/api/advisor/status", "/api/resource-explorer/status"])
def test_status_is_public(app, monkeypatch, path):
    r = TestClient(app).get(path)
    assert r.status_code == 200
    assert r.json() == {"reachable": True, "sso_configured": True}
    for mod in app.state.mods[:2]:
        monkeypatch.setattr(mod, "EGERIA_ADVISOR_SSO_SECRET", "")
    assert TestClient(app).get(path).json()["sso_configured"] is False


def test_trellis_sso_is_identical_to_quickstarts():
    assert (_MODULE_DIR / "trellis_sso.py").read_bytes() == (_QS / "trellis_sso.py").read_bytes()


def _functions(path: Path) -> dict:
    src = path.read_text()
    tree = ast.parse(src)
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out[node.name] = ast.get_source_segment(src, node)
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            out[node.targets[0].id] = ast.get_source_segment(src, node)
    return out


@pytest.mark.parametrize("name", ["advisor_check_urls", "browser_facing_url", "resource_explorer_check_urls",
                                  "_first_valid_host", "_LOOPBACK_HOSTS", "_VALID_HOST_RE"])
def test_url_helpers_match_quickstarts(name):
    fs, qs = _functions(_MODULE_DIR / "demo_config.py"), _functions(_QS / "demo_config.py")
    assert fs[name] == qs[name]


def test_portal_registers_both_handoff_routers():
    src = (_MODULE_DIR / "pyegeria_handler.py").read_text()
    assert "app.include_router(advisor_router)" in src
    assert "app.include_router(resource_explorer_router)" in src


def test_report_viewer_still_reports_no_persona_handoff():
    """report_viewer.resolve_viewer imports quickstart-only persona helpers; freshstart must not grow them."""
    import resource_explorer_handler
    assert not hasattr(resource_explorer_handler, "_load_personas")
    assert not hasattr(resource_explorer_handler, "_require_verified_or_local")


@pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")
def test_gen_env_keeps_the_trellis_settings(tmp_path):
    """gen-env.sh rewrites .env from scratch; the three trellis keys must survive, nothing else extra."""
    fs = tmp_path / "compose-configs" / "egeria-freshstart"
    infra = tmp_path / "compose-configs" / "shared-infra"
    fs.mkdir(parents=True)
    infra.mkdir(parents=True)
    shutil.copy2(_REPO / "compose-configs" / "egeria-freshstart" / "gen-env.sh", fs / "gen-env.sh")
    shutil.copy2(_REPO / "compose-configs" / "shared-infra" / "detect-engine.sh", infra / "detect-engine.sh")
    (fs / ".env").write_text(
        "HOST_FQDN=old\n"
        "EGERIA_ADVISOR_URL=https://advisor.example.test/\n"
        "EGERIA_RESOURCE_EXPLORER_URL=\n"
        "EGERIA_ADVISOR_SSO_SECRET=dummy-value\n"
        "SOMETHING_ELSE=dropped\n")
    env = {**os.environ, "CONTAINER_ENGINE": "docker", "COMPOSE_CMD": "docker compose"}
    subprocess.run(["bash", str(fs / "gen-env.sh")], check=True, capture_output=True, env=env, cwd=fs)
    lines = (fs / ".env").read_text().splitlines()
    assert "EGERIA_ADVISOR_URL=https://advisor.example.test/" in lines
    assert "EGERIA_ADVISOR_SSO_SECRET=dummy-value" in lines
    assert not any(l.startswith("EGERIA_RESOURCE_EXPLORER_URL=") for l in lines)   # empty: not carried
    assert not any(l.startswith("SOMETHING_ELSE=") for l in lines)
    assert any(l.startswith("HOST_FQDN=") and l != "HOST_FQDN=old" for l in lines)
    # a second run keeps them too (and does not duplicate them)
    subprocess.run(["bash", str(fs / "gen-env.sh")], check=True, capture_output=True, env=env, cwd=fs)
    lines = (fs / ".env").read_text().splitlines()
    assert lines.count("EGERIA_ADVISOR_SSO_SECRET=dummy-value") == 1
