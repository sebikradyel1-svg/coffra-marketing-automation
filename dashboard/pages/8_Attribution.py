"""
Attribution Page - Multi-Touch Attribution + Marketing Mix Modeling.

Reads outputs from notebooks 08, 09, 10 and visualizes attribution analysis:
- Method comparison (6 MTA + 1 MMM vs Ground Truth)
- Channel ROI / CPA analysis
- Bayesian credible intervals
- Strategic recommendations
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
import numpy as np

from lib.styling import inject_custom_css, page_header, data_disclosure, COFFRA_BROWN, MEDIUM_GRAY
from lib.plots import bar_chart, donut_chart, gauge_chart, COFFRA_PALETTE, apply_brand_layout
import plotly.graph_objects as go


st.set_page_config(page_title="Attribution | Coffra", layout="wide")
inject_custom_css()

page_header(
    "Marketing Attribution",
    "Multi-Touch Attribution + Bayesian Marketing Mix Model"
)

data_disclosure(
    "simulated",
    "Analysis on synthetic data (50K customers, 2 years daily spend) with known ground truth. "
    "Methodology validated against true channel contributions. Real Coffra deployment requires "
    "6+ months of actual touchpoint and spend data, plus quarterly holdout tests for "
    "incrementality validation."
)


# ============================================================
# RESOLVE PATHS
# ============================================================
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"


# ============================================================
# DATA LOADERS
# ============================================================

@st.cache_data
def load_attribution_data():
    data = {}

    # Final summary
    summary_path = PROCESSED_DIR / "attribution_final_summary.json"
    if summary_path.exists():
        with open(summary_path) as f:
            data['summary'] = json.load(f)

    # Unified comparison
    unified_path = PROCESSED_DIR / "attribution_unified_comparison.csv"
    if unified_path.exists():
        data['unified'] = pd.read_csv(unified_path)

    # MMM ROI
    roi_path = PROCESSED_DIR / "mmm_roi_analysis.csv"
    if roi_path.exists():
        data['roi'] = pd.read_csv(roi_path)

    # MMM detailed
    mmm_path = PROCESSED_DIR / "mmm_summary.json"
    if mmm_path.exists():
        with open(mmm_path) as f:
            data['mmm'] = json.load(f)

    # MTA detailed
    mta_path = PROCESSED_DIR / "mta_summary.json"
    if mta_path.exists():
        with open(mta_path) as f:
            data['mta'] = json.load(f)

    # Method assessment
    assess_path = PROCESSED_DIR / "attribution_method_assessment.csv"
    if assess_path.exists():
        data['assessment'] = pd.read_csv(assess_path)

    # Recommendations
    rec_path = PROCESSED_DIR / "attribution_recommendations.csv"
    if rec_path.exists():
        data['recommendations'] = pd.read_csv(rec_path)

    # Ground truth
    gt_path = PROCESSED_DIR / "attribution_ground_truth.json"
    if gt_path.exists():
        with open(gt_path) as f:
            data['ground_truth'] = json.load(f)

    return data


data = load_attribution_data()

if 'summary' not in data:
    st.error(
        "Attribution data not found. Run notebooks 07 → 08 → 09 → 10 in order to "
        "generate outputs in `data/processed/`."
    )
    st.stop()


# ============================================================
# SECTION: HEADLINE METRICS
# ============================================================
st.markdown("## Attribution Analysis Overview")

summary = data['summary']
mmm = data.get('mmm', {})

c1, c2, c3, c4 = st.columns(4)

with c1:
    n_methods = len(summary.get('methods_compared', []))
    st.metric("Methods compared", n_methods, help="6 MTA methods + 1 Bayesian MMM")

with c2:
    n_channels = len(summary.get('channels_analyzed', []))
    st.metric("Channels analyzed", n_channels)

with c3:
    fit_metrics = mmm.get('fit_metrics', {})
    r2 = fit_metrics.get('r2', 0)
    st.metric(
        "MMM R²",
        f"{r2:.3f}",
        help="Model fit quality. >0.6 acceptable for daily noisy time series.",
    )

with c4:
    cpa_ratio = summary.get('cpa_ratio_worst_to_best', 0)
    st.metric(
        "CPA spread (worst/best)",
        f"{cpa_ratio:.1f}x",
        help="Most expensive channel costs Nx more per acquisition than cheapest. Big spread = big optimization opportunity.",
    )


# ============================================================
# SECTION: METHOD COMPARISON
# ============================================================
st.markdown("## Method Comparison vs Ground Truth")

st.markdown(
    "Each method estimates channel contribution differently. The synthetic dataset has "
    "**known ground truth** so we can directly measure each method's accuracy."
)

if 'unified' in data:
    unified = data['unified']
    method_errors = summary.get('method_errors', {})

    # Build the long-format DataFrame for plotting
    methods = ['Last-Click', 'First-Click', 'Linear', 'Time-Decay', 'Markov', 'Shapley', 'MMM Bayesian']
    channels = unified['Channel'].tolist()

    # Grouped bar chart
    fig = go.Figure()

    method_colors = {
        'Last-Click': '#A1887F',
        'First-Click': '#BCAAA4',
        'Linear': '#D7CCC8',
        'Time-Decay': '#8D6E63',
        'Markov': '#6D4C41',
        'Shapley': '#5D4037',
        'MMM Bayesian': '#3E2723',
    }

    for method in methods:
        if method in unified.columns:
            fig.add_trace(go.Bar(
                name=method,
                x=channels,
                y=unified[method].values,
                marker_color=method_colors.get(method, '#6D4C41'),
            ))

    # Add ground truth as scatter overlay
    fig.add_trace(go.Scatter(
        name='Ground Truth',
        x=channels,
        y=unified['Ground Truth (%)'].values,
        mode='markers',
        marker=dict(symbol='diamond', size=18, color='red',
                     line=dict(color='white', width=2)),
    ))

    apply_brand_layout(fig, title="Channel Attribution by Method (% of paid conversions)", height=500)
    fig.update_layout(barmode='group', legend=dict(orientation='h', y=-0.15))
    st.plotly_chart(fig, use_container_width=True)

    # Method accuracy ranking
    st.markdown("### Method Accuracy Ranking")

    if method_errors:
        errors_df = pd.DataFrame(
            list(method_errors.items()),
            columns=['Method', 'Total Absolute Error (pp)']
        ).sort_values('Total Absolute Error (pp)')

        col_table, col_chart = st.columns([1, 1])

        with col_table:
            st.dataframe(errors_df, use_container_width=True, hide_index=True)

        with col_chart:
            fig_err = go.Figure()
            fig_err.add_trace(go.Bar(
                x=errors_df['Total Absolute Error (pp)'],
                y=errors_df['Method'],
                orientation='h',
                marker_color=COFFRA_BROWN,
            ))
            apply_brand_layout(fig_err, title="Total Error vs Ground Truth (lower is better)", height=300)
            fig_err.update_yaxes(autorange='reversed')
            st.plotly_chart(fig_err, use_container_width=True)

        st.info(
            f"**Best method:** {summary.get('best_method_by_accuracy', 'N/A')} "
            f"({summary.get('best_method_error_pp', 0):.1f} pp error). "
            f"**Worst:** {summary.get('worst_method_by_accuracy', 'N/A')} "
            f"({summary.get('worst_method_error_pp', 0):.1f} pp). "
            "Method ranking depends on path structure — Last-Click can outperform sophisticated "
            "methods if last-touch correlates with true contribution."
        )


# ============================================================
# SECTION: ROI / CPA ANALYSIS (FROM MMM)
# ============================================================
st.markdown("## Channel ROI Analysis (from Bayesian MMM)")

if 'roi' in data:
    roi = data['roi'].copy()

    # Sort by CPA
    roi_sorted = roi.sort_values('CPA (£)')

    col_metrics, col_chart = st.columns([1, 2])

    with col_metrics:
        best_ch = summary.get('best_channel_cpa', 'N/A')
        worst_ch = summary.get('worst_channel_cpa', 'N/A')
        best_cpa = summary.get('best_cpa_value', 0)
        worst_cpa = summary.get('worst_cpa_value', 0)

        st.markdown(f"**Most efficient channel**")
        st.markdown(
            f"<h3 style='color: #3E2723; margin: 0;'>{best_ch}</h3>"
            f"<p style='color: #6D4C41;'>£{best_cpa:.2f} CPA</p>",
            unsafe_allow_html=True,
        )

        st.markdown(f"**Least efficient channel**")
        st.markdown(
            f"<h3 style='color: #6D4C41; margin: 0;'>{worst_ch}</h3>"
            f"<p style='color: #A1887F;'>£{worst_cpa:.2f} CPA ({worst_cpa/best_cpa:.1f}x more)</p>",
            unsafe_allow_html=True,
        )

    with col_chart:
        # Color-coded CPA bars
        colors = []
        for ch in roi_sorted['Channel']:
            if ch == best_ch:
                colors.append('#3E2723')   # Best — dark
            elif ch == worst_ch:
                colors.append('#A1887F')   # Worst — light
            else:
                colors.append('#6D4C41')   # Mid

        fig_cpa = go.Figure()
        fig_cpa.add_trace(go.Bar(
            x=roi_sorted['CPA (£)'],
            y=roi_sorted['Channel'],
            orientation='h',
            marker_color=colors,
            text=[f'£{v:.2f}' for v in roi_sorted['CPA (£)']],
            textposition='outside',
        ))
        apply_brand_layout(fig_cpa, title="Cost Per Acquisition by Channel", height=320)
        fig_cpa.update_yaxes(autorange='reversed')
        st.plotly_chart(fig_cpa, use_container_width=True)

    # Detail table
    with st.expander("Full ROI table"):
        st.dataframe(roi.round(2), use_container_width=True, hide_index=True)


# ============================================================
# SECTION: MMM CONVERGENCE & FIT
# ============================================================
st.markdown("## MMM Bayesian Model Validation")

st.markdown(
    "Bayesian models must converge before estimates can be trusted. We use NUTS sampling "
    "with 2 chains × 1000 samples and check standard diagnostics."
)

if mmm:
    convergence = mmm.get('convergence', {})
    fit_metrics = mmm.get('fit_metrics', {})

    col_v1, col_v2, col_v3, col_v4 = st.columns(4)

    with col_v1:
        rhat = convergence.get('max_rhat', 0)
        rhat_status = "✓ GOOD" if rhat < 1.01 else "⚠ CHECK"
        st.metric("Max R-hat", f"{rhat:.3f}", help="Target < 1.01. Indicates chain convergence.")

    with col_v2:
        ess = convergence.get('min_ess_bulk', 0)
        st.metric("Min ESS", f"{ess:,}", help="Effective Sample Size. Target > 400.")

    with col_v3:
        r2 = fit_metrics.get('r2', 0)
        st.metric("R²", f"{r2:.3f}", help="Variance explained. >0.6 acceptable for noisy daily data.")

    with col_v4:
        coverage = fit_metrics.get('ci_coverage_pct', 0)
        st.metric("95% CI coverage", f"{coverage:.1f}%", help="Should be ~95% if model is well-calibrated.")

    if rhat < 1.01 and ess > 400:
        st.success(
            "Model converged successfully. Estimates can be trusted within stated uncertainty intervals."
        )
    else:
        st.warning(
            "Convergence diagnostics suggest model needs more samples or specification review."
        )


# ============================================================
# SECTION: METHOD ASSESSMENT
# ============================================================
st.markdown("## Honest Method Assessment")

st.markdown(
    "Each attribution method has strengths and structural failures. No method is universally "
    "best — production deployment uses multiple methods and triangulates."
)

if 'assessment' in data:
    st.dataframe(data['assessment'], use_container_width=True, hide_index=True, height=300)


# ============================================================
# SECTION: BUSINESS RECOMMENDATIONS
# ============================================================
st.markdown("## Coffra Action Plan")

if 'recommendations' in data:
    recommendations = data['recommendations']

    for _, row in recommendations.iterrows():
        with st.container():
            st.markdown(f"### {row['Recommendation']}")
            col_a, col_b, col_c = st.columns([2, 2, 1])
            with col_a:
                st.markdown(f"**Action:** {row['Action']}")
            with col_b:
                st.markdown(f"**Expected impact:** {row['Expected impact']}")
            with col_c:
                st.markdown(f"**Cost:** {row['Investment']}")
            st.markdown("---")


# ============================================================
# SECTION: METHODOLOGY
# ============================================================
st.markdown("## Methodology")

st.markdown(
    """
    **Data:**
    - 50,000 synthetic customers, 92-day window for MTA
    - 731 daily observations, 2-year window for MMM
    - 5 channels (Google Ads, Meta Ads, Instagram Organic, Email, Direct)
    - **Ground truth tracked:** True channel contribution stored in metadata for validation

    **MTA pipeline (notebook 08):**
    - 6 methods: Last-Click, First-Click, Linear, Time-Decay (7-day half-life),
      Markov Chain (removal effect), Shapley Values (exact enumeration over 2^5 coalitions)
    - Path-dependent — operates on individual customer journeys

    **MMM pipeline (notebook 09):**
    - Bayesian regression with PyMC + NUTS sampling
    - Adstock transformation (geometric carryover)
    - Hill saturation (diminishing returns)
    - Annual + weekly seasonality
    - Posterior credible intervals (95%) on all channel contributions

    **Validation:**
    - Both methods compared against synthetic ground truth
    - MMM: posterior predictive checks (R², MAE, MAPE, CI coverage)
    - MTA: per-method error analysis vs ground truth

    **Honest disclosure:**
    - Synthetic data validates methodology; does not reflect real Coffra performance
    - Real deployment requires 6+ months of UTM/spend data + holdout tests
    - Method choice depends on dataset structure — no universal winner
    """
)


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    f"<p style='color: {MEDIUM_GRAY}; font-size: 0.85rem;'>"
    "P5 Coffra Attribution Modeling · Built April 2026 · "
    "Notebooks 07-10 · Methodology: docs/13"
    "</p>",
    unsafe_allow_html=True,
)
