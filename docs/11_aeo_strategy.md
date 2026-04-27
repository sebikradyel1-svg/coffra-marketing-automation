# Coffra Answer Engine Optimization (AEO) Strategy

**Project:** P4 · Coffra Answer Engine Optimization
**Author:** Sebastian Kradyel
**Date:** April 2026
**Document:** docs/11_aeo_strategy.md

---

## 1. Why AEO Matters Now

The marketing landscape is undergoing the most significant shift since mobile-first design. By April 2026, the data is unambiguous:

- **ChatGPT** handles over 2 billion queries daily and reaches 883 million monthly active users (Frase 2026 AEO Guide).
- **Google AI Overviews** appear in nearly 55% of all Google searches (Frase 2026).
- **Gartner predicts** traditional search volume will drop 25% by 2026 due to AI chatbots and virtual agents.
- **AI-referred website sessions** grew 527% year-over-year through mid-2025 (Frase 2026).
- Over **65% of searches now end without a click** to a website (O8 Agency 2026).

For a brand like Coffra (specialty coffee D2C), this means a customer asking "what's the best Romanian specialty coffee roastery in Timișoara?" no longer scrolls through 10 blue links. They get a synthesized answer from ChatGPT, Perplexity, or Google AI Overviews. If Coffra is not cited in that answer, the brand effectively does not exist for that query.

**AEO is the discipline of structuring content so that AI engines cite your brand when they synthesize answers.** It is the natural evolution of SEO, not a replacement.

### The strategic implication

Coffra's marketing system to date (P1, P2, P3) has built strong foundations: persona-driven email automation, customer segmentation, lead scoring. But all of this assumes the customer has already discovered Coffra. AEO addresses the discovery layer: how does Coffra become the answer when someone asks an AI engine about specialty coffee in Romania?

This document specifies the strategy. The deliverables are immediately actionable — a marketing manager could begin implementing within a week.

---

## 2. AEO vs. SEO vs. GEO

The terminology is evolving fast. To avoid confusion, we use these definitions consistently:

| Discipline | What it optimizes for | Primary KPI |
|---|---|---|
| **SEO (Search Engine Optimization)** | Ranking in Google's blue links (positions 1-10) | Organic traffic |
| **AEO (Answer Engine Optimization)** | Being cited when AI engines synthesize answers | AI citations / visibility share |
| **GEO (Generative Engine Optimization)** | Same as AEO; sometimes used as broader umbrella term | Same as AEO |

### Key insight: SEO is foundation, AEO is layer

Studies show a 92% correlation between pages ranking in the top 10 organically and pages cited in AI Overviews (Surmado 2026). AI engines read the top search results. If a brand is not in the top 10 organic results, it is statistically unlikely to be cited.

**Strategic conclusion:** AEO does not replace SEO. It adds a structural layer on top of strong SEO. Coffra needs both.

---

## 3. How AI Engines Decide What to Cite

Different answer engines have different preferences. Coffra's AEO strategy must address each:

### ChatGPT (OpenAI)
- Favors **conversational, comprehensive content** that explains context alongside facts.
- Prefers content with **clear topic authority** (a brand demonstrably knows its niche).
- Citations come from web indexing through Bing.

### Perplexity
- Heaviest reliance on **citation practices and factual accuracy**.
- Rewards **freshness** — recent content is privileged.
- Multi-channel presence matters (Reddit, news outlets, documentation).

### Google AI Overviews / Gemini
- Pulls from top 10 organic results — strong traditional SEO foundation is essential.
- **Multimodal** — analyzes images and video frames as entities (Cubitrek 2026).
- Privileges schema-marked content.

### Microsoft Copilot
- **B2B-leaning**, draws heavily from LinkedIn for professional queries.
- Bing index foundation.

### Claude (Anthropic)
- Prefers **long-form, comprehensive guides**.
- Less commonly used for product discovery, more for analytical queries.

