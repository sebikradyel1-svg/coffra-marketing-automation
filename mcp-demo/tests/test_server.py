"""Call the MCP server's tool directly, without Claude Desktop or an API key."""

import asyncio
import json
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR))

pytest.importorskip("xgboost")
pytest.importorskip("shap")

import server  # noqa: E402

LEAD = {
    "Age": 43, "Income": 30558, "AdSpend": 2076.535113910116, "WebsiteVisits": 9,
    "PagesPerVisit": 7.818844717795544, "TimeOnSite": 14.229981592378053, "SocialShares": 83,
    "EmailOpens": 11, "EmailClicks": 4, "PreviousPurchases": 2, "LoyaltyPoints": 951,
    "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
    "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
    "CampaignType_Consideration": False, "CampaignType_Conversion": True, "CampaignType_Retention": False,
}


def _call(name, args):
    return asyncio.run(server.mcp.call_tool(name, args))


def _text(result) -> str:
    content = result[0] if isinstance(result, tuple) else result
    return content[0].text


def test_exactly_one_tool_named_score_lead():
    tools = asyncio.run(server.mcp.list_tools())
    assert [t.name for t in tools] == ["score_lead"]
    assert tools[0].inputSchema["required"] == ["lead"]


def test_tool_matches_existing_function():
    from scoring import score_lead

    assert json.loads(_text(_call("score_lead", {"lead": LEAD}))) == score_lead(LEAD)


def test_score_in_range_with_three_factors():
    out = json.loads(_text(_call("score_lead", {"lead": LEAD})))
    assert 0.0 <= out["score"] <= 1.0
    assert len(out["top_factors"]) == 3
    assert {"feature", "shap_value", "direction"} <= set(out["top_factors"][0])


def test_missing_feature_is_an_error():
    bad = {k: v for k, v in LEAD.items() if k != "Age"}
    with pytest.raises(Exception, match="Age"):
        _call("score_lead", {"lead": bad})
