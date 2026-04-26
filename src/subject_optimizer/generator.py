"""
Subject line variant generator using Anthropic Claude API.

Calls Claude to generate 5 distinct subject line variants for a given email
brief, calibrated to a specific persona's tone and constraints.

Usage:
    from subject_optimizer.generator import generate_variants
    from subject_optimizer.config import get_persona

    persona = get_persona("connoisseur")
    variants = generate_variants(
        email_brief="Welcome email with free sample pack offer...",
        persona=persona,
    )
"""

import json
import os
from typing import List, Dict, Any

from anthropic import Anthropic

from .config import PersonaConfig
from .prompts import build_generator_prompt, PROMPT_VERSION
from .cache import ResponseCache


# Default model — Claude Sonnet (good balance of quality and cost for this task)
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 2000


def _extract_first_json_object(text: str) -> str:
    """
    Extracts the first complete JSON object from text by tracking brace balance.
    Handles cases where Claude adds explanatory text or corrections after the JSON.
    """
    text = text.strip()
    # Strip any markdown fence wrappers
    if text.startswith("```"):
        # Find first { after the fence opener
        start = text.find("{")
    else:
        start = text.find("{")

    if start == -1:
        return text  # No JSON found, let json.loads fail naturally

    # Walk the string tracking braces, accounting for strings (where braces don't count)
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
                # Found the matching closing brace
                return text[start:i + 1]

    return text[start:]  # Unmatched braces, return what we have


def generate_variants(
    email_brief: str,
    persona: PersonaConfig,
    model: str = DEFAULT_MODEL,
    use_cache: bool = True,
    cache: ResponseCache | None = None,
) -> Dict[str, Any]:
    """
    Generate 5 subject line variants for an email brief.

    Args:
        email_brief: Plain text describing the email's purpose and content
        persona: PersonaConfig defining target audience constraints
        model: Anthropic model identifier
        use_cache: If True, return cached response when available
        cache: Optional ResponseCache instance (creates one if None)

    Returns:
        Dict with structure:
            {
                "variants": [
                    {"text": str, "char_count": int, "angle": str, "rationale": str},
                    ... (5 total)
                ],
                "metadata": {
                    "persona": str,
                    "model": str,
                    "prompt_version": str,
                    "from_cache": bool,
                    "input_tokens": int (if from API),
                    "output_tokens": int (if from API)
                }
            }

    Raises:
        ValueError: If API returns malformed JSON
        anthropic.APIError: For API-level errors (rate limit, auth, etc.)
    """
    # Cache check
    cache = cache or ResponseCache()
    cache_args = (persona.name, email_brief, PROMPT_VERSION, "generate", model)

    if use_cache:
        cached = cache.get(*cache_args)
        if cached is not None:
            cached["metadata"]["from_cache"] = True
            return cached

    # Build prompt
    prompt = build_generator_prompt(persona, email_brief)

    # Call Claude
    client = Anthropic()  # Reads ANTHROPIC_API_KEY from env automatically

    response = client.messages.create(
        model=model,
        max_tokens=DEFAULT_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    # Parse response
    raw_text = response.content[0].text.strip()

    # Strip markdown code fences if Claude adds them despite our instructions
    if raw_text.startswith("```"):
        # Remove first line (```json or similar) and last line (```)
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    # Robust JSON extraction: find first complete JSON object
    # Claude sometimes adds explanatory text or self-corrections after the JSON
    raw_text = _extract_first_json_object(raw_text)

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Claude returned malformed JSON. Raw response:\n{raw_text}\n\nError: {e}"
        )

    if "variants" not in parsed or not isinstance(parsed["variants"], list):
        raise ValueError(f"Expected 'variants' list in response. Got: {parsed}")

    # Recompute char_count to be safe (don't trust Claude's count)
    for v in parsed["variants"]:
        v["char_count"] = len(v["text"])

    # Wrap with metadata
    result = {
        "variants": parsed["variants"],
        "metadata": {
            "persona": persona.name,
            "model": model,
            "prompt_version": PROMPT_VERSION,
            "from_cache": False,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
    }

    # Save to cache
    if use_cache:
        cache.set(result, *cache_args)

    return result
