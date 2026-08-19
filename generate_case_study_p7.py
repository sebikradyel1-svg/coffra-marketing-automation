"""
Coffra P7 Case Study PDF Generator
Author: Sebastian Kradyel
Date: July 2026

Generates case study PDF for P7 Lead Intelligence Agent project.
Brand-aligned styling consistent with P1-P5.
"""

from pathlib import Path
import matplotlib

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Font registration
DEJAVU_PATH = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DejaVuSans", str(DEJAVU_PATH / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(DEJAVU_PATH / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", str(DEJAVU_PATH / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", str(DEJAVU_PATH / "DejaVuSans-BoldOblique.ttf")))
registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
                    italic="DejaVuSans-Oblique", boldItalic="DejaVuSans-BoldOblique")

FONT_REGULAR = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"
FONT_ITALIC = "DejaVuSans-Oblique"

# Colors
COFFRA_BROWN = colors.HexColor("#3E2723")
COFFRA_BROWN_LIGHT = colors.HexColor("#6D4C41")
COFFRA_CREAM = colors.HexColor("#EFEBE9")
DARK_GRAY = colors.HexColor("#212121")
MEDIUM_GRAY = colors.HexColor("#616161")
LIGHT_GRAY = colors.HexColor("#E0E0E0")

# Setup
OUTPUT_DIR = Path("case_study")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "P7_Coffra_Lead_Intelligence_Case_Study.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE), pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    topMargin=2.0 * cm, bottomMargin=2.0 * cm,
    title="P7 Coffra Lead Intelligence Agent - Case Study",
    author="Sebastian Kradyel",
)

base_styles = getSampleStyleSheet()
styles = {
    "title": ParagraphStyle("title", parent=base_styles["Heading1"],
        fontName=FONT_BOLD, fontSize=28, textColor=COFFRA_BROWN,
        leading=34, spaceAfter=8, alignment=TA_LEFT),
    "subtitle": ParagraphStyle("subtitle", parent=base_styles["Normal"],
        fontName=FONT_REGULAR, fontSize=14, textColor=MEDIUM_GRAY,
        leading=18, spaceAfter=20, alignment=TA_LEFT),
    "h1": ParagraphStyle("h1", parent=base_styles["Heading1"],
        fontName=FONT_BOLD, fontSize=18, textColor=COFFRA_BROWN,
        leading=22, spaceBefore=18, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=base_styles["Heading2"],
        fontName=FONT_BOLD, fontSize=13, textColor=COFFRA_BROWN_LIGHT,
        leading=17, spaceBefore=14, spaceAfter=6),
    "body": ParagraphStyle("body", parent=base_styles["BodyText"],
        fontName=FONT_REGULAR, fontSize=10, textColor=DARK_GRAY,
        leading=14, spaceAfter=8, alignment=TA_JUSTIFY),
    "body_small": ParagraphStyle("body_small", parent=base_styles["BodyText"],
        fontName=FONT_REGULAR, fontSize=9, textColor=DARK_GRAY,
        leading=12, spaceAfter=6),
    "url_callout": ParagraphStyle("url_callout", parent=base_styles["Normal"],
        fontName=FONT_BOLD, fontSize=12, textColor=COFFRA_BROWN,
        leading=16, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4),
}


def horizontal_rule(color=COFFRA_BROWN, width=1):
    return HRFlowable(width="100%", thickness=width, color=color, spaceBefore=4, spaceAfter=10)


def create_table(data, col_widths=None, header=True, alt_rows=True):
    if col_widths is None:
        col_widths = [None] * len(data[0])
    cell_style = ParagraphStyle("cell", fontName=FONT_REGULAR, fontSize=9,
                                 textColor=DARK_GRAY, leading=12, alignment=TA_LEFT)
    header_cell_style = ParagraphStyle("header_cell", fontName=FONT_BOLD, fontSize=9,
                                        textColor=colors.white, leading=12, alignment=TA_LEFT)
    wrapped_data = []
    for i, row in enumerate(data):
        wrapped_row = []
        for cell in row:
            if isinstance(cell, str):
                style_to_use = header_cell_style if (header and i == 0) else cell_style
                wrapped_row.append(Paragraph(cell, style_to_use))
            else:
                wrapped_row.append(cell)
        wrapped_data.append(wrapped_row)
    table = Table(wrapped_data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, LIGHT_GRAY),
    ]
    if header:
        style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), COFFRA_BROWN),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
        ])
    if alt_rows and header:
        for i in range(2, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), COFFRA_CREAM))
    table.setStyle(TableStyle(style))
    return table


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(MEDIUM_GRAY)
    canvas.drawString(2.2 * cm, 1.2 * cm,
                      "P7 Coffra Lead Intelligence Agent · Sebastian Kradyel · July 2026")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


