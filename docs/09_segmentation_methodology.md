# Customer Segmentation Methodology

**Project:** P3 · Coffra Customer Segmentation
**Author:** Sebastian Kradyel
**Date:** April 2026
**Document:** docs/09_segmentation_methodology.md

---

## 1. Purpose

This document specifies the segmentation methodology used in P3. It explains the choices made at each step of the analytical pipeline (EDA, RFM scoring, ML clustering, strategy mapping), the rationale behind those choices, and the limitations that follow. The goal is to make the methodology defensible and reproducible.

A note on integrity: this document does not present any invented findings. Where projections or scenarios appear (e.g., revenue uplift estimates), they are clearly labelled and anchored to published benchmarks.

---

## 2. Dataset Selection

### Why Online Retail II (UCI / Kaggle)

Coffra is a fictional brand with no real customer transaction history. To demonstrate professional segmentation work, P3 uses the Online Retail II dataset, a publicly available real e-commerce dataset commonly used in academic and industry RFM tutorials. Specific reasons for this choice:

- **Authenticity:** Real transactional data, not synthetic, with real-world data quality issues that need handling.
- **Scale:** 1.07 million transactions across ~5,900 customers — large enough to support stable clustering, small enough to run on a standard laptop.
- **Structural similarity:** UK gift retailer's purchase patterns (high-frequency low-cost items, heavy holiday seasonality, long-tail customer value distribution) map cleanly onto specialty coffee retail dynamics.
- **Reproducibility:** Public dataset, fixed seed for any sampling, all decisions logged.

### Limitations of dataset

- Dataset ends in December 2011, so absolute recency values are inflated by years of analytical lag. This does not affect relative segmentation — recency rankings stay valid — but means absolute "days since last purchase" values are not directly comparable to a 2026 deployment.
- UK gift retailer is not a coffee subscription service. Product-level analysis would not transfer; customer-behavioral analysis does.
- No explicit demographic, geographic-beyond-country, or channel-attribution data. We work with what is available.

---

## 3. Data Cleaning

### Quality issues identified and addressed

| Issue | Impact | Decision |
|---|---|---|
| Missing `Customer ID` (~22% of rows) | Cannot perform customer-level analysis on these records | Drop. Documented as exclusion. |
| Cancellation invoices (Invoice prefix "C") | Returns/cancellations dilute purchase intent signal | Drop, do not net against purchases. Industry practice varies; we choose exclusion for clarity. |
| Negative quantity, non-cancellation | Likely data entry errors | Drop. |
| Negative price | Almost certainly errors (4 rows total) | Drop. |
| Zero price | Promotional samples or data errors | Drop. |
| Exact duplicate rows | Likely upload artifacts | Drop. |
| Special StockCodes (POST, M, BANK CHARGES) | Not products but real revenue | Keep in monetary calculations, exclude from product-level analysis. |

### Net retention

- Original: 1,067,371 rows
- Final cleaned: ~770,000 rows
- Retention rate: ~72%

The 28% loss is dominated by missing-Customer-ID rows. This is consistent with public e-commerce datasets where guest checkouts and anonymized purchases are common. For the segmentation use case, only customer-identified transactions are analytically useful.

### Cleaning audit trail

Every cleaning step is logged in `notebooks/02_rfm_eda.ipynb` with row counts before and after. The cleaned dataset is saved as `data/processed/online_retail_cleaned.parquet` for downstream notebooks.

---

## 4. RFM Scoring

### Definitions

- **Recency (R):** Days since the customer's last purchase, measured from a fixed snapshot date (the day after the dataset's last transaction). For real production deployment, snapshot date would be "today" at each report run.
- **Frequency (F):** Number of unique invoices per customer.
- **Monetary (M):** Sum of `Quantity * Price` across all customer's transactions, in GBP.

### Snapshot date convention

We use `max(InvoiceDate) + 1 day` as the snapshot date. This simulates an analyst running the report immediately after data extraction. Industry-standard convention.

