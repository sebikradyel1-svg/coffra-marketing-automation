# Qualification agent eval

> **EXPERIMENT.** A component-level evaluation of the Qualification agent,
> not part of the live pipeline in `src/lead_intelligence/`. Nothing there was
> modified. Style follows [`governance_calibration/`](../governance_calibration/).

## What this measures, and what it does not

It checks whether the agent **applies the model's score and the documented
tier thresholds faithfully**: given a lead, does it call `score_lead`, keep the
score, and map it to the tier the thresholds define? Tier comparison is exact
match; there is no LLM judge.

- **Synthetic leads.** Generated from feature ranges, not real customers.
- **Tiers derive from the model's own score.** The expected tier is the real
  `score_lead()` output plus the thresholds, so the model is correct by
  construction. This is **agent fidelity, not predictive accuracy**; it says
  nothing about whether a score predicts conversion.
- **Small sample.** 40 valid-field leads + 4 bad-field leads, one run each.
  The agent is not deterministic, so a rerun can differ.
- **The thresholds live only in the prompt.** HOT / WARM / COLD cut-offs exist
  only as prose in the agent's `SYSTEM_PROMPT`
  (`src/lead_intelligence/agents/qualification.py`), not as code constants.
  That prompt is exactly what this eval checks. `common.py` parses the numbers
  out of that string at load time (no copies) and fails loudly if the wording
  changes.

## Eval set (`build_eval_set.py`)

Fixed seed (42). Candidates are drawn at random, scored with the real
`score_lead()`, and selected into groups:

| Group | n | Definition |
|---|---|---|
| `clear_hot` / `clear_warm` / `clear_cold` | 10 each | at least 0.10 away from every threshold |
| `borderline` | 10 | 5 within 0.02 of each threshold; expected tier by the exact rule on the rounded score |
| `bad_field` | 4 | 2 missing a required field (`Age`, `Income`), 2 with a non-numeric value (`WebsiteVisits`, `TimeOnSite`) |

**Feature ranges.** The repo has no raw lead dataset and
`feature_spec_v1.json` lists column names only. Numeric ranges are the
**min/max of the 20 rows in `models/sample_predictions_v1.csv`**, the only raw
feature values in the repo. That is a narrow basis (n=20). Integer-valued
columns are drawn as integers, `EmailClicks` is capped at `EmailOpens`, and
booleans / one-hot flags are sampled at random (at most one channel flag and
one campaign-type flag; all-false is the baseline category).

If a band cannot be filled, the builder stops with exit code 2 and writes
nothing; it does not loosen the margins.

**Bad-field leads.** Their expected tier is WARM, taken from the prompt
instruction at `qualification.py:60-62` ("if the tool fails, return tier
WARM"). This comes from a **prompt instruction, not from verified-desirable
behavior**: nobody has established that WARM is the right outcome for a
broken lead. They are reported on a separate line and are not part of the
headline accuracy. The builder checks that each one really makes
`score_lead()` raise.

### `eval_set.json` is generated locally

`eval_set.json` is **not committed here**. The saved model files were pickled
with older scikit-learn / xgboost versions, so scores differ across
environments. Generate it where you will run the eval:

```bash
pip install -r requirements.txt && pip install -r qualification_eval/requirements.txt
python qualification_eval/build_eval_set.py      # writes qualification_eval/eval_set.json
```

The `xgboost`, `scikit-learn` and `shap` versions are recorded in it.

## Harness (`eval_harness.py`)

```bash
export ANTHROPIC_API_KEY=...                       # Windows PowerShell: $env:ANTHROPIC_API_KEY="..."
python qualification_eval/eval_harness.py          # real agent, writes results.json
python qualification_eval/eval_harness.py --stub   # fake agent, writes results_stub.json
```

- Runs `run_qualification` on each lead (the same real-agent wiring idea as
  the governance harness's `real_agent_adapter`). Real mode needs the API key
  and exits without writing anything if it is unset.
- **Environment drift.** Each lead's score is recomputed with `score_lead()`
  at run time and compared with the stored score (tolerance 1e-6). Mismatches
  are listed as "environment drift", excluded from accuracy, and the agent is
  not called on them. Package versions are recorded in both `eval_set.json`
  and `results.json`.
- **Headline accuracy** is on the valid-field leads only (up to 40), with a
  per-group breakdown, a confusion matrix (expected rows, predicted columns;
  `INVALID` = crash or non-tier output), and every misclassified lead with the
  raw agent output. A crash counts as a miss.
- **Score fidelity.** Also records whether the agent's returned `score` equals
  the tool's score (tolerance 1e-6).
- The bad-field leads get their own line.
- **Stub mode** is a deterministic fake agent for testing the plumbing. Its
  output is not a result and `results_stub.json` is labeled as such.

## Results (single run, 2026-10-07)

On the 40 valid-field leads the agent returned the expected tier in 39 cases
(97.5%; 30/30 on the three clear groups, 9/10 on the borderline group). With
n=40 and one run per lead this is a rough estimate (95% Wilson interval about
87% to 99.6%), and the agent is not deterministic.

The single miss was BORD08 (model score 0.399, expected COLD): the agent
reported the score rounded to 0.40, treated it as the WARM threshold and
returned WARM. Rounding crossed a threshold in two borderline cases (BORD03
and BORD08); the agent handled the first correctly and the second
incorrectly, so this shows the failure exists, not how often it occurs.

Score fidelity: the harness required the agent's score to equal the tool's
score to 1e-6, which held in 7 of 40 cases. The agent rounds scores to two
decimals in 33 of 40 cases and reports full precision in the rest. All 40
returned scores are within 0.005 of the tool score, so this is rounding and
not altered scores. The 1e-6 tolerance was a design error in this experiment
and is kept as run.

Bad-field leads (separate line; the expected WARM comes from a prompt
instruction): 1 of 4 matched. For the two leads with a missing field (BAD01,
BAD02) the agent's output could not be parsed (JSONDecodeError) and no tier
was recorded; the harness did not save the raw text. For the two leads with an
invalid value (BAD03, BAD04) the agent did not apply the documented WARM
fallback. According to its own reasoning text it replaced the invalid value
with 0, scored the lead and tiered it: BAD03 landed on WARM only because the
imputed score fell in the WARM band, BAD04 on COLD. The harness does not
record tool calls, so the imputation is known only from the agent's text.

Not measured: reasoning quality, predictive accuracy, run-to-run variability.
results.json does not record the agent's model or a timestamp..

## Tests

```bash
pip install -r qualification_eval/requirements.txt
python -m pytest qualification_eval -rs
```

Tests that need the model dependencies (xgboost, shap, scikit-learn,
anthropic) are skipped with a reason when those are missing; check the `-rs`
output, since skipped tests have not run.

Only one of the five leads near the 0.70 threshold (BORD02) lies above it, so the HOT side of that boundary is tested by a single case.
