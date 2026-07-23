"""
Lead scoring tool.

Loads the trained XGBoost model, its StandardScaler, and the feature spec
(models/lead_scoring_xgboost_v1.joblib, feature_scaler_v1.joblib,
feature_spec_v1.json) and exposes score_lead() to score a single lead:
returns a conversion-probability score in [0, 1] plus the top-3 SHAP
factors behind it.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import shap

MODELS_DIR = Path(__file__).resolve().parent / "models"
MODEL_PATH = MODELS_DIR / "lead_scoring_xgboost_v1.joblib"
SCALER_PATH = MODELS_DIR / "feature_scaler_v1.joblib"
FEATURE_SPEC_PATH = MODELS_DIR / "feature_spec_v1.json"


@lru_cache(maxsize=1)
def _load_artifacts():
    with open(FEATURE_SPEC_PATH, encoding="utf-8") as f:
        spec = json.load(f)
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    explainer = shap.TreeExplainer(model)
    return spec, model, scaler, explainer


def _email_engagement_rate(lead: dict[str, Any]) -> float:
    opens = lead.get("EmailOpens") or 0
    clicks = lead.get("EmailClicks") or 0
    return clicks / opens if opens else 0.0


def _engagement_score(lead: dict[str, Any]) -> float:
    """
    CAVEAT: EngagementScore is an engineered feature from the original
    training pipeline, and feature_spec_v1.json does not record its formula.
    This is a linear approximation reverse-engineered from the 20 rows in
    models/sample_predictions_v1.csv (R^2 ~ 0.97 against those rows, but not
    an exact match) - treat it as a placeholder. If you have the original
    feature-engineering code, use it instead; or pass "EngagementScore"
    directly in the lead dict to skip this approximation entirely.
    """
    eer = lead.get("EmailEngagementRate")
    if eer is None:
        eer = _email_engagement_rate(lead)
    return (
        0.1967 * lead.get("WebsiteVisits", 0)
        + 0.3374 * lead.get("PagesPerVisit", 0)
        + 0.2636 * lead.get("TimeOnSite", 0)
        - 0.1588 * eer
        + 1.826
    )


def _build_feature_vector(lead: dict[str, Any], feature_columns: list[str]) -> pd.DataFrame:
    lead = dict(lead)
    lead.setdefault("EmailEngagementRate", _email_engagement_rate(lead))
    lead.setdefault("EngagementScore", _engagement_score(lead))

    missing = [col for col in feature_columns if col not in lead]
    if missing:
        raise KeyError(f"Lead is missing required feature(s): {missing}")

    values = [float(lead[col]) for col in feature_columns]
    return pd.DataFrame([values], columns=feature_columns)


def score_lead(lead: dict[str, Any]) -> dict[str, Any]:
    """
    Score a single lead with the trained XGBoost model.

    Parameters
    ----------
    lead : dict
        Raw lead attributes keyed by the names in
        models/feature_spec_v1.json -> feature_columns (e.g. "Age",
        "Income", "WebsiteVisits", ..., one-hot flags like "Gender_Male",
        "CampaignChannel_PPC", "CampaignType_Conversion"). Engineered
        features "EmailEngagementRate" / "EngagementScore" are computed
        automatically if omitted.

    Returns
    -------
    dict:
        "score": float in [0, 1], probability the lead converts.
        "top_factors": up to 3 dicts, ranked by |SHAP value|:
            {"feature": str, "shap_value": float, "direction": "increases"|"decreases"}
    """
    spec, model, scaler, explainer = _load_artifacts()
    feature_columns = spec["feature_columns"]

    X = _build_feature_vector(lead, feature_columns)
    # NOTE: the XGBoost model was trained on raw (unscaled) features -
    # feature_scaler_v1.joblib belongs to the logistic-regression baseline
    # from the same training run, not to this model. Confirmed by comparing
    # predictions against models/sample_predictions_v1.csv: passing scaled
    # input decorrelates completely from the recorded predictions (corr
    # ~0.04), while passing raw input matches them almost exactly (corr
    # ~0.9999999). Do not scale X before predict_proba/SHAP here.
    score = float(model.predict_proba(X)[0, 1])

    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):  # binary-classification SHAP APIs vary by version
        shap_values = shap_values[1]
    shap_row = np.asarray(shap_values)[0]

    ranked_idx = np.argsort(-np.abs(shap_row))[:3]
    top_factors = [
        {
            "feature": feature_columns[i],
            "shap_value": round(float(shap_row[i]), 4),
            "direction": "increases" if shap_row[i] > 0 else "decreases",
        }
        for i in ranked_idx
    ]

    return {"score": round(score, 4), "top_factors": top_factors}


if __name__ == "__main__":
    sample_lead = {
        "Age": 34,
        "Income": 62000,
        "AdSpend": 3200.0,
        "WebsiteVisits": 18,
        "PagesPerVisit": 6.4,
        "TimeOnSite": 9.8,
        "SocialShares": 40,
        "EmailOpens": 12,
        "EmailClicks": 5,
        "PreviousPurchases": 3,
        "LoyaltyPoints": 1800,
        "Gender_Male": True,
        "CampaignChannel_PPC": False,
        "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": True,
        "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False,
        "CampaignType_Conversion": True,
        "CampaignType_Retention": False,
    }

    result = score_lead(sample_lead)
    print(f"Lead score: {result['score']:.2%}")
    print("Top factors:")
    for factor in result["top_factors"]:
        print(f"  - {factor['feature']}: {factor['shap_value']:+.4f} ({factor['direction']} score)")
