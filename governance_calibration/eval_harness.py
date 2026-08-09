"""
Governance Reviewer calibration harness — v3.

Same real_agent_adapter as before, matching your run_governance(draft, lead)
signature exactly. The one change from v2: this version saves each draft's
raw agent reasoning (claims_checked, flags, summary) into eval_results.json,
not just the PASS/REVISE verdict — so if something looks off, you can see
exactly why the agent decided what it decided, without re-running anything.
"""
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. BASELINE (placeholder, runs with zero setup — do not cite its numbers)
# ---------------------------------------------------------------------------

def baseline_governance_agent(draft_text, facts):
    import re
    draft_words = set(re.findall(r"[a-zăâîșț]+", draft_text.lower()))
    best_overlap = 0
    for fact in facts:
        fact_words = set(re.findall(r"[a-zăâîșț]+", fact["text"].lower()))
        best_overlap = max(best_overlap, len(draft_words & fact_words))
    verdict = "PASS" if best_overlap >= 4 else "REVISE"
    return {"verdict": verdict, "flagged_claims": [] if verdict == "PASS" else ["low grounding overlap"], "raw": None}


# ---------------------------------------------------------------------------
# 2. REAL AGENT ADAPTER — wraps agents.governance.run_governance()
# ---------------------------------------------------------------------------
def real_agent_adapter(draft_text, facts):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "lead_intelligence"))
    from agents.governance import run_governance  # noqa: E402

    draft = {"subject": "", "message": draft_text, "personalization_basis": "calibration test — no specific lead"}
    lead = {}

    result = run_governance(draft, lead)
    verdict = "PASS" if result["verdict"] == "APPROVE" else "REVISE"
    flagged = [c["claim"] for c in result.get("claims_checked", []) if not c.get("supported", True)]
    return {"verdict": verdict, "flagged_claims": flagged, "raw": result}


# ---------------------------------------------------------------------------
# 3. PICK WHICH AGENT TO RUN
# ---------------------------------------------------------------------------
#agent_fn = baseline_governance_agent
agent_fn = real_agent_adapter   # <- uncomment this (and comment the line above) to run for real
# ---------------------------------------------------------------------------


def load_data():
    here = Path(__file__).resolve().parent
    with open(here / "brand_facts.json", encoding="utf-8") as f:
        facts = json.load(f)["facts"]
    with open(here / "calibration_set.json", encoding="utf-8") as f:
        drafts = json.load(f)["drafts"]
    return facts, drafts


def run_eval(agent_fn, facts, drafts):
    rows = []
    for d in drafts:
        pred = agent_fn(d["draft_text"], facts)
        rows.append({
            "id": d["id"],
            "ground_truth": d["ground_truth_verdict"],
            "predicted": pred["verdict"],
            "correct": pred["verdict"] == d["ground_truth_verdict"],
            "flagged_claims": pred.get("flagged_claims", []),
            "raw": pred.get("raw"),
        })
    return rows


def confusion_counts(rows):
    tp = sum(1 for r in rows if r["ground_truth"] == "REVISE" and r["predicted"] == "REVISE")
    fn = sum(1 for r in rows if r["ground_truth"] == "REVISE" and r["predicted"] == "PASS")
    fp = sum(1 for r in rows if r["ground_truth"] == "PASS" and r["predicted"] == "REVISE")
    tn = sum(1 for r in rows if r["ground_truth"] == "PASS" and r["predicted"] == "PASS")
    return tp, fn, fp, tn


def report(rows):
    tp, fn, fp, tn = confusion_counts(rows)
    n = len(rows)
    accuracy = (tp + tn) / n if n else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("=" * 60)
    print(f"GOVERNANCE REVIEWER CALIBRATION v3 — {n} drafts")
    print("=" * 60)
    print(f"{'':20}Predicted PASS   Predicted REVISE")
    print(f"{'Actual PASS':20}{tn:<17}{fp}")
    print(f"{'Actual REVISE':20}{fn:<17}{tp}")
    print("-" * 60)
    print(f"Accuracy:            {accuracy:.1%}")
    print(f"Precision (REVISE):  {precision:.1%}   (of flagged drafts, % that deserved it)")
    print(f"Recall (REVISE):     {recall:.1%}   (of bad drafts, % actually caught)")
    print(f"F1 (REVISE):         {f1:.1%}")
    print("-" * 60)

    missed = [r["id"] for r in rows if r["ground_truth"] == "REVISE" and r["predicted"] == "PASS"]
    if missed:
        print(f"MISSED (should've been REVISE, agent said PASS): {', '.join(missed)}")
    over_flagged = [r["id"] for r in rows if r["ground_truth"] == "PASS" and r["predicted"] == "REVISE"]
    if over_flagged:
        print(f"OVER-FLAGGED (was fine, agent said REVISE):      {', '.join(over_flagged)}")
        print("  -> check eval_results.json[rows][id]['raw'] for each one to see the agent's stated reason")
    print("=" * 60)

    return {"n": n, "accuracy": accuracy, "precision": precision, "recall": recall,
            "f1": f1, "tp": tp, "fn": fn, "fp": fp, "tn": tn,
            "missed_ids": missed, "over_flagged_ids": over_flagged}


if __name__ == "__main__":
    facts, drafts = load_data()
    rows = run_eval(agent_fn, facts, drafts)
    metrics = report(rows)

    out_path = Path(__file__).resolve().parent / "eval_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"rows": rows, "metrics": metrics}, f, indent=2, ensure_ascii=False)
    print(f"\nSaved results (including per-draft agent reasoning) to {out_path}")
