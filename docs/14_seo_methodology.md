# Technical SEO + GEO Audit Methodology

**Project:** P6 · Coffra Technical SEO + GEO Audit
**Author:** Sebastian Kradyel
**Date:** April 2026
**Document:** docs/14_seo_methodology.md

---

## 1. The Business Question

Coffra publishes content across six pillars (P4) and runs a marketing automation system (P1–P3). But content that isn't discoverable generates no return. **Are Coffra's pages technically sound enough for Google to crawl, index, and surface them — and are they structured well enough for AI engines to cite them?**

Two related questions follow:

- **Technical SEO:** Are there crawlability, indexability, page speed, or mobile usability issues blocking organic visibility?
- **GEO/AEO (Generative Engine Optimization / Answer Engine Optimization):** Now that Google AI Overviews, Perplexity, and ChatGPT browse the web and generate answers, is Coffra's content structured to be cited in those answers — not just ranked in blue-link SERPs?

These are distinct but connected. A page with poor Core Web Vitals may rank lower in Google's algorithm but still get cited in an AI Overview if its Schema markup and content structure are strong. A page with perfect technical SEO but no Schema markup will likely be invisible to AI engines. Both dimensions must be audited.

---

## 2. Why Technical SEO and GEO Together

Traditional SEO audits focus exclusively on search engine crawlability and ranking signals. GEO/AEO is a newer discipline (Princeton GEO benchmark, Aggarwal et al., 2023) measuring citation frequency in AI-generated responses. The two are increasingly intertwined:

| Dimension | Technical SEO | GEO / AEO |
|---|---|---|
| **Primary signal** | Crawlability, page speed, indexability | Schema markup, content authority, answer-format structure |
| **Output measured** | Rankings, impressions, clicks (GSC) | Citation rate in AI Overviews, Perplexity, ChatGPT |
| **Primary tool** | Google Search Console, PageSpeed Insights | Sampling queries via AI platforms |
| **Improvement lever** | CWV optimization, canonical tags, sitemap | JSON-LD templates, FAQ/HowTo format, entity disambiguation |
| **Time to result** | 2–12 weeks (crawl + reindex cycle) | 1–4 weeks (AI engines re-crawl frequently) |
| **Data availability** | Rich (GSC API, CrUX) | Sparse (no official API; requires sampling) |

**Key insight:** Fixing Technical SEO is table stakes — it removes blockers. GEO optimization is the emerging edge — it captures the growing share of search interactions that never produce a blue-link click.

---

## 3. Technical SEO Audit Framework

### 3.1 Audit categories

Six categories, ordered from foundational to performance:

**1. Crawlability**
Can Googlebot access all pages? Checks: robots.txt, XML sitemap, crawl budget, crawl errors in GSC.

**2. Indexability**
Are the right pages indexed? Checks: canonical tags, noindex tags, duplicate content, hreflang for multilingual content.

**3. Page Speed (Core Web Vitals)**
Does the page load fast enough? Checks: LCP, INP, CLS, FCP, TTFB against Google thresholds.

**4. Schema Markup**
Is structured data present and valid? Checks: JSON-LD presence, Rich Results Test, Schema.org Validator.

**5. Mobile Usability**
Does the page work on mobile? Checks: viewport meta tag, tap target sizes, text legibility, Google Mobile-Friendly Test.

**6. Security**
Is the site trustworthy? Checks: HTTPS enforcement, SSL certificate, mixed content warnings.

### 3.2 Core Web Vitals thresholds

Google's current CWV thresholds (Good / Needs Improvement / Poor):

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s – 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200ms – 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 – 0.25 | > 0.25 |
| FCP (First Contentful Paint) | < 1.8s | 1.8s – 3.0s | > 3.0s |
| TTFB (Time to First Byte) | < 800ms | 800ms – 1.8s | > 1.8s |

INP replaced FID (First Input Delay) in March 2024. Any audit using FID as a Core Web Vital is outdated.

### 3.3 Scoring methodology

Overall SEO health score is a weighted composite:

```
SEO Health Score = CWV (30%) + Schema Coverage (25%) + GSC Performance (25%) + GEO Citations (20%)
```

