"""
EXPERIMENT: build the Qualification-agent eval set (synthetic leads).

Draws synthetic leads, scores each with the real score_lead(), and selects:
  10 clear HOT, 10 clear WARM, 10 clear COLD (>= MARGIN_CLEAR from every threshold),
  10 borderline (5 within BORDERLINE_MARGIN of each threshold),
  4 bad-field leads (2 missing a required field, 2 with a non-numeric value).

Numeric feature ranges = min/max of the 20 rows in
src/lead_intelligence/models/sample_predictions_v1.csv (the only raw feature
values in the repo; feature_spec_v1.json has names only). Expected tiers come
from the real score plus the thresholds parsed from the agent's prompt.

Run:  python build_eval_set.py [--out eval_set.json]
Scores depend on the installed xgboost / scikit-learn / shap versions, which
are recorded in the output. Exit code 2 (nothing written) if a band can't be filled.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path
from typing import Any

from common import (
    HERE, LEAD_INTELLIGENCE_DIR, environment_versions, expected_tier,
    has_documented_fallback, load_agent_prompt, parse_thresholds,
)

SEED = 42
POOL_SIZE = 4000
MARGIN_CLEAR = 0.10
BORDERLINE_MARGIN = 0.02
N_CLEAR = 10
N_BORDERLINE_PER_THRESHOLD = 5

SAMPLE_CSV = LEAD_INTELLIGENCE_DIR / "models" / "sample_predictions_v1.csv"
FEATURE_SPEC = LEAD_INTELLIGENCE_DIR / "models" / "feature_spec_v1.json"
FALLBACK_CITATION = "src/lead_intelligence/agents/qualification.py:60-62 (SYSTEM_PROMPT: tool fails -> tier WARM)"
ENGINEERED = ("EmailEngagementRate", "EngagementScore")  # computed by score_lead() if omitted
CHANNELS = ["CampaignChannel_PPC", "CampaignChannel_Referral", "CampaignChannel_SEO", "CampaignChannel_Social Media"]
TYPES = ["CampaignType_Consideration", "CampaignType_Conversion", "CampaignType_Retention"]


def load_sample_ranges() -> dict[str, dict[str, Any]]:
    with open(FEATURE_SPEC, encoding="utf-8") as f:
        columns = json.load(f)["feature_columns"]
    numeric = [c for c in columns if c not in ENGINEERED and c not in CHANNELS + TYPES and c != "Gender_Male"]
    with open(SAMPLE_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ranges = {}
    for col in numeric:
        vals = [float(r[col]) for r in rows]
        is_int = all(v == int(v) for v in vals)
        ranges[col] = {"min": min(vals), "max": max(vals), "integer": is_int}
    return {"n_sample_rows": len(rows), "columns": ranges}


def draw_lead(rng: random.Random, ranges: dict[str, dict[str, Any]]) -> dict[str, Any]:
    lead: dict[str, Any] = {}
    for col, r in ranges.items():
        lead[col] = rng.randint(int(r["min"]), int(r["max"])) if r["integer"] else rng.uniform(r["min"], r["max"])
    # Clicks cannot exceed opens; redraw within the sample range capped at opens.
    cr = ranges["EmailClicks"]
    lead["EmailClicks"] = rng.randint(int(cr["min"]), max(int(cr["min"]), min(int(cr["max"]), int(lead["EmailOpens"]))))
    lead["Gender_Male"] = rng.random() < 0.5
    # One-hot groups: exactly one flag or none (the dropped baseline category).
    channel = rng.choice(CHANNELS + [None])
    ctype = rng.choice(TYPES + [None])
    for c in CHANNELS:
        lead[c] = c == channel
    for t in TYPES:
        lead[t] = t == ctype
    return lead


def make_bad_leads(base_leads: list[dict[str, Any]], score_lead) -> list[dict[str, Any]]:
    mutations = [
        ("missing_field", "Age", None),
        ("missing_field", "Income", None),
        ("invalid_value", "WebsiteVisits", "n/a"),
        ("invalid_value", "TimeOnSite", "unknown"),
    ]
    out = []
    for i, ((kind, field, value), base) in enumerate(zip(mutations, base_leads), start=1):
        lead = dict(base)
        if kind == "missing_field":
            del lead[field]
        else:
            lead[field] = value
        try:
            score_lead(lead)
        except Exception as exc:  # noqa: BLE001 - we want exactly the failures the agent's tool would see
            error = f"{type(exc).__name__}: {exc}"
        else:
            raise RuntimeError(f"Bad lead {kind}/{field} did not make score_lead() raise; cannot use it")
        out.append({
            "id": f"BAD{i:02d}", "group": "bad_field", "lead": lead, "model_score": None,
            "expected_tier": "WARM", "expected_basis": FALLBACK_CITATION,
            "defect": {"kind": kind, "field": field}, "tool_error": error,
        })
    return out


def build(seed: int = SEED, pool_size: int = POOL_SIZE) -> dict[str, Any]:
    sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
    from scoring import score_lead

    prompt = load_agent_prompt()
    thresholds = parse_thresholds(prompt)
    if not has_documented_fallback(prompt):
        raise RuntimeError("No documented tool-failure fallback found in the agent prompt; bad-field leads must be excluded")
    hot, warm = thresholds["hot"], thresholds["warm"]

    ranges = load_sample_ranges()
    rng = random.Random(seed)
    pool = []
    for _ in range(pool_size):
        lead = draw_lead(rng, ranges["columns"])
        pool.append((lead, score_lead(lead)["score"]))

    def pick(pred, n):
        return [(l, s) for l, s in pool if pred(s)][:n]

    selections = {
        "clear_hot": pick(lambda s: s >= hot + MARGIN_CLEAR, N_CLEAR),
        "clear_warm": pick(lambda s: warm + MARGIN_CLEAR <= s <= hot - MARGIN_CLEAR, N_CLEAR),
        "clear_cold": pick(lambda s: s <= warm - MARGIN_CLEAR, N_CLEAR),
    }
    near_hot = pick(lambda s: abs(s - hot) <= BORDERLINE_MARGIN, N_BORDERLINE_PER_THRESHOLD)
    near_warm = pick(lambda s: abs(s - warm) <= BORDERLINE_MARGIN, N_BORDERLINE_PER_THRESHOLD)
    selections["borderline"] = near_hot + near_warm
    expected_sizes = {"clear_hot": N_CLEAR, "clear_warm": N_CLEAR, "clear_cold": N_CLEAR,
                      "borderline": 2 * N_BORDERLINE_PER_THRESHOLD}
    short = {g: (len(selections[g]), n) for g, n in expected_sizes.items() if len(selections[g]) < n}
    if short:
        raise BandNotFilled(short, pool_size)

    used = {id(l) for sel in selections.values() for l, _ in sel}
    spare = [l for l, _ in pool if id(l) not in used][:4]

    leads = []
    prefix = {"clear_hot": "HOT", "clear_warm": "WARM", "clear_cold": "COLD", "borderline": "BORD"}
    for group, sel in selections.items():
        for i, (lead, score) in enumerate(sel, start=1):
            leads.append({
                "id": f"{prefix[group]}{i:02d}", "group": group, "lead": lead, "model_score": score,
                "expected_tier": expected_tier(score, thresholds),
                "expected_basis": "thresholds parsed from agent SYSTEM_PROMPT applied to score_lead()",
            })
    leads += make_bad_leads(spare, score_lead)

    return {
        "experiment": True,
        "note": "Synthetic leads; expected tiers derive from the model's own score. Measures agent fidelity, not predictive accuracy.",
        "seed": seed, "pool_size": pool_size,
        "thresholds": thresholds, "clear_margin": MARGIN_CLEAR, "borderline_margin": BORDERLINE_MARGIN,
        "ranges_source": "min/max of the 20 rows in src/lead_intelligence/models/sample_predictions_v1.csv",
        "ranges": ranges, "environment": environment_versions(), "leads": leads,
    }


class BandNotFilled(Exception):
    def __init__(self, short: dict[str, tuple[int, int]], pool_size: int):
        self.short, self.pool_size = short, pool_size
        super().__init__(
            "Could not fill band(s) from a pool of %d leads: %s"
            % (pool_size, ", ".join(f"{g} got {got}/{want}" for g, (got, want) in short.items()))
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=HERE / "eval_set.json")
    args = parser.parse_args()
    try:
        eval_set = build()
    except BandNotFilled as exc:
        print(f"STOP: {exc}. Nothing written; margins were not loosened.", file=sys.stderr)
        return 2
    args.out.write_text(json.dumps(eval_set, indent=2, ensure_ascii=False), encoding="utf-8")
    counts: dict[str, int] = {}
    for item in eval_set["leads"]:
        counts[item["group"]] = counts.get(item["group"], 0) + 1
    print(f"Wrote {args.out}: {counts}; environment {eval_set['environment']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
