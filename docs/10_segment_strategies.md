# Segment Strategies — Coffra Playbook

**Project:** P3 · Coffra Customer Segmentation
**Author:** Sebastian Kradyel
**Date:** April 2026
**Document:** docs/10_segment_strategies.md

---

## 1. Purpose

This document is the operational playbook that translates customer segments into Coffra-specific marketing actions. It is written to be deployment-ready: a marketing manager could read this on Monday and configure HubSpot/Brevo workflows by Wednesday.

Each segment entry includes:

- **Profile:** RFM signature and behavioral description
- **Coffra context:** Which Coffra persona aligns and why
- **Recommended action:** Specific tactic with channel and cadence
- **P1 reference:** Which existing P1 email content to reuse or adapt
- **Expected impact:** Realistic projection with rationale
- **Watch-outs:** Common mistakes to avoid

Where projections appear, they are anchored to industry benchmarks (Klaviyo, Bloomreach 2024) and clearly labelled as scenarios, not measurements.

---

## 2. Tier 1 — Retain and Amplify

### Champions

**Profile:** Top quintile on all RFM dimensions. Recent (last 30-60 days), frequent (10+ purchases), high-spending (top 20%).

**Coffra context:** Primarily Connoisseurs, with a small subset of high-engagement Daily Ritualists (Coffra Pass active subscribers). These customers are evangelists in the making.

**Recommended action:** Retention-first with amplification opportunity. Avoid promotional discounts (signals to Connoisseurs that the brand is desperate). Instead, invest in exclusivity and access.

**Specific tactics:**
- **Personal email from Sebastian (Roaster):** Quarterly note about new lots being cupped, with first-access purchase offer.
- **Private cupping events:** 4-6 times per year, invite-only at Coffra Timișoara location. Free.
- **Referral program:** Track referrals via unique code; reward both referrer and referee with a free 250g bag (no discount, just product).
- **First access to new origins:** 48-hour exclusive purchase window before public launch.

**Channel and cadence:** High-touch email (monthly), event invitations (quarterly), referral-program-trigger emails (event-based).

**P1 reference:** Adapt E5 Comparison Test (Connoisseur) for value escalation. E10 Community Invitation (Daily Ritualist) for event-format inspiration.

**Expected impact:** Maintain 90%+ annual retention. Drive 0.3-0.5 referrals per Champion per year, contributing 15-20% of new customer acquisition. Industry benchmarks support these ranges for high-engagement specialty retail.

**Watch-outs:**
- Do not over-communicate. Champions disengage from brands that nag.
- Do not discount. Erodes premium positioning.
- Do not generic-template their emails. They notice.

---

### Loyal Customers

**Profile:** R≥4, FM≥4. Slightly less recent or less high-spending than Champions, but consistently engaged. Backbone of recurring revenue.

**Coffra context:** Primarily Connoisseurs in their first year of subscription, plus Daily Ritualists who have moved beyond casual into ritual.

**Recommended action:** Subscription upsell + loyalty rewards. The goal is to push them up to Champion tier or stabilize them at Loyal.

**Specific tactics:**
- **Subscription pitch sequence:** If not yet subscribed, deploy P1 Email 4 (Subscription Pitch) with risk-reversal trial offer (first month at 50%, cancel anytime).
- **Tier benefits:** Subscribers get free shipping, 5% lifetime discount, birthday gift (250g of monthly featured origin).
- **Quarterly survey:** "Tell us what you'd want to see next." 3 questions, 60-second completion. Builds product-development input loop.
- **Bi-weekly newsletter:** Origin stories, brewing techniques, community spotlights. No hard sell.

**Channel and cadence:** Email automation (HubSpot workflow), bi-weekly newsletter, quarterly product update.

**P1 reference:** E4 Subscription Pitch for upsell. E2 Origin Story for newsletter content template.

**Expected impact:** 15-25% subscription conversion within 90 days for non-subscribers. 3-5% defection per quarter for subscribers (industry standard for premium subscriptions). Net retention 85%+.

**Watch-outs:**
- Do not over-personalize. Algorithmic recommendations work, but creepy product-suggestion emails reduce trust.
- Subscription pitches must respect autonomy: easy cancellation must be clearly stated.

---

## 3. Tier 2 — Develop and Convert

### Potential Loyalists

**Profile:** R≥4, FM=3. Recent buyers with moderate frequency and spending. Showing the right behaviors but not yet at scale.