Each component is scored 0–100 before weighting:
- **CWV:** Percentage of metrics in "Good" range (5 metrics × 20 points each)
- **Schema Coverage:** Percentage of templates passing validation × richness bonus
- **GSC Performance:** Normalized impressions + CTR + avg. position composite
- **GEO Citations:** Citation rate on tested queries (raw percentage)

Weighting rationale: CWV is highest because it directly affects ranking algorithm. Schema and GSC are equal — Schema is the primary GEO lever, GSC measures organic performance. GEO citations are weighted last because sampling is imprecise and the metric is newer.

---

## 4. Google Search Console Integration

### 4.1 What GSC provides

Google Search Console API provides:
- **Performance data:** Impressions, clicks, CTR, average position — by query, page, country, device, date
- **Coverage data:** Indexed pages, crawl errors, indexing warnings
- **Core Web Vitals:** Field data (real user measurements) from Chrome UX Report
- **Rich Results:** Eligibility and errors for Schema-enhanced pages

### 4.2 Snapshot architecture

Consistent with P2 (live dashboard), GSC data is extracted via the Search Console API and stored as a local JSON snapshot. This avoids OAuth re-authentication on every dashboard load and maintains reproducibility:

```
data/snapshots/
├── gsc_snapshot.json       # queries, pages, impressions, clicks, CTR, position
├── gsc_coverage.json       # indexed pages, crawl errors
└── gsc_extracted_at.txt    # timestamp of last extraction
```

**Extraction parameters:**
- Date range: 90 days from extraction date
- Dimensions: query + page
- Row limit: 25,000 (API max)
- Filters: none (all queries, all pages)

### 4.3 API authentication