story = []

# COVER
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Lead Intelligence Agent", styles["title"]))
story.append(Paragraph(
    "A multi-agent pipeline for lead qualification, outreach, and governance — "
    "from ML score to a reviewed, human-approved message",
    styles["subtitle"]))
story.append(horizontal_rule())

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Live Dashboard: <a href='https://coffra-marketing-dashboard.streamlit.app/Lead_Intelligence' "
    "color='#3E2723'>coffra-marketing-dashboard.streamlit.app</a>",
    styles["url_callout"]))
story.append(Spacer(1, 0.4 * cm))

# Metadata
metadata_data = [
    ["Project", "P7 · Coffra Lead Intelligence Agent"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "July 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Stack", "Python · Anthropic Claude API · XGBoost + SHAP · LangChain + FAISS · Streamlit"],
    ["Agents", "4 chained: Qualification → Outreach → Governance → Human Approval"],
    ["Status", "v1.0 — agents + RAG grounding + dashboard integration + case study"],
]
metadata_table = Table(metadata_data, colWidths=[3.5 * cm, 12.5 * cm])
metadata_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
    ("FONTNAME", (1, 0), (1, -1), FONT_REGULAR),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("TEXTCOLOR", (0, 0), (0, -1), COFFRA_BROWN),
    ("TEXTCOLOR", (1, 0), (1, -1), DARK_GRAY),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(metadata_table)

story.append(Spacer(1, 0.5 * cm))

# Executive Summary
story.append(Paragraph("Executive Summary", styles["h1"]))

story.append(Paragraph(
    "P1 built a lead scoring model and a static three-tier segmentation table (Sales-Ready / "
    "Warm MQL / Cold) mapping score to action. That table was a specification, not a system — "
    "someone still had to read a score, decide a tier, draft outreach, check it for compliance, "
    "and get a human to approve it. P7 operationalizes that specification into a live, agentic "
    "pipeline: four chained agents that call the P1 model as a tool, draft grounded outreach, "
    "enforce a governance rubric, and stop at a human-approval checkpoint before anything would "
    "reach a real inbox.",
    styles["body"]))

story.append(Paragraph(
    "The architecture deliberately separates generation from evaluation: a Qualification Agent "
    "scores and routes, an Outreach Agent drafts, and a distinct Governance Reviewer — with no "
    "authority to rewrite, only to verdict — checks the draft claim-by-claim against approved "
    "brand sources before a human ever sees it. This split mirrors current practice in AI "
    "evaluation and governance: the agent that generates content should not be the same agent "
    "that grades it.",
    styles["body"]))

story.append(Paragraph(
    "This case study documents the system honestly, including three real issues found and fixed "
    "during development — a model artifact mismatch, a governance rubric that missed a grounding "
    "failure on its first pass, and a JSON parsing edge case — and a calibration of the "
    "Governance Reviewer against a 50-draft hand-labeled test set (100% recall, 88.2% precision), "
    "because a measured claim about how well a component works is worth more than an "
    "architectural description of it.",
    styles["body"]))

