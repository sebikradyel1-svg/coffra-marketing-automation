"""
Lead Quality Page - XGBoost lead scoring model insights.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from lib.styling import inject_custom_css, page_header, data_disclosure, COFFRA_BROWN, COFFRA_BROWN_LIGHT
from lib.data_loaders import load_model_metrics, load_feature_spec, load_sample_predictions
from lib.plots import bar_chart, donut_chart, gauge_chart, histogram, apply_brand_layout


st.set_page_config(page_title="Lead Quality | Coffra", layout="wide")
inject_custom_css()

page_header(
    "Lead Quality",
    "XGBoost lead scoring model — performance, distribution, and persona mapping"
)

data_disclosure(
    "real",
    "Model trained on Kaggle 'Predict Conversion in Digital Marketing' dataset (8,000 records). "
    "Fixed random seed for reproducibility. Sample predictions table is from held-out test set."
)


# ============================================================
# LOAD DATA
# ============================================================
metrics = load_model_metrics()
feature_spec = load_feature_spec()
sample_preds = load_sample_predictions()


# ============================================================
# MODEL PERFORMANCE OVERVIEW
# ============================================================
st.markdown("## Model Performance")

xgb = metrics.get("models", {}).get("xgboost", {})
logreg = metrics.get("models", {}).get("logistic_regression", {})

col1, col2, col3 = st.columns(3)

with col1:
    auc = xgb.get("test_roc_auc", 0)
    st.plotly_chart(
        gauge_chart(auc * 100, max_value=100, label="Test ROC-AUC", height=280),
        use_container_width=True,
    )

with col2:
    pr_auc = xgb.get("test_pr_auc", 0)
    st.plotly_chart(
        gauge_chart(pr_auc * 100, max_value=100, label="Test PR-AUC", height=280),
        use_container_width=True,
    )

with col3:
    cv_mean = xgb.get("cv_roc_auc_mean", 0)
    cv_std = xgb.get("cv_roc_auc_std", 0)
    st.markdown("### CV Performance")
    st.metric("Mean CV ROC-AUC", f"{cv_mean:.4f}")
    st.metric("Standard deviation", f"±{cv_std:.4f}")
    st.caption("Cross-validated on training set with 5 folds")


# ============================================================
# BASELINE COMPARISON
# ============================================================
st.markdown("## Baseline Comparison")

st.markdown(
    "Logistic Regression as the baseline establishes a floor; XGBoost must beat it to justify "
    "the additional complexity. See full notebook for cross-validation and ablation details."
)

comparison_df = pd.DataFrame({
    "Model": ["Logistic Regression (baseline)", "XGBoost"],
    "CV ROC-AUC": [
        f"{logreg.get('cv_roc_auc_mean', 0):.4f} ± {logreg.get('cv_roc_auc_std', 0):.4f}",
        f"{xgb.get('cv_roc_auc_mean', 0):.4f} ± {xgb.get('cv_roc_auc_std', 0):.4f}",
    ],
    "Test ROC-AUC": [
        f"{logreg.get('test_roc_auc', 0):.4f}",
        f"{xgb.get('test_roc_auc', 0):.4f}",
    ],
    "Test PR-AUC": [
        f"{logreg.get('test_pr_auc', 0):.4f}",
        f"{xgb.get('test_pr_auc', 0):.4f}",
    ],
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)


# ============================================================
# CLASS BALANCE
# ============================================================
st.markdown("## Dataset Class Balance")

balance = metrics.get("class_balance", {})
converted = balance.get("converted", 0)
not_converted = balance.get("not_converted", 0)

if converted or not_converted:
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.plotly_chart(
            donut_chart(
                labels=["Converted", "Did not convert"],
                values=[converted, not_converted],
                title="Class Distribution",
                height=350,
            ),
            use_container_width=True,
        )
    with col_b:
        st.markdown("### Honest disclosure")
        st.markdown(
            f"""
            The training data has an **atypical class balance**: {converted:,} converted vs
            {not_converted:,} not converted (~88% positive class).

            Real marketing conversion rates are typically 2-5%. This dataset likely represents
            a filtered population or synthetic data designed for ML practice.

            **Mitigations applied:**
            - Used `class_weight='balanced'` for Logistic Regression
            - Used `scale_pos_weight` for XGBoost
            - Reported PR-AUC alongside ROC-AUC for imbalance-aware evaluation
            """
        )


# ============================================================
# SAMPLE PREDICTIONS WITH PERSONA MAPPING
# ============================================================
st.markdown("## Sample Predictions")

st.markdown(
    "Twenty test set predictions, with each contact's predicted probability mapped to a "
    "Coffra lead segment based on score thresholds (0-40 cold, 40-80 warm MQL, 80+ sales-ready)."
)

if not sample_preds.empty:
    # Distribution of lead scores
    st.markdown("### Score Distribution (sample)")
    if "lead_score_0_100" in sample_preds.columns:
        st.plotly_chart(
            histogram(
                sample_preds["lead_score_0_100"].tolist(),
                bins=10,
                x_label="Lead Score (0-100)",
                title="Distribution of lead scores in sample",
                height=300,
            ),
            use_container_width=True,
        )

    # Segment counts
    if "segment" in sample_preds.columns:
        segment_counts = sample_preds["segment"].value_counts().to_dict()
        st.markdown("### Segment Breakdown")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Low (0-40)", segment_counts.get("Low", 0))
        with col2:
            st.metric("Medium (40-80)", segment_counts.get("Medium", 0))
        with col3:
            st.metric("High / MQL (80+)", segment_counts.get("High (MQL handoff)", 0))

    # Sample table (limit columns for readability)
    st.markdown("### Sample table (first 10 rows)")
    display_cols = ["true_label", "predicted_probability", "lead_score_0_100", "segment"]
    display_cols = [c for c in display_cols if c in sample_preds.columns]
    if display_cols:
        st.dataframe(
            sample_preds[display_cols].head(10).round(3),
            use_container_width=True,
            hide_index=True,
        )
else:
    st.info("Sample predictions not yet generated. Run the lead scoring notebook to populate.")


# ============================================================
# FEATURE ENGINEERING DISCLOSURE
# ============================================================
st.markdown("## Feature Engineering")

if feature_spec:
    eng_features = feature_spec.get("engineered_features", [])
    leakage_dropped = feature_spec.get("dropped_leakage_columns", [])
    zero_var_dropped = feature_spec.get("dropped_zero_var_columns", [])

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("**Engineered features**")
        for f in eng_features:
            st.markdown(f"- `{f}`")

    with col_r:
        st.markdown("**Removed before training (leakage / zero variance)**")
        for f in leakage_dropped + zero_var_dropped:
            st.markdown(f"- `{f}`")

    st.caption(
        "Removing leakage features before training is essential. A model that uses "
        "`ConversionRate` as a feature to predict `Conversion` would achieve near-perfect "
        "metrics during training but fail in production because the feature does not exist "
        "before conversion happens."
    )


# ============================================================
# DEPLOYMENT MAPPING
# ============================================================
st.markdown("## Coffra Production Mapping")

st.markdown(
    """
    Lead scores translate into HubSpot workflow actions:

    | Score | Segment | Action |
    | --- | --- | --- |
    | 80-100 | High (Sales-Ready) | Immediate handoff to Sebastian; personal email |
    | 40-80 | Medium (Warm MQL) | Accelerated nurture; weekly contact; activation incentive |
    | 0-40 | Low (Cold) | Standard nurture; 2-4 week cadence |

    See full mapping rationale in the lead scoring notebook (`notebooks/01_lead_scoring_eda_and_model.ipynb`).
    """
)