Uses a Service Account with domain-level delegation (preferred over OAuth for server-side apps). Credentials stored as environment variable `GSC_SERVICE_ACCOUNT_JSON` — never committed to repository.

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_service_account_info(
    json.loads(os.environ["GSC_SERVICE_ACCOUNT_JSON"]),
    scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
)
service = build("searchconsole", "v1", credentials=creds)
```

### 4.4 Key metrics and interpretation

**Impressions:** How many times a page appeared in search results. High impressions + low CTR = title/meta description optimization opportunity.

**CTR (Click-Through Rate):** Clicks / Impressions. Industry average varies by position: position 1 ≈ 28%, position 3 ≈ 11%, position 10 ≈ 2.5%.

**Average Position:** Mean ranking across all queries where the page appeared. Below 10 means not on page 1 — optimize content and acquire backlinks.

**Coverage (Indexed Pages):** If fewer pages are indexed than exist, investigate: crawl errors, noindex tags, duplicate content, or thin content may be blocking indexation.

---

## 5. Schema.org Markup Framework

### 5.1 Why Schema matters for GEO

Schema.org JSON-LD is the primary technical lever for GEO/AEO performance. The Princeton GEO study (Aggarwal et al., 2023) found that pages with structured data receive significantly higher citation rates in AI-generated responses — the mechanism being that LLMs can parse structured entities more reliably than free-form prose.

Practically: a page with `FAQPage` schema provides explicit question-answer pairs that an AI engine can extract with high confidence. The same content without schema requires the model to infer structure from prose — lower confidence, lower citation probability.

### 5.2 Template inventory (P4 → P6 extension)

12 JSON-LD templates were implemented in P4. P6 adds validation tracking and GEO impact measurement:

| Schema Type | Pages | GEO Citation Impact | Validation Status |
|---|---|---|---|
| Product | 8 | High | Valid |
| Organization | 1 | Medium | Valid |
| WebSite | 1 | Low | Valid |
| BreadcrumbList | 24 | Low | Valid |
| FAQPage | 6 | High | Valid |
| HowTo | 4 | High | Valid |
| Article | 12 | High | Valid |
| Review | 5 | Medium | Valid |
| SiteLinksSearchBox | 1 | Low | Valid |
| LocalBusiness | 1 | Medium | Valid |
| VideoObject | 3 | Medium | Warning |
| Recipe | 2 | High | Valid |

`VideoObject` warning: `duration` property requires ISO 8601 format (`PT2M30S`), not plain integer seconds. Fix is one-line per template; queued for next sprint.

### 5.3 Validation methodology

Three-layer validation:

1. **Syntax check:** Schema.org Validator (`validator.schema.org`) — checks JSON-LD syntax and required property completeness
2. **Rich Results eligibility:** Google Rich Results Test (`search.google.com/test/rich-results`) — confirms Google can parse the markup and the page is eligible for enhanced SERP features
3. **Live monitoring:** GSC Rich Results report — tracks actual rich result appearances in search results over time

A template passes validation only if it clears all three layers.

### 5.4 GEO citation boost classification

Each schema type is classified by expected GEO citation impact:

- **High:** Types that provide explicit answer-format content (FAQ, HowTo, Recipe, Article, Product with detailed specs) — AI engines can extract specific answers
- **Medium:** Types that establish entity identity and relationships (Organization, Review, VideoObject, LocalBusiness) — improve entity disambiguation
- **Low:** Types that aid navigation and site structure (BreadcrumbList, WebSite, SiteLinksSearchBox) — minimal direct GEO impact

---

## 6. GEO / AEO Citation Monitoring

### 6.1 What we measure

**Citation rate:** The percentage of test queries for which the target domain appears in the AI-generated response. Formally:

```
Citation Rate = (Queries where target domain is cited) / (Total test queries) × 100
```

This is analogous to click-through rate in traditional SEO — a behavioral signal that can be tracked over time.

### 6.2 Platforms monitored

Four AI platforms monitored:

| Platform | Interface | Mechanism | Update Frequency |
|---|---|---|---|
| Google AI Overviews | Google Search | Inline generative answer above organic results | Multiple times/day |
| Perplexity | perplexity.ai | AI-first answer engine with citations | Real-time |
| ChatGPT (Browse) | chat.openai.com | Browse mode — live web access | Real-time |
| Bing Copilot | bing.com | Integrated into Bing SERP | Real-time |

Each platform has different citation behaviors. Google AI Overviews tends to cite authoritative domains with strong E-E-A-T signals. Perplexity cites more broadly, including newer pages. ChatGPT Browse is influenced by recency and page load speed. Bing Copilot mirrors much of Google's authority signals.

### 6.3 Query sampling methodology

Adapted from Princeton GEO benchmark (Aggarwal et al., 2023):

1. Define a set of representative queries across Coffra's 6 content pillars
2. Minimum 8 queries per pillar = 48 queries per platform
3. For each query, submit to the platform and record:
   - Was the domain cited? (binary)
   - Was the page title cited? (optional)
   - Was any specific fact from the page reproduced? (optional)
4. Calculate citation rate per platform
5. Repeat weekly; track trend

**Sampling cadence:** Weekly for Perplexity and ChatGPT (API-accessible); monthly manual spot-check for Google AI Overviews (no stable API as of April 2026).

### 6.4 Baseline and post-Schema comparison

The most important metric is the **before/after delta** from Schema implementation. Without a baseline, citation rates are meaningless (a 40% citation rate could reflect pre-existing brand authority, not Schema implementation).

**Baseline period:** October–November 2025 (before P4 Schema implementation)
**Post-implementation:** November 2025 onwards

This design approximates a pre-post study. A cleaner design would use a holdout set of pages without Schema as a control group — planned for v1.1.

---

## 7. Looker Studio Export Layer

### 7.1 Why a Looker Studio layer

Looker Studio is the most commonly required dashboard tool in Marketing Operations job descriptions. Including a Looker Studio integration demonstrates:
- Ability to structure data for BI tool consumption
- Understanding of connector patterns (Google Sheets → Looker Studio)
- Production mindset: dashboard data should be refreshable, not static

### 7.2 Export schema

Five datasets, each structured for direct Looker Studio Google Sheets connector:

**gsc_queries.csv**
```
query | impressions | clicks | ctr_pct | avg_position
```

**cwv_diagnostics.csv**
```
metric | value | threshold_good | status | priority
```

**schema_coverage.csv**
```
schema_type | pages_covered | validation_status | rich_result_eligible | geo_citation_boost
```

**geo_citation_trend.csv**
```
month | google_aio_pct | perplexity_pct | chatgpt_browse_pct | bing_copilot_pct
```

**seo_audit_checklist.csv**
```
category | check | status | notes
```

### 7.3 Connection guide

Full step-by-step guide is available in the P6 README. The recommended dashboard structure:
- **Page 1:** GSC Performance (impressions, clicks, CTR, position trend)
- **Page 2:** Technical Health (CWV scorecard, audit checklist)
- **Page 3:** GEO/AEO Monitoring (citation rate by platform, trend over time)

---

## 8. Synthetic and Snapshot Data Design

### 8.1 Data types in P6

P6 uses three data types, clearly labeled in the dashboard:

| Component | Type | Rationale |
|---|---|---|
| GSC Queries | Snapshot | Real GSC data extracted April 2026 |
| Core Web Vitals | Simulated | Coffra (Streamlit-hosted) has no real CrUX data; benchmarks used |
| Schema Coverage | Real | 12 templates validated via Schema.org Validator + Rich Results Test |
| GEO Citations | Simulated | No real organic traffic; Princeton GEO benchmark methodology applied |
| Technical Audit | Real | Manual checks via GSC, PageSpeed Insights, Validator |

### 8.2 CWV simulation methodology

CWV values are simulated using realistic benchmarks for a Streamlit Cloud-hosted site:
- LCP baseline: 1.8–2.2s (typical for server-side rendered Python apps with no CDN)
- INP baseline: 80–120ms (Streamlit's event loop is responsive for simple interactions)
- CLS baseline: 0.02–0.06 (Streamlit renders components in predictable order)
- FCP baseline: 0.8–1.1s (first paint fast; content render depends on data loading)
- TTFB baseline: 280–380ms (Streamlit Cloud latency, US East servers)

A real deployment on a custom domain with CDN and optimized assets would show meaningfully lower LCP and TTFB.

### 8.3 GEO simulation methodology

Citation rates are simulated using pre-post deltas from Princeton GEO benchmark:

**Pre-Schema baseline:** 3–5% citation rate (unstructured pages with no Schema markup — typical for new domains without authority)

**Post-Schema trajectory:** Modeled as logistic growth from baseline to a ceiling:
```
citation_rate(t) = ceiling / (1 + exp(-k * (t - t_midpoint)))
```
Where:
- `ceiling` = 45–50% (consistent with top-performing structured pages in Princeton study)
- `k` = growth rate parameter (steeper for FAQPage/HowTo, shallower for Product)
- `t_midpoint` = ~8 weeks post-implementation (indexation + model re-training lag)

---

## 9. Validation Framework

### 9.1 Technical audit validation

- **Reproducibility:** All checks documented with specific tool + URL used; any auditor running the same tools should reach the same conclusion
- **Threshold sourcing:** All thresholds cited from Google's official documentation (web.dev, developers.google.com) with version dates
- **False negative check:** After fixing a flagged issue, re-run the specific check to confirm resolution

### 9.2 Schema validation pipeline

Three-step validation is mandatory for each template change:
1. Validate locally with `python-schemaorg` or `schema-dts` before deployment
2. Run Google Rich Results Test on staging URL
3. Confirm GSC Rich Results report shows no new errors within 72 hours of deployment

### 9.3 GEO monitoring reliability

Citation monitoring via manual sampling is inherently noisy:
- AI platforms produce non-deterministic outputs — the same query may yield different responses on consecutive runs
- Sample size of 48 queries per platform gives ~±14% margin of error at 95% confidence
- Trend direction is more reliable than point estimates — use rolling 4-week average to reduce noise

Planned improvement: increase to 100 queries per platform (±10% margin of error) and implement API-based sampling for Perplexity and ChatGPT to reduce manual effort.

---

## 10. Honest Limitations

### 10.1 GSC data

- GSC excludes queries with very low impression counts (privacy threshold) — long-tail queries are underrepresented
- GSC position data is averaged across all users and devices — actual position varies by user, location, and search history
- Coffra is a fictional brand with minimal real traffic; GSC snapshot reflects a small real-data footprint

### 10.2 Core Web Vitals

- CrUX (field data) requires sufficient real user traffic to generate data. Coffra has insufficient traffic for CrUX; PageSpeed Insights lab data is used as proxy
- Lab data may not reflect real-world performance across user devices and network conditions
- CWV thresholds change periodically — this audit is accurate as of April 2026

### 10.3 GEO / AEO monitoring

- No official API for Google AI Overviews citation monitoring as of April 2026 — manual sampling required
- AI platforms update frequently; citation behavior may change without notice as models are retrained
- Citation rate improvement after Schema may be partially attributable to other factors (content freshness, backlinks acquired simultaneously)
- Princeton GEO benchmark used a set of general-domain queries; Coffra-specific queries may not generalize

### 10.4 Schema markup

- Schema markup does not guarantee rich results or AI citations — it improves probability
- Google reserves the right to ignore Schema markup if the on-page content does not support the claims made in JSON-LD
- Some schema types (e.g., Recipe, Product) have strict required properties that must be met for rich result eligibility

---

## 11. Implementation Stack

| Layer | Tool | Rationale |
|---|---|---|
| GSC data extraction | Google Search Console API v3 | Official API; Service Account auth |
| CWV measurement | PageSpeed Insights API | Free, no authentication required |
| Schema validation | Schema.org Validator + Rich Results Test | Official validation tools |
| GEO monitoring | Manual sampling + Perplexity API (planned) | No alternative for AI Overview monitoring |
| Data storage | JSON snapshots in `/data/snapshots/` | Consistent with P2 snapshot architecture |
| Dashboard | Streamlit (existing infrastructure) | Consistent with P1–P5 |
| Looker Studio export | CSV via `st.download_button` | Direct connector compatibility |
| Visualization | `st.line_chart`, `st.dataframe`, `st.progress` | Native Streamlit, no extra dependencies |

---

## 12. Project Structure

```
P6 Technical SEO + GEO Audit/
├── data/
│   └── snapshots/
│       ├── gsc_snapshot.json
│       ├── gsc_coverage.json
│       └── gsc_extracted_at.txt
├── docs/
│   └── 14_seo_methodology.md          # This document
├── dashboard/pages/
│   └── 6_Technical_SEO_GEO_Audit.py   # Live dashboard page
└── case_study/
    └── P6_Coffra_SEO_Audit.pdf
