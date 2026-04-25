# Coffra Subject Line Optimizer

A Claude-powered tool that generates and scores email subject line variants
calibrated to specific buyer personas. Built as part of the Coffra P1 marketing
automation portfolio project.

## What It Does

Given an email brief and a target persona, the tool:

1. **Generates 5 distinct subject line variants** using 5 different strategic
   angles (direct, curiosity, insider, counter-intuitive, invitation).
2. **Scores each variant** on 4 dimensions (clarity, intrigue, brand fit,
   mobile readability), each 0-10, max total 40.
3. **Recommends a winner** with rationale grounded in persona constraints.
4. **Flags forbidden words** that violate brand voice guidelines.
5. **Caches responses** to reduce API cost during iteration.

## Personas Supported

- **The Connoisseur (Andrei)** — English, technical-mentor tone, signed by
  Sebastian (Roaster & Founder)
- **The Daily Ritualist (Bianca)** — Romanian, warm-conversational tone,
  signed by Ioana (Community Manager)

Both personas are defined in detail in `docs/02_persona_connoisseur.md` and
`docs/03_persona_daily_ritualist.md`.

## Architecture

```
src/
├── subject_optimizer/
│   ├── __init__.py
│   ├── config.py        # Persona definitions, brand voice rules
│   ├── prompts.py       # Templated prompts for Claude API
│   ├── generator.py     # Stage 1: generate 5 variants
│   ├── critic.py        # Stage 2: score and pick winner
│   └── cache.py         # JSON-based response cache
└── streamlit_app.py     # Web UI
```

The two-stage pipeline (generator + critic) reduces bias compared to a single
prompt that does both. Each stage uses its own prompt template, allowing
independent iteration.

## Setup

### 1. Install dependencies

```bash
cd coffra-marketing-automation

pip install anthropic streamlit python-dotenv
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and paste your real ANTHROPIC_API_KEY
```

Get your API key at: https://console.anthropic.com/settings/keys

### 3. Run the Streamlit app

```bash
streamlit run src/streamlit_app.py
```

The app opens at `http://localhost:8501`.

## Usage Example (Programmatic)

```python
from subject_optimizer.config import get_persona
from subject_optimizer.generator import generate_variants
from subject_optimizer.critic import score_variants, merge_generation_and_evaluation

persona = get_persona("connoisseur")
brief = "Welcome email for new subscriber. Free sample pack on first order over 150 RON."

# Stage 1
generation = generate_variants(email_brief=brief, persona=persona)

# Stage 2
evaluation = score_variants(
    email_brief=brief,
    persona=persona,
    variants=generation["variants"],
)

# Merge and inspect
result = merge_generation_and_evaluation(generation, evaluation)
print(f"Winner: {result['winner']['variant_text']}")
for v in result["variants"]:
    print(f"  {v['text']} — {v['total_score']}/40")
```

## Cost Estimate

Per call (one full generate+score cycle): approximately $0.005-0.015 USD,
depending on prompt length and variant complexity. Caching reduces this to zero
for identical inputs.

## Limitations of v1

- **Scores are qualitative**, not predicted open rates. A v2 could integrate
  industry benchmarks (Mailchimp 2025 Food & Beverage: 22.1% avg open rate)
  for quantitative prediction.
- **No A/B validation** of scoring accuracy against real campaign data —
  scoring quality is bounded by Claude's understanding of marketing copy.
- **Romanian quality** is good but not native-equivalent. A native Romanian
  reviewer should validate Daily Ritualist outputs before production use.

## License & Credits

Internal portfolio project. Author: Sebastian Kradyel.
