"""
EXPERIMENT: local MCP server exposing the existing score_lead() as one tool.

Imports score_lead from src/lead_intelligence/scoring.py (no copy), so the
model, SHAP logic and feature spec stay in one place. Runs over stdio.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

LEAD_INTELLIGENCE_DIR = Path(__file__).resolve().parent.parent / "src" / "lead_intelligence"
sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
from scoring import score_lead as _score_lead  # noqa: E402

# Same wording as SCORE_LEAD_TOOL in agents/qualification.py, so the token
# comparison measures the protocol and not different descriptions.
TOOL_DESCRIPTION = (
    "Scores a lead with the trained XGBoost conversion model. Returns "
    "a conversion probability in [0, 1] and the top 3 contributing "
    "features (SHAP-based) with their direction of influence."
)

mcp = FastMCP("coffra-lead-scoring")


@mcp.tool(name="score_lead", description=TOOL_DESCRIPTION)
def score_lead(lead: dict[str, Any]) -> str:
    """Score one lead; returns the same JSON string the agent's tool_result carries today."""
    return json.dumps(_score_lead(lead))


if __name__ == "__main__":
    mcp.run(transport="stdio")
