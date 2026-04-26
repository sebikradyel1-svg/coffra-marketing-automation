"""
Subject line variant critic using Anthropic Claude API.

Scores each variant from generate_variants() on 4 dimensions and recommends
a winner. Provides rationale grounded in persona constraints.

Usage:
    from subject_optimizer.critic import score_variants

    evaluation = score_variants(
        email_brief="Welcome email with free sample pack...",
        persona=persona,
        variants=variants,
    )
"""

import json
from typing import Dict, Any, List

from anthropic import Anthropic

from .config import PersonaConfig
from .prompts import build_critic_prompt, PROMPT_VERSION
from .cache import ResponseCache


DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 3000


def _extract_first_json_object(text: str) -> str:
    """
    Extracts the first complete JSON object from text by tracking brace balance.
    Handles cases where Claude adds explanatory text or corrections after the JSON.
    """
    text = text.strip()
    if text.startswith("```"):
        start = text.find("{")
    else:
        start = text.find("{")

    if start == -1:
        return text

    depth = 0
    in_string = False
    escape_next = False

    for i in range(start, len(text)):
        char = text[i]

        if escape_next:
            escape_next = False
            continue

        if char == "\\":
            escape_next = True
            continue

        if char == '"' and not escape_next:
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]

    return text[start:]


def score_variants(
    email_brief: str,
    persona: PersonaConfig,
    variants: List[Dict[str, Any]],
    model: str = DEFAULT_MODEL,
    use_cache: bool = True,
    cache: ResponseCache | None = None,
) -> Dict[str, Any]:
    """
    Score subject line variants on 4 dimensions and pick a winner.

    Args:
        email_brief: Plain text describing the email's purpose
        persona: PersonaConfig defining target audience
        variants: List of variant dicts (from generate_variants)
        model: Anthropic model identifier
        use_cache: If True, return cached response when available
        cache: Optional ResponseCache instance

    Returns:
        Dict with structure:
            {
                "evaluations": [
                    {
                        "variant_text": str,
                        "scores": {clarity, intrigue, brand_fit, mobile_readability},
                        "total_score": int,  # max 40
                        "biggest_strength": str,
                        "biggest_weakness": str,
                        "forbidden_words_used": List[str]
                    },
                    ...
                ],
                "winner": {
                    "variant_text": str,
                    "rationale": str
                },
                "metadata": {...}
            }
    """
    # Build a stable representation of variants for caching
    # (sorted by text to ensure cache hits are consistent regardless of order)
    variants_for_cache = sorted([v["text"] for v in variants])
    cache = cache or ResponseCache()
    cache_args = (
        persona.name,
        email_brief,
        "||".join(variants_for_cache),
        PROMPT_VERSION,
        "score",
        model,
    )

    if use_cache:
        cached = cache.get(*cache_args)
        if cached is not None:
            cached["metadata"]["from_cache"] = True
            return cached

    # Format variants as JSON string for the prompt
    variants_simple = [
        {"text": v["text"], "char_count": v.get("char_count", len(v["text"]))}
        for v in variants
    ]
    variants_json = json.dumps(variants_simple, ensure_ascii=False, indent=2)

    # Build prompt and call Claude
    prompt = build_critic_prompt(persona, email_brief, variants_json)
    client = Anthropic()

    response = client.messages.create(
        model=model,
        max_tokens=DEFAULT_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    # Robust JSON extraction
    raw_text = _extract_first_json_object(raw_text)

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Claude returned malformed JSON. Raw response:\n{raw_text}\n\nError: {e}"
        )

    # Validate structure
    if "evaluations" not in parsed or "winner" not in parsed:
        raise ValueError(f"Expected 'evaluations' and 'winner' keys. Got: {parsed}")

    # Verify total_score is correctly computed
    for ev in parsed["evaluations"]:
        scores = ev.get("scores", {})
        computed_total = sum(scores.values())
        if ev.get("total_score") != computed_total:
            ev["total_score"] = computed_total

    # Verify forbidden words check (defensive — re-run on our side)
    for ev in parsed["evaluations"]:
        text_lower = ev["variant_text"].lower()
        actual_forbidden = [
            word for word in persona.forbidden_words
            if word.lower() in text_lower
        ]
        ev["forbidden_words_used"] = actual_forbidden

    result = {
        "evaluations": parsed["evaluations"],
        "winner": parsed["winner"],
        "metadata": {
            "persona": persona.name,
            "model": model,
            "prompt_version": PROMPT_VERSION,
            "from_cache": False,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }

    if use_cache:
        cache.set(result, *cache_args)

    return result


def merge_generation_and_evaluation(
    generation: Dict[str, Any],
    evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Merge variant generation output with evaluation output into a single
    unified result, easier for downstream UI to render.

    Returns a dict with all 5 variants enriched with their scores and a
    top-level winner field.
    """
    # Index evaluations by variant text for fast lookup
    eval_by_text = {ev["variant_text"]: ev for ev in evaluation["evaluations"]}

    enriched_variants = []
    for v in generation["variants"]:
        ev = eval_by_text.get(v["text"], {})
        enriched_variants.append({
            **v,
            "scores": ev.get("scores", {}),
            "total_score": ev.get("total_score", 0),
            "biggest_strength": ev.get("biggest_strength", ""),
            "biggest_weakness": ev.get("biggest_weakness", ""),
            "forbidden_words_used": ev.get("forbidden_words_used", []),
        })

    # Sort by total_score descending
    enriched_variants.sort(key=lambda x: x.get("total_score", 0), reverse=True)

    return {
        "variants": enriched_variants,
        "winner": evaluation["winner"],
        "metadata": {
            "persona": generation["metadata"]["persona"],
            "generation_from_cache": generation["metadata"].get("from_cache", False),
            "evaluation_from_cache": evaluation["metadata"].get("from_cache", False),
            "total_input_tokens": (
                generation["metadata"].get("input_tokens", 0)
                + evaluation["metadata"].get("input_tokens", 0)
            ),
            "total_output_tokens": (
                generation["metadata"].get("output_tokens", 0)
                + evaluation["metadata"].get("output_tokens", 0)
            ),
        },
    }
