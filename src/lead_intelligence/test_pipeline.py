"""
Smoke test for the lead-intelligence pipeline after the move to
src/lead_intelligence/.

Runs the same 3 test leads (HOT, WARM, COLD) from app.py through the full
pipeline - qualification -> routing -> outreach -> governance -> human
approval checkpoint - with plain console output instead of Streamlit, to
confirm the move didn't break anything.
"""

from __future__ import annotations

import json
import sys

from agents.governance import run_governance
from agents.outreach import run_outreach
from agents.qualification import run_qualification
from utils.logger import log_decision

# Same feature values as app.py's SAMPLE_LEADS, keyed HOT/WARM/COLD.
SAMPLE_LEADS = {
    "HOT — score_lead 0.98": {
        "Age": 43, "Income": 30558, "AdSpend": 2076.535113910116, "WebsiteVisits": 9,
        "PagesPerVisit": 7.818844717795544, "TimeOnSite": 14.229981592378053, "SocialShares": 83,
        "EmailOpens": 11, "EmailClicks": 4, "PreviousPurchases": 2, "LoyaltyPoints": 951,
        "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False, "CampaignType_Conversion": True, "CampaignType_Retention": False,
    },
    "WARM — score_lead 0.69": {
        "Age": 50, "Income": 142268, "AdSpend": 8942.383205298067, "WebsiteVisits": 17,
        "PagesPerVisit": 8.230105487315821, "TimeOnSite": 2.9949215147235426, "SocialShares": 40,
        "EmailOpens": 17, "EmailClicks": 14, "PreviousPurchases": 1, "LoyaltyPoints": 659,
        "Gender_Male": True, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": True, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": True, "CampaignType_Conversion": False, "CampaignType_Retention": False,
    },
    "COLD — score_lead 0.10": {
        "Age": 69, "Income": 124120, "AdSpend": 3245.107267196306, "WebsiteVisits": 18,
        "PagesPerVisit": 1.531658022805355, "TimeOnSite": 2.028837116426164, "SocialShares": 83,
        "EmailOpens": 8, "EmailClicks": 0, "PreviousPurchases": 9, "LoyaltyPoints": 452,
        "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": True,
        "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False, "CampaignType_Conversion": False, "CampaignType_Retention": True,
    },
}


def run_pipeline(label: str, lead: dict) -> None:
    print(f"\n{'=' * 70}\n{label}\n{'=' * 70}")

    print("\n1. Qualification")
    qual = run_qualification(lead)
    print(f"   Score: {qual['score']:.2f}")
    print(f"   Tier: {qual['tier']} -> Action: {qual['action']}")
    print(f"   Reasoning: {qual['reasoning']}")
    print("   Top factors: " + ", ".join(qual["top_factors"]))
    log_decision("qualification", lead, qual)

    print("\n2. Routing")
    if qual["action"] == "OUTREACH":
        print("   Lead HOT -> Outreach Agent")

        print("\n3. Outreach draft")
        draft = run_outreach(lead, qual)
        print(f"   Subject: {draft['subject']}")
        print(f"   Message: {draft['message']}")
        print(f"   Personalization basis: {draft['personalization_basis']}")
        log_decision("outreach", {"lead": lead, "qualification": qual}, draft)

        print("\n4. Governance check")
        review = run_governance(draft, lead)
        print(f"   Verdict: {review['verdict']} — {review['summary']}")
        if review["verdict"] == "REVISE":
            print("   Claims checked:")
            print(json.dumps(review["claims_checked"], ensure_ascii=False, indent=2))
            print("   Flags:")
            print(json.dumps(review["flags"], ensure_ascii=False, indent=2))
        elif review["flags"]:
            print("   Flags (soft):")
            print(json.dumps(review["flags"], ensure_ascii=False, indent=2))
        log_decision("governance", draft, review)

        print("\n5. Human approval")
        if review["verdict"] == "REVISE":
            print("   Status: blocat — necesită revizuire înainte de aprobare umană")
        else:
            print("   Status: pending human review (Approve & send / Send back for revision)")
    elif qual["action"] == "NURTURE":
        print("   Lead WARM -> secvență de nurture (handoff)")
    else:
        print("   Lead COLD -> disqualified")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    for label, lead in SAMPLE_LEADS.items():
        run_pipeline(label, lead)

    print(f"\n{'=' * 70}\nDone — all {len(SAMPLE_LEADS)} test leads ran through the full pipeline.\n{'=' * 70}")
