# Coffra Marketing Automation

> **Full-funnel lead nurture and cart abandonment recovery for a fictional D2C specialty coffee brand.**
> A portfolio project demonstrating AI-augmented marketing automation: persona-driven email design, machine learning lead scoring, AI subject line optimization with Claude API, and HubSpot workflow implementation.

---

## What's in this repo

This is **Project 1 (P1)** in a 6-project portfolio targeting AI Marketing Specialist and Marketing Automation roles. P1 takes a fictional specialty coffee brand (Coffra, Timișoara) from strategy to operational implementation, with every step documented and reproducible.

The brand is fictional — by design. This project deliberately avoids using real customer data or real brand identity, which would create privacy and legal risks. All content is original, all data is public (Kaggle), and all "brand" decisions are documented as fictional design choices.

---

## Quick navigation

### Strategy & content (8 documents)

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

### Code & models

| Path | Purpose |
|---|---|
| [`notebooks/01_lead_scoring_eda_and_model.ipynb`](notebooks/01_lead_scoring_eda_and_model.ipynb) | Lead scoring model: EDA, leakage audit, XGBoost vs Logistic Regression baseline, SHAP explainability |
| [`src/subject_optimizer/`](src/subject_optimizer/) | AI Subject Line Optimizer Python package (Claude API + caching) |
| [`src/streamlit_app.py`](src/streamlit_app.py) | Streamlit UI for the Subject Line Optimizer |
| [`src/models/`](src/models/) | Saved model artifacts (joblib, JSON metrics, sample predictions) |

### Visual evidence

| Path | Contents |
|---|---|
| [`screenshots/hubspot/`](screenshots/hubspot/) | HubSpot implementation screenshots (workflows, emails, segments, contacts) and Subject Optimizer UI |

---

## Project highlights

### Persona-driven, multi-language design
- Two distinct personas with separate journeys (English for Connoisseur, Romanian for Daily Ritualist) — segmentation is structural, not cosmetic.
- Different sender identities (Sebastian as Roaster & Founder vs Ioana as Community Manager) provide rhetorical separation.
- Asymmetric incentive design: no-discount discipline for Connoisseur (value escalation only), aspirational positioning for Daily Ritualist.

### AI-augmented tooling
- **Subject Line Optimizer** generates 5 variants and scores them on 4 dimensions using a two-stage Claude pipeline (generator + critic). SHA-256 cached for cost efficiency. Streamlit UI for demo.
- **Lead Scoring Model** (XGBoost) achieves Test ROC-AUC 0.78 on the Kaggle Predict Conversion in Digital Marketing dataset, with explicit data leakage audit (3 columns dropped before modeling) and SHAP global + local explanations.

### Honest implementation transparency
- HubSpot trial limitations are disclosed: workflows visualize timing logic with delay actions because Send Marketing Email is locked behind Marketing Hub Pro. Production deployment path documented.
- A/B testing methodology is complete and pre-registered, but live execution is deferred until a consent-based pilot list of 100+ exists. No invented results.
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

---

## Project status

**P1 v1.0 — complete.** All design and implementation artifacts shipped. Live A/B testing deferred to v1.1.

| Component | Status |
|---|---|
| Strategy & personas | Complete |
| 13 emails (10 nurture + 3 cart recovery) | Complete |
| Lead scoring model | Complete |
| AI Subject Line Optimizer | Complete |
| HubSpot implementation (visual) | Complete |
| A/B testing methodology | Complete |
| Live A/B testing | Deferred to v1.1 |
| Case study PDF | In progress |

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

[**LinkedIn**](https://www.linkedin.com/in/paul-sebastian-kradyel/) · [**GitHub**](https://github.com/sebikradyel1-svg)

---

## License & disclaimer

This is a portfolio project. Coffra is a fictional brand created for demonstration; no real Coffra business exists. All persona names (Andrei, Bianca) are fictional archetypes, not real individuals. Data used for the lead scoring model is from a public Kaggle dataset and does not contain real Coffra customer information. Industry benchmarks are cited from Mailchimp's 2025 published report.

Code in this repository is available for reference and learning. Email copy, persona profiles, and strategic frameworks are original work; please credit if reused.
