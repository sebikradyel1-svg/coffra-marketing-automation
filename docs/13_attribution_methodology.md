# Attribution Modeling Methodology

**Project:** P5 · Coffra Attribution Modeling
**Author:** Sebastian Kradyel
**Date:** April 2026
**Document:** docs/13_attribution_methodology.md

---

## 1. The Business Question

Coffra invests in multiple marketing channels: paid search (Google Ads), paid social (Meta Ads, Instagram), email automation (HubSpot), organic search (SEO + AEO), referrals, and direct traffic. **Which channels actually drive conversions?** Beyond that: which channel deserves the next marketing dollar?

Naive measurement attributes the conversion to the **last touchpoint** ("last-click attribution"). This systematically underestimates upper-funnel channels (display ads, organic search, content marketing) and overestimates lower-funnel channels (branded search, retargeting). The CMO who reallocates budget based on last-click data ends up cutting the channels that actually drive growth.

Attribution modeling solves this. Two complementary disciplines exist:

- **Multi-Touch Attribution (MTA):** Granular, individual-level. Tracks each customer's touchpoints and distributes conversion credit across them.
- **Marketing Mix Modeling (MMM):** Aggregate, channel-level. Uses time-series regression on spend and conversions to estimate channel contribution.

This document specifies the methodology for both, applied to a Coffra-style synthetic dataset.

---

## 2. Why Both Approaches

The naive answer is "use both — they're complementary." The honest answer is more nuanced. Each method has strengths and structural failures:

| Dimension | MTA | MMM |
|---|---|---|
| **Granularity** | Individual customer journey | Aggregate weekly/daily spend |
| **Data requirement** | UTM tracking, cookies, click logs | Channel spend + conversions over time |
| **Privacy compliance** | Increasingly hard (cookie deprecation, GDPR) | Privacy-safe (no individual data) |
| **Cross-channel reach** | Limited to digitally-trackable channels | Includes TV, OOH, podcast, etc. |
| **Captures incrementality** | Heuristic-based, often poor | Designed to estimate causal effect |
| **Time to first result** | Days | 2-3 months of historical data |
| **Assumption rigor** | Path-dependent, often violated | Time-series, also violated |

**Key insight:** MTA tells you *how customers got here*. MMM tells you *what would have happened if we hadn't spent on a channel*. These are different questions. A senior analyst applies both.

---

## 3. Multi-Touch Attribution (MTA) — Methods

Five methods will be implemented, ordered from naive to sophisticated:

### 3.1 Last-Click Attribution (baseline)
100% credit to the final touchpoint before conversion.

**Use case:** Industry baseline. Required to show how naive attribution misallocates credit.

**Math:** `credit(channel_i) = 1 if i is final touchpoint else 0`

### 3.2 First-Click Attribution
100% credit to the first touchpoint in the journey.

**Use case:** Mirror of last-click. Useful for understanding upper-funnel channels.

### 3.3 Linear Attribution
Equal credit to all touchpoints in the path.

**Use case:** Simple, interpretable. No channel privileged.

**Math:** `credit(channel_i) = 1/n` where n = touchpoints in path.

### 3.4 Time-Decay Attribution
More credit to touchpoints closer to conversion.

**Use case:** Reflects intuition that recent interactions matter more.

**Math:** `credit(channel_i) = exp(-lambda * t_i) / sum(exp(-lambda * t_j))` where t_i is days from conversion.

### 3.5 Markov Chain Attribution (probabilistic)
Models the customer journey as a Markov chain. Channel contribution is measured as the **removal effect**: how much would the conversion rate drop if this channel were removed?

**Use case:** Captures non-linear interactions between channels. The current state of the art for digital MTA.

**Math:** 
1. Build transition matrix between channels (and to conversion/dropout states)
2. Compute baseline conversion probability
3. For each channel, compute conversion probability with that channel removed
4. Removal effect = (baseline - removed) / baseline
5. Normalize to sum to 1 across channels

### 3.6 Shapley Value Attribution (game-theoretic)
Borrowed from cooperative game theory. Distributes credit fairly based on each channel's marginal contribution across all possible coalitions.

**Use case:** Mathematically optimal fairness. Computationally expensive (2^n combinations).

**Math:**
For channel i: `Shapley(i) = sum over all coalitions S not containing i of: (|S|! * (n-|S|-1)! / n!) * (v(S∪{i}) - v(S))`

Where v(S) = conversion rate when only channels in S are active.

For practical computation with 5+ channels, we use Monte Carlo sampling rather than full enumeration.

---

## 4. Marketing Mix Modeling (MMM) — Bayesian Approach