**Coffra context:** Connoisseur-trajectory customers in their 30-90-day window. The graduating class — they will become Loyal Customers if marketing executes well.

**Recommended action:** Accelerated nurture to push them to Loyal status. The full P1 Connoisseur 5-email sequence runs here, plus optional persona-trigger touchpoints.

**Specific tactics:**
- **Full P1 Connoisseur sequence (English):** E1 Welcome → E2 Origin Story → E3 Brewing Guide → E4 Subscription Pitch → E5 Comparison Test, over 14 days.
- **Behavioral triggers:** If user opens Origin Story but doesn't click, send follow-up with deeper-dive video. If user clicks Brewing Guide, send V60 cheat sheet PDF.
- **SMS opt-in:** For US/UK customers, offer SMS for shipment notifications. Drives engagement without nag.

**Channel and cadence:** Email automation primary, SMS secondary, weekly cadence for first 60 days then bi-weekly.

**P1 reference:** Full Connoisseur 5-email sequence (`docs/04_email_copy_connoisseur.md`).

**Expected impact:** 30-40% promotion to Loyal within 90 days. Industry benchmarks for premium specialty subscriptions support this range.

**Watch-outs:**
- Do not skip Email 3 (Brewing Guide) — it is the value-delivery email that builds trust before the subscription pitch.
- Do not start the Subscription Pitch (E4) before E3 lands. Sequence integrity matters.

---

### Recent Customers

**Profile:** R=5, FM=1. Just signed up or just made first purchase. Insufficient signal to determine persona.

**Coffra context:** Either persona possible — needs explicit discovery before personalization. The most important and most fragile segment.

**Recommended action:** Onboarding first, persona discovery second. Welcome email + persona-routing survey within first 7 days.

**Specific tactics:**
- **Welcome email (E1):** Coffra brand intro, founder note from Sebastian, free shipping reminder, expectations for nurture sequence.
- **Persona-routing survey:** 1 question — "Are you here for the daily coffee experience (cafés, ritual, atmosphere) or for specialty single-origin beans (sourcing, brewing, technique)?"
- **Persona-routing logic:** Survey response stored in HubSpot `hs_persona` property. Triggers entry into either Connoisseur or Daily Ritualist nurture sequence.
- **Default behavior:** If no survey response in 7 days, assign to Daily Ritualist as default (broader appeal, less intimidating content).

**Channel and cadence:** 4 emails over 14 days, then handoff to persona-specific sequence.

**P1 reference:** E1 Welcome (both personas). Survey uses HubSpot native form.

**Expected impact:** 25-35% survey response rate (industry standard for low-friction single-question surveys). 70-80% of remaining customers correctly assigned via default fallback.

**Watch-outs:**
- Do not assume persona from first product purchased. A coworker who buys someone a Coffra Pass for a gift is not a Daily Ritualist.
- Survey question must be conversational, not a "quiz." Friction kills response rate.

---

### Promising

**Profile:** R≥4, FM≤2. Recent but low-engagement. Either a curious browser or a hesitant first-time buyer.

**Coffra context:** Probable Daily Ritualist trajectory. Not yet committed; needs invitation, not pitch.

**Recommended action:** Coffra Pass introduction with low-friction trial offer. Lifestyle anchoring over technical content.

**Specific tactics:**
- **Coffra Pass trial:** 7-day pass at 50% discount, no commitment. Auto-converts to monthly only if customer opts in explicitly.
- **Instagram-first content:** Behind-the-scenes café content, barista personalities, customer scenes. Drives Instagram follow + organic engagement.
- **Café visit incentive:** "First espresso on us" — bring this email to Timișoara location for a free shot. Tracks foot traffic.

**Channel and cadence:** Email + Instagram retargeting, bi-weekly cadence.

**P1 reference:** E4 Coffra Pass (Daily Ritualist sequence), E3 Three Rituals (lifestyle scenarios).

**Expected impact:** 10-15% Coffra Pass trial conversion. 20-30% of trial customers convert to paid Pass after first month.

**Watch-outs:**
- Do not push the technical Connoisseur sequence here. Wrong persona = unsubscribe.
- Café-visit incentives must be redeemable easily (no app required, no minimum purchase).

---

## 4. Tier 3 — Re-engage and Recover

### Customers Needing Attention

**Profile:** R=3, FM≥3. Mid-recency, mid-engagement. Early warning sign of disengagement.

**Coffra context:** Mostly Daily Ritualists drifting from active habit. Catchable if intervention is timely.

