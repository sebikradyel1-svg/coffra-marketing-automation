# CLAUDE.md

## Project overview
- Coffra Marketing Automation: a 7-project portfolio for a **fictional** D2C specialty coffee brand (synthetic or public data only).
- Covers persona email automation, XGBoost lead scoring, RFM segmentation, AEO, MTA/Bayesian MMM attribution, technical SEO/GEO audit, and an agentic lead pipeline.
- P7 (`src/lead_intelligence/`) is the live pipeline: Qualification -> Outreach -> Governance Reviewer -> human approval.
- A 10-page Streamlit dashboard (`dashboard/`) is deployed on Streamlit Cloud; it reads committed data under `data/` and `src/`.
- Claude models are called through the Anthropic API; docs and case-study PDFs live in `docs/` and `case_study/`.

## Where the agents live
- `src/lead_intelligence/agents/qualification.py`: scores and routes leads (calls the XGBoost model in `scoring.py`).
- `src/lead_intelligence/agents/outreach.py`: RAG-grounded first-touch drafts (index in `src/lead_intelligence/rag/`).
- `src/lead_intelligence/agents/governance.py`: Governance Reviewer that checks claims against `src/lead_intelligence/data/brand_sources.md`.
- Related, not agents: `src/subject_optimizer/` (generator + critic for subject lines).

## Running tests and the calibration harness
Install: `pip install -r requirements.txt`. Both commands below call the Anthropic API, so they need `ANTHROPIC_API_KEY` in the environment.
- Pipeline smoke test (there is no pytest suite): `cd src/lead_intelligence && python test_pipeline.py`
- Governance calibration (50 API calls): `cd governance_calibration && python eval_harness.py`
  - `agent_fn` at the bottom of `eval_harness.py` selects the agent. `baseline_governance_agent` is a placeholder whose numbers must not be cited; `real_agent_adapter` runs the real agent.
  - Output is saved to `governance_calibration/eval_results.json`.

## Rules
1. **Never commit secrets.** Read `ANTHROPIC_API_KEY` from the environment. `.env` is gitignored; only `.env.example` (placeholders) is committed.
2. **Do not modify the live pipeline in `src/lead_intelligence/` unless the task says so.** New work goes in separate folders.
3. **Never invent results.** Every number in docs must come from a real run whose output is saved in a results file. If something cannot run in this environment (e.g. no API key or network), say so and stop.
4. **Label experiments as experiments** in READMEs.
