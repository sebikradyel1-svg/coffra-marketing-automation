"""
Qualification Agent for the Coffra lead-intelligence system.

Calls the Claude API with tool use: the model receives a lead, calls
score_lead (from scoring.py) as a tool to get the model-based conversion
score and its top contributing factors, then decides a tier (HOT/WARM/COLD)
and next action, with reasoning grounded in what the tool actually returned.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scoring import score_lead  # noqa: E402

load_dotenv()

MODEL = "claude-sonnet-5"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """Ești Qualification Agent pentru sistemul de lead intelligence al Coffra.
Sarcina: pentru fiecare lead primit, îl califici și decizi tier-ul și
acțiunea următoare. Nu redactezi outreach — doar califici și routezi.

Ai acces la o unealtă: score_lead(lead) — returnează un scor de conversie
(0-1) din modelul XGBoost antrenat, plus contribuțiile principale ale
feature-urilor (stil SHAP). FOLOSEȘTE ÎNTOTDEAUNA unealta înainte să
decizi — nu ghici scorul din intuiție.

Pași:
1. Apelează score_lead cu datele lead-ului.
2. Interpretează scorul și contribuțiile: ce a împins scorul sus/jos
   (fit: rol, industrie, mărime companie; engagement: comportament).
3. Decide tier-ul pe praguri:
   - score >= 0.70 → HOT (rutează la outreach, echivalent SQL)
   - 0.40 <= score < 0.70 → WARM (rutează la nurture)
   - score < 0.40 → COLD (disqualify, cu motiv)
4. Scrie un raționament scurt, explicabil, ancorat în contribuțiile reale
   ale modelului — nu vag, ci "scor sus pentru rol de decizie + cerere de
   demo; scăzut pe industrie mai puțin relevantă".

Returnează STRICT JSON:
{
  "score": 0.00,
  "tier": "HOT" | "WARM" | "COLD",
  "action": "OUTREACH" | "NURTURE" | "DISQUALIFY",
  "reasoning": "explicație scurtă ancorată în contribuțiile modelului",
  "top_factors": ["factor 1", "factor 2", "factor 3"]
}

Reguli: nu inventezi factori care nu vin din unealtă. Dacă unealta
eșuează, returnezi tier "WARM" ca fallback sigur — nu descalifici pe
baza unei erori. Pragurile sunt configurabile; respectă-le exact."""

SCORE_LEAD_TOOL = {
    "name": "score_lead",
    "description": (
        "Scores a lead with the trained XGBoost conversion model. Returns "
        "a conversion probability in [0, 1] and the top 3 contributing "
        "features (SHAP-based) with their direction of influence."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "lead": {
                "type": "object",
                "description": (
                    "Lead attributes keyed by the feature names in "
                    "models/feature_spec_v1.json (Age, Income, AdSpend, "
                    "WebsiteVisits, PagesPerVisit, TimeOnSite, SocialShares, "
                    "EmailOpens, EmailClicks, PreviousPurchases, "
                    "LoyaltyPoints, plus one-hot flags like Gender_Male, "
                    "CampaignChannel_PPC, CampaignType_Conversion, etc.)."
                ),
            }
        },
        "required": ["lead"],
    },
}


def _run_score_lead_tool(tool_input: dict[str, Any]) -> tuple[str, bool]:
    try:
        result = score_lead(tool_input["lead"])
        return json.dumps(result), False
    except Exception as exc:  # tool failure must reach the model as an error, not crash the agent
        return f"score_lead failed: {exc}", True


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()
    # Claude occasionally escapes apostrophes as \' inside JSON strings;
    # that's not a valid JSON escape (apostrophes never need escaping)
    # and breaks json.loads, so strip it before parsing.
    cleaned = cleaned.replace("\\'", "'")
    return json.loads(cleaned)


def run_qualification(lead: dict[str, Any]) -> dict[str, Any]:
    """
    Run the Qualification Agent on a single lead.

    Sends the lead to Claude with score_lead wired up as a tool. Claude
    calls the tool, reasons over the score + SHAP factors, and returns the
    tier/action/reasoning JSON defined in SYSTEM_PROMPT.

    Returns the parsed JSON dict from the agent's final response.
    """
    client = Anthropic()

    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": (
                "Califică acest lead:\n\n" + json.dumps(lead, ensure_ascii=False, indent=2)
            ),
        }
    ]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=[SCORE_LEAD_TOOL],
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            final_text = "".join(
                block.text for block in response.content if block.type == "text"
            )
            return _extract_json(final_text)

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            output, is_error = _run_score_lead_tool(block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": is_error,
                }
            )
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    sample_leads = {
        "HOT": {
            "Age": 43, "Income": 30558, "AdSpend": 2076.535113910116, "WebsiteVisits": 9,
            "PagesPerVisit": 7.818844717795544, "TimeOnSite": 14.229981592378053, "SocialShares": 83,
            "EmailOpens": 11, "EmailClicks": 4, "PreviousPurchases": 2, "LoyaltyPoints": 951,
            "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
            "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
            "CampaignType_Consideration": False, "CampaignType_Conversion": True, "CampaignType_Retention": False,
        },
        "WARM": {
            "Age": 50, "Income": 142268, "AdSpend": 8942.383205298067, "WebsiteVisits": 17,
            "PagesPerVisit": 8.230105487315821, "TimeOnSite": 2.9949215147235426, "SocialShares": 40,
            "EmailOpens": 17, "EmailClicks": 14, "PreviousPurchases": 1, "LoyaltyPoints": 659,
            "Gender_Male": True, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
            "CampaignChannel_SEO": True, "CampaignChannel_Social Media": False,
            "CampaignType_Consideration": True, "CampaignType_Conversion": False, "CampaignType_Retention": False,
        },
        "COLD": {
            "Age": 69, "Income": 124120, "AdSpend": 3245.107267196306, "WebsiteVisits": 18,
            "PagesPerVisit": 1.531658022805355, "TimeOnSite": 2.028837116426164, "SocialShares": 83,
            "EmailOpens": 8, "EmailClicks": 0, "PreviousPurchases": 9, "LoyaltyPoints": 452,
            "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": True,
            "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
            "CampaignType_Consideration": False, "CampaignType_Conversion": False, "CampaignType_Retention": True,
        },
    }

    for label, lead in sample_leads.items():
        raw_score = score_lead(lead)["score"]
        result = run_qualification(lead)
        print(f"=== {label} lead (raw score_lead: {raw_score}) ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()