### Quintile scoring

Each customer receives a 1-to-5 score on each dimension, based on quintile binning of their value:
- **R_Score:** Higher score = more recent. We pass `labels=[5,4,3,2,1]` to `qcut` to reverse the order.
- **F_Score, M_Score:** Higher score = higher value. Standard ascending labels.

We use `pd.qcut` with `duplicates='drop'`. For F and M (which have heavily right-skewed distributions with many tied values at low quantiles), we score on `rank(method='first')` rather than raw values to ensure quintiles are roughly balanced.

### Composite scores

- **`RFM_Score`:** String concatenation of R_Score, F_Score, M_Score (e.g., "555" for top customers).
- **`FM_Score`:** Average of F_Score and M_Score, rounded to nearest integer. Used for the simplified 2D segment framework.

---

## 5. Standard 11-Segment Framework

### Why 11 segments

The 11-segment framework is the industry standard taught in marketing analytics literature (e.g., Putler, Klaviyo, Bloomreach blogs). It uses the 2D `R_Score × FM_Score` grid with named cells:

- **Champions** (R≥5, FM≥5): Best customers, recent and high-value.
- **Loyal Customers** (R≥4, FM≥4): Strong relationship.
- **Potential Loyalists** (R≥4, FM≥3): Newer customers showing promise.
- **Recent Customers** (R=5, FM=1): Just signed up, not yet engaged.
- **Promising** (R≥4, FM≤2): New, low-engagement, but recent.
- **Customers Needing Attention** (R=3, FM≥3): Drifting away from active.
- **About to Sleep** (R=3, FM≤2): Drifting and disengaged.
- **At Risk** (R≤2, FM=3): Mid-value customers going inactive.
- **Cannot Lose Them** (R≤2, FM≥4): High-value customers going inactive — top priority.
- **Hibernating** (R=2, FM≤2): Long-dormant low-value.
- **Lost** (R=1): Very long-dormant; suppress from active list.

### Why this framework over alternatives

- **Interpretability:** Marketing stakeholders understand "Cannot Lose Them" instinctively. They do not understand "Cluster 3."
- **Action-orientation:** Each segment has a known marketing playbook in the literature.
- **Balance:** 11 segments is enough granularity to differentiate strategy without overwhelming.
- **Foundation for ML:** RFM scores serve as features for the clustering step, providing apples-to-apples comparison.

---

## 6. Pareto Validation

We compute the cumulative revenue contribution sorted by customer value to verify the dataset has the expected long-tail distribution. The result confirms a strong Pareto pattern: the top 20% of customers contribute approximately 70-80% of revenue. This is the structural reason segmentation is valuable: differentiated investment per segment is justified by differential revenue contribution.

If the dataset had been uniform (every customer roughly equal), segmentation would have been unnecessary.

---

## 7. ML Clustering — Method Selection

### Why both K-Means and Hierarchical

We deliberately apply two algorithms with different assumptions to validate that any structure we adopt is robust:

| Method | Assumes | Strengths | Weaknesses |
|---|---|---|---|
| K-Means | Spherical, equal-size clusters | Fast, scalable, interpretable centroids | Requires `k` upfront, sensitive to scaling, struggles with non-spherical structure |
| Hierarchical (Agglomerative, Ward linkage) | None about cluster shape | Dendrogram for visual inspection, no k upfront | O(n^2) memory, slower on large datasets |

If both methods agree (high Adjusted Rand Index), we have confidence the clusters represent real structure rather than algorithm artifacts.

### Why log-transform Frequency and Monetary

Both Frequency and Monetary distributions are heavily right-skewed (long tails of high-value customers). Distance-based clustering treats raw values literally — a customer with £10,000 monetary will dominate the distance from a customer with £100. Log transformation (`np.log1p`) compresses the tail and brings the distribution closer to normal, making distance computations more meaningful for clustering.