**Practical implication for Coffra:** A multi-engine AEO strategy is needed. We cannot optimize for ChatGPT and ignore Perplexity. The good news: most AEO best practices help across all engines simultaneously.

---

## 4. The Princeton GEO Findings — Evidence-Based Tactics

The Princeton GEO research (2024) empirically tested 10,000 queries across major AI engines, measuring how content tactics impact LLM citation probability. The findings provide a foundation for evidence-based AEO:

| Tactic | Citation Visibility Impact |
|---|---|
| Adding expert quotes to content | **+41%** |
| Including statistics with sources | **+30%** |
| Adding citations to authoritative sources | **+30%** |
| Adding fluency optimization | Minimal |
| Adding keyword stuffing | **Negative** |

(Source: Princeton GEO Study 2024, cited in Surmado 2026 AEO guide.)

These four findings define the core content tactics for Coffra:

1. **Expert quotes:** Quote roasters, baristas, coffee scientists. Quote Sebastian as founder.
2. **Statistics with attribution:** "Coffra sources from farms at 1,800-2,200m altitude" rather than "high altitude." Cite specific origins.
3. **Authoritative citations:** Link to Specialty Coffee Association, James Hoffmann content, scientific sources.
4. **Avoid keyword stuffing:** Write naturally, not for keyword density.

---

## 5. Coffra AEO Audit — Current State Assessment

Before defining strategy, audit current AEO posture. Since Coffra is fictional and has no live website, this audit is hypothetical but uses a real methodology that would apply to live deployment.

### Audit dimensions

For each Coffra-relevant query, test 5 AI engines (ChatGPT, Perplexity, Claude, Gemini, Copilot) and measure:

1. **Brand mentioned?** Yes/No
2. **Brand cited as source?** Yes/No
3. **Information accuracy?** Correct / Partially correct / Wrong
4. **Sentiment of mention?** Positive / Neutral / Negative
5. **Prominence of mention?** First / Middle / Last in response

### Test queries for Coffra

The audit should run across query types matching customer journey stages:

| Stage | Query type | Example |
|---|---|---|
| Discovery | Generic category | "best specialty coffee in Romania" |
| Comparison | Brand vs alternatives | "Coffra vs other Romanian coffee brands" |
| Evaluation | Use case fit | "best coffee subscription for V60 users" |
| Trust | Brand credibility | "is Coffra a good specialty coffee brand" |
| Local | Geographic | "specialty coffee shops in Timișoara" |
| Product | Specific product | "Coffra Ethiopia Gelana characteristics" |

### Expected baseline (for a new brand)

A new brand like Coffra would typically see:
- 0% citation rate at launch
- Rising to 5-10% after 6 months of consistent AEO work
- Reaching 25-40% for category-specific queries after 12-18 months

The notebook `06_aeo_audit.ipynb` automates this audit so it can be re-run monthly.

---

## 6. Coffra AEO Strategy — Six Pillars

### Pillar 1: Authoritative Brand Content

**Goal:** Establish Coffra as a recognized entity in AI knowledge graphs.

**Tactics:**
- Create a brand "About" page that uses semantic-triple structure: "Coffra is a specialty coffee roaster founded in Timișoara in 2026 by Sebastian Kradyel."
- Build a knowledge graph of Coffra facts: founded date, location, founder, products, certifications, sourcing partners.
- Use consistent naming across all platforms (Google Business Profile, social media, press mentions).
- Add `Organization` schema to homepage with all key facts (covered in `docs/12_schema_implementation.md`).

**Success metric:** Coffra mentioned by name when asked "What is Coffra?" across all 5 AI engines within 3 months of launch.

---

### Pillar 2: Answer-First Content Architecture

**Goal:** Make every page directly extractable as an answer by AI engines.

