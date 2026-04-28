# Coffra Marketing Automation

> **AI-augmented marketing system for a fictional D2C specialty coffee brand.**
> A 5-project portfolio demonstrating modern marketing analytics: persona automation, ML lead scoring, customer segmentation, AEO content strategy, and Bayesian attribution modeling.

---

## Live Demo

**[coffra-marketing-dashboard.streamlit.app](https://coffra-marketing-dashboard.streamlit.app/)**

Eight-page Streamlit dashboard covering lead scoring (XGBoost + SHAP), AI subject line generation, HubSpot CRM snapshot, campaign funnels, customer segmentation, AEO analysis, and multi-method attribution modeling. Brand-aligned with Coffra design system.

---

## What's in this repo

This repository contains 5 production-grade projects targeting **AI Marketing Specialist** and **Marketing Automation** roles. Each project is independently scoped, fully documented, and integrates with the live dashboard.

The brand is fictional — by design. This avoids privacy and legal risks of using real customer data. All content is original, all data is public (Kaggle, UCI) or synthetic (with documented generation), and all "brand" decisions are explicit fictional design choices.

---

## Projects

### P1 — Marketing Automation

Persona-driven email automation system with two distinct journeys (English Connoisseur, Romanian Daily Ritualist), AI Subject Line Optimizer using Claude API, and XGBoost lead scoring model.

**Key artifacts:**
- 13 emails (10 nurture + 3 cart recovery) with full copy decisions log
- Lead scoring model: Test ROC-AUC 0.78, explicit data leakage audit, SHAP explainability
- AI Subject Line Optimizer: generator + critic pipeline, SHA-256 caching
- HubSpot workflows implemented (with disclosed trial limitations)
- A/B testing methodology pre-registered

### P2 — Marketing Dashboard (Live)

Multi-page Streamlit application deployed to Streamlit Cloud with auto-rebuild on git push.

**Key artifacts:**
- 8 dashboard pages (Lead Quality, Subject Optimizer, HubSpot CRM, Funnel, Methodology, Segments, AEO, Attribution)
- Coffra brand design system (light theme, brown accent palette)
- HubSpot Private App API extraction script
- Snapshot-based data architecture for stable post-trial demo

### P3 — Customer Segmentation

RFM analysis with K-Means + Hierarchical clustering on Online Retail II UCI dataset (1.07M transactions, 5,878 customers).

**Key artifacts:**
- 11 standard rule-based RFM segments
- K-Means (k=4) + Hierarchical clustering with cross-validation (ARI = 0.613)
- **Strategic insight:** Probable Connoisseurs = 14.4% of customers, 61.8% of revenue (4.3x concentration ratio)
- **£240K projected annual uplift** (+23% over untargeted baseline)
- Coffra-specific deployment playbook for all 11 segments
- Live dashboard integration

### P4 — AEO Content Strategy (2026 Trend)

Answer Engine Optimization framework for AI search era. Strategy, schemas, and automated audit.

**Key artifacts:**
- 6-pillar AEO strategy with 12-month content calendar
- 12 Schema.org JSON-LD implementations (copy-paste ready)
- Automated AEO audit script (multi-engine query battery via Anthropic API)
- AI Visibility Score / Citation Rate / Sentiment metrics framework
- Live dashboard integration

### P5 — Attribution Modeling

Multi-Touch Attribution + Bayesian Marketing Mix Model with PyMC. Validated against synthetic data with known ground truth.

**Key artifacts:**
- 6 MTA methods: Last-Click, First-Click, Linear, Time-Decay, Markov Chain (removal effect), Shapley Values (exact enumeration)
- Bayesian MMM with PyMC + NUTS sampling, adstock + Hill saturation
- Convergence diagnostics: R-hat = 1.00, ESS = 750, R² = 0.69, MAPE = 11.3%, 95% CI coverage = 95.2%
- **Strategic finding:** Email is 8x more cost-efficient than Meta Ads (CPA £1.92 vs £15.44)
- Honest method assessment (no universal winner — depends on path structure)
- Live dashboard integration

---

## Quick navigation

### Strategy & content (13 documents)

| File | Project | Purpose |
|---|---|---|
| [`docs/01_business_context.md`](docs/01_business_context.md) | P1 | Coffra brand foundation |
| [`docs/02_persona_connoisseur.md`](docs/02_persona_connoisseur.md) | P1 | Andrei (32, specialty coffee enthusiast) |
| [`docs/03_persona_daily_ritualist.md`](docs/03_persona_daily_ritualist.md) | P1 | Bianca (30, aspirational consumer) |
| [`docs/04_email_copy_connoisseur.md`](docs/04_email_copy_connoisseur.md) | P1 | 5 nurture emails (EN), 14-day sequence |
| [`docs/05_email_copy_daily_ritualist.md`](docs/05_email_copy_daily_ritualist.md) | P1 | 5 nurture emails (RO), parallel journey |
| [`docs/06_email_copy_cart_recovery.md`](docs/06_email_copy_cart_recovery.md) | P1 | 3 cart recovery emails (Connoisseur) |
| [`docs/07_hubspot_workflow_specs.md`](docs/07_hubspot_workflow_specs.md) | P1 | HubSpot implementation spec |
| [`docs/08_ab_testing_methodology.md`](docs/08_ab_testing_methodology.md) | P1 | A/B test methodology with chi-square |
| [`docs/09_segmentation_methodology.md`](docs/09_segmentation_methodology.md) | P3 | RFM + clustering methodology |
| [`docs/10_segment_strategies.md`](docs/10_segment_strategies.md) | P3 | Coffra deployment playbook |
| [`docs/11_aeo_strategy.md`](docs/11_aeo_strategy.md) | P4 | AEO 6-pillar strategy + content calendar |
| [`docs/12_schema_implementation.md`](docs/12_schema_implementation.md) | P4 | 12 Schema.org JSON-LD templates |
| [`docs/13_attribution_methodology.md`](docs/13_attribution_methodology.md) | P5 | MTA + MMM methodology |

### Notebooks (10 notebooks)

| Path | Project | Purpose |
|---|---|---|
| [`notebooks/01_lead_scoring_eda_and_model.ipynb`](notebooks/01_lead_scoring_eda_and_model.ipynb) | P1 | XGBoost + SHAP, Kaggle dataset |
| [`notebooks/02_rfm_eda.ipynb`](notebooks/02_rfm_eda.ipynb) | P3 | EDA + data quality on Online Retail II |
| [`notebooks/03_rfm_scoring_and_segments.ipynb`](notebooks/03_rfm_scoring_and_segments.ipynb) | P3 | RFM scoring + 11 segments |
| [`notebooks/04_customer_clustering.ipynb`](notebooks/04_customer_clustering.ipynb) | P3 | K-Means + Hierarchical clustering |
| [`notebooks/05_segment_to_strategy.ipynb`](notebooks/05_segment_to_strategy.ipynb) | P3 | Strategy mapping + financial projection |
| [`notebooks/06_aeo_audit.ipynb`](notebooks/06_aeo_audit.ipynb) | P4 | Multi-engine AEO audit (Anthropic API) |
| [`notebooks/07_data_generation.ipynb`](notebooks/07_data_generation.ipynb) | P5 | Synthetic data with known ground truth |
| [`notebooks/08_multi_touch_attribution.ipynb`](notebooks/08_multi_touch_attribution.ipynb) | P5 | 6 MTA methods (Markov, Shapley, etc.) |
| [`notebooks/09_marketing_mix_model.ipynb`](notebooks/09_marketing_mix_model.ipynb) | P5 | Bayesian MMM with PyMC + NUTS |
| [`notebooks/10_attribution_comparison.ipynb`](notebooks/10_attribution_comparison.ipynb) | P5 | Cross-method comparison + business insights |

### Code & dashboards

| Path | Purpose |
|---|---|
| [`src/subject_optimizer/`](src/subject_optimizer/) | AI Subject Line Optimizer Python package |
| [`src/streamlit_app.py`](src/streamlit_app.py) | Streamlit UI for Subject Optimizer |
| [`src/models/`](src/models/) | Saved model artifacts |
| [`dashboard/`](dashboard/) | Multi-page Streamlit app (live deployment) |
| [`extract_hubspot_snapshot.py`](extract_hubspot_snapshot.py) | HubSpot Private App API extraction |
| [`generate_case_study.py`](generate_case_study.py) | P1 case study PDF generator |
| [`generate_case_study_p2.py`](generate_case_study_p2.py) | P2 case study PDF generator |
| [`generate_case_study_p3.py`](generate_case_study_p3.py) | P3 case study PDF generator |
| [`generate_case_study_p4.py`](generate_case_study_p4.py) | P4 case study PDF generator |
| [`generate_case_study_p5.py`](generate_case_study_p5.py) | P5 case study PDF generator |

---

## Project status

**All 5 projects v1.0 — complete.**

| Project | Component | Status |
|---|---|---|
| **P1** | Strategy + 13 emails + ML model + AI tooling + HubSpot | ✅ Complete |
| **P2** | Live dashboard with 8 pages | ✅ [Live](https://coffra-marketing-dashboard.streamlit.app/) |
| **P3** | RFM + ML clustering + dashboard + case study | ✅ Complete |
| **P4** | AEO strategy + 12 schemas + audit + dashboard | ✅ Complete |
| **P5** | MTA + Bayesian MMM + dashboard + case study | ✅ Complete |

---

## Cross-project skills demonstrated

- **Marketing strategy:** persona development, content design, journey mapping
- **ML supervised:** XGBoost lead scoring with SHAP explainability
- **ML unsupervised:** K-Means + Hierarchical clustering with cross-validation
- **Bayesian methods:** PyMC MMM with NUTS sampling, posterior credible intervals
- **Causal inference:** Markov chain removal effects, Shapley value attribution
- **AI integration:** Anthropic Claude API for content generation + audit
- **Production deployment:** Live Streamlit Cloud with CI/CD via GitHub
- **Schema.org expertise:** 12 JSON-LD types for AEO 2026 trend
- **Statistical rigor:** chi-square A/B tests, convergence diagnostics, posterior predictive checks
- **Honest documentation:** transparent disclosure of synthetic data, assumptions, limitations

## Data integrity principles

- All projects use either public datasets (Kaggle, UCI) or synthetic data (with explicit generation methodology)
- Financial projections labelled as scenarios, anchored to industry benchmarks (Klaviyo, Bloomreach, McKinsey)
- HubSpot trial limitations disclosed (Send Marketing Email locked behind Marketing Hub Pro)
- A/B testing methodology pre-registered, live execution deferred until consent-based pilot
- Attribution methodology validated against known ground truth in synthetic data
- AEO audit baseline = 0% expected for unlaunched fictional brand
- Industry benchmarks cited explicitly with source attribution

---

## Tech stack

**Strategy & writing:** Markdown, Git for versioned editorial workflow

**Data & ML:** Python 3.11 · pandas · scikit-learn · XGBoost · SHAP · PyMC 5.x · ArviZ

**AI integration:** Anthropic Claude API (claude-sonnet-4-6) for subject optimization and AEO audit

**Visualization:** Plotly (interactive) · matplotlib (PDF reports) · seaborn (notebooks)

**Web & deployment:** Streamlit · Streamlit Community Cloud · ReportLab (PDF generation)

**CRM:** HubSpot Free + Marketing Hub Trial · HubSpot Private App API

---

## Reproducing the project

```bash
git clone https://github.com/sebikradyel1-svg/coffra-marketing-automation.git
cd coffra-marketing-automation

python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
pip install pymc arviz   # For P5 MMM

# Run dashboard
streamlit run dashboard/streamlit_dashboard.py

# Run notebooks in order (via Jupyter or VSCode):
# P1: notebooks/01
# P3: notebooks/02 → 03 → 04 → 05
# P4: notebooks/06
# P5: notebooks/07 → 08 → 09 → 10
```

---

## Author

**Sebastian Kradyel** · Marketing Master's (9.54 GPA, Babeș-Bolyai University)
Reșița, Romania · LinkedIn: [in/sebastian-kradyel](https://www.linkedin.com/in/sebastian-kradyel)

Looking for: **AI Marketing Specialist** · **Marketing Automation Manager** · **Marketing Analytics** roles in Romania, Western Europe, or remote.

---

*This portfolio demonstrates production-grade marketing engineering. Every component is designed to be both technically rigorous and immediately useful in a real marketing operations context.*
