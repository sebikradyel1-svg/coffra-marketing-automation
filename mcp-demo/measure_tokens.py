"""
EXPERIMENT: measure the token size of the score_lead tool definition in the
direct tool-use version (SCORE_LEAD_TOOL in agents/qualification.py) vs the
MCP version (schema as FastMCP generates it, mapped to Anthropic's format),
plus a minimal "noop" tool as a reference for the fixed tool-use overhead.

Each definition is counted with the Anthropic token-counting endpoint as
(request with the tool) - (same request without tools). Needs ANTHROPIC_API_KEY.
Writes mcp-demo/results.json. Run:  python measure_tokens.py
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "src" / "lead_intelligence"))

MODEL = "claude-sonnet-5"
RESULTS_PATH = HERE / "results.json"
# Minimal tool (name only, empty object schema) to make the fixed tool-use
# overhead visible. Approximate: its name is shorter and it has no description.
NOOP_TOOL = {"name": "noop", "input_schema": {"type": "object", "properties": {}}}
PROBE_MESSAGES = [{"role": "user", "content": "ping"}]


def direct_tool_definition() -> dict[str, Any]:
    from agents.qualification import SCORE_LEAD_TOOL

    return SCORE_LEAD_TOOL


def mcp_tool_definition() -> dict[str, Any]:
    """The tool as an MCP client would see it, converted to Anthropic's tool format."""
    from server import mcp

    tools = asyncio.run(mcp.list_tools())
    tool = next(t for t in tools if t.name == "score_lead")
    return {"name": tool.name, "description": tool.description, "input_schema": tool.inputSchema}


def make_api_counter(client: Any, model: str = MODEL) -> Callable[[list[dict[str, Any]]], int]:
    def count(tools: list[dict[str, Any]]) -> int:
        kwargs: dict[str, Any] = {"model": model, "messages": PROBE_MESSAGES}
        if tools:
            kwargs["tools"] = tools
        return client.messages.count_tokens(**kwargs).input_tokens

    return count


def measure(count: Callable[[list[dict[str, Any]]], int], model: str = MODEL) -> dict[str, Any]:
    direct, mcp_def = direct_tool_definition(), mcp_tool_definition()
    baseline = count([])
    direct_tokens = count([direct]) - baseline
    mcp_tokens = count([mcp_def]) - baseline
    overhead = count([NOOP_TOOL]) - baseline
    return {
        "experiment": True,
        "model": model,
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "baseline_no_tools_tokens": baseline,
        "direct_tool_use_tokens": direct_tokens,
        "mcp_tokens": mcp_tokens,
        "difference_mcp_minus_direct": mcp_tokens - direct_tokens,
        "fixed_overhead_reference": overhead,
        "direct_minus_overhead": direct_tokens - overhead,
        "mcp_minus_overhead": mcp_tokens - overhead,
        "fixed_overhead_tool": NOOP_TOOL,
        "direct_definition": direct,
        "mcp_definition": mcp_def,
    }


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set; nothing measured, results.json not written.", file=sys.stderr)
        return 1
    from anthropic import Anthropic

    results = measure(make_api_counter(Anthropic()))
    RESULTS_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