**Tactics:**
- **The 50-Word Rule:** Place a clear, concise 40-60 word answer at the top of every page or section (Cubitrek 2026).
- **Answer Blocks:** Structure content as Question → 50-word answer → Detailed explanation → Examples → Citation.
- **FAQ schema** on relevant pages.
- **Clear headers** that match natural language queries: "How does Coffra source its coffee?" not "Sourcing approach."

**Example for Coffra "Coffra Pass" page:**

```
H1: What is Coffra Pass?

[40-word answer block]
Coffra Pass is a monthly subscription giving members 15 cafés
at any Coffra location for 245 RON. It includes filter coffee,
espresso, and seasonal specials, with no cancellation fees.

[Then expand with details, scenarios, FAQ, etc.]
```

**Success metric:** AI engines cite the answer block verbatim when answering "What is Coffra Pass?" within 60 days of publication.

---

### Pillar 3: E-E-A-T Signals at Scale

**Goal:** Demonstrate Experience, Expertise, Authoritativeness, Trustworthiness — the framework AI engines use to assess source quality.

**Tactics:**
- **Author bios** on every blog post linking to Sebastian's LinkedIn and bio page. Use `Person` schema.
- **Expert quotes** integrated into content (per Princeton +41% lift).
- **Sources cited** for every statistic (per Princeton +30% lift).
- **Original photography** of farms, roasting process, baristas — not stock images.
- **Customer testimonials** with full names and verifiable details.
- **Press mentions** in trusted outlets — invest in PR for "best coffee in Timișoara" type listicles.

**Success metric:** When ChatGPT is asked "Who are experts in Romanian specialty coffee?" Sebastian Kradyel / Coffra appears in the answer within 6 months.

---

### Pillar 4: Schema Markup as a Foundation

**Goal:** Help AI engines parse Coffra content unambiguously.

**Schemas to deploy:**
- `Organization` — homepage
- `LocalBusiness` — café locations
- `Product` — every coffee product page (origin, weight, price, roast date, taste notes)
- `FAQPage` — FAQ section, Coffra Pass page, individual product pages
- `Article` — blog posts with `author`, `datePublished`, `dateModified`
- `Recipe` — brewing guides
- `Review` — collected customer reviews
- `Event` — cupping events, brewing classes

**Detailed copy-paste-ready schemas in `docs/12_schema_implementation.md`.**

**Success metric:** All schemas validate without errors via Google Rich Results Test. AI engines cite specific product attributes (origin, altitude, roast date) when asked.

---

### Pillar 5: Conversational Content That Anticipates Intent

**Goal:** Match how users actually ask AI engines, not how they typed in Google.

**Query intent shift:**

| Old SEO query | New AEO query |
|---|---|
| "specialty coffee Timișoara" | "where can I get really good single-origin coffee in Timișoara that isn't a chain" |
| "Ethiopia coffee" | "what's the difference between Ethiopia Gelana and Ethiopia Yirgacheffe" |
| "coffee subscription" | "is a coffee subscription worth it for someone who only drinks coffee on weekends" |

**Tactics:**
- Build content around long-tail conversational queries.
- Use **prompt research** instead of keyword research: ask ChatGPT "what would someone ask before buying specialty coffee for the first time?" and write content for those prompts.
- Use **semantic triples** in writing: "[Subject] [Predicate] [Object]" structures that AI agents parse cleanly.
- Avoid generic content like "Top 10 coffee tips." AI engines have access to thousands of these. Be specific, opinionated, original.

**Success metric:** Coffra cited for niche conversational queries (long-tail) within 6 months. Generic category queries take 12-18 months.

---

### Pillar 6: Multi-Channel Entity Reinforcement

**Goal:** Reinforce Coffra's brand identity consistently across the web so AI engines build a coherent entity profile.

