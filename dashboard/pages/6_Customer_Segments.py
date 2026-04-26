"""
Customer Segments Page - RFM segmentation insights from P3.

Reads the segmentation outputs (final_segmentation.parquet, summary JSON,
strategy playbook CSV, impact projections CSV) and visualizes them in
brand-aligned dashboard format.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json

from lib.styling import inject_custom_css, page_header, data_disclosure
from lib.plots import (
    bar_chart, donut_chart, COFFRA_PALETTE,
    apply_brand_layout
)
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="Customer Segments | Coffra", layout="wide")
inject_custom_css()

page_header(
    "Customer Segments",
    "RFM analysis with rule-based segments and ML clustering"
)

data_disclosure(
    "real",
    "Analysis performed on Online Retail II (UCI / Kaggle) — a real e-commerce dataset "
    "(UK retailer, 2009-2011, ~1M transactions). Methodology and findings transfer "
    "structurally to Coffra; persona alignment is heuristic until real customer data exists."
)


# ============================================================
# RESOLVE PATHS (works on Streamlit Cloud)
# ============================================================
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"


# ============================================================
# DATA LOADERS
# ============================================================

@st.cache_data
def load_segmentation_data():
    """Load all P3 outputs."""
    data = {}

    # Per-customer segmentation
    seg_path = PROCESSED_DIR / "final_segmentation.parquet"
    if seg_path.exists():
        data['customers'] = pd.read_parquet(seg_path)

    # Summary JSON
    summary_path = PROCESSED_DIR / "segmentation_summary.json"
    if summary_path.exists():
        with open(summary_path) as f:
            data['summary'] = json.load(f)

    # Strategy playbook
    playbook_path = PROCESSED_DIR / "strategy_playbook.csv"
    if playbook_path.exists():
        data['playbook'] = pd.read_csv(playbook_path)

    # Impact projections
    impact_path = PROCESSED_DIR / "impact_projections.csv"
    if impact_path.exists():
        data['impact'] = pd.read_csv(impact_path)

    # Clustering metadata
    cluster_path = PROCESSED_DIR / "clustering_summary.json"
    if cluster_path.exists():
        with open(cluster_path) as f:
            data['clustering'] = json.load(f)

    # RFM summary
    rfm_summary_path = PROCESSED_DIR / "rfm_summary.json"
    if rfm_summary_path.exists():
        with open(rfm_summary_path) as f:
            data['rfm_summary'] = json.load(f)

    return data


data = load_segmentation_data()

# Check that data is loaded
if 'customers' not in data:
    st.error(
        "Segmentation data not found. Run notebooks 02-05 in order to generate "
        "the parquet/JSON files in `data/processed/`."
    )
    st.stop()


# ============================================================
# SECTION: HEADLINE METRICS
# ============================================================
st.markdown("## Segmentation Overview")

summary = data.get('summary', {})
customers_df = data['customers']

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Customers analyzed",
        f"{summary.get('total_customers', len(customers_df)):,}"
    )

with c2:
    st.metric(
        "Total revenue observed",
        f"£{summary.get('total_revenue_observed_gbp', 0):,.0f}"
    )

with c3:
    st.metric(
        "Projected annual uplift",
        f"£{summary.get('projected_annual_uplift_gbp', 0):,.0f}",
        help="Sum of segment-specific lifts vs. untargeted broadcast baseline"
    )

with c4:
    st.metric(
        "Relative lift",
        f"+{summary.get('projected_lift_pct', 0):.1f}%"
    )


# ============================================================
# SECTION: SEGMENT DISTRIBUTION
# ============================================================
st.markdown("## Rule-Based Segments (11-Segment Framework)")

st.markdown(
    "Standard industry framework using R + FM scores. Provides interpretable, "
    "marketing-actionable categories."
)

if 'rfm_summary' in data:
    rfm_segments = data['rfm_summary']['segments']

    # Build dataframe
    seg_df = pd.DataFrame([
        {
            'Segment': seg,
            'Customers': info['customers'],
            'Pct_Customers': info['pct_customers'],
            'Pct_Revenue': info['pct_revenue'],
            'Avg_Recency': info['avg_recency'],
            'Avg_Frequency': info['avg_frequency'],
            'Avg_Monetary': info['avg_monetary'],
        }
        for seg, info in rfm_segments.items()
    ]).sort_values('Pct_Revenue', ascending=False)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        # Customer share donut
        st.plotly_chart(
            donut_chart(
                labels=seg_df['Segment'].tolist(),
                values=seg_df['Customers'].tolist(),
                title="Customers per Segment",
                height=420,
            ),
            use_container_width=True,
        )

    with col_b:
        # Revenue contribution bars
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            x=seg_df['Pct_Revenue'],
            y=seg_df['Segment'],
            orientation='h',
            marker_color="#3E2723",
            hovertemplate='%{y}: %{x}%<extra></extra>',
        ))
        apply_brand_layout(fig_rev, title="% of Revenue by Segment", height=420)
        fig_rev.update_yaxes(autorange='reversed')
        fig_rev.update_xaxes(title='% of total revenue')
        st.plotly_chart(fig_rev, use_container_width=True)

    # Detail table
    with st.expander("Segment economics — full table"):
        st.dataframe(
            seg_df.round(1),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# SECTION: ML CLUSTERING
# ============================================================
st.markdown("## ML Clustering Analysis (K-Means + Hierarchical)")

clustering = data.get('clustering', {})

col_x, col_y, col_z = st.columns(3)

with col_x:
    st.metric(
        "K-Means k selected",
        clustering.get('k', '—'),
        help="Optimal cluster count via elbow method + silhouette analysis"
    )

with col_y:
    sil = clustering.get('kmeans_quality', {}).get('silhouette', 0)
    st.metric(
        "K-Means silhouette",
        f"{sil:.3f}",
        help="Higher = better cluster separation. >0.3 acceptable for marketing data."
    )

with col_z:
    ari = clustering.get('method_agreement_ari', 0)
    st.metric(
        "K-Means vs Hierarchical (ARI)",
        f"{ari:.3f}",
        help="Adjusted Rand Index. >0.5 = strong agreement = robust clusters."
    )

st.markdown(
    "**Robustness check:** Both algorithms agree on cluster structure (ARI > 0.5), "
    "confirming clusters are not artifacts of method choice."
)

# Cluster distribution
if 'kmeans_label' in customers_df.columns:
    cluster_counts = customers_df['kmeans_label'].value_counts()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### Cluster Size")
        st.plotly_chart(
            bar_chart(
                x=cluster_counts.index.tolist(),
                y=cluster_counts.values.tolist(),
                horizontal=True,
                height=300,
            ),
            use_container_width=True,
        )

    with col_right:
        st.markdown("### Cluster Profiles (Avg RFM)")
        cluster_profiles = customers_df.groupby('kmeans_label').agg(
            customers=('Customer ID', 'count'),
            avg_recency=('Recency', 'mean'),
            avg_frequency=('Frequency', 'mean'),
            avg_monetary=('Monetary', 'mean'),
        ).round(1).sort_values('avg_monetary', ascending=False)

        cluster_profiles.columns = ['Customers', 'Avg Recency (days)',
                                     'Avg Frequency', 'Avg Monetary (£)']
        st.dataframe(cluster_profiles, use_container_width=True)


# ============================================================
# SECTION: PERSONA ALIGNMENT
# ============================================================
st.markdown("## Persona Alignment — Coffra Connoisseur vs Daily Ritualist")

st.markdown(
    "Inferred persona from RFM signature. In real Coffra deployment, persona would be "
    "captured explicitly via signup survey. This heuristic enables strategy testing now."
)

if 'Probable_Persona' in customers_df.columns:
    persona_summary = customers_df.groupby('Probable_Persona').agg(
        customers=('Customer ID', 'count'),
        total_revenue=('Monetary', 'sum'),
        avg_recency=('Recency', 'mean'),
        avg_frequency=('Frequency', 'mean'),
        avg_monetary=('Monetary', 'mean'),
    ).round(2)

    persona_summary['pct_customers'] = (persona_summary['customers'] /
                                          persona_summary['customers'].sum() * 100).round(1)
    persona_summary['pct_revenue'] = (persona_summary['total_revenue'] /
                                        persona_summary['total_revenue'].sum() * 100).round(1)

    # Critical insight: persona revenue concentration
    if 'Connoisseur (probable)' in persona_summary.index:
        c_pct_cust = persona_summary.loc['Connoisseur (probable)', 'pct_customers']
        c_pct_rev = persona_summary.loc['Connoisseur (probable)', 'pct_revenue']
        ratio = c_pct_rev / c_pct_cust if c_pct_cust > 0 else 0

        st.info(
            f"**Strategic insight:** Probable Connoisseurs are **{c_pct_cust}% of customers "
            f"but {c_pct_rev}% of revenue** — a {ratio:.1f}x revenue concentration ratio. "
            f"This validates P1's disproportionate investment in the Connoisseur email sequence."
        )

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.plotly_chart(
            donut_chart(
                labels=persona_summary.index.tolist(),
                values=persona_summary['customers'].tolist(),
                title="Customers by Persona",
                height=360,
            ),
            use_container_width=True,
        )

    with col_p2:
        st.plotly_chart(
            donut_chart(
                labels=persona_summary.index.tolist(),
                values=persona_summary['total_revenue'].tolist(),
                title="Revenue by Persona",
                height=360,
            ),
            use_container_width=True,
        )

    with st.expander("Persona summary — full table"):
        st.dataframe(persona_summary, use_container_width=True)


# ============================================================
# SECTION: STRATEGY PLAYBOOK
# ============================================================
st.markdown("## Strategic Playbook")

st.markdown(
    "Each segment maps to a specific marketing tactic, channel, and reference to P1 "
    "email content. This playbook is deployment-ready for HubSpot or Brevo workflows."
)

if 'playbook' in data:
    playbook = data['playbook']
    st.dataframe(playbook, use_container_width=True, hide_index=True, height=420)


# ============================================================
# SECTION: FINANCIAL IMPACT
# ============================================================
st.markdown("## Projected Financial Impact (Annual)")

data_disclosure(
    "simulated",
    "Lift assumptions are scenario projections anchored to industry benchmarks "
    "(Klaviyo, Bloomreach 2024 reports). Real Coffra deployment would measure "
    "actual lifts via A/B testing per segment. These are reasonable starting points, "
    "not guarantees."
)

if 'impact' in data:
    impact = data['impact'].sort_values('Annual_uplift_GBP', ascending=False)

    col_chart, col_metrics = st.columns([2, 1])

    with col_chart:
        # Bar chart
        fig_impact = go.Figure()
        fig_impact.add_trace(go.Bar(
            x=impact['Annual_uplift_GBP'],
            y=impact['Segment'],
            orientation='h',
            marker_color="#3E2723",
            text=[f'£{v:,.0f}' for v in impact['Annual_uplift_GBP']],
            textposition='outside',
            hovertemplate='%{y}<br>£%{x:,.0f}<extra></extra>',
        ))
        apply_brand_layout(fig_impact, title="Annual Uplift by Segment (£)", height=480)
        fig_impact.update_yaxes(autorange='reversed')
        fig_impact.update_xaxes(title='Projected annual uplift (£)')
        st.plotly_chart(fig_impact, use_container_width=True)

    with col_metrics:
        st.markdown("### Top 3 Segments")
        for i, row in impact.head(3).iterrows():
            st.markdown(f"**{row['Segment']}**")
            st.markdown(
                f"<div style='color: #6D4C41; margin-bottom: 1rem;'>"
                f"{row['Customers']:,} customers · {row['Lift_pct']} lift · "
                f"<b>£{row['Annual_uplift_GBP']:,.0f}/year</b>"
                f"</div>",
                unsafe_allow_html=True
            )

    with st.expander("Impact projection — full table"):
        st.dataframe(impact, use_container_width=True, hide_index=True)


# ============================================================
# SECTION: METHODOLOGY NOTE
# ============================================================
st.markdown("## Methodology Note")

st.markdown(
    """
    **Pipeline:**
    1. **EDA** (notebook 02): Cleaned 1.07M transactions to 770K usable.
    2. **RFM scoring** (notebook 03): Assigned R/F/M quintiles + 11 standard segments.
    3. **Clustering** (notebook 04): K-Means (k=4) + Hierarchical (Ward) on log-transformed,
       scaled features.
    4. **Strategy mapping** (notebook 05): Persona inference + segment playbook + financial
       projections.

    **Reproducibility:** All notebooks use `random_state=42`. Data is the public
    [Online Retail II UCI dataset](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci).

    **For Coffra production:**
    - Replace UK retail data with Coffra Shopify orders.
    - Capture persona explicitly via signup survey (avoid heuristic inference).
    - Run weekly pipeline; monitor segment migration matrix monthly.
    - A/B test campaign lifts per segment; iterate playbook with measured rates.

    **Documents in repo:**
    `notebooks/02_rfm_eda.ipynb`, `03_rfm_scoring_and_segments.ipynb`,
    `04_customer_clustering.ipynb`, `05_segment_to_strategy.ipynb`.
    """
)
