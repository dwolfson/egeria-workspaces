"""PY-48 (Architect): the MCP wrapper counts only known good statuses as succeeded.

_build_structured_response used to default a missing status to "success" and count every row that was not
"failure" as succeeded, so a "warning" row (no processor, or a 6.4 command on an older platform) or a status nobody
had heard of came back as success True. Now only success, deferred and read count as succeeded; a missing or unknown
status is a failure with words. Rows that are not commands are still skipped. This also protects the Portal on an
older pyegeria pin, which still sends the "warning" rows.

The same file is in both trees (quickstart and freshstart keep identical copies of mcp_server.py).
"""
import json
import sys
from pathlib import Path

import pytest

_MODULE_DIR = Path(__file__).resolve().parent.parent
if str(_MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(_MODULE_DIR))

import mcp_server  # noqa: E402


def _run(*rows, directive="process"):
    raw = {"output": "", "results": list(rows), "hints": []}
    return json.loads(mcp_server._build_structured_response(raw, directive))


def _row(status="success", **extra):
    row = {"is_command": True, "verb": "Create", "object_type": "Project", "message": "m"}
    if status != "__missing__":
        row["status"] = status
    return {**row, **extra}


@pytest.mark.parametrize("status", ["success", "deferred", "read"])
def test_a_known_good_status_is_succeeded(status):
    out = _run(_row(status))
    assert out["success"] is True and out["commands_succeeded"] == 1 and out["commands_failed"] == 0


@pytest.mark.parametrize("status", ["something_new", "warning", "", None, "SUCCESS", "error"])
def test_any_other_status_is_a_failure_with_words(status):
    out = _run(_row(status))
    assert out["success"] is False
    assert out["commands_succeeded"] == 0 and out["commands_failed"] == 1
    [err] = out["execution_errors"]
    assert "not a known good status" in err["message"] and err["command"] == "Create Project"


def test_a_missing_status_is_a_failure_not_a_default_success():
    out = _run(_row("__missing__"))
    assert out["success"] is False and out["commands_failed"] == 1
    assert "no status" in out["execution_errors"][0]["message"]
    assert out["commands_detail"][0]["status"] == "unknown"


def test_the_words_name_the_status_and_keep_the_rows_own_message():
    out = _run(_row("something_new", message="No processor registered for 'Display Name'"))
    message = out["execution_errors"][0]["message"]
    assert "'something_new'" in message and "No processor registered for 'Display Name'" in message


def test_a_bad_row_among_good_ones_is_partial():
    out = _run(_row("success"), _row("something_new"), _row("deferred"))
    assert out["commands_total"] == 3 and out["commands_succeeded"] == 2 and out["commands_failed"] == 1
    assert out["success"] is False and out["partial"] is True


def test_a_failure_row_still_reports_as_before():
    out = _run(_row("failure", errors=["Validation failed: x"]))
    assert out["success"] is False and out["validation_errors"][0]["message"] == "Validation failed: x"
    assert out["execution_errors"] == []


def test_rows_that_are_not_commands_are_still_skipped():
    out = _run({"is_command": False}, _row("success"))
    assert out["commands_total"] == 1 and out["success"] is True
