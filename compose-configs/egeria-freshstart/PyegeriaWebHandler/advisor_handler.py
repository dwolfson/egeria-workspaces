"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Egeria Advisor portal handoff (freshstart) — the "trellis" family app, same
SSO handoff mechanism as quickstart's advisor_handler.py via trellis_sso.py.
No exclusive lock: Advisor is multi-user (its own login and session store).

Identity — by design different from quickstart
------------------------------------------------
Quickstart hands off as the Coco *persona* the browser picked, minting a fresh
Egeria token from that persona's password. Freshstart has no personas: every
portal user signs in to freshstart's own Egeria (server-managed auth), and the
session already carries that user's Egeria bearer token. So the handoff is
always the signed-in user, and the token handed on is their own — the portal
never handles a password here.

Because the token is freshstart's, the Advisor / Resource Explorer instance at
EGERIA_ADVISOR_URL / EGERIA_RESOURCE_EXPLORER_URL must target freshstart's Egeria
(8443, fs-view-server), not quickstart's.
"""

import time
from types import SimpleNamespace

import httpx
from fastapi import APIRouter, HTTPException, Request
from jose import JWTError, jwt
from loguru import logger

from demo_config import (
    EGERIA_ADVISOR_SSO_SECRET,
    EGERIA_ADVISOR_URL,
    advisor_check_urls,
    browser_facing_url,
)
from trellis_sso import encode_portal_sso_token

router = APIRouter(prefix="/api/advisor", tags=["advisor"])


def _egeria_token_expired(token: str) -> bool:
    """True when the Egeria token's exp claim is in the past (read unverified; Egeria verifies it)."""
    try:
        exp = jwt.get_unverified_claims(token).get("exp")
    except JWTError:
        return False
    return isinstance(exp, (int, float)) and exp <= time.time()


def session_sso_token(request: Request) -> str:
    """Mint the trellis SSO JWT for the signed-in portal user, around their own Egeria token.

    401 when nobody is signed in, or when the session's Egeria token has expired
    (the trellis app would only reject it); the user signs in again for a fresh one.
    """
    from demo_auth_handler import require_user
    user = require_user(request)
    if not user.egeria_token or _egeria_token_expired(user.egeria_token):
        raise HTTPException(status_code=401, detail="Your Egeria session has expired; sign in again")
    # trellis_sso's claim shape reads .id / .role from the Portal user (quickstart's User model)
    portal_user = SimpleNamespace(id=user.user_id, role=user.role)
    return encode_portal_sso_token(portal_user, user.user_id, {"display_name": user.display_name},
                                   user.egeria_token)


# Same TTL-cached reachability pattern as quickstart — avoids hitting the
# remote host on every client's status poll.
_reachable_cache = {"ok": False, "checked_at": 0.0}
_REACHABLE_TTL_SECONDS = 15


async def _advisor_reachable() -> bool:
    now = time.time()
    if now - _reachable_cache["checked_at"] < _REACHABLE_TTL_SECONDS:
        return _reachable_cache["ok"]
    ok = False
    for check_url in advisor_check_urls():
        try:
            async with httpx.AsyncClient(verify=False, timeout=1.5) as client:
                await client.head(check_url)
            ok = True
            break
        except Exception:
            continue
    _reachable_cache.update(ok=ok, checked_at=now)
    return ok


@router.get("/status")
async def advisor_status():
    """Public — reachability + whether SSO is configured. No lock state to report."""
    reachable = await _advisor_reachable()
    return {
        "reachable":      reachable,
        "sso_configured": bool(EGERIA_ADVISOR_SSO_SECRET),
    }


@router.post("/handoff")
async def handoff(request: Request):
    """Mint an SSO handoff URL for the signed-in user. No lock to acquire."""
    if not EGERIA_ADVISOR_SSO_SECRET:
        raise HTTPException(status_code=503, detail="Egeria Advisor SSO is not configured (EGERIA_ADVISOR_SSO_SECRET unset)")
    try:
        sso_token = session_sso_token(request)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"advisor: SSO token minting failed: {exc}")
        raise HTTPException(status_code=502, detail="Could not prepare Advisor session")

    base = browser_facing_url(EGERIA_ADVISOR_URL, request, 7880)
    advisor_sso_url = f"{base.rstrip('/')}/#pt={sso_token}"
    return {"ok": True, "advisor_sso_url": advisor_sso_url}
