import json
import sys

import pytest

import eval_harness as h


def _row(id_, group, expected, predicted, drift=False, score_ok=True):
    return {
        "id": id_, "group": group, "expected": expected, "predicted": None if drift else predicted,
        "correct": None if drift else predicted == expected, "environment_drift": drift,
        "agent_score": 0.5, "runtime_model_score": 0.5, "score_matches_tool": None if drift else score_ok,
        "raw": {"tier": predicted}, "error": None,
    }


# --- pure metric tests: no model dependencies needed --------------------------------
def test_compute_metrics_headline_groups_confusion_and_bad_field_separate():
    rows = [
        _row("H1", "clear_hot", "HOT", "HOT"), _row("H2", "clear_hot", "HOT", "WARM"),
        _row("W1", "clear_warm", "WARM", "WARM"), _row("C1", "clear_cold", "COLD", "COLD"),
        _row("B1", "borderline", "HOT", "HOT"), _row("X1", "bad_field", "WARM", "WARM"),
        _row("X2", "bad_field", "WARM", "COLD"),
    ]
    m = h.compute_metrics(rows)
    assert m["headline_valid_field"] == {"n": 5, "correct": 4, "accuracy": 0.8}
    assert m["per_group"]["clear_hot"]["accuracy"] == 0.5
    assert m["confusion_matrix_expected_by_predicted"]["HOT"] == {"HOT": 2, "WARM": 1, "COLD": 0, "INVALID": 0}
    assert m["bad_field_separate"] == {"n": 2, "correct": 1, "accuracy": 0.5}
    assert {x["id"] for x in m["misclassified"]} == {"H2", "X2"}


def test_drift_is_excluded_from_accuracy_and_reported_separately():
    rows = [_row("H1", "clear_hot", "HOT", "HOT"), _row("H2", "clear_hot", "HOT", None, drift=True)]
    m = h.compute_metrics(rows)
    assert m["headline_valid_field"]["n"] == 1
    assert m["environment_drift"] == {"n": 1, "ids": ["H2"]}


def test_score_fidelity_counts_mismatches():
    rows = [_row("H1", "clear_hot", "HOT", "HOT"), _row("H2", "clear_hot", "HOT", "HOT", score_ok=False)]
    sf = h.compute_metrics(rows)["score_fidelity"]
    assert sf == {"n": 2, "agent_score_equals_tool_score": 1, "mismatched_ids": ["H2"]}


def test_normalize_tier():
    assert h.normalize_tier(" hot ") == "HOT"
    assert h.normalize_tier(None) == "INVALID" and h.normalize_tier("MAYBE") == "INVALID"


def test_real_mode_without_api_key_exits_and_writes_nothing(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    out = tmp_path / "results.json"
    monkeypatch.setattr(sys, "argv", ["eval_harness.py", "--out", str(out)])
    assert h.main() == 1
    assert not out.exists()
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


# --- tests that call score_lead(): need the model dependencies ----------------------
def test_stub_agent_end_to_end(eval_set, tmp_path, monkeypatch):
    set_path, out = tmp_path / "eval_set.json", tmp_path / "out.json"
    set_path.write_text(json.dumps(eval_set), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["eval_harness.py", "--stub", "--eval-set", str(set_path), "--out", str(out)])
    assert h.main() == 0
    res = json.loads(out.read_text(encoding="utf-8"))
    assert res["mode"] == "stub" and "plumbing" in res["note"]
    assert res["metrics"]["headline_valid_field"]["n"] == 40
    assert res["metrics"]["bad_field_separate"]["n"] == 4
    assert res["environment"] and res["eval_set_environment"]


def test_wrong_and_crashing_agents_are_recorded_as_misses(eval_set):
    items = [i for i in eval_set["leads"] if i["id"] in ("HOT01", "COLD01", "WARM01")]

    def wrong(lead):
        return {"tier": "COLD", "score": 0.0, "raw": {"tier": "COLD"}, "error": None}

    rows = h.run_eval(wrong, items)
    by_id = {r["id"]: r["correct"] for r in rows}
    assert by_id == {"HOT01": False, "WARM01": False, "COLD01": True}
    crashed = h.run_eval(lambda lead: {"tier": None, "score": None, "raw": None, "error": "Boom"}, items)
    assert all(r["predicted"] == "INVALID" and r["error"] == "Boom" for r in crashed)
    assert len(h.compute_metrics(crashed)["misclassified"]) == 3


def test_environment_drift_detected_and_agent_not_called(eval_set):
    item = json.loads(json.dumps(next(i for i in eval_set["leads"] if i["id"] == "HOT01")))
    item["model_score"] += 0.01
    calls = []
    rows = h.run_eval(lambda lead: calls.append(1) or {"tier": "HOT", "score": 0.9, "raw": {}, "error": None}, [item])
    assert rows[0]["environment_drift"] is True and calls == []


def test_score_fidelity_flags_agent_that_changes_the_score(eval_set):
    item = next(i for i in eval_set["leads"] if i["id"] == "HOT01")
    rows = h.run_eval(lambda lead: {"tier": "HOT", "score": item["model_score"] - 0.05, "raw": {}, "error": None}, [item])
    assert rows[0]["correct"] is True and rows[0]["score_matches_tool"] is False