**Recommended action:** Re-engagement with personalization. "We noticed you" tone — not desperate, not pushy.

**Specific tactics:**
- **Last-purchase reminder:** Email referencing their most recent purchase ("Your Ethiopia Sidamo would pair beautifully with...") with a recommendation for the next purchase.
- **Loyalty stamp card status:** "You're 2 stamps away from a free 250g of any single origin." Gamification works for moderate-engagement customers.
- **Café visit nudge (for local customers):** "Drop by, we'll set up a tasting flight on the house."

**Channel and cadence:** 3-touch campaign over 21 days. Email primary.

**P1 reference:** Adapt cart recovery 1h/24h/72h cadence (`docs/06_email_copy_cart_recovery.md`).

**Expected impact:** 18-22% reactivation (purchase or café visit within 30 days).

**Watch-outs:**
- Do not lead with discount. Erodes margin and trains customers to wait for discount emails.
- Do not assume they forgot. Some customers buy from competitors — acknowledge that and re-earn the relationship.

---

### About to Sleep

**Profile:** R=3, FM≤2. Drifting and disengaged. Small but present opportunity.

**Coffra context:** Daily Ritualist drift mode. Low investment so far, easy to lose.

**Recommended action:** Light touch reminder of Coffra value. Not a campaign — a single thoughtful email.

**Specific tactics:**
- **Lifestyle anchoring email:** Adapt E3 Three Rituals (Daily Ritualist) — "When was the last time you took 20 minutes for yourself?"
- **Single-product spotlight:** Feature one easy-to-love product (signature blend, not single-origin) at standard price.

**Channel and cadence:** 2 emails over 30 days.

**P1 reference:** E3 Three Rituals (Daily Ritualist sequence).

**Expected impact:** 12-15% prevented churn (next purchase within 60 days).

**Watch-outs:**
- Tone must be warm, not desperate. "We miss you" reads needy. "We thought of you" reads like a friend.

---

### Cannot Lose Them

**Profile:** R≤2, FM≥4. High-value customers going inactive. Top priority for retention.

**Coffra context:** Almost certainly Connoisseurs. Each customer is worth £500+ in expected lifetime value.

**Recommended action:** High-priority win-back, executed personally by Sebastian. Generic email automation will fail here.

**Specific tactics:**
- **Personal email from Sebastian:** Hand-written, no template. Reference what they previously bought, ask if anything changed.
- **Phone call (optional):** For top decile of this segment, follow up email with a phone call. ROI justifies the time.
- **Custom offer:** Small thank-you (free 250g of their favorite origin) without strings attached.

**Channel and cadence:** Personal email immediately. Phone follow-up within 7 days for highest-value subset.

**P1 reference:** No template applies — must be custom written.

**Expected impact:** 40-55% win-back rate. Per-customer ROI is exceptional given high lifetime value.

**Watch-outs:**
- Do not delegate. The whole point is Sebastian's personal investment. A delegated email defeats the purpose.
- Do not include marketing language. Read like a friend reaching out, not a brand.

---

### At Risk

**Profile:** R≤2, FM=3. Mid-value customers going inactive.

**Coffra context:** Mixed personas. Approach must be persona-neutral or persona-detected.

**Recommended action:** Win-back with asymmetric incentives by persona. Daily Ritualists respond to small discounts; Connoisseurs respond to access offers.

**Specific tactics:**
- **For Connoisseurs:** Sample of new origin — "We just got Yirgacheffe, send us your address and we'll mail a 50g sample." Free, no purchase required.
- **For Daily Ritualists:** 15% off next order via personal code. Time-bound (14 days) but not aggressive about urgency.
- **For Unaligned:** Default to Daily Ritualist treatment.

**Channel and cadence:** 2-3 emails over 14 days, with retargeting ads if budget allows.

**P1 reference:** E2 Quick Thought (cart recovery template — free shipping + sample).

**Expected impact:** 12-18% win-back within 30 days.

**Watch-outs:**
- Do not run identical messages to all At-Risk customers. Persona detection improves response by 1.5-2x.

---

## 5. Tier 4 — Suppress and Reset

### Hibernating

**Profile:** R=2, FM≤2. Long-dormant, low historical value.

**Coffra context:** Persona usually unknown. Long time since meaningful engagement.

**Recommended action:** Last-chance win-back, then suppress. Single email; if no engagement, suppress from active marketing list.

