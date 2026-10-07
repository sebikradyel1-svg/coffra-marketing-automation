"""
EXPERIMENT: local MCP server exposing the existing score_lead() as one tool.

Imports score_lead from src/lead_intelligence/scoring.py (no copy), so the
model, SHAP logic and feature spec stay in one place. Runs over stdio.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

LEAD_INTELLIGENCE_DIR = Path(__file__).resolve().parent.parent / "src" / "lead_intelligence"
sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
from scoring import score_lead as _score_lead  # noqa: E402

# Reuse the description strings from the direct tool-use definition (imported,
# not copied), so the token comparison measures the protocol and not different
# wording. This makes the server depend on agents.qualification (and thus on
# anthropic); it is not standalone.
from agents.qualification import SCORE_LEAD_TOOL  # noqa: E402

TOOL_DESCRIPTION = SCORE_LEAD_TOOL["description"]
LEAD_DESCRIPTION = SCORE_LEAD_TOOL["input_schema"]["properties"]["lead"]["description"]

mcp = FastMCP("coffra-lead-scoring")


@mcp.tool(name="score_lead", description=TOOL_DESCRIPTION)
def score_lead(lead: Annotated[dict[str, Any], Field(description=LEAD_DESCRIPTION)]) -> str:
    """Score one lead; returns the same JSON string the agent's tool_result carries today."""
    return json.dumps(_score_lead(lead))


if __name__ == "__main__":
    mcp.run(transport="stdio")
