"""
Lead Intelligence Agent Page - Multi-agent lead qualification & outreach system (P7).

Demonstrates:
- Qualification Agent: Claude + score_lead tool (XGBoost conversion model, SHAP factors)
- Routing: HOT -> outreach, WARM -> nurture handoff, COLD -> disqualify
- Outreach Agent: Claude + RAG (grounded in approved brand talking points only)
- Governance Reviewer: claim-by-claim verification against brand sources, APPROVE/REVISE verdict
- Human approval checkpoint (simulated - no message is actually sent)

Live agent runs: pressing "Run agent" calls the real Claude API via the agents in
src/lead_intelligence/agents/, same pipeline as the original app.py prototype.
"""

import sys
from pathlib import Path

PAGE_DIR = Path(__file__).resolve().parent
DASHBOARD_DIR = PAGE_DIR.parent
REPO_ROOT = DASHBOARD_DIR.parent

sys.path.insert(0, str(DASHBOARD_DIR))
sys.path.insert(0, str(REPO_ROOT))

import streamlit as st

from lib.styling import inject_custom_css, page_header, data_disclosure, COFFRA_BROWN_LIGHT, MEDIUM_GRAY

from src.lead_intelligence.agents.qualification import run_qualification
from src.lead_intelligence.agents.outreach import run_outreach
from src.lead_intelligence.agents.governance import run_governance
from src.lead_intelligence.utils.logger import log_decision


st.set_page_config(page_title="Lead Intelligence Agent | Coffra", page_icon="C", layout="wide")
inject_custom_css()

page_header(
    "Lead Intelligence Agent",
    "Multi-agent pipeline: qualification -> routing -> outreach -> governance -> human approval"
)

data_disclosure(
    "simulated",
    "Coffra is a fictional brand used as a sandbox for this portfolio. Agent runs below call "
    "the real Claude API and the trained XGBoost model live - only the brand and the leads are "
    "simulated. No message is ever actually sent; human approval is a UI checkpoint only."
)


# ============================================================
# SAMPLE LEADS (same feature values used to validate score_lead thresholds)
# ============================================================
SAMPLE_LEADS = {
    "Hot — score_lead 0.98": {
        "Age": 43, "Income": 30558, "AdSpend": 2076.535113910116, "WebsiteVisits": 9,
        "PagesPerVisit": 7.818844717795544, "TimeOnSite": 14.229981592378053, "SocialShares": 83,
        "EmailOpens": 11, "EmailClicks": 4, "PreviousPurchases": 2, "LoyaltyPoints": 951,
        "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False, "CampaignType_Conversion": True, "CampaignType_Retention": False,
    },
    "Warm — score_lead 0.69": {
        "Age": 50, "Income": 142268, "AdSpend": 8942.383205298067, "WebsiteVisits": 17,
        "PagesPerVisit": 8.230105487315821, "TimeOnSite": 2.9949215147235426, "SocialShares": 40,
        "EmailOpens": 17, "EmailClicks": 14, "PreviousPurchases": 1, "LoyaltyPoints": 659,
        "Gender_Male": True, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": True, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": True, "CampaignType_Conversion": False, "CampaignType_Retention": False,
    },
    "Cold — score_lead 0.10": {
        "Age": 69, "Income": 124120, "AdSpend": 3245.107267196306, "WebsiteVisits": 18,
        "PagesPerVisit": 1.531658022805355, "TimeOnSite": 2.028837116426164, "SocialShares": 83,
        "EmailOpens": 8, "EmailClicks": 0, "PreviousPurchases": 9, "LoyaltyPoints": 452,
        "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": True,
        "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False, "CampaignType_Conversion": False, "CampaignType_Retention": True,
    },
}


# ============================================================
# LEAD SELECTION
# ============================================================
st.markdown("## Run the Pipeline")

col_in, col_arch = st.columns([2, 1])

with col_in:
    choice = st.selectbox("Alege un lead de test", list(SAMPLE_LEADS))
    lead = SAMPLE_LEADS[choice]
    with st.expander("Lead features (raw input)"):
        st.json(lead)
    run = st.button("Run agent", type="primary")

with col_arch:
    st.markdown("### Cum funcționează")
    st.markdown(
        "1. **Qualification** — apelează modelul XGBoost (tool)\n"
        "2. **Routing** — hot / warm / cold\n"
        "3. **Outreach** — draft personalizat (RAG)\n"
        "4. **Governance** — verifică guardrails\n"
        "5. **Human approval** — checkpoint final"
    )


# ============================================================
# PIPELINE RUN
# ============================================================
if run:
    st.markdown("## 1. Qualification")
    with st.spinner("Qualification Agent — scoring lead..."):
        qual = run_qualification(lead)
    log_decision("qualification", lead, qual)

    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric("Score", f"{qual['score']:.2f}")
    with c2:
        st.markdown(f"**Tier:** {qual['tier']} → **Action:** {qual['action']}")
        st.info(qual["reasoning"])
        st.caption("Top factors: " + ", ".join(qual["top_factors"]))

    st.markdown("## 2. Routing")
    if qual["action"] == "OUTREACH":
        st.success("Lead HOT → Outreach Agent")

        st.markdown("## 3. Outreach Draft")
        with st.spinner("Outreach Agent — drafting message (RAG-grounded)..."):
            draft = run_outreach(lead, qual)
        log_decision("outreach", {"lead": lead, "qualification": qual}, draft)

        st.markdown(f"**Subject:** {draft['subject']}")
        st.text(draft["message"])
        st.caption(f"Personalizare: {draft['personalization_basis']}")

        st.markdown("## 4. Governance Check")
        with st.spinner("Governance Reviewer — verifying claims against brand sources..."):
            review = run_governance(draft, lead)
        log_decision("governance", draft, review)

        verdict_fn = st.success if review["verdict"] == "APPROVE" else st.warning
        verdict_fn(f"{review['verdict']} — {review['summary']}")

        if review["verdict"] == "REVISE":
            st.markdown("**Claims verificate (descompuse):**")
            st.dataframe(review["claims_checked"], use_container_width=True)
            st.markdown("**Flags:**")
            st.json(review["flags"])
        elif review["flags"]:
            st.markdown("**Flags (soft):**")
            st.json(review["flags"])
        else:
            with st.expander("Claims verificate (toate susținute)"):
                st.dataframe(review["claims_checked"], use_container_width=True)

        st.markdown("## 5. Human Approval")
        if review["verdict"] == "REVISE":
            st.markdown(
                f"<span style='color: {COFFRA_BROWN_LIGHT}; font-weight: 600;'>"
                "Status: blocat — necesită revizuire înainte de aprobare umană</span>",
                unsafe_allow_html=True,
            )
            st.button("Trimite la revizuire")
        else:
            st.markdown(
                f"<span style='color: {MEDIUM_GRAY};'>Status: pending human review (simulat — "
                "niciun mesaj nu e trimis efectiv)</span>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            c1.button("Approve & send")
            c2.button("Send back for revision")

    elif qual["action"] == "NURTURE":
        st.warning("Lead WARM → secvență de nurture (handoff)")
    else:
        st.error("Lead COLD → disqualified")
