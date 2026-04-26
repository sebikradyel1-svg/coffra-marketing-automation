"""
Subject Optimizer Page - AI-generated subject lines analysis.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from lib.styling import inject_custom_css, page_header, data_disclosure
from lib.data_loaders import load_optimizer_cache, get_optimizer_summary
from lib.plots import bar_chart, donut_chart, grouped_bar_chart


st.set_page_config(page_title="Subject Optimizer | Coffra", layout="wide")
inject_custom_css()

page_header(
    "Subject Line Optimizer",
    "AI-generated subject lines: variants, angles, and per-persona scoring"
)

data_disclosure(
    "real",
    "Real outputs from the Claude-powered Subject Line Optimizer (src/subject_optimizer/). "
    "Each entry below was generated and scored by Claude API calls cached locally."
)


# ============================================================
# LOAD DATA
# ============================================================
cache = load_optimizer_cache()
summary = get_optimizer_summary()


# ============================================================
# SUMMARY METRICS
# ============================================================
st.markdown("## Cache Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Generations", summary["total_generations"])
with c2:
    st.metric("Evaluations", summary["total_evaluations"])
with c3:
    st.metric("Variants Total", len(summary["all_variants"]))
with c4:
    st.metric("Estimated Cost (USD)", f"${summary['estimated_cost_usd']:.4f}")

st.caption(
    f"Token usage: {summary['total_input_tokens']:,} input + "
    f"{summary['total_output_tokens']:,} output. "
    f"Cost estimate based on Claude Sonnet 4.6 pricing (verify on anthropic.com/pricing)."
)


# ============================================================
# PERSONA BREAKDOWN
# ============================================================
st.markdown("## Persona Coverage")

if summary["all_variants"]:
    df = pd.DataFrame(summary["all_variants"])
    persona_counts = df["persona"].value_counts().to_dict()

    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.plotly_chart(
            donut_chart(
                labels=list(persona_counts.keys()),
                values=list(persona_counts.values()),
                title="Variants by persona",
                height=320,
            ),
            use_container_width=True,
        )
    with col_r:
        st.markdown("### Why coverage matters")
        st.markdown(
            """
            For the AI Subject Optimizer to be useful in a multi-persona system, it must
            generate variants calibrated to each persona's voice. The cache shows whether
            the tool has been exercised across both personas, validating the
            persona-conditional prompt design.

            If one persona dominates the cache, the tool's prompts for that persona may
            be more refined than the other — a useful signal for prompt iteration.
            """
        )
else:
    st.info("No variants in cache yet. Run the Subject Optimizer to populate.")


# ============================================================
# ANGLE DISTRIBUTION
# ============================================================
st.markdown("## Strategic Angle Distribution")

if summary["all_variants"]:
    df = pd.DataFrame(summary["all_variants"])
    angle_counts = df["angle"].value_counts().reset_index()
    angle_counts.columns = ["angle", "count"]

    st.plotly_chart(
        bar_chart(
            x=angle_counts["angle"].tolist(),
            y=angle_counts["count"].tolist(),
            title="Angles used across all generated variants",
            height=350,
        ),
        use_container_width=True,
    )

    st.caption(
        "The Optimizer generates 5 variants per call, using 5 distinct angles "
        "(direct, curiosity, insider, counter-intuitive, invitation). A balanced distribution "
        "indicates the prompt is working as intended."
    )


# ============================================================
# CHARACTER LENGTH ANALYSIS
# ============================================================
st.markdown("## Subject Line Length Distribution")

if summary["all_variants"]:
    df = pd.DataFrame(summary["all_variants"])

    col_a, col_b = st.columns(2)

    with col_a:
        avg_chars = df["char_count"].mean()
        max_chars = df["char_count"].max()
        min_chars = df["char_count"].min()
        st.metric("Average length", f"{avg_chars:.1f} chars")
        st.metric("Min length", f"{min_chars} chars")
        st.metric("Max length", f"{max_chars} chars")

    with col_b:
        # Compliance: under 50 chars (mobile preview cutoff)
        compliant = (df["char_count"] <= 50).sum()
        total = len(df)
        compliance_pct = (compliant / total * 100) if total else 0

        st.metric("Mobile-compliant (<= 50 chars)", f"{compliance_pct:.1f}%")
        st.markdown(
            f"<span style='color: gray;'>{compliant} of {total} variants pass mobile preview cutoff.</span>",
            unsafe_allow_html=True,
        )

    # Histogram of lengths
    st.markdown("### Length distribution")
    from lib.plots import histogram as hist_fn
    st.plotly_chart(
        hist_fn(
            df["char_count"].tolist(),
            bins=10,
            x_label="Subject line length (characters)",
            title="Character count distribution",
            height=300,
        ),
        use_container_width=True,
    )


# ============================================================
# RECENT VARIANTS TABLE
# ============================================================
st.markdown("## Recent Generated Variants")

if summary["all_variants"]:
    df = pd.DataFrame(summary["all_variants"])
    # Show most recent (we don't have timestamps, so show last entries in cache)
    display_df = df.tail(15)[["persona", "text", "angle", "char_count"]]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("No variants in cache.")


# ============================================================
# WINNERS FROM EVALUATIONS
# ============================================================
st.markdown("## Selected Winners (from evaluations)")

if cache["evaluations"]:
    winners = []
    for ev in cache["evaluations"]:
        winner = ev.get("winner", {})
        if winner.get("variant_text"):
            winners.append({
                "persona": ev.get("metadata", {}).get("persona", "unknown"),
                "winner_text": winner["variant_text"],
                "rationale": winner.get("rationale", "")[:200] + ("..." if len(winner.get("rationale", "")) > 200 else ""),
            })

    if winners:
        st.dataframe(
            pd.DataFrame(winners),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No winners extracted from evaluations.")
else:
    st.info("No evaluations cached yet.")
