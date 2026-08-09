# Governance Reviewer — Human Calibration (v3)

## What happened so far

- **v1**: built against invented facts (wrong project entirely) — discarded.
- **v2**: built against the real `brand_sources.md`. You ran it for real:
  **100% recall, 68% precision.** The agent never let a genuinely bad claim
  through — it caught D41 (the exact ungrounded phrase from `governance.py`'s
  own system-prompt example) correctly. But it over-flagged 14 of 20 clean
  drafts.
- **Root cause found**: most v2 "clean" drafts included personalization
  language ("you've opened our emails several times, so...") that the
  agent had no way to verify, because the harness passes an empty `lead={}`
  dict. The agent was right to flag those — the test was flawed, not the
  agent. (Also caught: I'd mislabeled D01 in v2.)
- **v3** (this version): removed every lead-specific personalization claim.
  Every draft now makes a claim purely about Coffra's brand, product, or
  marketing system — the kind of thing `brand_sources.md` actually
  documents. This isolates one clean question: does the agent correctly
  verify claims against approved brand sources, independent of any
  lead-context confound?

## What's here

- `brand_facts.json` — unchanged from v2, the real facts from `data/brand_sources.md`
- `build_calibration_set.py` — generates `calibration_set.json`: 50 drafts (20 clean, 20 with a planted contradiction, 10 plausible-but-unverifiable)
- `calibration_set.json` — the v3 labeled set
- `eval_harness.py` — runs an agent, reports precision/recall/F1, **now also saves each draft's raw agent reasoning** to `eval_results.json` so you can inspect *why* something was flagged without re-running

## How to run it

1. Delete your old `governance_calibration/` folder (v2) and replace it with this one, in the same spot — next to `src/` in your project root:

   ```
   coffra-marketing-automation/
     src/lead_intelligence/agents/governance.py
     governance_calibration/          <- this folder
   ```

2. In `eval_harness.py`, find:

   ```python
   agent_fn = baseline_governance_agent
   # agent_fn = real_agent_adapter
   ```

   Comment the first line, uncomment the second.

3. Run:

   ```bash
   py eval_harness.py
   ```

   (50 API calls, same as before — expect a couple of minutes.)

## What to do with the numbers this time

If precision is still noticeably below recall, open `eval_results.json`
and look at the `raw` field for a couple of the over-flagged IDs — it has
the agent's own `claims_checked` and `summary`, so you'll see its exact
stated reason. Two realistic outcomes:

- **The reasons look legitimate** (e.g., it's reading a paraphrase as an
  "addition" per the strict "fără adăugiri" rule in your system prompt) —
  that's a real, useful finding: your agent is stricter about paraphrase
  than a human labeler might be. Worth a sentence in the case study.
- **The reasons look wrong** (it's inventing a contradiction that isn't
  there) — that's a real bug worth fixing before you cite the number.

Either way, you now have the receipts to tell the difference, which is the
actual point of calibrating a judge in the first place.

## Writing it up

> Calibrated the Governance Reviewer against a 50-draft test set built
> from the real approved brand sources — 20 clean claims, 20 planted
> contradictions, 10 plausible-but-unverifiable claims — labeled manually.
> Iterated on the test set itself after the first run surfaced a confound
> (personalization claims with no lead data to verify them against), then
> re-ran for a clean measurement: [X]% recall / [Y]% precision on flagging
> unsupported claims.

The fact that the calibration process itself needed a correction is worth
keeping in the writeup, not hiding. It's the same "here's what broke and
what I did about it" pattern your other case studies already use, and it's
more credible than a suspiciously clean first-try number.
