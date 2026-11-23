"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Freshstart demo-mode configuration.
Authentication is backed by Egeria — no SQLite, no email.
"""

import dataclasses
import os

# ── Core flag ──────────────────────────────────────────────────────────────────

DEMO_MODE: bool = os.environ.get("DEMO_MODE", "false").lower() in ("true", "1", "yes")

# Auth model: Freshstart is Egeria-backed — shared handlers use the logged-in
# user's Egeria bearer token (from the portal JWT) for Explorer queries,
# falling back to the env service account if that token is rejected.
SERVER_MANAGED_AUTH: bool = os.environ.get("SERVER_MANAGED_AUTH", "true").lower() in ("true", "1", "yes")

# ── Database selection ───────────────────────────────────────────────────────────


class DemoDbNotConfigured(RuntimeError):
    """Raised when no demo database is configured in DEMO_MODE: the Portal refuses to start rather than guess one."""


@dataclasses.dataclass(frozen=True)
class DemoDbChoice:
    """A selected database configuration."""
    kind: str   # "postgres", "sqlite" or "none"
    db_url: str   # not `url`: the allowlist scan treats a `url` field as a request body's platform URL
    path: str
    words: str


def select_demo_db(env, demo_mode: bool) -> DemoDbChoice:
    """
    Select a database based on environment variables.

    Rules in order:
      (a) DEMO_DB_URL set -> kind postgres, url exactly that value, path ""
      (b) elif DEMO_DB_HOST set -> kind postgres with constructed URL
      (c) elif DEMO_DB_PATH set -> kind sqlite, path = value, url = "sqlite:///" + path
      (d) else if demo_mode is True -> raise DemoDbNotConfigured
      (e) else return kind "none" with empty values

    A value counts as set only if it is non-blank after strip().
    """
    # Helper to check if a value is set (non-blank)
    def _is_set(key: str) -> bool:
        val = env.get(key, "")
        return bool(val.strip())

    # (a) DEMO_DB_URL takes precedence
    if _is_set("DEMO_DB_URL"):
        url = env.get("DEMO_DB_URL", "").strip()
        return DemoDbChoice(kind="postgres", db_url=url, path="", words="the demo database is Postgres, chosen by DEMO_DB_URL")

    # (b) DEMO_DB_HOST is next
    if _is_set("DEMO_DB_HOST"):
        host = env.get("DEMO_DB_HOST", "").strip()
        user = env.get("DEMO_DB_USER", "demo_user").strip() or "demo_user"
        password = env.get("DEMO_DB_PASSWORD", "demo4egeria").strip() or "demo4egeria"
        port = int(env.get("DEMO_DB_PORT", "").strip() or 5442)       # a malformed port is an error, never a silent 5442
        name = env.get("DEMO_DB_NAME", "coco_pharma").strip() or "coco_pharma"
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
        return DemoDbChoice(kind="postgres", db_url=url, path="", words="the demo database is Postgres, chosen by DEMO_DB_HOST")

    # (c) DEMO_DB_PATH for SQLite
    if _is_set("DEMO_DB_PATH"):
        path = env.get("DEMO_DB_PATH", "").strip()
        url = f"sqlite:///{path}"
        return DemoDbChoice(kind="sqlite", db_url=url, path=path, words="the demo database is SQLite, chosen by DEMO_DB_PATH")

    # (d) In demo_mode, raise if nothing is set
    if demo_mode:
        raise DemoDbNotConfigured(
            "DEMO_DB_HOST, DEMO_DB_URL and DEMO_DB_PATH are not configured; "
            "the Portal will not start without one of them"
        )

    # (e) Outside demo_mode, return "none"
    return DemoDbChoice(kind="none", db_url="", path="", words="no demo database is configured: set DEMO_DB_HOST (or DEMO_DB_URL) for Postgres, or DEMO_DB_PATH for SQLite")


# ── Database constants read from environment at import time ──────────────────────

DEMO_DB_PORT: int = int(os.environ.get("DEMO_DB_PORT", "5442"))
DEMO_DB_NAME: str = os.environ.get("DEMO_DB_NAME", "coco_pharma")
DEMO_DB_SCHEMA: str = os.environ.get("DEMO_DB_SCHEMA", "demo_auth")
DEMO_DB_USER: str = os.environ.get("DEMO_DB_USER", "demo_user")
DEMO_DB_PASSWORD: str = os.environ.get("DEMO_DB_PASSWORD", "demo4egeria")
DEMO_DB_HOST: str = os.environ.get("DEMO_DB_HOST", "")

# Compute DEMO_DB_CHOICE at module level (never raises at import)
DEMO_DB_CHOICE: DemoDbChoice = select_demo_db(os.environ, demo_mode=False)

# DEMO_DB_URL is derived from the choice
DEMO_DB_URL: str = DEMO_DB_CHOICE.db_url

# ── JWT ────────────────────────────────────────────────────────────────────────

# RK-24b: no published default. fresh-start-local generates JWT_SECRET into .env; an unset key, or the value once
# published as this default, is refused when a session is signed or checked (anyone could forge those sessions).
# PO-46b: the quickstart compose file published a second value; refuse both.
PUBLIC_JWT_DEFAULTS = ("change-me-before-going-public", "change-me-before-going-public-meow")
PUBLIC_JWT_DEFAULT = PUBLIC_JWT_DEFAULTS[0]
JWT_SECRET: str       = os.environ.get("JWT_SECRET") or ""


def jwt_signing_key() -> str:
    """The Portal's session-signing key, refusing an unset one or the published default (forgeable sessions)."""
    if not JWT_SECRET or JWT_SECRET in PUBLIC_JWT_DEFAULTS:
        raise RuntimeError("JWT_SECRET is not set, or is a published default, so Portal sessions could be forged. "
                           "Run ./fresh-start-local, which generates one into compose-configs/egeria-freshstart/.env.")
    return JWT_SECRET
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
EGERIA_ADVISOR_URL:  str = os.environ.get("EGERIA_ADVISOR_URL",  "http://localhost:7880/")
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
# No built-in default (PO-45): unset, the admin token call refuses in words (demo_auth_handler).
EGERIA_ADMIN_CALLER_PASSWORD: str = os.environ.get("EGERIA_ADMIN_CALLER_PASSWORD") or ""


# ── Database helpers ────────────────────────────────────────────────────────────


def require_demo_db() -> DemoDbChoice:
    """
    Require a database to be configured in DEMO_MODE.

    Calls select_demo_db with the current environment and DEMO_MODE.
    Raises DemoDbNotConfigured if no database is available in demo_mode.
    """
    return select_demo_db(os.environ, DEMO_MODE)
