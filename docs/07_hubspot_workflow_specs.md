# HubSpot Implementation Specs

**Project:** P1 · Coffra Marketing Automation
**Author:** Sebastian Kradyel
**Date:** April 2026
**Trial Period:** April 25 – May 9, 2026 (HubSpot Marketing Hub Pro 14-day trial)

---

## Executive Overview

This document maps the email design and lead scoring strategy (specified in `docs/04`, `docs/05`, `docs/06`, and the lead scoring notebook) to a working HubSpot implementation. It bridges the gap between strategic design and operational tooling.

The implementation includes:
- 2 buyer personas configured as a custom property and applied to test contacts
- 2 active segments dynamically filtered by persona
- 2 email drafts representing the welcome stage of each persona's nurture journey
- 3 workflows visualizing the timing logic for both nurture sequences and the cart recovery sequence

A transparent note on what was implemented versus what would be deployed in production with full Marketing Hub Pro access is provided in section 7.

---

## 1. Account & Brand Setup

The HubSpot account was configured with Coffra's brand identity to ensure all outbound communication carries consistent visual and operational context.

| Setting | Value |
|---|---|
| Account name | Coffra |
| Time zone | UTC +03:00 Bucharest |
| Date format | DD/MM/YYYY (EU) |
| Currency | RON (123 456,78 RON format) |
| Industry | Food & Beverage |
| Company address | Strada Alba Iulia 1, Timișoara 300077, Romania |
| Brand color (default) | #3E2723 (deep coffee brown) |
| Default font | Lato 13 |
| Connected email | coffra.coffee@gmail.com |

---

## 2. Persona Property

A custom dropdown property `Persona` was applied to the Contact object, with two segmentation values matching the personas defined in the strategy documents.

| Property | Value |
|---|---|
| Object type | Contact |
| Property name | Persona (HubSpot built-in `hs_persona`) |
| Field type | Dropdown select |
| Option 1 | `Connoisseur` (Andrei archetype, EN journey) |
| Option 2 | `Daily Ritualist` (Bianca archetype, RO journey) |

This property drives both the segment membership and the workflow trigger logic.

**Reference:** `docs/02_persona_connoisseur.md`, `docs/03_persona_daily_ritualist.md`

---

## 3. Test Contacts

Two test contacts were created to validate workflow eligibility and email rendering.

| Name | Email | Persona | Lifecycle Stage |
|---|---|---|---|
| Andrei Test-Connoisseur | paulsebastiankradyel@gmail.com | Connoisseur | Subscriber |
| Bianca Test-Ritualist | coffra.coffee@gmail.com | Daily Ritualist | Subscriber |

The two HubSpot sample contacts (Brian Halligan, Maria Johnson) were deleted to maintain a clean test environment.

---

## 4. Active Segments

Two active segments were created to dynamically group contacts by persona. Active segments update automatically as contacts' persona values change.

| Segment Name | Filter | Type | Current Members |
|---|---|---|---|
| Connoisseur Subscribers | Persona is any of Connoisseur | Active | 1 (Andrei) |
| Daily Ritualist Subscribers | Persona is any of Daily Ritualist | Active | 1 (Bianca) |

These segments serve as the audience source for the corresponding marketing emails.

---

## 5. Marketing Email Drafts

To demonstrate visual implementation while keeping scope realistic, two emails (one per persona) were fully built in HubSpot's email editor. The remaining 11 emails (4 nurture per persona + 3 cart recovery for Connoisseur) remain specified in markdown for production deployment.

### 5.1 Connoisseur E1 — Welcome + Sample Pack

| Field | Value |
|---|---|
| Email name | Connoisseur E1 - Welcome + Sample Pack |
| Subject | Ethiopia Gelana just landed. You're in. |
| Preview text | Ethiopia Gelana Abaya. 1850m. Naturally processed. Try 80g on us. |
| Sender | Coffra (paulsebastiankradyel via HubSpot proxy domain) |
| Audience | Connoisseur Subscribers segment |
| Subscription type | Marketing Information |
| Body source | `docs/04_email_copy_connoisseur.md` (Email 1 FINAL v1) |
| Status | Draft |

