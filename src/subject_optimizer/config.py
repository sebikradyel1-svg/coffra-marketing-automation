"""
Configuration module for the Subject Line Optimizer.

Centralizes persona definitions and brand voice constraints derived from
the Coffra persona documents (docs/02_persona_connoisseur.md and
docs/03_persona_daily_ritualist.md).

Editing this file is the canonical way to update the optimizer's understanding
of the personas — changes propagate automatically to prompts.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PersonaConfig:
    """Configuration for one persona target audience."""

    name: str
    description: str
    language: str  # 'EN' or 'RO'
    sender_identity: str
    tone_keywords: List[str]
    preferred_words: List[str]
    forbidden_words: List[str]
    max_subject_length: int = 50  # Mobile preview cutoff
    typical_email_context: str = ""


# ============================================================
# CONNOISSEUR PERSONA (Andrei)
# ============================================================
CONNOISSEUR = PersonaConfig(
    name="connoisseur",
    description=(
        "Andrei, 32, Senior Software Engineer in Timișoara. "
        "Specialty coffee enthusiast with V60, Aeropress, Comandante grinder. "
        "Reads James Hoffmann, Sprudge, r/espresso. "
        "Buys beans 3-4x/month at 250-400 RON/month. "
        "Income 8,000-20,000 RON. "
        "Values: craftsmanship, transparency, slow living, self-improvement. "
        "Trusts brands that signal technical expertise without performative pretension."
    ),
    language="EN",
    sender_identity="Sebastian, Roaster & Founder",
    tone_keywords=[
        "technical", "peer-to-peer", "specific", "measured",
        "confident", "data-aware", "no-fluff"
    ],
    preferred_words=[
        # Coffee technical
        "lot", "batch", "roast", "process", "altitude", "varietal",
        "cupping", "natural", "washed", "single origin", "micro-lot",
        "Ethiopia", "Colombia", "Guji", "Yirgacheffe",
        # Sensory
        "bright", "clean", "floral", "fruit-forward", "balanced",
        # Process language
        "calibrate", "dial in", "extract",
    ],
    forbidden_words=[
        "premium", "gourmet", "perfect", "amazing", "exquisite",
        "crafted with love", "wake up to the aroma", "passion",
        "best", "exclusive", "discover the magic",
        "limited time", "act now", "hurry",
    ],
    max_subject_length=50,
    typical_email_context=(
        "Connoisseur emails are sent over 14-day nurture sequence. "
        "Sender is Sebastian (Roaster & Founder). "
        "Tone evolves from welcome → process intimate → mentor casual → honest broker → calm finality."
    ),
)


# ============================================================
# DAILY RITUALIST PERSONA (Bianca)
# ============================================================
DAILY_RITUALIST = PersonaConfig(
    name="daily_ritualist",
    description=(
        "Bianca, 30, Senior in youth work / NGO, Reșița (hybrid remote). "
        "Single, sociable, uses cafés for networking and remote work. "
        "Income ~5,000 RON. Drinks 1-2 coffees/day (Nespresso home, cafés outside). "
        "Aspirational premium consumer: shops Shein + Paris boutique mix, "
        "values provenance for food & cosmetics, less for clothing. "
        "Influencers: gastronomy, lifestyle, travel (Europe). "
        "Platforms: Instagram, TikTok, Facebook (in that order). "
        "Decision-making: visual-first, social-driven, low technical research."
    ),
    language="RO",
    sender_identity="Ioana, Community Manager",
    tone_keywords=[
        "warm", "feminine-coded", "conversational", "invitational",
        "unhurried", "permission-giving", "non-pretentious"
    ],
    preferred_words=[
        # Emotional
        "ritual", "moment", "pauză", "tihnă", "slow morning",
        "cu drag", "bine ai venit",
        # Social
        "împreună", "prietenă", "între prietene",
        # Place
        "loc al tău", "acasă", "primitor",
        # Action invitations
        "vino", "treci pe la noi", "vezi",
    ],
    forbidden_words=[
        # Premium-pretentious
        "exclusiv", "rafinat", "deosebit", "selecție premium",
        # Marketing fluff
        "calitate superioară", "experiență de neuitat",
        # Promise tone
        "cea mai bună", "vei trăi",
        # Manipulative urgency
        "ofertă limitată", "doar astăzi", "ultima șansă",
        # Cringe community
        "familia noastră", "membrii VIP",
        # Too technical (off-persona)
        "single origin", "natural process", "cupping score", "V60",
    ],
    max_subject_length=50,
    typical_email_context=(
        "Daily Ritualist emails are sent over 14-day nurture sequence. "
        "Sender is Ioana (Community Manager). "
        "Tone evolves from welcome warmth → human connection → projection → honest broker → community closure."
    ),
)


# ============================================================
# EVALUATION CRITERIA
# ============================================================
EVALUATION_DIMENSIONS = {
    "clarity": {
        "description": "How clearly does the subject line communicate what the email is about?",
        "scale": "0-10 (10 = instantly clear, 0 = entirely opaque or misleading)",
    },
    "intrigue": {
        "description": "Does it create enough curiosity to motivate an open without being clickbait?",
        "scale": "0-10 (10 = compelling hook, 0 = ignored in inbox)",
    },
    "brand_fit": {
        "description": "Does the subject align with the persona's expected tone and Coffra's voice?",
        "scale": "0-10 (10 = perfect fit, 0 = sounds like a different brand)",
    },
    "mobile_readability": {
        "description": "Is it under the mobile preview cutoff (~50 chars) and scannable?",
        "scale": "0-10 (10 = fits perfectly, 0 = truncated mid-thought)",
    },
}


# ============================================================
# INDUSTRY BENCHMARKS (for reference, not used in v1 scoring)
# ============================================================
INDUSTRY_BENCHMARKS = {
    "food_beverage_avg_open_rate_pct": 22.1,
    "food_beverage_avg_ctr_pct": 2.3,
    "specialty_premium_uplift_factor": 1.15,  # Premium brands tend to outperform avg by ~15%
    "source": "Mailchimp 2025 Email Marketing Benchmarks (Food & Beverage segment)",
    "note": (
        "These benchmarks are for reference and are NOT used to compute predicted open rates in v1. "
        "v1 produces qualitative scoring only. v2 may add quantitative prediction."
    ),
}


def get_persona(name: str) -> PersonaConfig:
    """Retrieve a persona config by name."""
    name = name.lower().replace("-", "_").replace(" ", "_")
    if name == "connoisseur":
        return CONNOISSEUR
    elif name in ("daily_ritualist", "ritualist"):
        return DAILY_RITUALIST
    else:
        raise ValueError(
            f"Unknown persona: '{name}'. "
            f"Valid options: 'connoisseur', 'daily_ritualist'"
        )
