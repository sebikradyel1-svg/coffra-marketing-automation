"""
Coffra Subject Line Optimizer — Streamlit Web App

A demo-ready interface for generating and scoring email subject line variants.
Run with:
    streamlit run src/streamlit_app.py

This is the primary demo surface for the AI tool. Designed to be screenshotted
and recorded for portfolio purposes.
"""

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Add src/ to path so subject_optimizer imports work when running via streamlit
sys.path.insert(0, str(Path(__file__).resolve().parent))

from subject_optimizer.config import get_persona, EVALUATION_DIMENSIONS
from subject_optimizer.generator import generate_variants
from subject_optimizer.critic import score_variants, merge_generation_and_evaluation
from subject_optimizer.cache import ResponseCache


# ============================================================
# APP CONFIG
# ============================================================
st.set_page_config(
    page_title="Coffra Subject Line Optimizer",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load env vars (ANTHROPIC_API_KEY)
load_dotenv()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("Coffra Subject Optimizer")
st.sidebar.markdown(
    "**v1.0** — AI-powered subject line generator and critic for the Coffra "
    "marketing automation system. Built with Claude API."
)

st.sidebar.divider()

# Persona selector
persona_choice = st.sidebar.radio(
    "Target persona",
    options=["connoisseur", "daily_ritualist"],
    format_func=lambda x: {
        "connoisseur": "The Connoisseur (Andrei) — EN",
        "daily_ritualist": "The Daily Ritualist (Bianca) — RO",
    }[x],
)

persona = get_persona(persona_choice)

# Caching toggle
use_cache = st.sidebar.checkbox(
    "Use response cache",
    value=True,
    help="Avoids re-paying for identical requests. Recommended ON during testing.",
)

# Cache stats
cache = ResponseCache()
stats = cache.stats()
st.sidebar.caption(
    f"Cache: {stats['entries']} entries · {stats['total_size_kb']} KB"
)

if st.sidebar.button("Clear cache", help="Removes all cached responses"):
    n = cache.clear()
    st.sidebar.success(f"Removed {n} cache entries.")
    st.rerun()

st.sidebar.divider()

# API key check
api_key_status = "Configured" if os.getenv("ANTHROPIC_API_KEY") else "MISSING"
st.sidebar.caption(f"API key: {api_key_status}")

if api_key_status == "MISSING":
    st.sidebar.error(
        "ANTHROPIC_API_KEY not found. Create a .env file with your key, then restart."
    )

# ============================================================
# MAIN AREA
# ============================================================
st.title("Coffra Subject Line Optimizer")
st.markdown(
    "Generate 5 subject line variants tailored to the selected persona, "
    "then score them on clarity, intrigue, brand fit, and mobile readability."
)

# Persona context display
with st.expander(f"Persona context: {persona.name}", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Sender identity:** {persona.sender_identity}")
        st.markdown(f"**Language:** {persona.language}")
        st.markdown(f"**Max subject length:** {persona.max_subject_length} chars")
    with col2:
        st.markdown(f"**Tone keywords:** {', '.join(persona.tone_keywords)}")
        st.markdown(
            f"**Forbidden words ({len(persona.forbidden_words)}):** "
            f"{', '.join(persona.forbidden_words[:8])}..."
        )
    st.caption(persona.description)

# Email brief input
st.markdown("### Email brief")
st.caption(
    "Describe what the email is about. Include the offer, the trigger, and the "
    "desired action. The more specific, the better the variants."
)

# Pre-load examples for quick demo
example_briefs = {
    "(custom)": "",
    "Connoisseur — Welcome": (
        "Welcome email triggered by newsletter signup. New subscriber gets a free "
        "Discovery Sample Pack (3x80g of Ethiopia Gelana, Colombia La Esperanza, "
        "Signature Blend) on their first order over 150 RON. Tone should be "
        "technical and confident, signaling Coffra's micro-lot focus and "
        "transparent roast dating practices. Sender: Sebastian, Roaster & Founder."
    ),
    "Connoisseur — Origin Story": (
        "Email 2 in nurture sequence. Tells the story of how we selected the "
        "Ethiopia Gelana Abaya lot — we evaluated 7 samples and rejected 4 for "
        "moisture inconsistency, vague processing documentation, and high "
        "defect counts. Demonstrates rigor and competence. Sebastian as sender."
    ),
    "Daily Ritualist — Welcome": (
        "Welcome email pentru subscriber nou la newsletter. Oferă prima cafea "
        "gratuită la prima vizită in locația Coffra din Timișoara, strada Alba "
        "Iulia. Tonul e warm, invitational, focusat pe experience nu pe produs. "
        "Sender: Ioana, Community Manager."
    ),
    "Daily Ritualist — Coffra Pass pitch": (
        "Email 4 în secvența nurture. Pitch pentru Coffra Pass (245 RON/lună, "
        "15 cafele, prioritate la lansări noi). Pozitionat NU ca daily default, "
        "ci ca aspirational purchase pentru momente upgrade — nou job, proiect "
        "terminat, cadou. Trial 199 RON prima lună fără auto-renewal. "
        "Sender: Ioana."
    ),
}

selected_example = st.selectbox(
    "Load example brief",
    options=list(example_briefs.keys()),
)

email_brief = st.text_area(
    "Brief",
    value=example_briefs[selected_example],
    height=180,
    placeholder=(
        "Example: Welcome email for new subscriber. Offers free sample pack on "
        "first order over 150 RON. Tone should match the Connoisseur persona's "
        "technical, transparent voice. Sender: Sebastian, Roaster & Founder."
    ),
)

# Run button
col_btn, col_info = st.columns([1, 3])
with col_btn:
    run_clicked = st.button(
        "Generate and score",
        type="primary",
        disabled=(api_key_status == "MISSING" or not email_brief.strip()),
    )
with col_info:
    if api_key_status == "MISSING":
        st.warning("API key required. See sidebar.")
    elif not email_brief.strip():
        st.info("Enter an email brief or load an example.")

# ============================================================
# EXECUTION
# ============================================================
if run_clicked:
    with st.spinner("Generating variants..."):
        try:
            generation = generate_variants(
                email_brief=email_brief,
                persona=persona,
                use_cache=use_cache,
                cache=cache,
            )
        except Exception as e:
            st.error(f"Generation failed: {e}")
            st.stop()

    with st.spinner("Scoring variants..."):
        try:
            evaluation = score_variants(
                email_brief=email_brief,
                persona=persona,
                variants=generation["variants"],
                use_cache=use_cache,
                cache=cache,
            )
        except Exception as e:
            st.error(f"Scoring failed: {e}")
            st.stop()

    result = merge_generation_and_evaluation(generation, evaluation)

    # ============================================================
    # RESULTS DISPLAY
    # ============================================================
    st.divider()
    st.markdown("### Results")

    # Winner banner
    winner = result["winner"]
    st.success(f"**Winner:** {winner['variant_text']}")
    st.caption(winner["rationale"])

    # Token usage stats
    meta = result["metadata"]
    cache_status = []
    if meta["generation_from_cache"]:
        cache_status.append("generation cached")
    if meta["evaluation_from_cache"]:
        cache_status.append("evaluation cached")
    cache_str = " · ".join(cache_status) if cache_status else "fresh API calls"

    st.caption(
        f"Tokens used: {meta['total_input_tokens']} input + "
        f"{meta['total_output_tokens']} output · {cache_str}"
    )

    # Variants ranked
    st.markdown("#### All variants (ranked by total score)")

    for i, v in enumerate(result["variants"], 1):
        with st.container(border=True):
            top_col1, top_col2 = st.columns([4, 1])
            with top_col1:
                st.markdown(f"**#{i} — {v['text']}**")
                st.caption(f"Angle: {v['angle']} · {v['char_count']} chars")
            with top_col2:
                st.metric("Total", f"{v['total_score']}/40")

            # Score breakdown
            scores = v.get("scores", {})
            score_cols = st.columns(4)
            with score_cols[0]:
                st.metric("Clarity", f"{scores.get('clarity', 0)}/10")
            with score_cols[1]:
                st.metric("Intrigue", f"{scores.get('intrigue', 0)}/10")
            with score_cols[2]:
                st.metric("Brand fit", f"{scores.get('brand_fit', 0)}/10")
            with score_cols[3]:
                st.metric("Mobile", f"{scores.get('mobile_readability', 0)}/10")

            # Strength / weakness
            sw_col1, sw_col2 = st.columns(2)
            with sw_col1:
                st.markdown(f"**Strength:** {v.get('biggest_strength', '—')}")
            with sw_col2:
                st.markdown(f"**Weakness:** {v.get('biggest_weakness', '—')}")

            # Forbidden words check
            if v.get("forbidden_words_used"):
                st.error(
                    f"Forbidden words detected: {', '.join(v['forbidden_words_used'])}"
                )

            # Rationale
            with st.expander("Generator rationale"):
                st.write(v.get("rationale", "—"))

    # ============================================================
    # METHODOLOGY EXPANDER (for portfolio transparency)
    # ============================================================
    with st.expander("Methodology"):
        st.markdown(
            """
            **Two-stage pipeline:**
            1. **Generator** — Claude generates 5 variants using 5 distinct strategic
               angles (direct, curiosity, insider, counter-intuitive, invitation).
            2. **Critic** — Claude scores each variant on 4 dimensions independently,
               then recommends a winner.

            **Why two stages?** Separating generation from evaluation reduces bias —
            the critic judges variants without knowing which one was generated first
            or whether they were generated together.

            **Forbidden words** are checked twice: by the generator (instructed to
            avoid them) and by the critic (instructed to flag them). A defensive
            third check is performed in Python on raw text for safety.

            **Caching** uses SHA-256 hash of (persona, brief, prompt_version, model)
            as the key. Identical inputs return identical cached output. Bumping
            `PROMPT_VERSION` in `prompts.py` invalidates the cache automatically.

            **Limitations of v1:**
            - Scores are qualitative judgments, not predicted open rates.
            - No A/B test data to validate scoring against actual performance.
            - Quality bounded by Claude's understanding of Romanian marketing
              context (good but not native-equivalent).
            """
        )

# Footer
st.divider()
st.caption(
    "Coffra Subject Line Optimizer v1.0 · Built by Sebastian Kradyel · "
    "Part of the P1 marketing automation portfolio project."
)