**Tactics:**
- **Google Business Profile** fully optimized (hours, photos, posts, FAQ).
- **Wikipedia presence** — once Coffra has enough press coverage to qualify (typically 18-24 months in for a small brand).
- **Wikidata entry** for the brand and its founder.
- **LinkedIn** — Sebastian active, posting about specialty coffee, sourcing, marketing automation.
- **Industry directories** — Specialty Coffee Association member directory, Romanian craft coffee directories.
- **Local press** — pitch stories to Timișoara local media. Quotes from Sebastian.
- **Reviews** — encourage customers to leave detailed reviews on Google, TripAdvisor (for café), Trustpilot (for online shop).

**Success metric:** When AI engines describe Coffra, the description is consistent across engines. No conflicting information ("founded 2026" vs "founded 2025").

---

## 7. AEO-Specific Content Calendar

The above pillars require a sustained content investment. Below is a 12-month content calendar prioritized by AEO impact.

### Month 1-2: Foundation

- [ ] Optimize homepage with `Organization` schema and brand answer block.
- [ ] Create founder page with `Person` schema and Sebastian's bio.
- [ ] Set up Google Business Profile with full information.
- [ ] Audit existing site (or build new) with all `Product` schemas.
- [ ] Run baseline AEO audit (notebook 06).

### Month 3-4: Answer Architecture

- [ ] Restructure all product pages with answer blocks at top.
- [ ] Add FAQ sections to: Coffra Pass page, subscription page, sourcing page, brewing guides.
- [ ] Implement `FAQPage` schema across these.
- [ ] Publish 4-6 detailed blog posts answering specific niche queries (e.g., "What's the difference between natural and washed Ethiopia coffee?").

### Month 5-6: E-E-A-T Investment

- [ ] Photograph all sourcing trips, roasting process, baristas.
- [ ] Collect customer testimonials with consent.
- [ ] Pitch 3-5 local press stories about Coffra.
- [ ] Get Sebastian quoted in industry articles or invited to podcasts.
- [ ] Re-run AEO audit to measure progress.

### Month 7-9: Conversational Expansion

- [ ] Use prompt research to identify 20 high-value conversational queries.
- [ ] Publish 10-15 detailed answers (long-form, with expert quotes and citations).
- [ ] Update existing content to be more conversationally structured.

### Month 10-12: Authority Building

- [ ] Pitch for "Best of" listicles in industry publications.
- [ ] Sebastian publishes thought leadership on LinkedIn weekly.
- [ ] Build partnerships with other specialty coffee brands for cross-citation.
- [ ] Re-run AEO audit; target 20-30% citation rate for category-specific queries.

---

## 8. Measurement Framework

Traditional SEO metrics (rankings, traffic, click-through rate) do not capture AEO performance. New metrics are needed.

### Primary AEO metrics

| Metric | Definition | Source |
|---|---|---|
| **AI Visibility Score** | % of priority queries where Coffra is mentioned across 5 engines | Manual or automated audit (notebook 06) |
| **Citation Rate** | % of priority queries where Coffra is cited as a source | Same audit |
| **Sentiment Score** | Average sentiment of Coffra mentions in AI responses | Manual classification or sentiment API |
| **Information Accuracy Rate** | % of Coffra-related facts in AI responses that are correct | Manual verification |
| **AI-Referred Sessions** | Website sessions originating from AI engine clicks | Google Analytics 4 with custom referrer parsing |
| **AI-Influenced Conversions** | Conversions where AI was a touchpoint in the journey | Multi-touch attribution model (future P5) |

### Secondary metrics (legacy SEO baseline)

- Organic traffic to AEO-optimized pages
- Featured snippet wins
- Voice search appearances
- Schema validation errors (target: 0)

### Reporting cadence

- **Weekly:** Content publication count, schema validation status
- **Monthly:** AI Visibility Score audit (notebook 06), AI-Referred Sessions (GA4)
- **Quarterly:** Sentiment analysis, comprehensive AEO posture review

---

## 9. Coffra Implementation Priorities

Given limited resources for a small specialty coffee brand, prioritize as follows:

### Tier 1 — Must do (Week 1-4)

