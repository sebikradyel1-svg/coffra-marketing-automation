"""Shared helpers for the Qualification agent eval (EXPERIMENT).

The tier thresholds are not constants in the repo: they exist only as prose in
the Qualification agent's SYSTEM_PROMPT (src/lead_intelligence/agents/
qualification.py). We parse them out of that string at load time instead of
copying the numbers, and fail loudly if the wording changes.
"""

from __future__ import annotations

import re
import sys
from importlib import metadata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAD_INTELLIGENCE_DIR = HERE.parent / "src" / "lead_intelligence"
TIERS = ("HOT", "WARM", "COLD")

_HOT_RE = re.compile(r"score\s*>=\s*(\d+(?:\.\d+)?)\s*→\s*HOT")
_WARM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*<=\s*score\s*<\s*(\d+(?:\.\d+)?)\s*→\s*WARM")
_COLD_RE = re.compile(r"score\s*<\s*(\d+(?:\.\d+)?)\s*→\s*COLD")
_FALLBACK_RE = re.compile(r"Dacă unealta\s+eșuează,\s+returnezi tier\s+\"WARM\"")


def parse_thresholds(prompt: str) -> dict[str, float]:
    """Return {"hot": x, "warm": y}: score >= hot is HOT, warm <= score < hot is WARM, else COLD."""
    hot, warm, cold = _HOT_RE.search(prompt), _WARM_RE.search(prompt), _COLD_RE.search(prompt)
    if not (hot and warm and cold):
        raise ValueError("Could not find all three tier rules (HOT/WARM/COLD) in the prompt text")
    hot_t, warm_lo, warm_hi, cold_t = (float(x) for x in (hot[1], warm[1], warm[2], cold[1]))
    if not (hot_t == warm_hi and warm_lo == cold_t and warm_lo < hot_t):
        raise ValueError("Tier rules in the prompt are not consistent with each other")
    return {"hot": hot_t, "warm": warm_lo}


def has_documented_fallback(prompt: str) -> bool:
    """True if the prompt documents 'tool fails -> tier WARM'."""
    return bool(_FALLBACK_RE.search(prompt))


def expected_tier(score: float, thresholds: dict[str, float]) -> str:
    if score >= thresholds["hot"]:
        return "HOT"
    if score >= thresholds["warm"]:
        return "WARM"
    return "COLD"


def load_agent_prompt() -> str:
    sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
    from agents.qualification import SYSTEM_PROMPT

    return SYSTEM_PROMPT


def load_thresholds() -> dict[str, float]:
    return parse_thresholds(load_agent_prompt())


def environment_versions() -> dict[str, str | None]:
    """Versions of the packages that influence the model's scores."""
    out: dict[str, str | None] = {}
    for key, dist in (("xgboost", "xgboost"), ("scikit-learn", "scikit-learn"), ("shap", "shap")):
        try:
            out[key] = metadata.version(dist)
        except metadata.PackageNotFoundError:
            out[key] = None
    return out