# Key outcomes
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Pipeline architecture", "4 chained agents: Qualification (tool use) → Outreach (RAG) → Governance (claim verification) → Human approval"],
    ["Qualification model", "P1's XGBoost lead scorer wrapped as a Claude tool call; SHAP top-3 factors surfaced in every decision"],
    ["Tier thresholds", "HOT ≥ 0.70 (outreach) · WARM 0.40-0.70 (nurture) · COLD < 0.40 (disqualify)"],
    ["Grounding", "RAG (LangChain + FAISS, local sentence-transformer embeddings) restricts outreach claims to approved brand sources"],
    ["Governance", "Claim-by-claim decomposition, APPROVE/REVISE verdict; any unsupported claim forces REVISE — no holistic pass"],
    ["Governance calibration", "100% recall · 88.2% precision · 92% accuracy against a 50-draft hand-labeled test set (Aug 2026)"],
    ["Live verification", "All 3 test leads (HOT/WARM/COLD) run end-to-end locally and on Streamlit Cloud; both APPROVE and REVISE verdicts observed live"],
    ["Deployment", "Integrated as page 10 of the existing Coffra Streamlit dashboard (P2)"],
]
story.append(create_table(outcomes_data, col_widths=[4 * cm, 12 * cm]))

story.append(Spacer(1, 0.4 * cm))

# PROBLEM STATEMENT AND APPROACH
story.append(Paragraph("Problem Statement and Approach", styles["h1"]))

story.append(Paragraph("The challenge", styles["h2"]))
story.append(Paragraph(
    "A trained model that outputs a probability is not a decisioning system. Between 'the model "
    "says 0.98' and 'a rep sends a message' sit several distinct judgments: which tier does this "
    "score map to, what does that mean for the next action, what should the outreach say, is what "
    "it says actually true, and should a human sign off. Collapsing all of that into a single "
    "'do everything' LLM call makes each judgment unauditable — if the output is wrong, there is "
    "no way to tell whether scoring, drafting, or reviewing failed.",
    styles["body"]))

story.append(Paragraph(
    "P7 addresses this by decomposing the pipeline into agents with narrow, single-purpose "
    "responsibilities, each independently inspectable and independently testable, connected by "
    "structured JSON contracts rather than free-form handoffs.",
    styles["body"]))

story.append(Paragraph("Scope decisions", styles["h2"]))

scope_data = [
    ["Decision", "Choice", "Rationale"],
    ["Agent decomposition", "4 narrow agents, not 1 mega-agent", "Isolates failure points; each agent has an auditable, single responsibility"],
    ["Grounding strategy", "RAG over approved data/brand_sources.md", "Prevents outreach from inventing product or brand claims"],
    ["Governance rigor", "Forced claim-by-claim JSON decomposition, not a holistic pass/fail", "An impressionistic reviewer misses mixed true/false sentences (see Rigor and Limitations)"],
    ["Human checkpoint", "Simulated UI approval; no message is ever actually sent", "Portfolio safety — demonstrates the governance pattern without live-send risk"],
    ["Test leads", "3 fixed synthetic leads (HOT / WARM / COLD)", "Reproducible, deterministic verification of all three tiers and both governance verdicts"],
]
story.append(create_table(scope_data, col_widths=[3.5 * cm, 5.5 * cm, 7 * cm]))