```

---

## 13. Connection to Rest of Portfolio

| Project | Connection to P6 |
|---|---|
| P1 — Email Automation | Email channel drives organic traffic; GEO citations of email content boost CRM engagement |
| P2 — Live Dashboard | P6 is page 6 in the same Streamlit app; snapshot architecture is identical |
| P3 — Customer Segmentation | GSC query data can be segmented by buyer persona (Connoisseur vs Daily Ritualist queries) |
| P4 — AEO Content Strategy | P4 built the Schema templates; P6 validates, monitors, and measures their GEO impact |
| P5 — Attribution Modeling | Once GEO-referred traffic grows, AI Overview / Perplexity becomes a measurable channel in MMM |

---

## 14. Roadmap (v1.1+)

- **GSC automation:** Scheduled weekly extraction via GitHub Actions + Google Cloud Run
- **CrUX integration:** Real field data as Coffra traffic grows; replace lab data simulations
- **Perplexity API sampling:** Automate citation monitoring for Perplexity (API available)
- **Google AI Overviews:** Monitor for official API; interim — Playwright-based scraper (with rate limiting and robots.txt compliance)
- **Competitive benchmarking:** Compare Coffra citation rates against 3 competitor coffee brands
- **Schema A/B test:** Deploy Schema on a subset of pages, withhold from matched pages, measure citation rate difference — proper experimental design for GEO attribution

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 2026** | Initial methodology document. Technical audit framework, GSC integration, Schema validation pipeline, GEO citation monitoring methodology, Looker Studio export layer, synthetic data design. |
