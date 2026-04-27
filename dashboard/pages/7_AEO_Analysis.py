"""
AEO Analysis Page - Answer Engine Optimization audit results.

Reads aeo_audit_summary.json and aeo_audit_results.parquet from notebook 06.
Visualizes brand visibility, citation rate, sentiment distribution, and
strategy recommendations for AI search era.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json

from lib.styling import inject_custom_css, page_header, data_disclosure, COFFRA_BROWN, MEDIUM_GRAY
from lib.plots import bar_chart, donut_chart, gauge_chart, COFFRA_PALETTE, apply_brand_layout
import plotly.graph_objects as go


st.set_page_config(page_title="AEO Analysis | Coffra", layout="wide")
inject_custom_css()

page_header(
    "AEO Analysis",
    "Answer Engine Optimization — brand visibility audit across AI search platforms"
)

data_disclosure(
    "real",
    "Audit results from running the Coffra brand query battery against the Claude API. "
    "Production system would also test ChatGPT, Perplexity, Gemini, and Copilot. "
    "Coffra is fictional — baseline visibility is expected near 0%, establishing the "
    "measurement methodology for tracking AEO progress over time."
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
def load_aeo_data():
    data = {}

    summary_path = PROCESSED_DIR / "aeo_audit_summary.json"
    if summary_path.exists():
        with open(summary_path) as f:
            data['summary'] = json.load(f)

    results_path = PROCESSED_DIR / "aeo_audit_results.parquet"
    if results_path.exists():
        data['results'] = pd.read_parquet(results_path)

    return data


data = load_aeo_data()

if 'summary' not in data:
    st.warning(
        "AEO audit data not found. Run `notebooks/06_aeo_audit.ipynb` to generate it. "
        "Until then, this page shows the AEO strategy framework without live audit metrics."
    )

    # Show strategy framework even without audit data
    summary = {}
    results = pd.DataFrame()
else:
    summary = data['summary']
    results = data.get('results', pd.DataFrame())


# ============================================================
# SECTION: WHY AEO MATTERS
# ============================================================
st.markdown("## Why AEO Matters in 2026")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("ChatGPT users (monthly)", "883M", help="Source: Frase 2026 AEO Guide")
with c2:
    st.metric("Google AI Overviews", "55%", help="% of all searches showing AI Overview (Frase 2026)")
with c3:
    st.metric("AI session growth (YoY)", "+527%", help="Mid-2025 data — AI-referred sessions")
with c4:
    st.metric("Predicted SEO traffic loss", "-25%", help="Gartner forecast for 2026 due to AI chatbots")

st.markdown(
    """
    The marketing landscape is shifting from blue links to synthesized AI answers. Customers
    asking "best specialty coffee in Romania" now get a synthesized answer from ChatGPT or
    Perplexity, not a list of websites to click through. Brands not cited in AI answers are
    effectively invisible to that query.
    """
)


# ============================================================
# SECTION: COFFRA AEO SCORECARD
# ============================================================
st.markdown("## Coffra AEO Scorecard")

if summary:
    audit_date = summary.get('audit_date_human', 'Not yet run')
    engine = summary.get('engine_tested', 'Not tested')

    st.caption(f"Last audit: {audit_date} · Engine tested: {engine}")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        viz_score = summary.get('ai_visibility_score', 0)
        st.plotly_chart(
            gauge_chart(viz_score, max_value=100, label="AI Visibility Score (%)", height=280),
            use_container_width=True,
        )
        st.caption(
            "% of priority queries where Coffra is mentioned by AI engines. "
            "Baseline near 0% expected for unlaunched brand."
        )

    with col_b:
        priority_viz = summary.get('high_priority_visibility', 0)
        st.plotly_chart(
            gauge_chart(priority_viz, max_value=100, label="High-Priority Visibility (%)", height=280),
            use_container_width=True,
        )
        st.caption(
            "% of business-critical queries (discovery, local, comparison) where "
            "Coffra appears in AI responses."
        )

    with col_c:
        citation = summary.get('citation_rate', 0)
        st.plotly_chart(
            gauge_chart(citation, max_value=100, label="Citation Rate (%)", height=280),
            use_container_width=True,
        )
        st.caption(
            "% of queries where Coffra URL is cited as source. Strongest AEO signal — "
            "indicates AI engines treat Coffra as authoritative."
        )

    # By stage breakdown
    by_stage = summary.get('by_stage', {})
    if by_stage:
        st.markdown("### Visibility by Customer Journey Stage")

        stage_df = pd.DataFrame([
            {
                'Stage': stage,
                'Queries': info['queries'],
                'Mention Rate (%)': info['mention_rate'],
                'Citation Rate (%)': info['citation_rate'],
            }
            for stage, info in by_stage.items()
        ]).sort_values('Mention Rate (%)', ascending=False)

        col_chart, col_table = st.columns([1, 1])

        with col_chart:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=stage_df['Mention Rate (%)'],
                y=stage_df['Stage'],
                orientation='h',
                marker_color=COFFRA_BROWN,
                name='Mention Rate',
                text=[f'{v:.0f}%' for v in stage_df['Mention Rate (%)']],
                textposition='outside',
            ))
            apply_brand_layout(fig, title="Brand Mention Rate by Stage", height=350)
            fig.update_xaxes(range=[0, 105])
            fig.update_yaxes(autorange='reversed')
            st.plotly_chart(fig, use_container_width=True)

        with col_table:
            st.dataframe(stage_df, use_container_width=True, hide_index=True)


# ============================================================
# SECTION: SENTIMENT DISTRIBUTION
# ============================================================
if summary and summary.get('sentiment_distribution'):
    st.markdown("## Sentiment Analysis")

    sentiment_dist = summary['sentiment_distribution']

    col_pie, col_explain = st.columns([1, 1])

    with col_pie:
        # Map sentiment categories to colors
        sentiment_colors = {
            'positive': COFFRA_BROWN,
            'neutral': COFFRA_BROWN_LIGHT if False else "#6D4C41",
            'negative': '#D84315',
            'no_mention': '#BCAAA4',
        }

        labels = list(sentiment_dist.keys())
        values = list(sentiment_dist.values())
        colors = [sentiment_colors.get(l, '#BCAAA4') for l in labels]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker_colors=colors,
            textinfo='label+percent',
        )])
        apply_brand_layout(fig, title="Sentiment Distribution Across Queries", height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col_explain:
        st.markdown(
            """
            ### Sentiment categories explained

            - **Positive:** AI engine describes Coffra in favorable terms
              (quality, recommended, trusted, premium).
            - **Neutral:** Coffra mentioned without strong qualitative framing.
            - **Negative:** AI engine expresses skepticism or warns about brand
              (e.g., "no information available," "fictional").
            - **No mention:** Coffra not referenced in response at all.

            For an unlaunched fictional brand, "no mention" is expected to dominate.
            As AEO content publishes, sentiment shifts toward neutral first, then
            positive as authority builds.
            """
        )


# ============================================================
# SECTION: PRINCETON GEO STUDY FINDINGS
# ============================================================
st.markdown("## Evidence-Based AEO Tactics")

st.markdown(
    "Princeton GEO research (2024) tested 10,000 queries across major AI engines and "
    "measured how content tactics impact citation probability. These findings drive "
    "Coffra's AEO content strategy:"
)

princeton_data = pd.DataFrame([
    {'Tactic': 'Add expert quotes to content', 'Citation Lift': '+41%'},
    {'Tactic': 'Include statistics with sources', 'Citation Lift': '+30%'},
    {'Tactic': 'Add citations to authoritative sources', 'Citation Lift': '+30%'},
    {'Tactic': 'Add fluency optimization', 'Citation Lift': 'Minimal'},
    {'Tactic': 'Keyword stuffing', 'Citation Lift': 'Negative'},
])

st.dataframe(princeton_data, use_container_width=True, hide_index=True)

st.caption(
    "Source: Princeton GEO Study (2024), as cited in Surmado 2026 AEO Guide."
)


# ============================================================
# SECTION: SIX PILLARS OF COFFRA AEO STRATEGY
# ============================================================
st.markdown("## Coffra AEO Strategy — Six Pillars")

pillars_data = pd.DataFrame([
    {
        'Pillar': '1. Authoritative Brand Content',
        'Goal': 'Establish Coffra as recognized entity in AI knowledge graphs',
        'Key Tactic': 'Organization schema + consistent facts across web',
    },
    {
        'Pillar': '2. Answer-First Architecture',
        'Goal': 'Make every page directly extractable as AI answer',
        'Key Tactic': '50-Word Rule + Answer Blocks at top of pages',
    },
    {
        'Pillar': '3. E-E-A-T Signals at Scale',
        'Goal': 'Demonstrate Experience, Expertise, Authoritativeness, Trust',
        'Key Tactic': 'Author bios + expert quotes + cited sources',
    },
    {
        'Pillar': '4. Schema Markup Foundation',
        'Goal': 'Help AI parse Coffra content unambiguously',
        'Key Tactic': '12 schema types deployed (see docs/12)',
    },
    {
        'Pillar': '5. Conversational Content',
        'Goal': 'Match how users ask AI engines (long-tail, natural)',
        'Key Tactic': 'Prompt research + semantic-triple structure',
    },
    {
        'Pillar': '6. Multi-Channel Reinforcement',
        'Goal': 'Reinforce brand identity across the web',
        'Key Tactic': 'GBP + Wikipedia + LinkedIn + industry directories',
    },
])

st.dataframe(pillars_data, use_container_width=True, hide_index=True)

st.markdown(
    "Full strategy detailed in [`docs/11_aeo_strategy.md`](https://github.com/sebikradyel1-svg/coffra-marketing-automation/blob/main/docs/11_aeo_strategy.md). "
    "Schema implementations in [`docs/12_schema_implementation.md`](https://github.com/sebikradyel1-svg/coffra-marketing-automation/blob/main/docs/12_schema_implementation.md)."
)


# ============================================================
# SECTION: PER-QUERY DETAIL TABLE
# ============================================================
if not results.empty:
    st.markdown("## Audit Detail — Per Query")

    display_cols = ['query_id', 'stage', 'priority', 'query', 'language',
                    'brand_mentioned', 'cited_as_source', 'sentiment']
    available_cols = [c for c in display_cols if c in results.columns]

    if available_cols:
        st.dataframe(
            results[available_cols].head(20),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# SECTION: MEASUREMENT FRAMEWORK
# ============================================================
st.markdown("## Measurement Framework")

st.markdown(
    """
    Traditional SEO metrics (rankings, traffic, CTR) cannot measure AEO performance.
    Coffra tracks these AEO-specific KPIs:
    """
)

metrics_data = pd.DataFrame([
    {
        'Metric': 'AI Visibility Score',
        'Definition': '% of priority queries where Coffra is mentioned across 5 engines',
        'Source': 'This audit (notebook 06)',
        'Cadence': 'Monthly',
    },
    {
        'Metric': 'Citation Rate',
        'Definition': '% of queries where Coffra is cited as source URL',
        'Source': 'This audit',
        'Cadence': 'Monthly',
    },
    {
        'Metric': 'Sentiment Score',
        'Definition': 'Average sentiment of Coffra mentions in AI responses',
        'Source': 'This audit',
        'Cadence': 'Monthly',
    },
    {
        'Metric': 'Information Accuracy Rate',
        'Definition': '% of Coffra facts in AI responses that are correct',
        'Source': 'Manual verification + ground truth',
        'Cadence': 'Quarterly',
    },
    {
        'Metric': 'AI-Referred Sessions',
        'Definition': 'Website sessions originating from AI engine clicks',
        'Source': 'Google Analytics 4',
        'Cadence': 'Daily',
    },
    {
        'Metric': 'AI-Influenced Conversions',
        'Definition': 'Conversions where AI was a touchpoint',
        'Source': 'Multi-touch attribution model (future P5)',
        'Cadence': 'Monthly',
    },
])

st.dataframe(metrics_data, use_container_width=True, hide_index=True)


# ============================================================
# SECTION: METHODOLOGY
# ============================================================
st.markdown("## Methodology Note")

if summary:
    st.markdown(
        f"""
        **Audit methodology:**
        - Query battery of {summary.get('total_queries', 'N/A')} queries spanning customer journey stages
        - Each query submitted to {summary.get('engine_tested', 'AI engine')}
        - Responses parsed for brand mention, citation, sentiment
        - Production system would test ChatGPT, Perplexity, Gemini, Copilot in addition to Claude

        **{summary.get('baseline_disclosure', '')}**

        **Notes:** {summary.get('methodology_note', '')}
        """
    )
else:
    st.markdown(
        """
        Audit methodology designed for production deployment. To run:
        ```bash
        cd notebooks
        jupyter lab 06_aeo_audit.ipynb
        # Run All Cells
        ```

        Output: `data/processed/aeo_audit_summary.json` and `aeo_audit_results.parquet`.
        Refresh this page after notebook completes.
        """
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    f"<p style='color: {MEDIUM_GRAY}; font-size: 0.85rem;'>"
    "P4 Coffra AEO Strategy · Built April 2026 · "
    "Strategy: docs/11 · Schemas: docs/12 · Audit: notebooks/06"
    "</p>",
    unsafe_allow_html=True,
)
