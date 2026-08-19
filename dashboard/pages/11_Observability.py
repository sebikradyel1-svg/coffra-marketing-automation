"""
Observability Page - REVISE vs APPROVE trend for the Governance Reviewer (P7).

Reads the existing logs/decisions.jsonl (already written by log_decision in
utils/logger.py on every pipeline run - no new logging needed for this page)
and plots the weekly split of governance verdicts. This turns the one-off
50-draft calibration test (100% recall / 88.2% precision) into an ongoing
signal: if REVISE rate drifts up over time, that's visible here instead of
only being caught by re-running the manual test set.
"""

import json
import sys
from pathlib import Path

PAGE_DIR = Path(__file__).resolve().parent
DASHBOARD_DIR = PAGE_DIR.parent
REPO_ROOT = DASHBOARD_DIR.parent

sys.path.insert(0, str(DASHBOARD_DIR))
sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
import plotly.express as px
import streamlit as st

from lib.styling import inject_custom_css, page_header

LOG_PATH = REPO_ROOT / "src" / "lead_intelligence" / "logs" / "decisions.jsonl"

st.set_page_config(page_title="Observability | Coffra", page_icon="C", layout="wide")
inject_custom_css()

page_header(
    "Observability",
    "Rata săptămânală REVISE vs APPROVE a Governance Reviewer-ului, din log-ul de decizii al pipeline-ului",
)


def load_governance_events() -> pd.DataFrame:
    """Parse logs/decisions.jsonl and keep only governance-step verdicts."""
    if not LOG_PATH.exists():
        return pd.DataFrame(columns=["timestamp", "verdict"])

    rows = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("step") != "governance":
                continue
            verdict = (record.get("output") or {}).get("verdict")
            if verdict not in ("APPROVE", "REVISE"):
                continue
            rows.append({"timestamp": record["timestamp"], "verdict": verdict})

    return pd.DataFrame(rows)


df = load_governance_events()

if df.empty:
    st.info(
        "Încă nu există decizii de governance în log. Rulează agentul din "
        "pagina Lead Intelligence (pentru lead-uri HOT) ca să populezi datele."
    )
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["week"] = df["timestamp"].dt.to_period("W").apply(lambda p: p.start_time.date())

    weekly = df.groupby(["week", "verdict"]).size().reset_index(name="count")

    total = len(df)
    approve_rate = (df["verdict"] == "APPROVE").mean() * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Total verdicte", total)
    c2.metric("APPROVE rate", f"{approve_rate:.1f}%")
    c3.metric("Săptămâni acoperite", df["week"].nunique())

    fig = px.bar(
        weekly,
        x="week",
        y="count",
        color="verdict",
        barmode="group",
        color_discrete_map={"APPROVE": "#4CAF50", "REVISE": "#E07A5F"},
        labels={"week": "Săptămână", "count": "Număr verdicte", "verdict": "Verdict"},
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Date brute"):
        st.dataframe(
            df.sort_values("timestamp", ascending=False),
            use_container_width=True,
        )
