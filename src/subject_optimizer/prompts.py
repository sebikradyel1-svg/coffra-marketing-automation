"""
Prompt templates for the Subject Line Optimizer.

Two prompts are defined:
    1. GENERATOR_PROMPT: Generates 5 subject line variants
    2. CRITIC_PROMPT: Scores variants on 4 dimensions

Both prompts use structured output (JSON) for reliable parsing. Prompts are
versioned via the PROMPT_VERSION constant — bump it when making semantic changes.
"""

PROMPT_VERSION = "1.0"


# ============================================================
# GENERATOR PROMPT
# ============================================================
GENERATOR_PROMPT_TEMPLATE = """You are an expert email subject line copywriter for Coffra, a fictional specialty coffee brand based in Timișoara, Romania. Your job is to generate 5 distinct subject line variants for a given email brief, calibrated precisely to the target persona.

# PERSONA CONTEXT
**Persona:** {persona_name}
**Description:** {persona_description}
**Sender Identity:** {sender_identity}
**Language:** {language}
**Max Subject Length:** {max_length} characters (mobile preview cutoff)

**Tone keywords (must be present):** {tone_keywords}
**Preferred words (use where natural):** {preferred_words}
**Forbidden words (NEVER use):** {forbidden_words}

# EMAIL BRIEF
{email_brief}

# YOUR TASK
Generate exactly 5 distinct subject line variants. Each variant should:
1. Be under {max_length} characters (count carefully)
2. Match the persona's tone (use tone_keywords as guide)
3. Avoid all forbidden_words
4. Use language: {language} (this is non-negotiable)
5. Take a different strategic angle than the others

Strategic angles to consider (use 5 different ones):
- Direct/specific (offer or fact upfront)
- Curiosity hook (intriguing without clickbait)
- Personal/insider (peer-to-peer, "you're in" framing)
- Counter-intuitive (surprising or self-deprecating)
- Question or invitation (low-commitment open)

# OUTPUT FORMAT
Return ONLY a JSON object with this exact structure (no preamble, no postscript):

{{
  "variants": [
    {{
      "text": "the subject line",
      "char_count": <integer>,
      "angle": "direct|curiosity|insider|counter_intuitive|invitation",
      "rationale": "1-sentence explanation of why this works for the persona"
    }},
    ... (4 more)
  ]
}}

Generate 5 variants now."""


# ============================================================
# CRITIC PROMPT
# ============================================================
CRITIC_PROMPT_TEMPLATE = """You are an expert email marketing analyst evaluating subject line variants for Coffra, a fictional specialty coffee brand. Your job is to score each variant on 4 dimensions and recommend the best one.

# PERSONA CONTEXT
**Persona:** {persona_name}
**Description:** {persona_description}
**Forbidden words check:** {forbidden_words}

# EMAIL BRIEF
{email_brief}

# VARIANTS TO EVALUATE
{variants_json}

# EVALUATION DIMENSIONS

**1. Clarity (0-10)**
How clearly does the subject communicate what the email is about?
- 10 = Instantly clear what the reader will get by opening
- 5 = Somewhat clear, requires inference
- 0 = Opaque, misleading, or confusing

**2. Intrigue (0-10)**
Does it create curiosity to motivate opening without being clickbait?
- 10 = Compelling hook that makes opening feel necessary
- 5 = Mildly interesting, could go either way
- 0 = Forgettable in inbox; or clickbait that erodes trust

**3. Brand Fit (0-10)**
Does it align with the persona's expected tone and Coffra's voice?
- 10 = Perfectly on-tone; reader recognizes Coffra immediately
- 5 = Generic, could be from any brand
- 0 = Off-brand; sounds like a different category entirely

**4. Mobile Readability (0-10)**
Is it under 50 chars and structured for inbox scanning?
- 10 = Under 45 chars, key message in first 30 chars
- 5 = 45-55 chars, slightly tight
- 0 = Over 55 chars; gets truncated mid-thought

# YOUR TASK

For each variant:
1. Score each dimension (0-10 integer)
2. Compute total score (sum of 4 dimensions, max 40)
3. Identify the single biggest strength and biggest weakness
4. Flag any forbidden words used (list them or empty array)

After all variants, recommend ONE as the winner with brief rationale.

# OUTPUT FORMAT
Return ONLY a JSON object with this exact structure (no preamble, no postscript):

{{
  "evaluations": [
    {{
      "variant_text": "the subject line text",
      "scores": {{
        "clarity": <int>,
        "intrigue": <int>,
        "brand_fit": <int>,
        "mobile_readability": <int>
      }},
      "total_score": <int, sum of above>,
      "biggest_strength": "1 sentence",
      "biggest_weakness": "1 sentence",
      "forbidden_words_used": []
    }},
    ... (one per variant)
  ],
  "winner": {{
    "variant_text": "text of winning variant",
    "rationale": "2-3 sentences on why this wins"
  }}
}}

Evaluate now."""


def build_generator_prompt(persona, email_brief: str) -> str:
    """Construct the generator prompt with persona-specific context."""
    return GENERATOR_PROMPT_TEMPLATE.format(
        persona_name=persona.name,
        persona_description=persona.description,
        sender_identity=persona.sender_identity,
        language=persona.language,
        max_length=persona.max_subject_length,
        tone_keywords=", ".join(persona.tone_keywords),
        preferred_words=", ".join(persona.preferred_words[:15]),  # Truncate to top 15
        forbidden_words=", ".join(persona.forbidden_words),
        email_brief=email_brief,
    )


def build_critic_prompt(persona, email_brief: str, variants_json: str) -> str:
    """Construct the critic prompt for scoring variants."""
    return CRITIC_PROMPT_TEMPLATE.format(
        persona_name=persona.name,
        persona_description=persona.description,
        forbidden_words=", ".join(persona.forbidden_words),
        email_brief=email_brief,
        variants_json=variants_json,
    )