story.append(Paragraph("Methodology principles", styles["h2"]))
story.append(Paragraph(
    "The same disciplines used across P1-P5 apply here: honest documentation of failures rather "
    "than only successes, reproducible test leads with fixed feature vectors, versioned prompts "
    "and code in Git, and — specific to this project — an explicit separation between the agent "
    "that generates content and the agent that evaluates it. That separation is a deliberate "
    "design decision, not an implementation detail: it is the same principle behind independent "
    "AI evaluation and governance layers now standard practice in production AI marketing "
    "systems, where the model producing an output should not also be the sole judge of its "
    "correctness.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# AGENT ARCHITECTURE
story.append(Paragraph("Agent Architecture", styles["h1"]))

story.append(Paragraph(
    "Four agents are chained in sequence, each receiving only the structured output of the "
    "previous step — no shared mutable state, no implicit context:",
    styles["body"]))

architecture_data = [
    ["Agent", "Role", "Technology"],
    ["1. Qualification", "Calls the P1 XGBoost model as a tool (score_lead), interprets the score plus its top-3 SHAP factors, and decides tier (HOT/WARM/COLD) and next action on fixed 0.70/0.40 thresholds", "Claude tool use · XGBoost · SHAP TreeExplainer"],
    ["2. Outreach", "Drafts a personalized first-touch message for HOT leads only, grounded in retrieved brand talking points so it cannot invent product claims", "Claude · RAG (LangChain + FAISS, all-MiniLM-L6-v2 embeddings)"],
    ["3. Governance", "Reviews the draft against a strict rubric: decomposes it into individual claims, checks each against approved sources, evaluates brand voice / banned patterns / compliance / personalization, returns APPROVE or REVISE", "Claude · structured JSON verdict, no rewrite authority"],
    ["4. Human approval", "UI checkpoint: REVISE blocks and routes to revision; APPROVE surfaces Approve & send / Send back for revision — no message is ever actually transmitted", "Streamlit dashboard (page 10)"],
]
story.append(create_table(architecture_data, col_widths=[3 * cm, 8 * cm, 5 * cm]))

story.append(Paragraph("Why the Qualification Agent calls a tool instead of guessing", styles["h2"]))
story.append(Paragraph(
    "The Qualification Agent's system prompt explicitly instructs it to always call score_lead "
    "before deciding a tier — never to estimate the score from intuition — and to fall back to "
    "WARM (not disqualify) if the tool call fails. This keeps the tier decision grounded in the "
    "actual XGBoost output and its SHAP factors rather than in the language model's own, "
    "unverifiable judgment of the lead.",
    styles["body"]))

story.append(Paragraph("Why the Outreach Agent is RAG-grounded", styles["h2"]))
story.append(Paragraph(
    "data/brand_sources.md — the approved talking points, segmentation table, and verified "
    "results from P1 — is chunked (300 characters, 40 overlap) and embedded locally with "
    "sentence-transformers, indexed in FAISS. Each outreach draft retrieves only the top-3 "
    "chunks most relevant to the lead's specific qualification signal, and the system prompt "
    "instructs the agent that any claim not traceable to those chunks must not be stated. This "
    "is the same grounding principle as the Governance Reviewer, applied one step earlier — "
    "reducing the number of ungrounded claims the reviewer has to catch downstream, without "
    "removing the need for the review itself.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# RIGOR AND LIMITATIONS
story.append(Paragraph("Rigor and Limitations", styles["h1"]))

story.append(Paragraph(
    "Three real issues surfaced during development. They are documented here in full because a "
    "process that catches and fixes its own failures is stronger evidence of engineering "
    "judgment than a system presented as having none.",
    styles["body"]))

story.append(Paragraph("Issue 1 — Model artifact mismatch", styles["h2"]))
story.append(Paragraph(
    "The initially saved model artifacts did not reproduce the predictions recorded in "
    "models/sample_predictions_v1.csv — correlation with true_label was 0.10, effectively "
    "random. The mismatch was diagnosed, the model was retrained and re-exported, and the final "
    "artifact reached a correlation of 0.834 against the same held-out predictions. A saved "
    ".joblib file that loads without error is not proof it is the right model — this is why "
    "score_lead's artifacts are checked against a recorded prediction sample rather than trusted "
    "on load.",
    styles["body"]))

story.append(Paragraph("Issue 2 — Governance grounding miss (V1 → V2)", styles["h2"]))
story.append(Paragraph(
    "The first version of the Governance Reviewer's system prompt asked it to evaluate the "
    "outreach draft holistically. On a test draft mixing a real fact with an ungrounded addition "
    "in the same sentence (\"Coffra is a D2C specialty coffee brand\" — true — chained with "
    "\"built for personal ritual, not standardized\" — an invented positioning claim), the V1 "
    "reviewer approved the whole sentence, missing the ungrounded half. The fix was structural, "
    "not cosmetic: the required JSON output was restructured to force claim-by-claim "
    "decomposition — every distinct assertion, even ones joined by a comma in the same sentence, "
    "must be listed and checked individually before any verdict is issued. Any claim marked "
    "unsupported now automatically forces a hard flag and a REVISE verdict; the reviewer can no "
    "longer average a bad claim away against good ones.",
    styles["body"]))
story.append(Paragraph(
    "The fix was confirmed 3/3 consistent in repeated testing, and confirmed again independently "
    "during live verification on Streamlit Cloud, where the Governance Reviewer returned a real "
    "REVISE verdict — catching an unsupported \"sales-ready\" claim the Outreach Agent had "
    "generated — with no test-specific prompting involved. That the failure mode was caught "
    "again, unprompted, in production is stronger evidence of the fix than the original test "
    "suite alone.",
    styles["body"]))

story.append(Paragraph("Calibration of the Governance Reviewer", styles["h2"]))
story.append(Paragraph(
    "Issue 2's fix was originally confirmed by 3/3 consistent runs on a single test draft plus "
    "one unprompted production catch. That is anecdotal evidence: it shows the reviewer can "
    "catch a grounding failure, not how often it does.",
    styles["body"]))
story.append(Paragraph(
    "To measure it, the reviewer was calibrated against a 50-draft test set built from the "
    "actual approved brand sources and labeled by hand: 20 drafts where every claim is directly "
    "supported, 20 with a single planted contradiction (wrong model, wrong platform, wrong "
    "threshold, invented performance figures), and 10 with plausible-sounding but unverifiable "
    "additions — the harder category, since nothing in them is technically false, it simply is "
    "not backed by anything. Labeling policy: a draft passes only if every claim in it is "
    "directly supported; a single contradicted or ungrounded claim makes the whole draft a "
    "REVISE, the same rule the reviewer's own rubric enforces.",
    styles["body"]))
story.append(Paragraph(
    "<b>Result: 100% recall, 88.2% precision, 92% overall accuracy.</b> The reviewer missed none "
    "of the 30 drafts that should have been flagged, including the exact \"built for personal "
    "ritual, not standardized\" phrasing from Issue 2 — confirming that fix holds under "
    "systematic testing rather than only in the original three runs. Four of twenty clean drafts "
    "were flagged unnecessarily.",
    styles["body"]))
story.append(Paragraph(
    "Recall was treated as the metric to optimize: an unsupported claim reaching a customer is a "
    "brand and compliance problem, while an unnecessary flag costs a human reviewer a few "
    "seconds. Erring toward over-flagging is the correct direction for a compliance filter, and "
    "the 88.2% precision reflects a reviewer that reads paraphrase strictly rather than one that "
    "reasons loosely.",
    styles["body"]))
story.append(Paragraph(
    "The calibration process itself required a correction worth noting. The first run returned "
    "100% recall but only 68% precision, which initially looked like an over-strict reviewer. "
    "Inspecting the flagged drafts showed the cause was in the test, not the agent: several "
    "\"clean\" drafts contained personalization claims about lead behaviour, and the harness "
    "passed an empty lead context, so the reviewer had nothing to verify them against and "
    "correctly flagged them. The test set was rebuilt to isolate brand-source grounding alone, "
    "which is what the reviewer is actually responsible for. Verifying personalization claims "
    "against real lead data is a separate test, not yet run.",
    styles["body"]))

story.append(Paragraph("Issue 3 — JSON parsing edge case, and the structural fix", styles["h2"]))
story.append(Paragraph(
    "Asking the model to emit its verdict as free-form JSON text proved fragile in several ways: "
    "on longer claim decompositions the response could be truncated mid-string when it ran out of "
    "the token budget, and the model occasionally produced small escaping quirks — both breaking "
    "json.loads on an otherwise reasonable response. Rather than keep patching the text parser "
    "defensively, the Governance Reviewer was migrated to tool use (function calling): the verdict "
    "schema is now declared as a tool the model must call, so the Anthropic API validates and "
    "returns a structured object directly, with no hand-written JSON parsing left in the code path. "
    "This eliminated the entire class of parsing failures rather than the single reported symptom — "
    "the same principle the Qualification Agent already used for its scoring tool.",
    styles["body"]))

story.append(Paragraph("Known limitations", styles["h2"]))
story.append(Paragraph(
    "The pipeline is verified against 3 fixed synthetic test leads, not a live, arbitrary lead "
    "stream — production deployment would need input validation for free-form leads. The "
    "human-approval step is a UI checkpoint only; no send integration exists, by design, for "
    "this portfolio. Governance evaluates against a fixed brand_sources.md; a real deployment "
    "would need a process for keeping that source of truth current as brand claims change. The "
    "governance calibration measures brand-source grounding only; whether the reviewer correctly "
    "verifies personalization claims against real lead data is untested. The 50-draft set is "
    "also fixed — a production system would need the test set to grow alongside "
    "brand_sources.md as claims change.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# SKILLS DEMONSTRATED AND NEXT STEPS
story.append(Paragraph("Skills Demonstrated and Next Steps", styles["h1"]))

story.append(Paragraph("Skills demonstrated by this project", styles["h2"]))

skills_data = [
    ["Category", "Skills"],
    ["Agentic AI", "Tool use / function calling, multi-agent orchestration, structured JSON contracts between agents"],
    ["AI evaluation & governance", "Generation/evaluation separation, claim-level grounding verification, APPROVE/REVISE verdict design, LLM-as-judge calibration against a hand-labeled test set with precision/recall measurement"],
    ["Retrieval-augmented generation", "LangChain + FAISS, local sentence-transformer embeddings, chunking strategy, top-k retrieval"],
    ["Machine learning", "XGBoost as an agentic tool, SHAP explainability surfaced in natural-language reasoning"],
    ["Prompt engineering", "System prompts enforcing tool-first behavior, safe fallbacks on tool failure, forced decomposition to prevent evaluation shortcuts"],
    ["Debugging & rigor", "Diagnosed and fixed a model artifact mismatch, a governance grounding miss, and a JSON parsing edge case — each documented with root cause and fix"],
    ["Deployment & production rigor", "Streamlit multi-page integration, live verification on Streamlit Cloud including a real production REVISE catch; API rate limiting with exponential backoff, and a live observability dashboard tracking the weekly REVISE-vs-APPROVE governance split"],
    ["Software engineering", "Python 3.13, Anthropic Claude API, joblib model artifacts, Git versioning"],
]
story.append(create_table(skills_data, col_widths=[4 * cm, 12 * cm]))

story.append(Paragraph("Next steps (v1.1 and beyond)", styles["h2"]))
story.append(Paragraph(
    "The following extensions would deepen this project for v1.1:",
    styles["body"]))

next_steps = [
    "<b>Broaden observability.</b> Rate limiting with backoff and a weekly REVISE-vs-APPROVE observability dashboard are now in place; a next step is richer metrics — per-criterion flag rates and latency percentiles — alongside the current verdict trend.",
    "<b>Caching on the 3 test leads.</b> Since the demo leads are fixed, their agent outputs could be cached to reduce latency and API cost for repeat visitors, with a manual refresh option.",
    "<b>Extension to custom leads.</b> Add a form for arbitrary lead input with schema validation against models/feature_spec_v1.json, rather than only the 3 fixed demo leads.",
]

for s in next_steps:
    story.append(Paragraph(f"• {s}", styles["body"]))

story.append(Paragraph("Project trajectory in portfolio", styles["h2"]))
story.append(Paragraph(
    "P7 is the seventh and most recent project in the portfolio. Where P1 established the lead "
    "scoring model and its static segmentation table, P7 closes the loop: it takes that model "
    "off the page and puts it inside a live, auditable decisioning system — scoring, drafting, "
    "reviewing, and checkpointing an outreach decision end-to-end, with the same standard of "
    "honest disclosure applied to the agents' own failure modes as P1-P5 applied to their "
    "models and methods.",
    styles["body"]))

story.append(Spacer(1, 0.6 * cm))
story.append(horizontal_rule())
story.append(Spacer(1, 0.4 * cm))

story.append(Paragraph("Contact", styles["h2"]))
story.append(Paragraph(
    "Sebastian Kradyel · Marketing Master's (9.54 GPA, Babeș-Bolyai University) · "
    "Reșița, Romania",
    styles["body_small"]))
story.append(Paragraph(
    "Live demo: <a href='https://coffra-marketing-dashboard.streamlit.app/' "
    "color='#3E2723'>coffra-marketing-dashboard.streamlit.app</a> · "
    "GitHub: github.com/sebikradyel1-svg",
    styles["body_small"]))

# Build
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF generated: {OUTPUT_FILE}")
print(f"Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