1. Homepage optimization with `Organization` schema and brand answer block.
2. Google Business Profile fully populated.
3. Founder bio page with `Person` schema.
4. Run baseline AEO audit.

### Tier 2 — Should do (Month 2-3)

5. Product pages with `Product` schema and answer blocks.
6. FAQ section with `FAQPage` schema.
7. Customer testimonials collection process.
8. First 4 detailed blog posts targeting niche queries.

### Tier 3 — Nice to have (Month 4-6)

9. Original photography across all content.
10. Press outreach campaign.
11. Recipe schema for brewing guides.
12. Sebastian's LinkedIn content cadence.

### Tier 4 — Long-term (Month 7-12)

13. Wikipedia/Wikidata presence (when qualified).
14. Industry partnership cross-citations.
15. Multi-language content (Romanian + English) with `inLanguage` schema annotations.

---

## 10. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| AI engines change citation algorithms unpredictably | High | Diversify across 5 engines; do not over-optimize for one. Re-audit monthly. |
| Competitors dominate AEO before Coffra launches | Medium | Move fast on Tier 1; prioritize unique angles (Romanian specialty coffee) where competition is thin. |
| AI hallucinations misrepresent Coffra | Medium | Monitor sentiment; correct misinformation through authoritative content; pitch corrections via PR. |
| AEO investment yields no measurable ROI for 6+ months | Medium-High | Track interim metrics (schema validation, content publication, audit scores). Long-term outcome is brand presence in AI era. |
| Privacy/data concerns from AI scraping | Low | Disclose AI scraping policy in robots.txt; engage in industry conversations on standards. |
| AEO becomes commoditized; everyone optimizes; visibility is harder | Inevitable (long-term) | Differentiate through unique brand voice, original content, authentic expertise. |

---

## 11. Coffra-Specific Strategic Bets

Beyond the universal AEO playbook, Coffra has specific advantages worth exploiting:

### Bet 1: Romanian specialty coffee niche

Most AEO content competition is English-language and US/UK-based. **Romanian specialty coffee is an under-served AEO niche.** A query like "specialty coffee Romania" has minimal competition. By owning this niche, Coffra can capture 60-80% citation share for category-specific queries within 12 months.

### Bet 2: Founder narrative

Sebastian's personal story (marketing master's, transitioning to coffee, deep technical interest) is **an authentic narrative AI engines find quotable**. Investing in personal LinkedIn presence and PR around this story builds entity recognition for both Coffra and Sebastian.

### Bet 3: Bilingual content advantage

Producing content in **both Romanian and English** with proper `inLanguage` schema annotations means Coffra can be cited for Romanian-language queries (where competition is essentially zero) and English-language queries (where Romania is rarely covered).

### Bet 4: Specialty community endorsement

Specialty coffee has a tight, active community on Reddit (r/Coffee, r/espresso), forums, and discussion platforms. **Earning organic mentions in these spaces is high-leverage** — AI engines weight these heavily for product authenticity assessments.

---

## 12. Next Steps

This document defines the strategy. The accompanying deliverables make it actionable:

- **Schema implementation guide** (`docs/12_schema_implementation.md`) — copy-paste-ready schemas for every Coffra page type.
- **AEO audit notebook** (`notebooks/06_aeo_audit.ipynb`) — automated monthly audit script.
- **AEO Analysis dashboard page** (`dashboard/pages/7_AEO_Analysis.py`) — live dashboard for tracking AEO posture.
- **Case study PDF** — formal documentation for the portfolio.

Implementation can begin Monday with Tier 1 priorities. Within 30 days, Coffra would have a measurable AEO baseline. Within 90 days, the first citations would begin appearing in AI engine responses for niche queries.

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 26, 2026** | Initial AEO strategy document. Six pillars, 12-month content calendar, measurement framework, Coffra-specific strategic bets. Anchored to current 2026 AEO research (Frase, HubSpot, Princeton GEO study, Surmado, Cubitrek). |
