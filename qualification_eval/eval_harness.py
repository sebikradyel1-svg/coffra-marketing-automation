"""
EXPERIMENT: component-level eval of the Qualification agent.

Measures whether the agent applies the model's score and the documented tier
thresholds faithfully (exact tier match, no LLM judge). It does NOT measure the
model's predictive accuracy. Style follows governance_calibration/eval_harness.py.

  python eval_harness.py          # real agent; needs ANTHROPIC_API_KEY; writes results.json
  python eval_harness.py --stub   # deterministic fake agent (plumbing test only); writes results_stub.json

Each lead's score is recomputed with score_lead() at run time and compared to
the stored score (tolerance 1e-6). Mismatches are reported as "environment
drift" and excluded from accuracy (the agent is not called on them).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

from common import HERE, LEAD_INTELLIGENCE_DIR, TIERS, environment_versions, expected_tier

DRIFT_TOLERANCE = 1e-6
SCORE_MATCH_TOLERANCE = 1e-6
VALID_GROUPS = ("clear_hot", "clear_warm", "clear_cold", "borderline")
BAD_GROUP = "bad_field"
PREDICTED_LABELS = TIERS + ("INVALID",)  # INVALID = agent crashed or returned a non-tier


# ---------------------------------------------------------------------------
# Agents: fn(lead) -> {"tier": str | None, "score": float | None, "raw": ..., "error": str | None}
# ---------------------------------------------------------------------------
def real_agent_adapter(lead: dict[str, Any]) -> dict[str, Any]:
    sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
    from agents.qualification import run_qualification  # noqa: E402

    try:
        raw = run_qualification(lead)
    except Exception as exc:  # noqa: BLE001 - a crash is a miss, and must be kept
        return {"tier": None, "score": None, "raw": None, "error": f"{type(exc).__name__}: {exc}"}
    return {"tier": raw.get("tier"), "score": raw.get("score"), "raw": raw, "error": None}


def stub_agent(lead: dict[str, Any]) -> dict[str, Any]:
    """PLUMBING ONLY: applies the thresholds to the real score. Its output is not a result."""
    from common import load_thresholds

    sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
    from scoring import score_lead

    try:
        score = score_lead(lead)["score"]
    except Exception:  # noqa: BLE001
        raw = {"score": None, "tier": "WARM", "action": "NURTURE", "reasoning": "stub: tool failed -> fallback"}
        return {"tier": "WARM", "score": None, "raw": raw, "error": None}
    tier = expected_tier(score, load_thresholds())
    raw = {"score": score, "tier": tier, "reasoning": "stub"}
    return {"tier": tier, "score": score, "raw": raw, "error": None}


# ---------------------------------------------------------------------------
# Eval
# ---------------------------------------------------------------------------
def runtime_score(lead: dict[str, Any]) -> tuple[float | None, str | None]:
    sys.path.insert(0, str(LEAD_INTELLIGENCE_DIR))
    from scoring import score_lead

    try:
        return score_lead(lead)["score"], None
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def normalize_tier(value: Any) -> str:
    tier = str(value).strip().upper() if value is not None else ""
    return tier if tier in TIERS else "INVALID"


def run_eval(agent_fn: Callable[[dict[str, Any]], dict[str, Any]], items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in items:
        now_score, now_error = runtime_score(item["lead"])
        if item["group"] == BAD_GROUP:
            drift = now_error is None  # bad lead no longer fails -> environment changed
        else:
            drift = now_score is None or abs(now_score - item["model_score"]) > DRIFT_TOLERANCE
        row = {
            "id": item["id"], "group": item["group"], "expected": item["expected_tier"],
            "stored_model_score": item["model_score"], "runtime_model_score": now_score,
            "runtime_tool_error": now_error, "environment_drift": drift,
        }
        if drift:
            row.update(predicted=None, correct=None, agent_score=None, score_matches_tool=None, raw=None, error=None)
        else:
            result = agent_fn(item["lead"])
            predicted = normalize_tier(result.get("tier"))
            agent_score = result.get("score")
            row.update(
                predicted=predicted, correct=predicted == item["expected_tier"], agent_score=agent_score,
                score_matches_tool=(
                    None if item["group"] == BAD_GROUP
                    else isinstance(agent_score, (int, float)) and abs(agent_score - now_score) <= SCORE_MATCH_TOLERANCE
                ),
                raw=result.get("raw"), error=result.get("error"),
            )
        rows.append(row)
    return rows


def _accuracy(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    correct = sum(1 for r in rows if r["correct"])
    return {"n": n, "correct": correct, "accuracy": correct / n if n else None}


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    drifted = [r for r in rows if r["environment_drift"]]
    valid = [r for r in rows if r["group"] in VALID_GROUPS and not r["environment_drift"]]
    bad = [r for r in rows if r["group"] == BAD_GROUP and not r["environment_drift"]]

    confusion = {e: {p: 0 for p in PREDICTED_LABELS} for e in TIERS}
    for r in valid:
        confusion[r["expected"]][r["predicted"]] += 1

    fidelity = [r for r in valid if r["score_matches_tool"] is not None]
    return {
        "headline_valid_field": _accuracy(valid),
        "per_group": {g: _accuracy([r for r in valid if r["group"] == g]) for g in VALID_GROUPS},
        "confusion_matrix_expected_by_predicted": confusion,
        "score_fidelity": {
            "n": len(fidelity), "agent_score_equals_tool_score": sum(1 for r in fidelity if r["score_matches_tool"]),
            "mismatched_ids": [r["id"] for r in fidelity if not r["score_matches_tool"]],
        },
        "bad_field_separate": _accuracy(bad),
        "environment_drift": {"n": len(drifted), "ids": [r["id"] for r in drifted]},
        "misclassified": [
            {k: r[k] for k in ("id", "group", "expected", "predicted", "agent_score", "runtime_model_score", "raw", "error")}
            for r in valid + bad if not r["correct"]
        ],
    }


def _pct(acc: dict[str, Any]) -> str:
    return "n/a" if acc["accuracy"] is None else f"{acc['accuracy']:.1%} ({acc['correct']}/{acc['n']})"


def report(metrics: dict[str, Any], mode: str) -> None:
    print("=" * 64)
    print(f"QUALIFICATION AGENT EVAL (experiment) - mode: {mode}")
    if mode == "stub":
        print("STUB MODE: plumbing test only; these numbers are not results.")
    print("=" * 64)
    print(f"Headline accuracy (valid-field leads): {_pct(metrics['headline_valid_field'])}")
    for g, acc in metrics["per_group"].items():
        print(f"  {g:<12} {_pct(acc)}")
    print("-" * 64)
    print("Confusion matrix (rows expected, cols predicted):")
    print(f"  {'':8}" + "".join(f"{p:<9}" for p in PREDICTED_LABELS))
    for e, cols in metrics["confusion_matrix_expected_by_predicted"].items():
        print(f"  {e:<8}" + "".join(f"{cols[p]:<9}" for p in PREDICTED_LABELS))
    sf = metrics["score_fidelity"]
    print(f"Agent score equals tool score: {sf['agent_score_equals_tool_score']}/{sf['n']}")
    print(f"Bad-field leads (separate; expected WARM from a prompt instruction): {_pct(metrics['bad_field_separate'])}")
    drift = metrics["environment_drift"]
    if drift["n"]:
        print(f"ENVIRONMENT DRIFT: {drift['n']} lead(s) excluded: {', '.join(drift['ids'])}")
    for m in metrics["misclassified"]:
        print(f"MISCLASSIFIED {m['id']} ({m['group']}): expected {m['expected']}, got {m['predicted']}")
    print("=" * 64)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--stub", action="store_true", help="use the deterministic fake agent (no API)")
    parser.add_argument("--eval-set", type=Path, default=HERE / "eval_set.json")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    mode = "stub" if args.stub else "real"
    if mode == "real" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set; nothing run, no results written.", file=sys.stderr)
        return 1
    if not args.eval_set.exists():
        print(f"{args.eval_set} not found. Run build_eval_set.py first.", file=sys.stderr)
        return 1
    out = args.out or HERE / ("results_stub.json" if args.stub else "results.json")

    eval_set = json.loads(args.eval_set.read_text(encoding="utf-8"))
    env_now = environment_versions()
    rows = run_eval(stub_agent if args.stub else real_agent_adapter, eval_set["leads"])
    metrics = compute_metrics(rows)
    report(metrics, mode)

    out.write_text(json.dumps({
        "experiment": True, "mode": mode,
        "note": "STUB: plumbing test, not a result" if args.stub else "Real agent run",
        "environment": env_now, "eval_set_environment": eval_set.get("environment"),
        "environment_matches_eval_set": env_now == eval_set.get("environment"),
        "thresholds": eval_set.get("thresholds"), "metrics": metrics, "rows": rows,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved results to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
