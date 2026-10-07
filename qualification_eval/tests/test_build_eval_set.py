import csv

import build_eval_set as b
from common import expected_tier


def test_group_sizes(eval_set):
    counts = {}
    for item in eval_set["leads"]:
        counts[item["group"]] = counts.get(item["group"], 0) + 1
    assert counts == {"clear_hot": 10, "clear_warm": 10, "clear_cold": 10, "borderline": 10, "bad_field": 4}


def test_deterministic_with_fixed_seed(eval_set):
    again = b.build()
    assert [(l["id"], l["lead"], l["model_score"]) for l in again["leads"]] == \
           [(l["id"], l["lead"], l["model_score"]) for l in eval_set["leads"]]


def test_expected_tiers_follow_thresholds(eval_set):
    t = eval_set["thresholds"]
    for item in eval_set["leads"]:
        if item["group"] != "bad_field":
            assert item["expected_tier"] == expected_tier(item["model_score"], t)


def test_clear_groups_keep_margin_and_borderline_is_near_a_threshold(eval_set):
    t, m, bm = eval_set["thresholds"], eval_set["clear_margin"], eval_set["borderline_margin"]
    for item in eval_set["leads"]:
        s = item["model_score"]
        if item["group"].startswith("clear_"):
            assert min(abs(s - t["hot"]), abs(s - t["warm"])) >= m - 1e-9
        elif item["group"] == "borderline":
            assert min(abs(s - t["hot"]), abs(s - t["warm"])) <= bm + 1e-9


def test_borderline_split_between_thresholds(eval_set):
    t, bm = eval_set["thresholds"], eval_set["borderline_margin"]
    near_hot = [i for i in eval_set["leads"] if i["group"] == "borderline" and abs(i["model_score"] - t["hot"]) <= bm]
    near_warm = [i for i in eval_set["leads"] if i["group"] == "borderline" and abs(i["model_score"] - t["warm"]) <= bm]
    assert len(near_hot) == len(near_warm) == 5


def test_bad_leads_fail_in_the_tool_and_expect_warm(eval_set):
    from scoring import score_lead
    import pytest

    bad = [i for i in eval_set["leads"] if i["group"] == "bad_field"]
    assert len(bad) == 4
    for item in bad:
        assert item["expected_tier"] == "WARM" and "qualification.py" in item["expected_basis"]
        with pytest.raises(Exception):
            score_lead(item["lead"])


def test_numeric_values_stay_within_sample_ranges(eval_set):
    with open(b.SAMPLE_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for item in eval_set["leads"]:
        if item["group"] == "bad_field":
            continue
        for col, r in eval_set["ranges"]["columns"].items():
            assert r["min"] <= float(item["lead"][col]) <= r["max"]
    assert eval_set["ranges"]["n_sample_rows"] == len(rows) == 20


def test_environment_versions_recorded(eval_set):
    assert set(eval_set["environment"]) == {"xgboost", "scikit-learn", "shap"}
    assert all(eval_set["environment"].values())


def test_band_not_filled_stops_instead_of_loosening(eval_set):
    import pytest

    with pytest.raises(b.BandNotFilled):
        b.build(pool_size=5)
