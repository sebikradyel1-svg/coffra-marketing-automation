"""
Coffra Marketing Dashboard - Main Page

Multi-page Streamlit app providing visibility into the Coffra marketing
automation system. Designed as a portfolio deliverable demonstrating
production-grade dashboard capabilities.

Run with:
    streamlit run dashboard/streamlit_dashboard.py

Pages are auto-discovered from dashboard/pages/.
"""

import sys
from pathlib import Path

# Ensure lib/ is importable regardless of where Streamlit is invoked
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from lib.styling import inject_custom_css, page_header, COFFRA_BROWN, MEDIUM_GRAY
from lib.data_loaders import (
    load_hubspot_metadata,
    load_model_metrics,
    get_optimizer_summary,
)


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Coffra Marketing Dashboard",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()


# ============================================================
# HEADER
# ============================================================
page_header(
    "Coffra Marketing Dashboard",
    "Operational visibility for the Coffra marketing automation system"
)


# ============================================================
# OVERVIEW
# ============================================================
st.markdown(
    """
    Welcome to the Coffra marketing operations dashboard. This is a portfolio
    deliverable demonstrating live data visualization for the marketing automation
    system documented in the [GitHub repository](https://github.com/sebikradyel1-svg/coffra-marketing-automation).

    Use the sidebar to navigate between operational views.
    """
)

st.markdown("### Quick Overview")

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

# Pull live values from snapshots
hubspot_meta = load_hubspot_metadata()
model_metrics = load_model_metrics()
optimizer_summary = get_optimizer_summary()

with col1:
    st.metric(
        label="Contacts in CRM",
        value=hubspot_meta.get("counts", {}).get("contacts", 0),
        help="Test contacts in HubSpot. Real production deployment would manage thousands."
    )

with col2:
    st.metric(
        label="Active Segments",
        value=hubspot_meta.get("counts", {}).get("segments", 0),
        help="Persona-based segments for workflow targeting."
    )

with col3:
    xgb_auc = model_metrics.get("models", {}).get("xgboost", {}).get("test_roc_auc", 0)
    st.metric(
        label="Lead Scoring Test AUC",
        value=f"{xgb_auc:.3f}" if xgb_auc else "—",
        help="XGBoost model performance on held-out test set."
    )

with col4:
    st.metric(
        label="Subject Variants Generated",
        value=len(optimizer_summary.get("all_variants", [])),
        help="Total subject line variants generated and scored by the AI Optimizer."
    )

st.markdown("---")


# ============================================================
# NAVIGATION GUIDE
# ============================================================
st.markdown("### Pages")

st.markdown(
    """
    - **Lead Quality** — Distribution of lead scores from the XGBoost model, with persona mapping.
    - **Subject Optimizer** — Performance of the AI-generated subject lines: variants, angles, scores.
    - **HubSpot CRM** — Snapshot of contacts, segments, and persona distribution from HubSpot.
    - **Campaign Funnel** — Email engagement and conversion funnel (simulated for demo).
    - **Methodology** — Honest disclosure of what is real, what is snapshot, what is simulated.
    """
)

st.markdown("---")


# ============================================================
# DATA TRANSPARENCY (footer)
# ============================================================
st.markdown("### Data Transparency")

extracted_at = hubspot_meta.get("extracted_at_human", "Not yet extracted")

st.markdown(
    f"""
    | Source | Type | Status |
    | --- | --- | --- |
    | HubSpot CRM | Snapshot | Extracted {extracted_at} |
    | Lead scoring model | Real | XGBoost trained on Kaggle dataset, fixed `random_state=42` |
    | Subject Optimizer cache | Real | {optimizer_summary.get('total_generations', 0)} generations + {optimizer_summary.get('total_evaluations', 0)} evaluations cached locally |
    | Campaign funnel data | Simulated | Mock data for demonstration; clearly labeled |

    See **Methodology** page for full disclosure.
    """
)

st.markdown("---")
st.markdown(
    f"<p style='color: {MEDIUM_GRAY}; font-size: 0.85rem;'>"
    "Coffra is a fictional brand created for portfolio demonstration. "
    "Author: Sebastian Kradyel · "
    "<a href='https://github.com/sebikradyel1-svg/coffra-marketing-automation' target='_blank'>GitHub</a>"
    "</p>",
    unsafe_allow_html=True,
)
