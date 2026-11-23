"""TR-134: the Portal image's demo sign-in database is chosen EXPLICITLY and fails closed.

It used to default DEMO_DB_HOST to "egeria-shared-postgres:5442", a Compose-only hostname, so anywhere else (the Helm chart sets
DEMO_DB_PATH=/app/demo-data/demo.db) every sign-in was a 500. Now (Architect's design):
  * DEMO_DB_HOST or DEMO_DB_URL set      -> Postgres
  * else DEMO_DB_PATH set                -> SQLite at that path
  * else, in DEMO_MODE                   -> REFUSE TO START, with words naming both settings
  * no silent fallback to SQLite when Postgres was meant: an explicit but unreachable DEMO_DB_HOST fails loudly and creates no file
  * the compose files that need the shared Postgres say so with DEMO_DB_HOST.
Both trees: quickstart and freshstart each have their own demo_config.py / demo_db.py (per-environment, not shared).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TREES = {"quickstart": ROOT / "compose-configs" / "egeria-quickstart", "freshstart": ROOT / "compose-configs" / "egeria-freshstart"}
SQLITE_TREES = ("quickstart",)          # where the SQLite engine is built (the image the Helm chart runs)


def _load(tree: str, env: dict, monkeypatch, name="demo_config"):
    """The tree's demo_config (or demo_db) module, freshly imported with exactly this environment (nothing else leaks in)."""
    for k in ("DEMO_MODE", "DEMO_DB_HOST", "DEMO_DB_URL", "DEMO_DB_PATH", "DEMO_DB_PORT", "DEMO_DB_NAME", "DEMO_DB_USER",
              "DEMO_DB_PASSWORD", "DEMO_DB_SCHEMA"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    handler = str(TREES[tree] / "PyegeriaWebHandler")
    monkeypatch.syspath_prepend(handler)
    for m in ("demo_config", "demo_db"):
        monkeypatch.delitem(sys.modules, m, raising=False)
    spec = importlib.util.spec_from_file_location(name, Path(handler) / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, mod)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(params=sorted(TREES))
def tree(request):
    return request.param


# ── each selection branch ──────────────────────────────────────────────────────────────────────────────────────────

def test_a_host_selects_postgres_and_builds_the_url_from_the_parts(tree, monkeypatch):
    cfg = _load(tree, {"DEMO_DB_HOST": "db.example", "DEMO_DB_PORT": "5433", "DEMO_DB_NAME": "n", "DEMO_DB_USER": "u",
                       "DEMO_DB_PASSWORD": "p"}, monkeypatch)
    c = cfg.select_demo_db({"DEMO_DB_HOST": "db.example", "DEMO_DB_PORT": "5433", "DEMO_DB_NAME": "n", "DEMO_DB_USER": "u",
                            "DEMO_DB_PASSWORD": "p"}, demo_mode=False)
    assert (c.kind, c.path) == ("postgres", "") and c.db_url == "postgresql+psycopg2://u:p@db.example:5433/n"


def test_a_host_alone_gets_the_other_parts_defaults_but_never_a_default_host(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    c = cfg.select_demo_db({"DEMO_DB_HOST": "pg"}, demo_mode=True)
    assert c.kind == "postgres" and c.db_url == "postgresql+psycopg2://demo_user:demo4egeria@pg:5442/coco_pharma"


def test_a_url_selects_postgres_and_is_used_verbatim(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    c = cfg.select_demo_db({"DEMO_DB_URL": "postgresql+psycopg2://a:b@h:1/d"}, demo_mode=True)
    assert (c.kind, c.db_url) == ("postgres", "postgresql+psycopg2://a:b@h:1/d")


def test_a_path_alone_selects_sqlite_at_that_path(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    c = cfg.select_demo_db({"DEMO_DB_PATH": "/app/demo-data/demo.db"}, demo_mode=True)
    assert (c.kind, c.path, c.db_url) == ("sqlite", "/app/demo-data/demo.db", "sqlite:////app/demo-data/demo.db")


@pytest.mark.parametrize("env", [{"DEMO_DB_HOST": "pg", "DEMO_DB_PATH": "/x/demo.db"},
                                 {"DEMO_DB_URL": "postgresql+psycopg2://a:b@h:1/d", "DEMO_DB_PATH": "/x/demo.db"}])
def test_postgres_wins_when_both_are_set(tree, monkeypatch, env):
    """The quickstart compose sets DEMO_DB_PATH (config.js lives beside it) AND the shared Postgres host: Postgres, as now."""
    cfg = _load(tree, {}, monkeypatch)
    assert cfg.select_demo_db(env, demo_mode=True).kind == "postgres"


def test_blank_values_count_as_unset(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    assert cfg.select_demo_db({"DEMO_DB_HOST": "  ", "DEMO_DB_URL": "", "DEMO_DB_PATH": "/x/d.db"}, demo_mode=True).kind == "sqlite"


# ── nothing set ────────────────────────────────────────────────────────────────────────────────────────────────────

def test_nothing_set_in_demo_mode_refuses_with_words_naming_both_settings(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    with pytest.raises(cfg.DemoDbNotConfigured) as info:
        cfg.select_demo_db({}, demo_mode=True)
    words = str(info.value)
    assert "DEMO_DB_HOST" in words and "DEMO_DB_PATH" in words and "DEMO_DB_URL" in words
    assert isinstance(info.value, RuntimeError)


def test_nothing_set_outside_demo_mode_selects_nothing_and_never_makes_a_default(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    c = cfg.select_demo_db({}, demo_mode=False)
    assert (c.kind, c.db_url, c.path) == ("none", "", "")
    assert "DEMO_DB_HOST" in c.words and "DEMO_DB_PATH" in c.words


def test_the_module_has_no_default_host_and_reads_the_environment_once_at_import(tree, monkeypatch):
    cfg = _load(tree, {}, monkeypatch)
    assert cfg.DEMO_DB_HOST == "" and "egeria-shared-postgres" not in Path(cfg.__file__).read_text(encoding="utf-8")
    assert cfg.DEMO_DB_CHOICE.kind == "none"
    cfg = _load(tree, {"DEMO_DB_PATH": "/tmp/x.db"}, monkeypatch)
    assert cfg.DEMO_DB_CHOICE.kind == "sqlite" and cfg.DEMO_DB_URL == "sqlite:////tmp/x.db"


def test_importing_the_module_in_demo_mode_with_nothing_set_does_not_crash_the_importer(tree, monkeypatch):
    """The refusal is the startup check's (require_demo_db), so tools that only import the module still can."""
    cfg = _load(tree, {"DEMO_MODE": "true"}, monkeypatch)
    with pytest.raises(cfg.DemoDbNotConfigured):
        cfg.require_demo_db()


def test_require_demo_db_passes_when_something_is_set(tree, monkeypatch):
    cfg = _load(tree, {"DEMO_MODE": "true", "DEMO_DB_HOST": "pg"}, monkeypatch)
    assert cfg.require_demo_db().kind == "postgres"