MMM uses time-series regression to estimate channel contribution to a target outcome (conversions, revenue). Modern MMM (Meta's Robyn, Google's LightweightMMM, Uber's Orbit) uses Bayesian methods for robustness.

### 4.1 Model specification

`y_t = baseline + sum_c [beta_c * Adstock(saturation(spend_c,t))] + seasonality_t + epsilon_t`

Where:
- `y_t` = daily/weekly conversions or revenue
- `baseline` = base conversions without any marketing
- `c` = channel index
- `Adstock(x)` = carryover transformation (advertising effect persists across days)
- `saturation(x)` = diminishing returns transformation (Hill or Michaelis-Menten)
- `beta_c` = channel-specific coefficient (priors in Bayesian framework)
- `seasonality_t` = seasonal/trend components

### 4.2 Adstock transformation

Advertising on day 0 generates effect on day 0 + smaller effects on days 1, 2, 3...

`Adstock(x_t) = x_t + alpha * Adstock(x_{t-1})`

Where `alpha` ∈ [0, 1] is the decay rate. We treat `alpha` as a learnable parameter with a Beta prior.

### 4.3 Saturation transformation

Doubling spend doesn't double effect. Hill saturation:

`saturation(x) = x^k / (x^k + S^k)`

Where `S` is the half-saturation point and `k` controls steepness. Both are learnable with informative priors.

### 4.4 Bayesian advantages

- **Uncertainty quantification:** We get posterior distributions over channel contributions, not point estimates.
- **Prior incorporation:** Industry knowledge (e.g., "search typically saturates faster than social") encoded as priors.
- **Regularization:** Priors prevent overfitting on small datasets (typical MMM has 100-200 weekly observations).

### 4.5 Implementation choice

We use **PyMC** for the Bayesian MMM. It is the standard Python framework for Bayesian inference. Alternative: lightweight_mmm (JAX-based) is faster but less flexible. PyMC chosen for portfolio because the model specification is more transparent and educational.

---

## 5. Synthetic Data Design

Coffra has no real conversion data. We generate a realistic dataset with **known ground truth** so the models can be validated against the data-generating process.

### 5.1 MTA dataset

- **N customers:** 50,000
- **Time range:** 90 days
- **Channels:** 5 (Google Ads, Meta Ads, Instagram organic, Email, Direct)
- **Touchpoint distribution:** Average 3 touchpoints per converter, 1-2 per non-converter
- **Channel-specific behaviors:**
  - Direct: high probability of being the only touchpoint (existing customers)
  - Email: high probability of being the final touchpoint (closer behavior)
  - Google Ads: high probability of being early-to-mid funnel
  - Meta Ads: appears across funnel stages
  - Instagram organic: skews early funnel (discovery)
- **Ground truth conversion influence per channel:** Stored in metadata; models compared against it.

### 5.2 MMM dataset

- **Time range:** 104 weeks (2 years)
- **Granularity:** Daily
- **Channels:** Same 5 as MTA
- **Spend patterns:** Realistic — higher in Q4 (holiday), lower in Q3 (summer slump), gradual growth over 2 years
- **Adstock parameters:** Each channel has known true alpha (decay rate)
- **Saturation parameters:** Each channel has known true half-saturation point
- **Baseline:** ~30% of conversions are organic baseline
- **Seasonality:** Sinusoidal annual + day-of-week patterns
- **Noise:** Gaussian noise on top of structural model

### 5.3 Why synthetic, not Kaggle

- **Criteo Attribution Dataset** (Kaggle): Real, but anonymized to the point where channel semantics are obscure. Hard to interpret in business terms.
- **Synthetic with ground truth:** Validates that our models work correctly. We can directly compare estimated channel contribution vs. true contribution.
- **Reproducibility:** Anyone clones the repo, runs `data_generation.ipynb`, gets same dataset (fixed seed).

---

## 6. Validation Framework

A model that says "Google Ads contributes 25% of conversions" is useless if you can't trust it. Validation:

### 6.1 MTA validation

- **Coherence checks:** Do all attribution methods sum to 100% of conversions?
- **Baseline comparison:** Are Markov / Shapley results different from naive (last-click)? If yes, by how much?
- **Convergence:** Does Monte Carlo Shapley converge as we increase samples?
- **Sensitivity:** How do results change if we vary the time-decay lambda parameter?

### 6.2 MMM validation

- **Posterior predictive check:** Generate samples from the fitted model, compare to actual data
- **Cross-validation:** Hold out final 4 weeks, refit, check forecast accuracy
- **Recovery test:** Compare estimated channel contributions to known ground truth in synthetic data
- **Convergence diagnostics:** R-hat statistic, effective sample size for each parameter

### 6.3 Cross-method validation

The most informative check: do MTA and MMM agree on channel ranking?

If MTA says "Email is top channel" and MMM says "Google Ads is top," **investigate**. Possible reasons:
- MTA's last-click bias is showing
- MMM is missing a non-modeled channel
- One method is poorly calibrated

A senior analyst expects ~70-80% agreement on channel ranking, with disagreements concentrated in mid-tier channels.

---

## 7. Business Output

The model output that matters to the marketing team:

### 7.1 Channel contribution table
For each channel: 
- Estimated contribution to conversions (mean + uncertainty interval)
- Cost per acquisition (CPA) attributable to that channel
- Marginal ROI: how much additional spend would produce additional conversions

### 7.2 Budget reallocation recommendation
Given current channel mix vs. optimal:
- Which channels should get more budget?
- Which should get less?
- What's the expected lift from reallocation?

### 7.3 Channel-specific insights
- Adstock decay rate (how long does this channel's effect persist?)
- Saturation point (when does additional spend stop helping?)
- Synergy with other channels

---

## 8. Honest Limitations

### 8.1 Synthetic data caveat
All conclusions in this project are about the synthetic dataset. They demonstrate methodology, not Coffra's actual channel performance. Real Coffra deployment would require:
- Live UTM tracking + conversion tracking (months of data)
- Real ad spend records by channel
- A/B holdout tests for incrementality validation

### 8.2 MTA limitations
- Cookie deprecation (Chrome 2024+) breaks cross-site MTA
- Privacy regulations (GDPR, CCPA) further restrict tracking
- Mobile/cross-device journey reconstruction is brittle
- Walled gardens (Meta, Google) provide aggregated data only

### 8.3 MMM limitations
- Assumes data-generating process matches model specification
- Sensitive to feature engineering (which seasonal terms to include?)
- Cannot identify channels with stable spend (no variance to learn from)
- Requires ~100+ weeks of data for stable estimates

### 8.4 What this analysis does NOT do
- Does not provide actual Coffra channel performance (no real data exists)
- Does not provide individual-customer LTV (different problem, not addressed here)
- Does not optimize creative/targeting within channel (out of scope)
- Does not provide statistical guarantees of incrementality (would require holdout testing)

---

## 9. Implementation Stack

| Layer | Tool | Rationale |
|---|---|---|
| Data generation | NumPy + Pandas | Reproducible synthetic data |
| MTA — heuristics | Pandas | Last-click, first-click, linear, time-decay |
| MTA — Markov | NumPy + ChannelAttribution-style | Custom implementation for transparency |
| MTA — Shapley | itertools + Monte Carlo | Game theory implementation |
| MMM | PyMC 5.x | Bayesian inference, posterior sampling |
| Visualization | Plotly | Interactive, dashboard-compatible |
| Dashboard | Streamlit | Existing portfolio infrastructure |

---

## 10. Project Structure

```
P5 Attribution Modeling/
├── notebooks/
│   ├── 07_data_generation.ipynb         # Synthetic data with ground truth
│   ├── 08_multi_touch_attribution.ipynb # 5 MTA methods + comparison
│   ├── 09_marketing_mix_model.ipynb     # PyMC Bayesian MMM
│   └── 10_attribution_comparison.ipynb  # Cross-method, business insights
├── docs/
│   └── 13_attribution_methodology.md    # This document
├── dashboard/pages/
│   └── 8_Attribution.py                 # Live dashboard page
└── case_study/
    └── P5_Coffra_Attribution_Case_Study.pdf
```

---

## 11. Coffra Application

Once Coffra has 6+ months of real channel data, the methodology adapts as follows:

### Phase 1 (Months 1-2): MTA pilot
- Implement UTM tracking on all channels via HubSpot + Google Analytics 4
- After 60 days of data, run MTA notebook on real data
- Compare last-click (current default) vs. Markov chain (proposed)
- Estimated reallocation impact: 10-15% lift in conversions per dollar (industry benchmark)

### Phase 2 (Months 3-6): MMM foundation
- Continue collecting daily channel spend + conversions
- After 6 months, refit MMM on real data
- Use uncertainty intervals to communicate confidence
- Triangulate with MTA findings — investigate disagreements

### Phase 3 (Months 6+): Continuous optimization
- Monthly model refits
- A/B holdout tests on top channels for incrementality validation
- Budget reallocation reviews quarterly
- Annual full methodology review

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 27, 2026** | Initial methodology document. MTA (5 methods) + MMM (Bayesian PyMC) framework, synthetic data design, validation approach, Coffra rollout plan. |
