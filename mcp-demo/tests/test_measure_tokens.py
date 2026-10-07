"""measure_tokens.py with a stub counter: no API key or network needed."""

import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR))

pytest.importorskip("anthropic")

import measure_tokens  # noqa: E402


def stub_count(tools):
    # Deterministic fake: 10 for the bare request + 1 per 4 chars of tool JSON.
    # These are NOT real token counts.
    return 10 + len(json.dumps(tools)) // 4


def test_measure_structure_and_arithmetic():
    r = measure_tokens.measure(stub_count)
    assert r["baseline_no_tools_tokens"] == 10
    assert r["difference_mcp_minus_direct"] == r["mcp_tokens"] - r["direct_tool_use_tokens"]
    assert r["direct_definition"]["name"] == r["mcp_definition"]["name"] == "score_lead"
    assert r["direct_tool_use_tokens"] > 0 and r["mcp_tokens"] > 0
    assert r["fixed_overhead_reference"] == stub_count([measure_tokens.NOOP_TOOL]) - 10
    assert r["direct_minus_overhead"] == r["direct_tool_use_tokens"] - r["fixed_overhead_reference"]
    assert r["mcp_minus_overhead"] == r["mcp_tokens"] - r["fixed_overhead_reference"]


def test_lead_property_description_identical_in_both_definitions():
    direct = measure_tokens.direct_tool_definition()["input_schema"]["properties"]["lead"]["description"]
    mcp_desc = measure_tokens.mcp_tool_definition()["input_schema"]["properties"]["lead"]["description"]
    assert direct and direct == mcp_desc


def test_tool_level_description_identical_in_both_definitions():
    assert (
        measure_tokens.direct_tool_definition()["description"]
        == measure_tokens.mcp_tool_definition()["description"]
    )


def test_mcp_definition_has_anthropic_shape():
    d = measure_tokens.mcp_tool_definition()
    assert set(d) == {"name", "description", "input_schema"}
    assert d["input_schema"]["type"] == "object"


def test_main_without_key_writes_nothing(monkeypatch, tmp_path):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(measure_tokens, "RESULTS_PATH", tmp_path / "results.json")
    assert measure_tokens.main() == 1
    assert not (tmp_path / "results.json").exists()
