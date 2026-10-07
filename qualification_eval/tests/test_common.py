import pytest

from common import expected_tier, has_documented_fallback, parse_thresholds

PROMPT = """
   - score >= 0.70 → HOT (x)
   - 0.40 <= score < 0.70 → WARM (y)
   - score < 0.40 → COLD (z)
Dacă unealta
eșuează, returnezi tier "WARM" ca fallback sigur
"""


def test_parse_thresholds():
    assert parse_thresholds(PROMPT) == {"hot": 0.70, "warm": 0.40}


def test_parse_thresholds_fails_loudly_on_changed_wording():
    with pytest.raises(ValueError):
        parse_thresholds("score is high -> HOT")


def test_parse_thresholds_rejects_inconsistent_rules():
    with pytest.raises(ValueError):
        parse_thresholds(PROMPT.replace("score < 0.40", "score < 0.30"))


def test_expected_tier_boundaries():
    t = {"hot": 0.70, "warm": 0.40}
    assert [expected_tier(s, t) for s in (0.70, 0.6999, 0.40, 0.3999)] == ["HOT", "WARM", "WARM", "COLD"]


def test_fallback_detection():
    assert has_documented_fallback(PROMPT)
    assert not has_documented_fallback("no fallback here")


def test_thresholds_match_real_agent_prompt():
    pytest.importorskip("anthropic", reason="anthropic not installed")
    pytest.importorskip("dotenv", reason="python-dotenv not installed")
    from common import load_agent_prompt, load_thresholds

    assert load_thresholds()["hot"] > load_thresholds()["warm"]
    assert has_documented_fallback(load_agent_prompt())
