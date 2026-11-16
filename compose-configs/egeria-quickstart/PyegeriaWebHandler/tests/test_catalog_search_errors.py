"""GET /api/catalog/search maps Egeria failures through egeria_error_mapping (PO-25). It used to wrap every
exception as HTTP 500, so an unknown or expired user (PyegeriaUnauthorizedException) showed as a server
error instead of 401. Its log lines also used %r, which loguru never interpolates ({} is loguru's style)."""
import re
import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_HERE))

httpx = pytest.importorskip("httpx")
fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

import catalog_search_handler as cs  # noqa: E402


def _unauthorized():
    from pyegeria.core._exceptions import PyegeriaUnauthorizedException
    req = httpx.Request("POST", "https://egeria-main:9443/servers/qs-view-server/api/token")
    resp = httpx.Response(401, request=req, text='{"class":"FFDCResponseBase","relatedHTTPCode":401}')
    return PyegeriaUnauthorizedException(resp, {"caller method": "test"}, {"userid": "someoneelse"})


class _CE:
    def __init__(self, errors):
        self.errors, self.calls = list(errors), []

    def find_elements_by_property_value(self, **kw):
        self.calls.append(kw.get("metadata_element_subtypes"))
        raise self.errors.pop(0)


@pytest.fixture
def search(monkeypatch):
    def run(errors, **params):
        ce = _CE(errors)
        monkeypatch.setattr(cs, "_classification_explorer", lambda *a, **k: ce)
        app = fastapi.FastAPI(); app.include_router(cs.router)
        return TestClient(app).get("/api/catalog/search", params={"q": "Local Dashboards", **params}), ce
    return run


def test_unauthorized_find_is_401_not_500(search):
    r, _ = search([_unauthorized()])
    assert r.status_code == 401, r.text


def test_unauthorized_on_unrestricted_retry_is_401(search, monkeypatch):
    monkeypatch.setattr(cs, "_is_unrecognized_type_error", lambda exc: True)
    r, ce = search([RuntimeError("unknown type"), _unauthorized()], types="NoSuchType")
    assert r.status_code == 401, r.text
    assert ce.calls == [["NoSuchType"], None]          # the retry really ran, unrestricted


def test_unexpected_error_is_still_500(search):
    r, _ = search([RuntimeError("boom")])
    assert r.status_code == 500


@pytest.mark.parametrize("tree", ["egeria-quickstart", "egeria-freshstart"])
def test_handler_uses_shared_mapping_and_loguru_placeholders(tree):
    p = _HERE.parent.parent / tree / "PyegeriaWebHandler" / "catalog_search_handler.py"
    if not p.exists():
        pytest.skip(f"{tree} not in this checkout")
    src = p.read_text()
    assert "raise_egeria_http_error(exc)" in src and "raise_egeria_http_error(exc2)" in src
    assert "status_code=500, detail=str(exc" not in src
    assert not re.search(r"logger\.\w+\([^)]*%[rsd]", src), "loguru does not interpolate %-style placeholders"
