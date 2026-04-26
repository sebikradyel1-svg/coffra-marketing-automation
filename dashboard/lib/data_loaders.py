"""
Coffra Dashboard - Data Loading Module.

Centralizes file I/O for all dashboard pages. Each loader is cached via
streamlit's @st.cache_data to avoid re-reading on every interaction.
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st


# Resolve paths relative to repo root (works regardless of where Streamlit is run from)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

SNAPSHOTS_DIR = REPO_ROOT / "data" / "snapshots"
MODELS_DIR = REPO_ROOT / "src" / "models"
CACHE_DIR = REPO_ROOT / "cache" / "subject_optimizer"


# ============================================================
# HUBSPOT SNAPSHOT
# ============================================================

@st.cache_data
def load_hubspot_contacts():
    """Load contacts from HubSpot snapshot."""
    path = SNAPSHOTS_DIR / "contacts.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_hubspot_segments():
    """Load segments from HubSpot snapshot."""
    path = SNAPSHOTS_DIR / "segments.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_hubspot_personas():
    """Load persona distribution from HubSpot snapshot."""
    path = SNAPSHOTS_DIR / "persona_distribution.json"
    if not path.exists():
        return {"distribution": {}, "property_definition": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_hubspot_metadata():
    """Load snapshot metadata (when extracted, etc)."""
    path = SNAPSHOTS_DIR / "snapshot_metadata.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def map_persona_label(internal_value: str) -> str:
    """Maps HubSpot internal persona values to human-readable labels."""
    mapping = {
        "persona_1": "Connoisseur",
        "persona_2": "Daily Ritualist",
        "persona_3": "(other)",
        "(unset)": "(unset)",
    }
    return mapping.get(internal_value, internal_value.replace("_", " ").title())


# ============================================================
# LEAD SCORING MODEL
# ============================================================

@st.cache_data
def load_model_metrics():
    """Load lead scoring model metrics."""
    path = MODELS_DIR / "metrics_v1.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_feature_spec():
    """Load lead scoring feature specification."""
    path = MODELS_DIR / "feature_spec_v1.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_sample_predictions():
    """Load sample predictions CSV from lead scoring."""
    path = MODELS_DIR / "sample_predictions_v1.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


# ============================================================
# SUBJECT OPTIMIZER CACHE
# ============================================================

@st.cache_data
def load_optimizer_cache():
    """
    Load all cached Subject Optimizer responses.

    Returns:
        dict with 'generations' and 'evaluations' lists, each entry containing
        the parsed JSON response plus its filename for traceability.
    """
    if not CACHE_DIR.exists():
        return {"generations": [], "evaluations": []}

    generations = []
    evaluations = []

    for json_file in sorted(CACHE_DIR.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        if "variants" in data:
            generations.append({
                "filename": json_file.name,
                **data,
            })
        elif "evaluations" in data:
            evaluations.append({
                "filename": json_file.name,
                **data,
            })

    return {"generations": generations, "evaluations": evaluations}


@st.cache_data
def get_optimizer_summary():
    """
    Aggregate Subject Optimizer cache into summary stats.

    Returns:
        dict with token usage, persona breakdown, top scores, etc.
    """
    cache_data = load_optimizer_cache()

    summary = {
        "total_generations": len(cache_data["generations"]),
        "total_evaluations": len(cache_data["evaluations"]),
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "personas_used": set(),
        "all_variants": [],
    }

    for gen in cache_data["generations"]:
        meta = gen.get("metadata", {})
        summary["total_input_tokens"] += meta.get("input_tokens", 0)
        summary["total_output_tokens"] += meta.get("output_tokens", 0)
        if meta.get("persona"):
            summary["personas_used"].add(meta["persona"])

        for v in gen.get("variants", []):
            summary["all_variants"].append({
                "persona": meta.get("persona", "unknown"),
                "text": v.get("text", ""),
                "char_count": v.get("char_count", 0),
                "angle": v.get("angle", "unknown"),
            })

    # Add evaluation token costs
    for ev in cache_data["evaluations"]:
        meta = ev.get("metadata", {})
        summary["total_input_tokens"] += meta.get("input_tokens", 0)
        summary["total_output_tokens"] += meta.get("output_tokens", 0)

    # Estimated cost (Claude Sonnet 4.6 pricing approx):
    # $3/MTok input, $15/MTok output (verify on https://www.anthropic.com/pricing)
    summary["estimated_cost_usd"] = (
        (summary["total_input_tokens"] / 1_000_000) * 3.0
        + (summary["total_output_tokens"] / 1_000_000) * 15.0
    )

    summary["personas_used"] = sorted(summary["personas_used"])
    return summary