Recency is left untransformed because its distribution is already reasonable (no extreme outliers — the maximum is bounded by the dataset's date range).

### Why StandardScaler (z-score normalization)

After log transformation, the three features still have different scales (Recency in days, log-Frequency in log-units, log-Monetary in log-units). Distance-based clustering is dominated by features with larger scales unless features are normalized. `StandardScaler` ensures each feature has mean 0 and standard deviation 1, giving each dimension equal weight in distance computation.

### Why k=4

We evaluated k from 2 to 10 using four metrics:
1. **Inertia (elbow method):** Visualized for elbow detection.
2. **Silhouette score:** Higher is better. Range [-1, 1].
3. **Davies-Bouldin index:** Lower is better.
4. **Calinski-Harabasz index:** Higher is better.

In practice, the metrics often disagree on the "best" k. We chose k=4 because:
- It captures the four major behavioral types (Best, Engaged Mid-Value, Light Buyers, Inactive) without being too granular for stakeholder communication.
- Silhouette at k=4 (~0.36) is acceptable for marketing data (>0.3 is conventional threshold).
- Lower k (2-3) would lose meaningful distinctions; higher k (5+) would over-fragment.

### Cluster labelling

K-Means returns numeric IDs without semantic meaning. We map clusters to descriptive labels by ranking them on average monetary value and inspecting recency:

- **Best Customers:** Top monetary, low recency (recent + high-value).
- **Engaged Mid-Value:** Mid monetary, mid recency.
- **Light Buyers:** Low monetary, low frequency, high recency.
- **Inactive / Lost:** Low monetary, low frequency, mid-recency one-time buyers.

Labels are heuristic; in production, labels would be reviewed by marketing stakeholders for terminology fit.

### Algorithm agreement

We compute the Adjusted Rand Index (ARI) between K-Means and Hierarchical cluster assignments. ARI of 0.61 indicates substantial agreement. The cross-tabulation confirms the same customers tend to land in equivalent clusters under both methods, validating cluster robustness.

---

## 8. Persona Alignment Heuristic

Coffra has two personas defined in P1: Connoisseur (technical, frequent, high-value) and Daily Ritualist (habitual, moderate). The Online Retail II dataset has no persona labels, so we infer probable persona from RFM signature:

| Persona | Frequency criterion | M_Score criterion | Recency criterion |
|---|---|---|---|
| Connoisseur (probable) | ≥10 invoices | ≥4 | ≤90 days |
| Daily Ritualist (probable) | 3-10 invoices | 2-4 | ≤180 days |
| Unaligned | Otherwise | — | — |

The "Unaligned" bucket captures customers who don't fit either profile cleanly — typically one-time buyers or customers with extreme recency. Approximately 60% of customers fall here.

### Limitations

- This is a heuristic, not a measured persona. Real Coffra deployment must capture persona explicitly via signup survey.
- The heuristic is biased toward already-active customers. New customers who match the Connoisseur profile may not yet have enough purchase history to qualify.
- Persona is a continuous spectrum, not a binary label. A heuristic forces a discrete assignment.

In production, persona inference would be a fallback used only when explicit persona data is missing, and would be flagged as low-confidence.

---

## 9. Financial Impact Projection

### What we computed

For each segment, we project annual revenue uplift from differentiated marketing campaigns vs. untargeted broadcast baseline. The formula:

```
monthly_baseline = customers × avg_monthly_orders × AOV
monthly_with_lift = customers × avg_monthly_orders × AOV × (1 + retention_lift + aov_uplift)
annual_uplift = (monthly_with_lift - monthly_baseline) × 12
```

### Assumptions

- **AOV = £20:** Coffra-specific assumption. Reasonable for a coffee subscription service with mixed product types.
- **Avg monthly orders per segment:** Estimated based on segment-specific behavior (Champions purchase ~2/month, Lost ~0/month, etc.).
- **Retention and AOV lift assumptions:** Anchored to public industry benchmarks from Klaviyo, Bloomreach 2024 reports for differentiated email marketing programs. Specific lifts vary by segment based on segment-specific intervention type.

### Honest disclosure

These projections are scenario-based, not measurements. They represent reasonable expectations for differentiated segment campaigns vs. a no-personalization baseline, **assuming** the campaigns are designed and executed competently. Actual lifts in a real deployment would vary based on:

- Campaign quality and creative execution
- Customer base composition vs. assumed averages
- Channel mix
- Competitive context
- Macroeconomic conditions

A real Coffra deployment would measure actual lifts via per-segment A/B testing and refine the assumption table iteratively.

### Why include projections at all

A segmentation analysis without financial framing is academic. The projection answers "is this worth doing?" — and the answer drives prioritization. The £240K total annual uplift estimate (against a £17M observed revenue base) corresponds to a +23% relative lift, which is well within published ranges for retention-focused marketing programs.

---

## 10. Limitations and Future Work

### Known limitations

- **Static analysis:** Customers shift segments over time; this analysis is a snapshot, not a longitudinal study.
- **3D RFM space:** Segmentation richness is bounded by the 3 dimensions analyzed. Adding product category preferences, channel behavior, or demographics would surface additional structure.
- **No causal inference:** RFM segments correlate with revenue but do not prove causation. A "Champion" might be a Champion because of marketing, or because of underlying customer characteristics — we cannot tell.
- **Cancellations excluded, not netted:** Some practitioners prefer to subtract returns from purchases. We excluded for clarity; the choice affects monetary values for high-return customers.
- **Persona inference is heuristic:** Real persona assignment requires explicit signal capture.
- **Lift assumptions are projections:** All financial impact numbers are scenario-based until validated via A/B testing.

### Future enhancements (v1.1+)

- **Add product diversity dimension:** A customer who buys 10 of the same product behaves differently from one who buys 10 different products. RFM does not distinguish.
- **Time-series segmentation:** Track segment migration over time. A "Champions → At Risk" customer requires immediate intervention; a "Promising → Loyal" customer is the success story we want to replicate.
- **Margin-weighted Monetary:** Use contribution margin instead of raw revenue to align segment value with business profitability.
- **Multi-armed bandit campaigns:** Replace fixed segment-strategy mapping with adaptive campaign allocation that learns from observed lifts.
- **Predictive churn model:** Train a supervised model on segment-migration history to predict churn risk before customers reach At Risk / Cannot Lose Them stages.

### Production roadmap

Documented in `notebooks/05_segment_to_strategy.ipynb` and the dashboard's Customer Segments page. Six-phase plan:

1. Data foundation (HubSpot + Shopify integration)
2. RFM pipeline (weekly refresh)
3. Segment workflows (HubSpot automation)
4. Persona survey (explicit capture)
5. Measurement (segment migration matrix)
6. Iteration (quarterly re-clustering)

---

## 11. Reproducibility

All analysis is reproducible from this repository:

- Public dataset: [Online Retail II UCI](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)
- Fixed `random_state=42` in all stochastic steps (KMeans, sampling)
- Pinned `requirements.txt`
- Notebooks numbered for sequential execution: 02 → 03 → 04 → 05
- Outputs saved to `data/processed/` for downstream consumption

To reproduce:

```bash
# 1. Download dataset to data/raw/online_retail_II.csv
# 2. Run notebooks in order:
jupyter lab notebooks/02_rfm_eda.ipynb
jupyter lab notebooks/03_rfm_scoring_and_segments.ipynb
jupyter lab notebooks/04_customer_clustering.ipynb
jupyter lab notebooks/05_segment_to_strategy.ipynb

# 3. View dashboard:
streamlit run dashboard/streamlit_dashboard.py
```

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 26, 2026** | Initial methodology document covering dataset selection, cleaning, RFM scoring, clustering, persona alignment, financial projection, and limitations. |
