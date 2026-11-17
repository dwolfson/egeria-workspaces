"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Freshstart demo-mode configuration.
Authentication is backed by Egeria — no SQLite, no email.
"""

import os
import re

# ── Core flag ──────────────────────────────────────────────────────────────────

DEMO_MODE: bool = os.environ.get("DEMO_MODE", "false").lower() in ("true", "1", "yes")

# Auth model: Freshstart is Egeria-backed — shared handlers use the logged-in
# user's Egeria bearer token (from the portal JWT) for Explorer queries,
# falling back to the env service account if that token is rejected.
SERVER_MANAGED_AUTH: bool = os.environ.get("SERVER_MANAGED_AUTH", "true").lower() in ("true", "1", "yes")

# ── Database (PostgreSQL on egeria-shared-postgres:5442, demo schema) ──────────
# Shared with quickstart — same coco_pharma DB, same demo.feedback table.

DEMO_DB_HOST:     str = os.environ.get("DEMO_DB_HOST",     "egeria-shared-postgres")
DEMO_DB_PORT:     int = int(os.environ.get("DEMO_DB_PORT", "5442"))
DEMO_DB_NAME:     str = os.environ.get("DEMO_DB_NAME",     "coco_pharma")
DEMO_DB_SCHEMA:   str = os.environ.get("DEMO_DB_SCHEMA",   "demo_auth")
DEMO_DB_USER:     str = os.environ.get("DEMO_DB_USER",     "demo_user")
DEMO_DB_PASSWORD: str = os.environ.get("DEMO_DB_PASSWORD", "demo4egeria")
DEMO_DB_URL:      str = (
    f"postgresql+psycopg2://{DEMO_DB_USER}:{DEMO_DB_PASSWORD}"
    f"@{DEMO_DB_HOST}:{DEMO_DB_PORT}/{DEMO_DB_NAME}"
)

# ── JWT ────────────────────────────────────────────────────────────────────────

JWT_SECRET: str       = os.environ.get("JWT_SECRET", "change-me-before-going-public")
JWT_ALGORITHM: str    = "HS256"
JWT_EXPIRY_USER_SEC: int  = int(os.environ.get("JWT_EXPIRY_USER_SECONDS",  "7200"))    # 2 h
JWT_EXPIRY_ADMIN_SEC: int = int(os.environ.get("JWT_EXPIRY_ADMIN_SECONDS", "604800"))  # 7 d

# ── Egeria ─────────────────────────────────────────────────────────────────────

EGERIA_PLATFORM_URL: str  = os.environ.get("EGERIA_PLATFORM_URL", "https://localhost:9443").rstrip("/")
EGERIA_VIEW_SERVER: str   = os.environ.get("EGERIA_VIEW_SERVER", "fs-view-server")
# Name registered by the Egeria platform in the metadata store (platform.name in application.properties).
EGERIA_PLATFORM_NAME: str = os.environ.get("EGERIA_PLATFORM_NAME", "OMAG Server Platform")

# User IDs granted admin role in the portal (Egeria handles its own RBAC separately).
# Comma-separated; bootstrap always included.
EGERIA_ADMIN_USERS: set[str] = {
    u.strip()
    for u in os.environ.get("EGERIA_ADMIN_USERS", "bootstrap").split(",")
    if u.strip()
}

# ── URLs ───────────────────────────────────────────────────────────────────────

SITE_URL: str = os.environ.get("SITE_URL", "https://localhost:7843").rstrip("/")

# Optional integrations — set in .env, not in yaml
EGERIA_ADVISOR_URL:  str = os.environ.get("EGERIA_ADVISOR_URL",  "")

# Portal -> trellis (Egeria Advisor, Resource Explorer) SSO handoff, as in
# quickstart's demo_config. EGERIA_ADVISOR_SSO_SECRET is the HS256 secret shared
# with Advisor's ADVISOR_PORTAL_SECRET and Resource Explorer's
# TRELLIS_PORTAL_SECRET; left empty, both tiles show "Not configured" and the
# handoff routes return 503. Unlike quickstart, both URLs default to empty, and
# a tile and its handoff stay inert ("Not configured") until its URL is set: the
# trellis instance must target freshstart's own Egeria (8443, fs-view-server),
# because the handoff carries the signed-in user's freshstart Egeria token, so
# there is no safe default (a localhost default could reach quickstart's trellis).
# The usual freshstart ports are Advisor 7880 and Resource Explorer 7810.
EGERIA_ADVISOR_SSO_SECRET: str = os.environ.get("EGERIA_ADVISOR_SSO_SECRET", "")
EGERIA_RESOURCE_EXPLORER_URL: str = os.environ.get("EGERIA_RESOURCE_EXPLORER_URL", "")
OBSIDIAN_VAULT_URL:  str = os.environ.get("OBSIDIAN_VAULT_URL",  "")
OBSIDIAN_GITHUB_URL: str = os.environ.get("OBSIDIAN_GITHUB_URL", "https://github.com/odpi/egeria-workspaces/tree/main/coco-workbooks")

# ── User directory ─────────────────────────────────────────────────────────────

EGERIA_USER_SECRETS_PATH: str = os.environ.get("EGERIA_USER_SECRETS_PATH", "/secrets/user-directory.omsecrets")

# ── Admin service account ───────────────────────────────────────────────────────
# Used to obtain a fresh Egeria bearer token for SecurityOfficer and admin API
# calls. The portal admin JWT lasts 7 days but the Egeria bearer token it carries
# expires sooner; this account's credentials are used to re-authenticate as needed.
# Set EGERIA_ADMIN_CALLER_PASSWORD in .env — never in yaml.

EGERIA_ADMIN_CALLER_ID: str       = os.environ.get("EGERIA_ADMIN_CALLER_ID", "bootstrap")
EGERIA_ADMIN_CALLER_PASSWORD: str = os.environ.get("EGERIA_ADMIN_CALLER_PASSWORD", "secret")


# ── Trellis tile URLs (verbatim from quickstart's demo_config) ────────────────

def advisor_check_urls() -> list:
    """URLs to try, in order, when checking if Advisor is reachable from inside
    this container. Always includes EGERIA_ADVISOR_URL itself (the public/real
    value), plus a host.docker.internal variant as a fallback — Advisor runs
    directly on the host, not in this compose network, and a public hostname
    routing back to this same machine may hit hairpin-NAT issues or simply not
    be port-forwarded (during setup) even though it works for real external
    users. Swapping just the hostname keeps EGERIA_ADVISOR_URL itself unchanged
    for anything sent to a browser.
    """
    if not EGERIA_ADVISOR_URL:
        return []
    from urllib.parse import urlsplit, urlunsplit
    parts = urlsplit(EGERIA_ADVISOR_URL)
    if parts.hostname in (None, "host.docker.internal"):
        return [EGERIA_ADVISOR_URL]
    port = f":{parts.port}" if parts.port else ""
    userinfo = f"{parts.username}{':' + parts.password if parts.password else ''}@" if parts.username else ""
    fallback_netloc = f"{userinfo}host.docker.internal{port}"
    fallback = urlunsplit((parts.scheme, fallback_netloc, parts.path, parts.query, parts.fragment))
    return [EGERIA_ADVISOR_URL, fallback]


# ── Browser-facing tile URLs ──────────────────────────────────────────────────
# EGERIA_ADVISOR_URL / EGERIA_RESOURCE_EXPLORER_URL are handed straight to the
# browser, so they must name a host the *browser* can reach -- not one this
# container can reach. A single configured value cannot do that for a
# deployment reached under several names (localhost on the box, a Tailscale
# MagicDNS name from a laptop, a public FQDN from outside), and the localhost
# defaults are wrong for every browser that is not on this machine.
#
# The portal already solves this for Jupyter, entirely client-side, in
# demo-portal.html:
#     'http://' + window.location.hostname + ':8888/?token=egeria'
# i.e. derive the host at click time from however the user reached the portal.
# These two tiles cannot do that in the browser, because their URL carries an
# SSO token minted server-side -- so we do the same derivation here, from the
# request that asked for the handoff.
#
# An explicitly configured non-loopback host always wins: a public deployment
# that must send users to a fixed URL (behind a CDN, or a different origin than
# the portal) keeps working exactly as before.

_LOOPBACK_HOSTS = {None, "", "localhost", "127.0.0.1", "::1", "host.docker.internal"}


_VALID_HOST_RE = re.compile(
    r"^(\[[0-9A-Fa-f:.]+\]|[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?)(:\d{1,5})?$")


def _first_valid_host(header_value) -> str:
    """First entry of an X-Forwarded-Host value that is a plausible host[:port].

    Skips junk entries (a misconfigured proxy once sent "i=99, localhost:8843");
    returns "" when none is valid so the caller falls back to the Host header.
    """
    for entry in (header_value or "").split(","):
        entry = entry.strip()
        if entry and _VALID_HOST_RE.match(entry):
            return entry
    return ""


def browser_facing_url(configured: str, request, default_port: int) -> str:
    """Resolve a tile URL that the caller's browser can actually reach.

    Returns `configured` untouched when it names a real (non-loopback) host.
    Otherwise rebuilds it against the hostname the browser used to reach the
    portal, preserving the configured scheme, port and path.
    """
    from urllib.parse import urlsplit, urlunsplit

    parts = urlsplit(configured or "")
    if parts.hostname not in _LOOPBACK_HOSTS:
        return configured

    # Behind Apache, ProxyPreserveHost/X-Forwarded-Host carry the browser's
    # host; fall back to the request URL for direct (unproxied) access.
    forwarded = _first_valid_host(request.headers.get("x-forwarded-host"))
    host = forwarded or request.headers.get("host", "") or (request.url.hostname or "")
    # Drop the browser's port (the tile has its own); keep a bracketed IPv6 literal whole.
    m = re.match(r"^(\[[^\]]+\]|[^:]+)(?::\d+)?$", host)
    host = (m.group(1) if m else host).strip("[]")
    if not host:
        return configured

    port = parts.port or default_port
    scheme = parts.scheme or "http"
    netloc = f"[{host}]:{port}" if ":" in host else f"{host}:{port}"
    return urlunsplit((scheme, netloc, parts.path or "/", parts.query, parts.fragment))


def resource_explorer_check_urls() -> list:
    """Same host.docker.internal-fallback pattern as advisor_check_urls() —
    see that function's docstring for the full rationale."""
    if not EGERIA_RESOURCE_EXPLORER_URL:
        return []
    from urllib.parse import urlsplit, urlunsplit
    parts = urlsplit(EGERIA_RESOURCE_EXPLORER_URL)
    if parts.hostname in (None, "host.docker.internal"):
        return [EGERIA_RESOURCE_EXPLORER_URL]
    port = f":{parts.port}" if parts.port else ""
    userinfo = f"{parts.username}{':' + parts.password if parts.password else ''}@" if parts.username else ""
    fallback_netloc = f"{userinfo}host.docker.internal{port}"
    fallback = urlunsplit((parts.scheme, fallback_netloc, parts.path, parts.query, parts.fragment))
    return [EGERIA_RESOURCE_EXPLORER_URL, fallback]
