"""
Methodology Page - Honest disclosure of what is real, what is snapshot, what is simulated.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from lib.styling import inject_custom_css, page_header, COFFRA_BROWN, MEDIUM_GRAY
from lib.data_loaders import load_hubspot_metadata, get_optimizer_summary, load_model_metrics


st.set_page_config(page_title="Methodology | Coffra", layout="wide")
inject_custom_css()

page_header(
    "Methodology",
    "Honest disclosure of data provenance, limitations, and production roadmap"
)


# ============================================================
# WHY THIS PAGE EXISTS
# ============================================================
st.markdown("## Why This Page Exists")

st.markdown(
    """
    Marketing portfolios often present invented metrics as if they were measured.
    This dashboard is built to a different standard: **every data point on every page
    is labelled by provenance** — real, snapshot, or simulated. This page documents
    what each label means and why the project takes this approach.

    For an AI Marketing Specialist role, this transparency is itself a deliverable.
    A senior recruiter learns more about your judgment from a clearly labeled limitation
    than from an inflated metric.
    """
)


# ============================================================
# DATA PROVENANCE TABLE
# ============================================================
st.markdown("## Data Provenance by Page")

provenance_df = pd.DataFrame([
    {
        "Page": "Lead Quality",
        "Type": "Real",
        "Source": "XGBoost model trained on Kaggle 'Predict Conversion in Digital Marketing' dataset (8,000 records)",
        "Reproducible?": "Yes — fixed random_state=42, public dataset, notebook in repo"
    },
    {
        "Page": "Subject Optimizer",
        "Type": "Real",
        "Source": "Cached responses from Anthropic Claude API (cache/subject_optimizer/)",
        "Reproducible?": "Yes with API key — same prompts produce semantically similar variants"
    },
    {
        "Page": "HubSpot CRM",
        "Type": "Snapshot",
        "Source": "HubSpot Marketing Hub trial via Private App API; extracted on snapshot date",
        "Reproducible?": "Snapshot is static. Live extraction script in repo (extract_hubspot_snapshot.py) but requires active trial"
    },
    {
        "Page": "Campaign Funnel",
        "Type": "Simulated",
        "Source": "Industry benchmarks (Mailchimp 2025 F&B) with reasonable scenario assumptions",
        "Reproducible?": "Yes — all calculations and assumptions documented inline"
    },
])
st.dataframe(provenance_df, use_container_width=True, hide_index=True)


# ============================================================
# DATA AGE
# ============================================================
st.markdown("## Data Age")

hubspot_meta = load_hubspot_metadata()
optimizer_summary = get_optimizer_summary()
model_metrics = load_model_metrics()

age_data = pd.DataFrame([
    {
        "Source": "HubSpot snapshot",
        "Captured": hubspot_meta.get("extracted_at_human", "(not captured)"),
        "Static after": hubspot_meta.get("trial_expires", "Trial expiry"),
    },
    {
        "Source": "Subject Optimizer cache",
        "Captured": "Continuous (each new generation)",
        "Static after": "Permanent (cached locally, no expiry)",
    },
    {
        "Source": "Lead scoring model",
        "Captured": "Notebook execution (April 2026)",
        "Static after": "Permanent (joblib artifact)",
    },
])
st.dataframe(age_data, use_container_width=True, hide_index=True)


# ============================================================
# WHAT IS NOT IN THIS DASHBOARD
# ============================================================
st.markdown("## What This Dashboard Does NOT Include (and Why)")

st.markdown(
    """
    Several metrics commonly seen on marketing dashboards are deliberately absent:

    - **Real email open and click rates** — Coffra has no live email sending. Showing
      "open rate" would mean inventing it. Methodology for measuring is documented in
      `docs/08_ab_testing_methodology.md`.

    - **Real ROI / CAC / LTV** — These require revenue data. Coffra is fictional.
      Reporting them would be invention.

    - **Real customer cohorts / retention curves** — Same reason as above.

    - **Real attribution data** — No paid traffic, no UTM parameter history,
      no multi-touch attribution model trained.

    What you see instead:
    - Real measurements where they exist (model performance, AI tool outputs)
    - Snapshot data where it was captured (CRM)
    - Simulated data where it is needed for visualization completeness, **clearly
      labeled with industry-anchored assumptions**
    """
)


# ============================================================
# PRODUCTION ROADMAP
# ============================================================
st.markdown("## Production Roadmap")

st.markdown(
    """
    To convert this portfolio dashboard into a live production system, the following
    changes would be required:
    """
)

roadmap = pd.DataFrame([
    {
        "Component": "HubSpot integration",
        "Current": "One-time snapshot via Private App",
        "Production": "Scheduled refresh (hourly cron) + live API fallback if snapshot is stale",
    },
    {
        "Component": "Email engagement",
        "Current": "Simulated (industry benchmarks)",
        "Production": "Pull from HubSpot/Brevo send reports via API; daily refresh",
    },
    {
        "Component": "Lead scoring",
        "Current": "Static model trained on public dataset",
        "Production": "Retrain monthly on Coffra-native data once 500+ labeled examples accumulate",
    },
    {
        "Component": "Attribution / ROI",
        "Current": "Not included",
        "Production": "Add UTM tracking, GA4 integration, 3-touch attribution model",
    },
    {
        "Component": "Deployment",
        "Current": "Streamlit Cloud (single-tenant)",
        "Production": "Multi-environment (dev/staging/prod), authentication, role-based access",
    },
])
st.dataframe(roadmap, use_container_width=True, hide_index=True)


# ============================================================
# RELATED DOCUMENTS
# ============================================================
st.markdown("## Related Documents in the Repository")

st.markdown(
    """
    For deeper detail on any aspect of this project, see:

    - `docs/01_business_context.md` — Coffra brand foundation
    - `docs/02_persona_connoisseur.md` and `docs/03_persona_daily_ritualist.md` — full personas
    - `docs/04_email_copy_connoisseur.md`, `docs/05_email_copy_daily_ritualist.md`,
      `docs/06_email_copy_cart_recovery.md` — full email copy with decisions logs
    - `docs/07_hubspot_workflow_specs.md` — HubSpot implementation specs and screenshots
    - `docs/08_ab_testing_methodology.md` — pre-registered A/B testing methodology
    - `notebooks/01_lead_scoring_eda_and_model.ipynb` — full ML notebook with leakage audit and SHAP
    - `case_study/P1_Coffra_Case_Study.pdf` — formal case study document

    Repository: [github.com/sebikradyel1-svg/coffra-marketing-automation](https://github.com/sebikradyel1-svg/coffra-marketing-automation)
    """
)


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    f"<p style='color: {MEDIUM_GRAY}; font-size: 0.85rem;'>"
    "Author: Sebastian Kradyel · Built April 2026 · "
    "Coffra is a fictional brand for portfolio demonstration."
    "</p>",
    unsafe_allow_html=True,
)
