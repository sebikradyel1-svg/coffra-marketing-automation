# Coffra Marketing Automation

> **Full-funnel lead nurture and cart abandonment recovery for a fictional D2C specialty coffee brand.**
> A portfolio project demonstrating AI-augmented marketing automation: persona-driven email design, machine learning lead scoring, AI subject line optimization with Claude API, and HubSpot workflow implementation.

---

## Live Demo

**[coffra-marketing-dashboard.streamlit.app](https://coffra-marketing-dashboard.streamlit.app/)**

Interactive marketing operations dashboard built with Streamlit. Covers lead quality (XGBoost model), AI subject line generation, HubSpot CRM snapshot, simulated campaign funnels, and a methodology page with transparent data provenance.

---

## What's in this repo

This is **Project 1 (P1)** in a 6-project portfolio targeting AI Marketing Specialist and Marketing Automation roles. P1 takes a fictional specialty coffee brand (Coffra, Timișoara) from strategy to operational implementation, with every step documented and reproducible.

The brand is fictional — by design. This project deliberately avoids using real customer data or real brand identity, which would create privacy and legal risks. All content is original, all data is public (Kaggle), and all "brand" decisions are documented as fictional design choices.

---

## Quick navigation

### Strategy & content (10 documents)

| File | Purpose |
|---|---|
| [`docs/01_business_context.md`](docs/01_business_context.md) | Coffra brand foundation — products, pricing, channels, voice, competitors |
| [`docs/02_persona_connoisseur.md`](docs/02_persona_connoisseur.md) | Andrei (32, specialty coffee enthusiast) — full psychographic profile |
| [`docs/03_persona_daily_ritualist.md`](docs/03_persona_daily_ritualist.md) | Bianca (30, aspirational premium consumer) — RO journey persona |
| [`docs/04_email_copy_connoisseur.md`](docs/04_email_copy_connoisseur.md) | 5 nurture emails (EN), 14-day sequence with full copy decisions log |
| [`docs/05_email_copy_daily_ritualist.md`](docs/05_email_copy_daily_ritualist.md) | 5 nurture emails (RO), parallel 14-day sequence with native voice notes |
| [`docs/06_email_copy_cart_recovery.md`](docs/06_email_copy_cart_recovery.md) | 3 cart recovery emails (Connoisseur), 1h/24h/72h cadence, no-discount discipline |
| [`docs/07_hubspot_workflow_specs.md`](docs/07_hubspot_workflow_specs.md) | HubSpot implementation spec with screenshots and trial limitations |
| [`docs/08_ab_testing_methodology.md`](docs/08_ab_testing_methodology.md) | A/B test methodology with chi-square analysis and pre-registration |
| [`docs/09_segmentation_methodology.md`](docs/09_segmentation_methodology.md) | RFM + clustering methodology with all decisions justified |
| [`docs/10_segment_strategies.md`](docs/10_segment_strategies.md) | Coffra-specific deployment playbook for all 11 customer segments |

### Code & models

| Path | Purpose |
|---|---|
| [`notebooks/01_lead_scoring_eda_and_model.ipynb`](notebooks/01_lead_scoring_eda_and_model.ipynb) | P1: Lead scoring model — EDA, leakage audit, XGBoost vs Logistic baseline, SHAP |
| [`notebooks/02_rfm_eda.ipynb`](notebooks/02_rfm_eda.ipynb) | P3: EDA + data quality audit on Online Retail II dataset |
| [`notebooks/03_rfm_scoring_and_segments.ipynb`](notebooks/03_rfm_scoring_and_segments.ipynb) | P3: RFM scoring with 11-segment standard framework |
| [`notebooks/04_customer_clustering.ipynb`](notebooks/04_customer_clustering.ipynb) | P3: K-Means + Hierarchical clustering with PCA visualization |
| [`notebooks/05_segment_to_strategy.ipynb`](notebooks/05_segment_to_strategy.ipynb) | P3: Coffra strategy mapping + financial impact projection |
| [`src/subject_optimizer/`](src/subject_optimizer/) | AI Subject Line Optimizer Python package (Claude API + caching) |
| [`src/streamlit_app.py`](src/streamlit_app.py) | Streamlit UI for the Subject Line Optimizer |
| [`src/models/`](src/models/) | Saved model artifacts (joblib, JSON metrics, sample predictions) |
| [`dashboard/`](dashboard/) | Multi-page Streamlit marketing analytics dashboard (live: [coffra-marketing-dashboard.streamlit.app](https://coffra-marketing-dashboard.streamlit.app/)) |
| [`extract_hubspot_snapshot.py`](extract_hubspot_snapshot.py) | One-time HubSpot data extraction script using Private App API |
| [`generate_case_study.py`](generate_case_study.py) | ReportLab PDF generator for the P1 case study |
| [`generate_case_study_p2.py`](generate_case_study_p2.py) | ReportLab PDF generator for the P2 dashboard case study |
| [`generate_case_study_p3.py`](generate_case_study_p3.py) | ReportLab PDF generator for the P3 segmentation case study |

### Visual evidence

| Path | Contents |
|---|---|
| [`screenshots/hubspot/`](screenshots/hubspot/) | HubSpot implementation screenshots (workflows, emails, segments, contacts) and Subject Optimizer UI |

---

## Project highlights

### P1: Persona-driven marketing automation
- Two distinct personas with separate journeys (English for Connoisseur, Romanian for Daily Ritualist) — segmentation is structural, not cosmetic.
- Different sender identities (Sebastian as Roaster & Founder vs Ioana as Community Manager) provide rhetorical separation.
- Asymmetric incentive design: no-discount discipline for Connoisseur (value escalation only), aspirational positioning for Daily Ritualist.

### P1: AI-augmented tooling
- **Subject Line Optimizer** generates 5 variants and scores them on 4 dimensions using a two-stage Claude pipeline (generator + critic). SHA-256 cached for cost efficiency. Streamlit UI for demo.
- **Lead Scoring Model** (XGBoost) achieves Test ROC-AUC 0.78 on the Kaggle Predict Conversion in Digital Marketing dataset, with explicit data leakage audit (3 columns dropped before modeling) and SHAP global + local explanations.

### P2: Live marketing analytics dashboard
- Multi-page Streamlit application deployed to Streamlit Cloud (free tier with auto-rebuild on git push).
- Five operational pages: Lead Quality, Subject Optimizer cache analytics, HubSpot CRM snapshot, Campaign Funnel (simulated), Methodology disclosure.
- Snapshot-based data architecture for stable post-trial demo. HubSpot Private App API extraction script committed for reproducibility.

### P3: Customer segmentation with ML clustering
- **RFM analysis** on Online Retail II UCI dataset (1.07M transactions, 5,878 customers after data quality audit and cleaning).
- **11 standard rule-based segments** + **K-Means (k=4) + Hierarchical clustering** with multi-method validation (ARI = 0.613 indicates substantial agreement).
- **Strategic insight:** Probable Connoisseurs are 14.4% of customers but 61.8% of revenue — a 4.3x revenue concentration ratio that empirically validates P1's investment in Connoisseur sequence.
- **£240K projected annual uplift** (+23% over untargeted baseline), with clearly disclosed industry-anchored assumptions.
- Live integration into P2 dashboard as new Customer Segments page.

### Honest implementation transparency
- HubSpot trial limitations are disclosed: workflows visualize timing logic with delay actions because Send Marketing Email is locked behind Marketing Hub Pro. Production deployment path documented.
- A/B testing methodology is complete and pre-registered, but live execution is deferred until a consent-based pilot list of 100+ exists. No invented results.
- All financial projections in P3 are scenario-based and labelled as such, anchored to public benchmarks (Klaviyo, Bloomreach 2024).
- Industry benchmarks (Mailchimp 2025 Food & Beverage) cited explicitly with source attribution.

---

## Tech stack

**Strategy & writing:** Markdown, Git for versioned editorial workflow
**Data & ML:** Python 3.11, pandas, scikit-learn, XGBoost, SHAP, joblib
**AI tooling:** Anthropic Claude API (claude-sonnet-4-6), Streamlit
**Marketing automation:** HubSpot Marketing Hub (trial), Brevo (planned for production)
**Reproducibility:** Pinned `requirements.txt`, fixed `random_state=42`, JSON cache for API responses
**Documentation:** Markdown + ReportLab for PDF case study generation

---

## How to run

### Lead scoring notebook

```bash
git clone https://github.com/sebikradyel1-svg/coffra-marketing-automation.git
cd coffra-marketing-automation

python -m venv venv
venv\Scripts\activate  # Windows; use source venv/bin/activate on macOS/Linux

pip install -r requirements.txt

jupyter lab
# Open notebooks/01_lead_scoring_eda_and_model.ipynb
# Run All Cells
```

Required: `data/raw/digital_marketing_campaign_dataset.csv` from [Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/predict-conversion-in-digital-marketing-dataset). Not committed to repo (5MB, reproducible from link).

### Subject Line Optimizer

```bash
# After activating venv
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY (get one at https://console.anthropic.com)

streamlit run src/streamlit_app.py
# App opens at http://localhost:8501
```

### Marketing Dashboard

```bash
# Requires snapshots in data/snapshots/ (run extract_hubspot_snapshot.py first if needed)
streamlit run dashboard/streamlit_dashboard.py
# Or view live: https://coffra-marketing-dashboard.streamlit.app/
```

---

## Project status

**P1 v1.0 — complete.** All design and implementation artifacts shipped. Live A/B testing deferred to v1.1.
**P2 v1.0 — complete.** Live dashboard deployed.
**P3 v1.0 — complete.** RFM + ML clustering + Coffra strategy playbook with dashboard integration.

| Component | Status |
|---|---|
| **P1 — Marketing Automation** | |
| Strategy & personas | Complete |
| 13 emails (10 nurture + 3 cart recovery) | Complete |
| Lead scoring model | Complete |
| AI Subject Line Optimizer | Complete |
| HubSpot implementation (visual) | Complete |
| A/B testing methodology | Complete |
| Case study PDF | Complete |
| **P2 — Marketing Dashboard** | |
| **Marketing dashboard (live)** | **[coffra-marketing-dashboard.streamlit.app](https://coffra-marketing-dashboard.streamlit.app/)** |
| Case study PDF | Complete |
| **P3 — Customer Segmentation** | |
| EDA + data quality (Online Retail II, 1.07M rows) | Complete |
| RFM scoring + 11-segment framework | Complete |
| K-Means + Hierarchical clustering (k=4, ARI=0.61) | Complete |
| Coffra strategy playbook + financial projection | Complete |
| Customer Segments dashboard page | Complete |
| Case study PDF | Complete |
| Live A/B testing | Deferred to v1.1 |

---

## What this project demonstrates

For an AI Marketing Specialist or Marketing Automation role, this project shows:

- **Strategic thinking:** persona segmentation is built on observed consumer psychology, not generic frameworks. Asymmetric incentive design reflects real understanding of buyer behavior.
- **Copy craft:** voice consistency across 13 emails, with documented copy decisions and trade-offs. Romanian and English written natively, not translated.
- **Marketing technology fluency:** HubSpot configured end-to-end (brand, segments, properties, workflows, emails). Trial limitations acknowledged and worked around.
- **AI integration:** Claude API used programmatically (not just conversationally) to build a real production tool. Two-stage pipeline reduces bias, caching reduces cost.
- **ML rigor:** Production-grade lead scoring with leakage audit, baseline comparison, cross-validation, SHAP explainability, and saved artifacts ready for deployment.
- **Statistical literacy:** A/B testing methodology designed correctly (chi-square, effect size, pre-registration, decision rules) — even though live test deferred.
- **Honest documentation:** known limitations are disclosed throughout, no invented metrics, no overstated claims.

---

## About the author

**Sebastian Kradyel** — Marketing Master's graduate (9.54 GPA, Babeș-Bolyai University) transitioning into AI/ML engineering and marketing automation. Based in Reșița, Romania. Active in Erasmus+ project coordination through ATOR Banatul de Munte.

[**LinkedIn**](https://www.linkedin.com/in/) (see GitHub profile for direct link) · [**GitHub**](https://github.com/sebikradyel1-svg)

---

## License & disclaimer

This is a portfolio project. Coffra is a fictional brand created for demonstration; no real Coffra business exists. All persona names (Andrei, Bianca) are fictional archetypes, not real individuals. Data used for the lead scoring model is from a public Kaggle dataset and does not contain real Coffra customer information. Industry benchmarks are cited from Mailchimp's 2025 published report.

Code in this repository is available for reference and learning. Email copy, persona profiles, and strategic frameworks are original work; please credit if reused.