**Specific tactics:**
- **One thoughtful email:** Reframe Coffra ("We've changed since you last visited"). Include single product feature + free-shipping offer.
- **Suppression rule:** No engagement (no open, no click) within 30 days = remove from active list. Eligible for re-engagement campaign in 6 months.

**Channel and cadence:** 1 email; if no engagement, exclude permanently from active sends.

**P1 reference:** Adapt E5 Comparison Test (Connoisseur) — final-chance language.

**Expected impact:** 5-8% reactivation. Main goal is list hygiene, not revenue.

**Watch-outs:**
- Do not retry within 6 months. Repeated emails to non-engagers hurt sender reputation across all email programs.
- Do not deeply discount as a Hail Mary. Sets bad precedent for future customer acquisition.

---

### Lost

**Profile:** R=1. Very long-dormant. Effectively churned.

**Coffra context:** Treat as inactive. No active marketing.

**Recommended action:** Suppression with periodic review.

**Specific tactics:**
- **Suppress from all active campaigns:** Email, SMS, paid retargeting.
- **Quarterly review:** Run a single "is this email address still active?" query (e.g., delivery-only check, no content) once per quarter to maintain list hygiene.
- **Annual reset campaign:** Once per year (typically before Black Friday), run a single broad "Are you still with us?" campaign across all Lost customers. Measure for revival; suppress non-responders again.

**Channel and cadence:** None active. Annual reset only.

**P1 reference:** N/A.

**Expected impact:** 1-2% organic reactivation (typically driven by external factors, not marketing). Annual reset campaign yields 3-5% reactivation; the rest stay suppressed.

**Watch-outs:**
- Do not delete. Customer history is valuable for analytics even if customer is inactive.
- Do not unsubscribe automatically. Let the customer decide.

---

## 6. Cross-Cutting Principles

### Persona consistency

Every campaign should respect the persona's voice rules established in P1. Connoisseurs do not respond to lifestyle imagery; Daily Ritualists do not respond to technical jargon. When in doubt, default to Daily Ritualist messaging — broader appeal, lower risk of offending.

### Discount discipline

Apply asymmetrically:
- Connoisseurs: minimal discounts (sample swaps, access offers preferred)
- Daily Ritualists: occasional discounts on entry-level products
- Cart recovery: free shipping > percentage off
- New customer acquisition: free trial > price discount

Discounting trains customers to wait. Sample/access offers train them to engage.

### Frequency hygiene

Maximum 2 emails per week to any customer regardless of segment. Exceed this and unsubscribe rates spike non-linearly. Use HubSpot frequency capping or equivalent.

### Suppression as a feature

Lost and Hibernating segments should be suppressed by default. This protects sender reputation, reduces email infrastructure cost, and keeps engagement metrics clean. Suppression is a feature, not a failure.

### Measurement loop

Every campaign needs:
- Pre-campaign baseline (segment-level conversion, retention rates)
- Hypothesis (expected lift)
- Measurement window (typically 30-60 days)
- Post-campaign analysis (actual lift vs. expected)
- Iteration (update playbook with measured rates)

Without this loop, segmentation is a one-shot academic exercise.

---

## 7. HubSpot Implementation Checklist

To deploy this playbook:

1. [ ] Configure custom property `Segment` (dropdown: Champions, Loyal Customers, etc.).
2. [ ] Build active segments per RFM segment (filter on Segment property).
3. [ ] Create email templates per segment-persona combination (~20 templates total).
4. [ ] Configure workflows triggered by Segment property changes.
5. [ ] Add suppression rule for Hibernating + Lost (do not enroll in active workflows).
6. [ ] Schedule monthly RFM refresh (cron job hits HubSpot API to update Segment property).
7. [ ] Build dashboard view of segment migration matrix (see Customer Segments page in P2 dashboard).
8. [ ] Define A/B testing protocol for each campaign (sample size, success metric, statistical method).
9. [ ] Document campaign-level KPIs in HubSpot reporting.
10. [ ] Quarterly review meeting: actual lifts vs. projected lifts; iterate playbook.

---

## 8. Versioning and Updates

This playbook is v1.0. It will be updated as:
- Real customer data accumulates (replace heuristic persona inference with explicit signal)
- Campaign A/B tests yield measured lifts (replace projections with measurements)
- New segments emerge (e.g., "Coffra Pass-only customers" once we have enough data)
- Coffra product line evolves (each new product needs segment-specific positioning)

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 26, 2026** | Initial strategy playbook for 11 RFM segments with Coffra-specific tactics, P1 references, and HubSpot deployment checklist. |
