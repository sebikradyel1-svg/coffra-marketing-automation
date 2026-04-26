# A/B Testing Methodology — Subject Line Optimization

**Project:** P1 · Coffra Marketing Automation
**Author:** Sebastian Kradyel
**Date:** April 2026
**Status:** Methodology specification (live testing deferred to v1.1)

---

## 1. Purpose & Honest Disclosure

This document specifies the A/B testing methodology that would validate the AI Subject Line Optimizer's recommendations against real subscriber behavior. The methodology is fully designed and reproducible. **Live testing was not executed** in v1.0 of P1 due to the absence of a consent-based pilot list of sufficient size (target: 100+ testers). This document exists to demonstrate testing rigor at the planning stage and to provide a deployment-ready protocol for future execution.

A note on integrity: this document does **not** report invented results. The "Expected Results" section presents plausible directional expectations grounded in published industry benchmarks, clearly labeled as predictions, not measurements.

---

## 2. Test Hypothesis

### Primary hypothesis (H1)

> A Subject Line Optimizer–recommended winning variant produces a higher open rate than a manually-crafted baseline subject line, when sent to the same persona-segmented audience.

### Null hypothesis (H0)

> There is no significant difference in open rate between the AI-recommended winning variant and the baseline subject line.

### Why this hypothesis matters

If H1 is supported, the AI Subject Line Optimizer is justified as a marketing automation investment. If H0 cannot be rejected, the tool needs refinement (better prompts, persona constraints, scoring dimensions) before production deployment.

---

## 3. Test Design

### Test type
Two-arm randomized controlled test with subject line as the only manipulated variable. Email body, sender, send time, and audience segment are held constant.

### Variants

**Variant A (Control — manually crafted baseline):**
> "Welcome to Coffra — your first order has a free sample inside"

This represents a reasonable but generic baseline that a junior marketer might write without persona-specific tooling.

**Variant B (Treatment — AI-optimized):**
> "Ethiopia Gelana just landed. You're in."

This is the winner from the Subject Line Optimizer when run against the Connoisseur persona with the welcome email brief (see `src/subject_optimizer/`). It scored 36/40 across the four evaluation dimensions.

### Sample size

**Target:** 200 contacts in the Connoisseur Subscribers segment.
**Allocation:** 100 in Variant A, 100 in Variant B (50/50 random split).

**Rationale for n=200:** With expected open rates around 22% (industry baseline for Food & Beverage per Mailchimp 2025), a sample of 100 per arm provides ~80% power to detect a 10 percentage-point difference at α=0.05. This is the smallest practical sample for directional confidence.

### Why not larger?

A sample of 1,000+ per arm would provide higher power and detect smaller effects. For Coffra (a fictional brand without a real subscriber list), this is hypothetical — a real deployment would scale based on list size. Documented here as the next step for v1.1.

### Randomization

Stratified random assignment within the Connoisseur Subscribers segment:
1. Pull all contacts where `Persona = Connoisseur`.
2. Sort by contact creation date (newest to oldest) to balance recency.
3. Assign odd-indexed contacts to Variant A, even-indexed to Variant B.

This pseudo-random assignment by index is acceptable for sample sizes under 500. For larger samples, a true randomization tool (Python `random.shuffle()` with fixed seed) is recommended.

---

## 4. Measurement

### Primary metric
**Open rate** — defined as `(unique opens / delivered) × 100`.

Unique opens are tracked via the email platform's tracking pixel (1×1 transparent image). HubSpot, Brevo, and Mailchimp all support this natively.

### Secondary metrics (informational, not for decision)
- Click-through rate (CTR) — clicks on CTA / opens
- Bounce rate — undeliverable / total sent
- Unsubscribe rate — unsubscribes / delivered

### Measurement window
- **Open rate measurement:** 48 hours from send time. Industry data shows >90% of opens occur within 48h.
- **CTR measurement:** 7 days from send time (clicks can lag opens significantly).
- **Unsubscribe measurement:** 7 days from send time.

