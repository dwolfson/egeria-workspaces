"""TR-134: the engine behind the explicit selection (tests/test_tr134_demo_db_selection.py has the selection itself).

SQLite at DEMO_DB_PATH works for register and sign-in (the Helm chart's case); an explicit Postgres host that is unreachable fails
LOUDLY and creates no SQLite file, and fails again on the next call (no half-built engine kept); nothing set is refused in words;
the Portal refuses to start in DEMO_MODE with nothing set; and the compose files that need the shared Postgres name it explicitly.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
QS = ROOT / "compose-configs" / "egeria-quickstart"
FS = ROOT / "compose-configs" / "egeria-freshstart"
TREES = {"quickstart": QS, "freshstart": FS}


def _fresh(tree: str, env: dict, monkeypatch):
    """demo_config and demo_db of this tree, freshly imported with exactly this environment."""
    for k in ("DEMO_MODE", "DEMO_DB_HOST", "DEMO_DB_URL", "DEMO_DB_PATH", "DEMO_DB_PORT", "DEMO_DB_NAME", "DEMO_DB_USER",
              "DEMO_DB_PASSWORD", "DEMO_DB_SCHEMA", "JWT_SECRET"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    handler = str(TREES[tree] / "PyegeriaWebHandler")
    monkeypatch.syspath_prepend(handler)
    for m in ("demo_config", "demo_db", "demo_auth_handler", "egeria_auth"):
        monkeypatch.delitem(sys.modules, m, raising=False)
    import demo_config  # noqa: F401
    import demo_db
    return sys.modules["demo_config"], demo_db


@pytest.fixture(params=sorted(TREES))
def tree(request):
    return request.param


# ── SQLite ────────────────────────────────────────────────────────────────────────────────────────────────────────

def test_sqlite_creates_the_tables_in_the_file_and_seeds_the_config(tree, tmp_path, monkeypatch):
    db_file = tmp_path / "nested" / "demo.db"
    cfg, db = _fresh(tree, {"DEMO_DB_PATH": str(db_file)}, monkeypatch)
    engine = db.get_engine()
    assert str(engine.url).startswith("sqlite") and db_file.is_file()
    from sqlalchemy import inspect

    assert {"users", "events", "favorites", "config"} <= set(inspect(engine).get_table_names())
    assert db.get_config("session_lifetime_user") == "7200"             # seeded
    db.set_config("last_reset_at", "x")
    assert db.get_config("last_reset_at") == "x"


def test_sqlite_models_have_no_schema_so_the_queries_work(tree, tmp_path, monkeypatch):
    cfg, db = _fresh(tree, {"DEMO_DB_PATH": str(tmp_path / "d.db")}, monkeypatch)
    assert db.User.__table__.schema is None and db.Event.__table__.schema is None
    from sqlalchemy.orm import Session

    with Session(db.get_engine()) as s:
        s.add(db.User(display_name="A", email="a@example.org", password_hash="x"))
        s.commit()
        assert s.query(db.User).filter_by(email="a@example.org").one().role == "user"


def test_postgres_models_keep_the_schema(tree, monkeypatch):
    cfg, db = _fresh(tree, {"DEMO_DB_HOST": "pg.example"}, monkeypatch)
    assert db.User.__table__.schema == "demo_auth"


def test_register_verify_and_sign_in_work_on_a_sqlite_path(tmp_path, monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    cfg, db = _fresh("quickstart", {"DEMO_DB_PATH": str(tmp_path / "demo.db"), "JWT_SECRET": "k" * 40}, monkeypatch)
    import demo_auth_handler as h

    sent = {}
    monkeypatch.setattr(h, "_send_email", lambda to, subject, html, text="", bcc=None: sent.update(text=text))
    app = FastAPI()
    app.include_router(h.router)
    c = TestClient(app)
    r = c.post("/api/auth/register", json={"display_name": "Ada", "email": "ada@example.org", "password": "correct horse 9"})
    assert r.status_code == 200, r.text
    assert c.post("/api/auth/login", json={"email": "ada@example.org", "password": "correct horse 9"}).status_code == 403   # unverified
    token = sent["text"].rsplit("/", 1)[1]
    assert c.get(f"/api/auth/verify/{token}", follow_redirects=False).status_code in (200, 302, 303, 307)
    ok = c.post("/api/auth/login", json={"email": "ada@example.org", "password": "correct horse 9"})
    assert ok.status_code == 200 and ok.json()["display_name"] == "Ada"
    assert c.post("/api/auth/login", json={"email": "ada@example.org", "password": "wrong"}).status_code == 401


# ── an explicit Postgres host fails loudly and never becomes SQLite ───────────────────────────────────────────────

def test_an_unreachable_explicit_host_fails_and_creates_no_sqlite_file(tree, tmp_path, monkeypatch):
    sqlite_file = tmp_path / "must-not-exist.db"
    cfg, db = _fresh(tree, {"DEMO_DB_HOST": "127.0.0.1", "DEMO_DB_PORT": "1", "DEMO_DB_PATH": str(sqlite_file)}, monkeypatch)
    from sqlalchemy.exc import OperationalError

    with pytest.raises(OperationalError):
        db.get_engine()
    assert not sqlite_file.exists() and not list(tmp_path.iterdir())
    with pytest.raises(OperationalError):          # again: a failed first attempt must not leave a half-built engine behind
        db.get_engine()
    assert db._engine is None


# ── nothing set ───────────────────────────────────────────────────────────────────────────────────────────────────

def test_with_nothing_set_the_engine_is_refused_in_words_never_defaulted(tree, monkeypatch):
    cfg, db = _fresh(tree, {}, monkeypatch)
    with pytest.raises(cfg.DemoDbNotConfigured) as info:
        db.get_engine()
    assert "DEMO_DB_HOST" in str(info.value) and "DEMO_DB_PATH" in str(info.value)


@pytest.mark.parametrize("tree", ["quickstart", "freshstart"])
def test_the_portal_refuses_to_start_in_demo_mode_with_no_database(tree):
    src = (TREES[tree] / "PyegeriaWebHandler" / "pyegeria_handler.py").read_text(encoding="utf-8")
    life = src[src.index("async def _lifespan"):]
    start = life.index("require_demo_db()")
    assert start < life.index("await obs_start()") < life.index("await jup_start()")       # before anything is started


# ── the compose files say it explicitly ───────────────────────────────────────────────────────────────────────────

def test_the_quickstart_compose_names_the_shared_postgres_explicitly():
    y = (QS / "egeria-quickstart.yaml").read_text(encoding="utf-8")
    assert 'DEMO_DB_HOST: "egeria-shared-postgres"' in y and 'DEMO_DB_PATH: "/app/demo-data/demo.db"' in y


def test_the_freshstart_compose_names_the_shared_postgres_explicitly():
    assert 'DEMO_DB_HOST: "egeria-shared-postgres"' in (FS / "egeria-freshstart.yaml").read_text(encoding="utf-8")


def test_the_public_demo_override_keeps_its_own_host():
    assert 'DEMO_DB_HOST: "host.docker.internal"' in (QS / "egeria-quickstart-demo.yaml").read_text(encoding="utf-8")


def test_no_image_code_names_the_compose_only_hostname_as_a_default():
    for t in TREES.values():
        for f in ("demo_config.py", "demo_db.py"):
            assert "egeria-shared-postgres" not in (t / "PyegeriaWebHandler" / f).read_text(encoding="utf-8").replace(
                "egeria-shared-postgres:5442, coco_pharma", "")