### 5.2 Daily Ritualist E1 — Welcome

| Field | Value |
|---|---|
| Email name | Daily Ritualist E1 - Welcome |
| Subject | Prima ta cafea la Coffra. Din partea noastră. |
| Preview text | Vino să bem o cafea împreună. Pe noi. În centru, la Coffra. |
| Sender | Coffra |
| Audience | Daily Ritualist Subscribers segment |
| Subscription type | Marketing Information |
| Body source | `docs/05_email_copy_daily_ritualist.md` (Email 1 FINAL v1) |
| Status | Draft |

---

## 6. Workflow Implementations

Three workflows were built to visualize the timing logic for each nurture and recovery sequence. Due to trial limitations (see section 7), the workflows use Delay actions only — in production with Marketing Hub Pro, Send Email actions would be inserted between delays.

### 6.1 Connoisseur Nurture Sequence

**Trigger:** Contact Persona is any of `Connoisseur`
**Re-enrollment:** Off (single pass per contact)

| Step | Action | Duration | Production Equivalent |
|---|---|---|---|
| 1 | Trigger fires | T+0 | Send Email 1: Welcome + Sample Pack |
| 2 | Delay | 3 days | (waiting for Email 2 send) |
| 3 | (Email 2 placeholder) | T+3 | Send Email 2: Origin Story |
| 4 | Delay | 3 days | (waiting for Email 3 send) |
| 5 | (Email 3 placeholder) | T+6 | Send Email 3: V60 Brewing Guide |
| 6 | Delay | 4 days | (waiting for Email 4 send) |
| 7 | (Email 4 placeholder) | T+10 | Send Email 4: Subscription Pitch |
| 8 | Delay | 4 days | (waiting for Email 5 send) |
| 9 | (Email 5 placeholder) | T+14 | Send Email 5: Comparison Test |
| 10 | End | — | Workflow complete |

**Reference:** `docs/04_email_copy_connoisseur.md`

### 6.2 Daily Ritualist Nurture Sequence

**Trigger:** Contact Persona is any of `Daily Ritualist`
**Re-enrollment:** Off

| Step | Action | Duration | Production Equivalent |
|---|---|---|---|
| 1 | Trigger fires | T+0 | Send Email 1: Welcome (RO) |
| 2 | Delay | 3 days | |
| 3 | (Email 2 placeholder) | T+3 | Send Email 2: Meet the People |
| 4 | Delay | 3 days | |
| 5 | (Email 3 placeholder) | T+6 | Send Email 3: Three Rituals |
| 6 | Delay | 4 days | |
| 7 | (Email 4 placeholder) | T+10 | Send Email 4: Coffra Pass |
| 8 | Delay | 4 days | |
| 9 | (Email 5 placeholder) | T+14 | Send Email 5: Community Invitation |
| 10 | End | — | Workflow complete |

**Reference:** `docs/05_email_copy_daily_ritualist.md`

### 6.3 Cart Recovery Sequence (Connoisseur)

**Trigger:** Contact Persona is any of `Connoisseur` (placeholder for production trigger)
**Production Trigger:** Cart abandoned event from Shopify integration
**Re-enrollment:** Off

| Step | Action | Duration | Production Equivalent |
|---|---|---|---|
| 1 | Trigger fires | T+0 | Cart abandoned detected |
| 2 | Delay | 1 hour | |
| 3 | (Email 1 placeholder) | T+1h | Send Email 1: Saving Your Spot |
| 4 | Delay | 23 hours | |
| 5 | (Email 2 placeholder) | T+24h | Send Email 2: Quick Thought |
| 6 | Delay | 48 hours | |
| 7 | (Email 3 placeholder) | T+72h | Send Email 3: Comparison Test |
| 8 | End | — | Workflow complete |

**Reference:** `docs/06_email_copy_cart_recovery.md`

---

## 7. Trial Limitations & Production Roadmap