### Quality controls
- Exclude tester accounts (Sebastian's own emails) from analysis.
- Exclude bounced emails from the denominator.
- Flag any single contact opening more than 5 times (indicates email client preview, not real interest).

---

## 5. Statistical Analysis

### Method: Chi-square test of independence (2×2 contingency table)

For two groups (A, B) and two outcomes (opened, not opened), the chi-square test determines whether the observed difference in open rates is statistically significant.

**Contingency table format:**

| | Opened | Not opened | Total |
|---|---|---|---|
| Variant A | a | b | a+b |
| Variant B | c | d | c+d |
| **Total** | a+c | b+d | n |

### Significance threshold
- α = 0.05 (95% confidence)
- Two-tailed test
- Reject H0 if p-value < 0.05

### Why chi-square (not t-test)

Open rate is a binary outcome at the individual level (each contact either opens or doesn't). Chi-square is the appropriate test for proportion comparison. A two-sample t-test on raw counts would be incorrect.

### Effect size

In addition to the p-value, report **Cramér's V** as effect size. For a 2×2 table, this is equivalent to the phi coefficient:

`φ = sqrt(χ² / n)`

Effect size interpretation:
- φ < 0.10: negligible
- 0.10 ≤ φ < 0.30: small
- 0.30 ≤ φ < 0.50: medium
- φ ≥ 0.50: large

### Computational tool

Run analysis in Python using `scipy.stats.chi2_contingency`:

```python
from scipy.stats import chi2_contingency

# Example contingency table
observed = [[opens_A, not_opens_A], [opens_B, not_opens_B]]
chi2, p_value, dof, expected = chi2_contingency(observed)

# Effect size
import numpy as np
n = sum(sum(row) for row in observed)
phi = np.sqrt(chi2 / n)

print(f"Chi-square: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")
print(f"Effect size (φ): {phi:.4f}")
```

---

## 6. Decision Rules

| Outcome | Decision |
|---|---|
| p < 0.05 AND φ ≥ 0.10 AND Variant B > Variant A | Adopt Variant B (Optimizer-recommended). Document AI uplift in case study. |
| p < 0.05 AND φ ≥ 0.10 AND Variant A > Variant B | Investigate Optimizer's scoring logic. Possible prompt tuning or persona refinement needed. |
| p < 0.05 AND φ < 0.10 | Reject H0 but practical effect is negligible. No action required. |
| p ≥ 0.05 | Cannot reject H0. Increase sample size for v1.1 retest, or accept that variants are equivalent at current sample. |

---

## 7. Expected Results (Predictions, Not Measurements)

These are **predictions** based on industry benchmarks, used to size expectations and validate test setup. They are not invented results.

### Industry baseline reference

Source: Mailchimp 2025 Email Marketing Benchmarks (Food & Beverage segment)
- Average open rate: 22.1%
- Average CTR: 2.3%
- Specialty/premium brands tend to outperform average by ~15% (factor 1.15)

### Predicted ranges

| Metric | Variant A (baseline) | Variant B (AI-optimized) |
|---|---|---|
| Open rate (predicted) | 18-22% | 24-30% |
| CTR (predicted) | 1.5-2.5% | 2.0-3.5% |
| Effect size (φ) | — | 0.10-0.20 (small to small-medium) |

The predicted open rate uplift for Variant B (4-8 percentage points) reflects the type of improvement seen when subject lines are personalized to persona-specific tone. **These are predictions for sizing purposes only.** Actual results would depend on list quality, send time, sender reputation, and many other factors.

---

## 8. Pre-Registration & Transparency

To prevent post-hoc cherry-picking of metrics, this section serves as a pre-registration of the analysis plan.

| Pre-registered choice | Specified value |
|---|---|
| Primary metric | Open rate |
| Sample size | 200 contacts |
| Significance threshold | α = 0.05 |
| Statistical test | Chi-square test of independence |
| Effect size measure | Cramér's V (φ for 2×2) |
| Measurement window | 48h for opens |
| Multiple comparisons correction | Not applicable (single primary test) |
| Subgroup analyses planned | None for v1.0 |
| Stopping rule | Pre-specified sample size; no early stopping |

**Deviations from this plan, if any, will be reported transparently in the results section of the case study.**

---

## 9. Implementation Checklist (for future live test)

When this test is executed live, the following steps must be completed in order:

1. [ ] Confirm sender domain authentication (SPF, DKIM, DMARC) on production sender
2. [ ] Build Variant A and Variant B in the email platform with identical body, footer, CTAs
3. [ ] Verify list quality: remove bounced/inactive contacts from prior 90 days
4. [ ] Define exclusion list (testers, internal accounts)
5. [ ] Schedule send for Tuesday-Thursday between 10:00-11:00 local time (highest engagement window per industry data)
6. [ ] Confirm tracking pixels and link wrapping are enabled
7. [ ] Send batch
8. [ ] Wait 48 hours
9. [ ] Export raw data: `contact_id, variant, opened (bool), clicked (bool)`
10. [ ] Run chi-square analysis in Python
11. [ ] Document results in case study with full disclosure of effect size, p-value, and limitations

---

## 10. Limitations

This methodology has known limitations that should be disclosed in any case study writeup:

- **Sample size is suggestive, not confirmatory.** A 200-person test is underpowered to detect effects smaller than 5 percentage points reliably.
- **Single-shot test.** Subject line performance varies by send time, day of week, news cycles, and inbox saturation. A single send cannot account for these confounders.
- **No control for prior engagement.** Subscribers who previously opened multiple Coffra emails are more likely to open again regardless of subject. A more rigorous design would stratify by engagement history.
- **Open rate is partially gamed by Apple Mail Privacy Protection (MPP).** Apple's privacy feature pre-fetches images, inflating reported opens. Industry estimates suggest 30-40% of reported opens may be MPP-driven, especially on mobile. Real opens are likely lower than reported.
- **Persona is the only segmentation criterion.** A live test would benefit from controlling for tenure on list, geographic region, and prior purchase history.

---

## 11. Future Work

For v1.1 of P1 or for P3 (Marketing Analytics Dashboard), the following extensions would strengthen this methodology:

- **Bayesian A/B test:** Adopt Beta-Binomial conjugate analysis to allow continuous monitoring without inflating false-positive rate.
- **Multi-armed bandit:** Replace fixed-arm A/B test with Thompson sampling for dynamic allocation toward better-performing variant during the test.
- **Holdout group:** Reserve 10% of audience as no-send control to measure absolute campaign impact, not just relative variant performance.
- **Persona stratification:** Run separate A/B tests for Connoisseur vs Daily Ritualist to detect persona-specific subject line effects.
- **Time-of-day testing:** Add send-time as a second factor (2×2 factorial design).

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 26, 2026** | Initial methodology document. Specifies hypothesis, design, sample size rationale, statistical method, decision rules, and limitations. Live testing deferred to v1.1 pending consent-based pilot list. |
