"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Trellis Studio from the Portal: "Edit in Studio" (owner decision C, 2026-11-14: shown wherever the signed-in user
can edit that spec or sheet). The Portal can't decide edit rights itself, so it asks Studio, as the user:

  GET  /api/studio/status     reachability + whether SSO is configured
  GET  /api/studio/can-edit   ?kind=spec|sheet&ref=<label or qualified name>  ->  {answer: yes|no|unknown, why}
  POST /api/studio/handoff    {kind, label} -> {ok, studio_sso_url}: Studio at /?open=<kind>:<label>#pt=<token>

Who asks: the user whose Egeria bearer token came with the request (X-Egeria-Token), never the Portal's service
user. The Portal signs its usual trellis SSO JWT around that token (trellis_sso.encode_portal_sso_token), trades it
at Studio's POST /api/auth/portal for a Studio session (cached per user and token until shortly before it expires,
traded again once on a 401, exactly as re_analytics.py does with Resource Explorer), and calls Studio's
/api/can-edit with it.

Absence is an answer: every failure (not signed in, SSO not configured, Studio unreachable, a refused sign-in, an
odd reply) is "unknown" with its reason, logged; the page shows the link only on "yes". Studio checks again when it
opens the artifact: the link is a hint, never the check. The hand-off token travels in the URL fragment (never
sent to a server, cleared by Studio at once, valid two minutes), as /api/advisor/handoff does.
"""
from __future__ import annotations

import hashlib
import threading
import time
from typing import Any, Dict, Optional, Tuple
from urllib.parse import quote

import httpx
from fastapi import APIRouter, HTTPException, Request
from loguru import logger
from pydantic import BaseModel

import demo_config
from demo_config import browser_facing_url

router = APIRouter(prefix="/api/studio", tags=["studio"])

KINDS = ("spec", "sheet")
ANSWERS = ("yes", "no", "unknown")
_TIMEOUT_S = 10.0
_EXPIRY_MARGIN_S = 60.0
_sessions: Dict[Tuple[str, str], Tuple[str, float]] = {}
_sessions_lock = threading.Lock()
_reachable = {"ok": False, "checked_at": 0.0}
_REACHABLE_TTL_S = 15


class _Unknown(Exception):
    """Studio's answer couldn't be had; the message says why."""


def _caller() -> Tuple[Optional[str], Optional[str], str]:
    """(egeria_token, user_id, why-not) for this request."""
    from egeria_auth import _token_expired, get_request_token, token_user
    token = get_request_token()
    if not token:
        return None, None, "you are not signed in here (no Egeria token came with the request)"
    if _token_expired(token):
        return None, None, "your Egeria sign-in has expired"
    user = token_user()
    if not user:
        return None, None, "your Egeria token names no user"
    return token, user, ""


def _api() -> str:
    return (demo_config.EGERIA_STUDIO_API_URL or "").rstrip("/")


def _expiry(jwt_token: str) -> float:
    try:
        from jose import jwt
        exp = jwt.get_unverified_claims(jwt_token).get("exp")
        if exp:
            return float(exp)
    except Exception:  # noqa: BLE001  fall back to a short life
        pass
    return time.time() + 300


def _key(user: str, token: str) -> Tuple[str, str]:
    return user, hashlib.sha256(token.encode()).hexdigest()[:16]


async def _exchange(user: str, token: str) -> str:
    from trellis_sso import encode_portal_sso_token
    if not demo_config.EGERIA_ADVISOR_SSO_SECRET:
        raise _Unknown("Portal SSO is not configured (EGERIA_ADVISOR_SSO_SECRET is unset)")
    if not _api():
        raise _Unknown("Studio's address is not configured (EGERIA_STUDIO_API_URL)")
    portal_token = encode_portal_sso_token(None, user, {"display_name": user}, token)
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT_S) as client:
            r = await client.post(f"{_api()}/api/auth/portal", json={"portal_token": portal_token})
    except httpx.HTTPError as exc:
        raise _Unknown(f"Studio is not reachable at {_api()} ({type(exc).__name__})") from exc
    reasons = {401: "Studio refused the Portal sign-in (Egeria did not accept the token, or it expired)",
               400: "Studio says the Portal sign-in is missing claims",
               503: "Portal sign-in is not configured on Studio (TRELLIS_PORTAL_SECRET)"}
    if r.status_code != 200:
        raise _Unknown(reasons.get(r.status_code, f"Studio's sign-in answered HTTP {r.status_code}"))
    session = (r.json() or {}).get("access_token")
    if not session:
        raise _Unknown("Studio's sign-in answer carried no session")
    with _sessions_lock:
        now = time.time()
        for k in [k for k, (_s, exp) in _sessions.items() if exp <= now]:   # drop expired sessions as we go
            del _sessions[k]
        _sessions[_key(user, token)] = (session, _expiry(session))
    return session


async def _session(user: str, token: str, fresh: bool = False) -> str:
    if not fresh:
        with _sessions_lock:
            hit = _sessions.get(_key(user, token))
        if hit and hit[1] - _EXPIRY_MARGIN_S > time.time():
            return hit[0]
    return await _exchange(user, token)


async def _ask(user: str, token: str, kind: str, ref: str) -> Dict[str, Any]:
    for fresh in (False, True):
        session = await _session(user, token, fresh=fresh)
        try:
            async with httpx.AsyncClient(timeout=_TIMEOUT_S) as client:
                r = await client.get(f"{_api()}/api/can-edit", params={"kind": kind, "ref": ref},
                                     headers={"Authorization": f"Bearer {session}"})
        except httpx.HTTPError as exc:
            raise _Unknown(f"Studio is not reachable at {_api()} ({type(exc).__name__})") from exc
        if r.status_code == 401 and not fresh:
            continue   # the cached Studio session ended: trade again, once
        if r.status_code != 200:
            raise _Unknown(f"Studio's can-edit answered HTTP {r.status_code}")
        body = r.json() or {}
        if body.get("answer") not in ANSWERS:
            raise _Unknown(f"Studio answered {str(body)[:80]!r}, not yes/no/unknown")
        return {"answer": body["answer"], "why": body.get("why") or ""}
    raise _Unknown("Studio refused the session twice")


@router.get("/status")
async def studio_status():
    """Public: whether Studio answers, and whether the hand-off can be signed. Nothing about any user."""
    now = time.time()
    if now - _reachable["checked_at"] >= _REACHABLE_TTL_S:
        ok = False
        if _api():
            try:
                async with httpx.AsyncClient(timeout=1.5) as client:
                    ok = (await client.get(f"{_api()}/health")).status_code == 200
            except Exception:  # noqa: BLE001
                ok = False
        _reachable.update(ok=ok, checked_at=now)
    return {"reachable": _reachable["ok"], "sso_configured": bool(demo_config.EGERIA_ADVISOR_SSO_SECRET),
            "url_configured": bool(demo_config.EGERIA_STUDIO_URL)}


@router.get("/can-edit")
async def can_edit(kind: str, ref: str):
    """May the signed-in user edit this spec or sheet? yes / no / unknown, from Studio, as them."""
    if kind not in KINDS or not (ref or "").strip():
        raise HTTPException(status_code=400, detail="kind is spec or sheet, and ref names it.")
    token, user, why = _caller()
    if not token:
        logger.info(f"studio: can-edit {kind} {ref!r}: unknown ({why})")
        return {"answer": "unknown", "why": why}
    try:
        out = await _ask(user, token, kind, ref.strip())
    except _Unknown as exc:
        logger.info(f"studio: can-edit {kind} {ref!r} for {user}: unknown ({exc})")
        return {"answer": "unknown", "why": str(exc)}
    if out["answer"] == "unknown":
        logger.info(f"studio: can-edit {kind} {ref!r} for {user}: unknown (Studio: {out['why']})")
    return out


class HandoffRequest(BaseModel):
    kind: str
    label: str


@router.post("/handoff")
async def handoff(request: Request, body: HandoffRequest):
    """Studio's URL for opening this spec or sheet, signed in as the caller. Studio re-checks the rights."""
    if not demo_config.EGERIA_ADVISOR_SSO_SECRET:
        raise HTTPException(status_code=503, detail="Portal SSO is not configured (EGERIA_ADVISOR_SSO_SECRET unset)")
    if body.kind not in KINDS or not body.label.strip():
        raise HTTPException(status_code=400, detail="kind is spec or sheet, and label names it.")
    token, user, why = _caller()
    if not token:
        raise HTTPException(status_code=401, detail=f"Sign in first: {why}.")
    from trellis_sso import encode_portal_sso_token
    sso = encode_portal_sso_token(None, user, {"display_name": user}, token)
    base = browser_facing_url(demo_config.EGERIA_STUDIO_URL, request, 8840).rstrip("/")
    target = quote(f"{body.kind}:{body.label.strip()}", safe=":")
    return {"ok": True, "studio_sso_url": f"{base}/?open={target}#pt={sso}"}
