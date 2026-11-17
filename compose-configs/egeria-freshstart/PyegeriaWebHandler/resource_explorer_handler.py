"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Resource Explorer portal handoff (freshstart) — same "trellis" family app as
Egeria Advisor (see advisor_handler.py), same SSO handoff. No exclusive lock:
Resource Explorer is multi-user, so this is a reachability check plus a token
mint.

Identity is the signed-in freshstart user, with their own Egeria token (see
advisor_handler.py's docstring for why this differs from quickstart's
persona-based handoff). This module deliberately has no _load_personas /
_require_verified_or_local: report_viewer.py treats their absence as "this
environment has no persona-based Resource Explorer viewer", which is right
for freshstart.
"""

import time

import httpx
from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from advisor_handler import session_sso_token
from demo_config import (
    EGERIA_ADVISOR_SSO_SECRET,
    EGERIA_RESOURCE_EXPLORER_URL,
    browser_facing_url,
    resource_explorer_check_urls,
)

router = APIRouter(prefix="/api/resource-explorer", tags=["resource-explorer"])


# Same TTL-cached reachability pattern as advisor_handler.py's
# _advisor_reachable — avoids hitting the remote host on every status poll.
_reachable_cache = {"ok": False, "checked_at": 0.0}
_REACHABLE_TTL_SECONDS = 15


async def _resource_explorer_reachable() -> bool:
    now = time.time()
    if now - _reachable_cache["checked_at"] < _REACHABLE_TTL_SECONDS:
        return _reachable_cache["ok"]
    ok = False
    for check_url in resource_explorer_check_urls():
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
async def resource_explorer_status():
    """Public — reachability + whether SSO is configured. No lock state to report."""
    reachable = await _resource_explorer_reachable()
    return {
        "reachable":      reachable,
        "sso_configured": bool(EGERIA_ADVISOR_SSO_SECRET),
    }


@router.post("/handoff")
async def handoff(request: Request):
    """Mint an SSO handoff URL for the signed-in user. No lock to acquire."""
    if not EGERIA_ADVISOR_SSO_SECRET:
        raise HTTPException(status_code=503, detail="Resource Explorer SSO is not configured (EGERIA_ADVISOR_SSO_SECRET unset)")
    try:
        sso_token = session_sso_token(request)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"resource explorer: SSO token minting failed: {exc}")
        raise HTTPException(status_code=502, detail="Could not prepare Resource Explorer session")

    base = browser_facing_url(EGERIA_RESOURCE_EXPLORER_URL, request, 7810)
    resource_explorer_sso_url = f"{base.rstrip('/')}/#pt={sso_token}"
    return {"ok": True, "resource_explorer_sso_url": resource_explorer_sso_url}