The HubSpot trial used here is **Sales Hub Pro**, not Marketing Hub Pro. As a result, the following actions are locked behind upgrade prompts:

| Locked Feature | Impact | Production Path |
|---|---|---|
| Send marketing email (workflow action) | Cannot trigger emails from workflows | Marketing Hub Pro at $890/month, or migrate to Brevo (free, includes workflow email actions) |
| Automated marketing emails | Cannot create emails specifically tagged for automation | Same as above |
| Lead scoring (advanced) | Manual property only, no rules engine | Marketing Hub Pro or custom implementation via the lead scoring model in `notebooks/01_lead_scoring_eda_and_model.ipynb` |

**Production deployment plan:**
1. **Option A — HubSpot upgrade:** Marketing Hub Pro replaces all delays with Send Email actions. Estimated migration time: 4 hours.
2. **Option B — Brevo migration:** Free tier supports automation workflows with native email sends. Estimated migration time: 6 hours including audience re-import.

The current implementation prioritizes **logic clarity and visual demonstration** over end-to-end live execution. All email content is production-ready (drafted in HubSpot for E1s, specified in markdown for the rest).

---

## 8. Screenshots Index

All screenshots are stored in `screenshots/hubspot/`. They are referenced throughout the case study (`case_study/P1_Coffra_Case_Study.pdf`).

| File | Subject |
|---|---|
| `email_list.png` | Marketing Email list with both drafts visible |
| `email_editor_connoisseur.png` | Connoisseur E1 email editor with subject and body |
| `email_editor_daily_ritualist.png` | Daily Ritualist E1 email editor with RO content |
| `segments_list.png` | Active segments page with both persona segments |
| `workflows_list.png` | Workflows overview with all three workflows listed |
| `workflow_connoisseur.png` | Connoisseur Nurture workflow canvas (4 delays) |
| `workflow_daily_ritualist.png` | Daily Ritualist Nurture workflow canvas (4 delays) |
| `workflow_cart_recovery.png` | Cart Recovery workflow canvas (3 delays) |
| `Coffra Subject Line Optimizer_1.png` | Subject Optimizer Streamlit UI — main view |
| `Coffra Subject Line Optimizer_2.png` | Subject Optimizer — variants generated |
| `Coffra Subject Line Optimizer_3.png` | Subject Optimizer — scores breakdown |
| `Coffra Subject Line Optimizer_4.png` | Subject Optimizer — winner selection rationale |

---

## 9. Lessons Learned

**What worked:**
- Reusing HubSpot's built-in `hs_persona` property avoided creating a redundant custom field and showed familiarity with HubSpot conventions.
- Designing emails first in markdown (with full versioning and copy decisions log) made HubSpot data entry mechanical and fast — no creative friction during implementation.
- Active segments tied to a single property simplified workflow triggers and kept the data model clean.

**What I would do differently in production:**
- Confirm trial scope (Sales vs Marketing Hub) before activating to avoid mid-build pivots.
- Set up email-sending domain authentication (SPF, DKIM, DMARC) on day 1 — even on free tier — for higher deliverability when transitioning to live sending.
- Build a single visual workflow with placeholder Send Email actions (when available) before scaling to multiple variants, then clone with persona-specific filters.

**Trade-off accepted for portfolio scope:**
- Implementing 13 full emails in HubSpot (5 nurture × 2 personas + 3 cart recovery) was deemed not worth the effort given the locked Send Email action. Two emails (one per persona) were implemented for visual demonstration; the remaining 11 are fully specified in markdown for production deployment.

---

## 10. Trial Cancellation Reminder

Trial expires **May 9, 2026**. Calendar reminder set for **May 7, 2026** to cancel and downgrade the account to Free. All implementation artifacts (screenshots, markdown specs, this document) are preserved post-cancellation.

---

## Versioning

| Version | Date | Changes |
|---|---|---|
| **v1.0** | **April 25, 2026** | Initial specs document covering 14-day trial implementation: brand setup, 2 personas, 2 segments, 2 email drafts, 3 workflows visualizing timing logic, full screenshots index, and production roadmap. |
