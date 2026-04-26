"""
Campaign Funnel Page - Simulated marketing pipeline visualization.

Clearly disclosed as simulated data (no real Coffra campaigns exist yet).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import numpy as np

from lib.styling import inject_custom_css, page_header, data_disclosure
from lib.plots import funnel_chart, line_chart, bar_chart, COFFRA_PALETTE


st.set_page_config(page_title="Campaign Funnel | Coffra", layout="wide")
inject_custom_css()

page_header(
    "Campaign Funnel",
    "Email engagement and conversion pipeline visualization"
)

data_disclosure(
    "simulated",
    "Coffra is a fictional brand with no active subscribers. The funnel below uses simulated "
    "data anchored to industry benchmarks (Mailchimp 2025 Food & Beverage averages: 22.1% open, "
    "2.3% CTR). In production, these values would come from HubSpot/Brevo email send reports."
)


# ============================================================
# SIMULATED FUNNEL (industry-anchored)
# ============================================================
st.markdown("## Persona Funnels")

st.markdown(
    "Two parallel funnels — one per persona — modelling a 14-day nurture campaign. "
    "Conversion rates anchored to specialty food/beverage benchmarks with a 1.15x premium-brand uplift."
)

# Industry-anchored numbers (Mailchimp 2025 F&B)
BASE_OPEN_RATE = 0.221  # 22.1%
BASE_CTR = 0.023        # 2.3%
PREMIUM_UPLIFT = 1.15
SUBSCRIBER_TO_OPEN = BASE_OPEN_RATE * PREMIUM_UPLIFT  # ~25.4%
OPEN_TO_CLICK = BASE_CTR * PREMIUM_UPLIFT * 4         # ~10.6% (clicks among openers, not all sends)
CLICK_TO_PURCHASE = 0.15  # ~15% (assumption: highly engaged clickers convert)


def simulate_funnel(starting_subscribers: int, persona_label: str, lift: float = 1.0):
    """Generate funnel stage counts for one persona."""
    opens = int(starting_subscribers * SUBSCRIBER_TO_OPEN * lift)
    clicks = int(opens * OPEN_TO_CLICK)
    customers = int(clicks * CLICK_TO_PURCHASE)

    return {
        "Subscribers": starting_subscribers,
        "Email Openers": opens,
        "Click-throughs": clicks,
        "Customers": customers,
    }


col_l, col_r = st.columns(2)

with col_l:
    st.markdown("### Connoisseur (EN journey)")
    conn_funnel = simulate_funnel(500, "Connoisseur", lift=1.10)

    st.plotly_chart(
        funnel_chart(
            stages=list(conn_funnel.keys()),
            values=list(conn_funnel.values()),
            title="",
            height=400,
        ),
        use_container_width=True,
    )

with col_r:
    st.markdown("### Daily Ritualist (RO journey)")
    dr_funnel = simulate_funnel(500, "Daily Ritualist", lift=1.0)

    st.plotly_chart(
        funnel_chart(
            stages=list(dr_funnel.keys()),
            values=list(dr_funnel.values()),
            title="",
            height=400,
        ),
        use_container_width=True,
    )

st.caption(
    "Connoisseur funnel uses a 1.10x lift assumption based on technical-content "
    "engagement premium. These are scenario assumptions, not measured values."
)


# ============================================================
# EMAIL-BY-EMAIL ENGAGEMENT (simulated cadence)
# ============================================================
st.markdown("## Engagement Decay Across Sequence")

st.markdown(
    "Open rates typically decline across a multi-email sequence as less-engaged subscribers "
    "drop off. Below is a simulated trajectory for the 5-email Connoisseur nurture."
)

# Simulated decay
emails = [
    "E1: Welcome",
    "E2: Origin Story",
    "E3: Brewing Guide",
    "E4: Subscription Pitch",
    "E5: Comparison Test",
]
# Realistic decay pattern — strong start, gradual tapering
open_rates = [32.5, 28.1, 26.3, 22.8, 19.4]
click_rates = [4.2, 3.8, 4.5, 3.1, 5.2]

col_a, col_b = st.columns(2)

with col_a:
    st.plotly_chart(
        line_chart(
            x=emails,
            y=open_rates,
            title="Simulated Open Rate (%) by Email",
            height=350,
        ),
        use_container_width=True,
    )

with col_b:
    st.plotly_chart(
        line_chart(
            x=emails,
            y=click_rates,
            title="Simulated Click Rate (%) by Email",
            height=350,
        ),
        use_container_width=True,
    )


# ============================================================
# CART RECOVERY PERFORMANCE
# ============================================================
st.markdown("## Cart Recovery Sequence (Simulated)")

st.markdown(
    "The 3-email cart recovery sequence (1h, 24h, 72h) shows declining open rates "
    "but stable conversion rates — the right metric is recovered cart percentage."
)

cart_emails = ["1h: Saving Spot", "24h: Quick Thought", "72h: Comparison Test"]
cart_open = [55.2, 38.4, 24.6]      # Higher than nurture (intent already shown)
cart_recovered = [12.1, 8.3, 6.4]   # Cart recovery rate per send

cart_df = pd.DataFrame({
    "Email": cart_emails,
    "Open Rate (%)": cart_open,
    "Recovery Rate (%)": cart_recovered,
})

col_x, col_y = st.columns([1, 2])

with col_x:
    st.dataframe(cart_df, use_container_width=True, hide_index=True)

with col_y:
    st.markdown("### Recovery economics")
    total_recovered = sum(cart_recovered) / 100  # Sum of percentages, treating as proportions
    st.metric(
        "Total recovered cart rate",
        f"{sum(cart_recovered):.1f}%",
        help="Cumulative recovery rate across all 3 emails. Industry average for cart recovery sequences is 15-25%."
    )
    st.markdown(
        "**Average order value** (Coffra estimate): 120 RON\n\n"
        "**Recovery value per 100 abandoned carts:**\n"
        f"~{int(sum(cart_recovered))} carts × 120 RON = **{int(sum(cart_recovered)) * 120:,} RON** recovered"
    )


# ============================================================
# DISCLOSURE FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    **Methodology notes:**

    All values on this page are simulated. Industry benchmarks used:
    - Mailchimp 2025 Food & Beverage email benchmarks (22.1% avg open, 2.3% avg CTR)
    - Premium brand uplift factor of 1.15 applied
    - Cart recovery rates anchored to industry standard 15-25% recovery range

    **Production replacement:** When Coffra has live email send data, this page would
    pull from HubSpot/Brevo email send reports and recalculate funnel metrics from
    actual events. The visualization structure stays the same; only the data source
    changes.
    """
)
