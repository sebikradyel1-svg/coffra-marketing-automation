"""
Coffra P4 Case Study PDF Generator
Author: Sebastian Kradyel
Date: April 2026

Generates case study PDF for P4 AEO Strategy project.
Brand-aligned styling consistent with P1, P2, P3.
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

OUTPUT_DIR = Path("case_study")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "P4_Coffra_AEO_Case_Study.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE), pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    topMargin=2.0 * cm, bottomMargin=2.0 * cm,
    title="P4 Coffra AEO Strategy - Case Study",
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
                      "P4 Coffra AEO Strategy · Sebastian Kradyel · April 2026")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


story = []

# COVER
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Answer Engine Optimization Strategy", styles["title"]))
story.append(Paragraph(
    "Positioning Coffra for the AI search era — schema, content, and audit framework",
    styles["subtitle"]))
story.append(horizontal_rule())

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Live Dashboard: <a href='https://coffra-marketing-dashboard.streamlit.app/AEO_Analysis' "
    "color='#3E2723'>coffra-marketing-dashboard.streamlit.app</a>",
    styles["url_callout"]))
story.append(Spacer(1, 0.4 * cm))

# Metadata
metadata_data = [
    ["Project", "P4 · Coffra Answer Engine Optimization"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "April 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Stack", "Strategy + Schema.org + Python (Anthropic API for audit) + Streamlit"],
    ["Status", "v1.0 — strategy complete with audit methodology and dashboard integration"],
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
    "P4 addresses a strategic gap in Coffra's marketing system: how to remain visible to "
    "customers in 2026 when AI engines (ChatGPT, Perplexity, Gemini, Copilot, Claude) "
    "increasingly synthesize answers instead of returning blue links. This is the discipline "
    "of Answer Engine Optimization (AEO), the natural evolution of SEO for the AI era.",
    styles["body"]))

story.append(Paragraph(
    "The deliverable comprises four artifacts: a strategic blueprint with six AEO pillars "
    "(docs/11), a copy-paste-ready Schema.org implementation guide covering 12 page types "
    "(docs/12), an automated multi-engine audit notebook (notebooks/06), and a live "
    "dashboard page (dashboard/pages/7_AEO_Analysis.py). Together they define how Coffra "
    "would position itself as a citable authority across AI engines.",
    styles["body"]))

story.append(Paragraph(
    "The work is grounded in current 2026 research: Frase's AEO guide, HubSpot's AEO trends "
    "report, the Princeton GEO empirical study (10,000 queries tested for citation impact), "
    "and recent industry analyses from Surmado, Cubitrek, and Green Flag Digital. Concrete "
    "tactics derive from these sources rather than general principles — for example, the "
    "Princeton finding that expert quotes increase AI citation visibility by 41% directly "
    "shapes Coffra's content priorities.",
    styles["body"]))

# Key outcomes
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Strategic blueprint", "6 AEO pillars + 12-month content calendar + measurement framework"],
    ["Schema implementation", "12 schema types with copy-paste JSON-LD (Organization, Product, FAQ, Recipe, etc.)"],
    ["Audit methodology", "Automated query battery against AI engine API; AI Visibility Score computed"],
    ["Dashboard integration", "AEO Analysis page added to live Streamlit deployment"],
    ["Strategic positioning", "Identified Romanian specialty coffee as under-served AEO niche for Coffra"],
    ["Documentation rigor", "Honest disclosure of limitations; Princeton GEO research cited; assumptions labeled"],
]
story.append(create_table(outcomes_data, col_widths=[5 * cm, 11 * cm]))

story.append(Spacer(1, 0.4 * cm))

# WHY AEO MATTERS
story.append(Paragraph("Why AEO Matters", styles["h1"]))

story.append(Paragraph(
    "The shift from SEO to AEO is not gradual — it is happening now. Concrete data from "
    "April 2026:",
    styles["body"]))

aeo_data = [
    ["Metric", "Value", "Source"],
    ["ChatGPT monthly active users", "883 million", "Frase 2026 AEO Guide"],
    ["ChatGPT daily queries", "2 billion+", "Frase 2026"],
    ["Google AI Overviews coverage", "55% of all searches", "Frase 2026"],
    ["AI-referred sessions growth (YoY)", "+527%", "Mid-2025 industry data"],
    ["Predicted SEO traffic loss by 2026", "-25%", "Gartner forecast"],
    ["Searches ending without click", "65%+", "O8 Agency 2026"],
    ["AI traffic conversion rate vs traditional", "3-4x higher", "Cubitrek 2026"],
]
story.append(create_table(aeo_data, col_widths=[6 * cm, 4 * cm, 6 * cm]))

story.append(Paragraph(
    "For a brand like Coffra (Romanian specialty coffee D2C), this means a customer asking "
    "an AI engine \"what's the best specialty coffee in Romania?\" no longer scrolls through "
    "10 blue links. They get a synthesized answer. If Coffra is not cited in that answer, "
    "the brand effectively does not exist for that query.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# AEO VS SEO
story.append(Paragraph("AEO vs SEO — The Disciplines Coexist", styles["h1"]))

story.append(Paragraph(
    "AEO does not replace SEO. Studies show a 92% correlation between pages ranking in the "
    "top 10 organic results and pages cited in AI Overviews (Surmado 2026). AI engines read "
    "top search results — so strong traditional SEO is the foundation. AEO adds a structural "
    "layer on top: making content extractable and citable by AI engines.",
    styles["body"]))

vs_data = [
    ["Discipline", "Optimizes for", "Primary KPI"],
    ["SEO (Search Engine Optimization)", "Ranking in Google's blue links (positions 1-10)", "Organic traffic"],
    ["AEO (Answer Engine Optimization)", "Being cited when AI engines synthesize answers", "AI citations / visibility share"],
    ["GEO (Generative Engine Optimization)", "Same as AEO; broader umbrella term", "Same as AEO"],
]
story.append(create_table(vs_data, col_widths=[5 * cm, 7 * cm, 4 * cm]))

story.append(Spacer(1, 0.4 * cm))

# SIX PILLARS
story.append(Paragraph("Coffra AEO Strategy — Six Pillars", styles["h1"]))

story.append(Paragraph(
    "The strategy organizes around six pillars, each with a goal and concrete tactics. Full "
    "detail in docs/11_aeo_strategy.md.",
    styles["body"]))

pillars_data = [
    ["#", "Pillar", "Goal", "Key Tactic"],
    ["1", "Authoritative Brand Content", "Establish Coffra as recognized entity in AI knowledge graphs", "Organization schema + consistent facts across web"],
    ["2", "Answer-First Architecture", "Make every page directly extractable as AI answer", "50-Word Rule + Answer Blocks at top of pages"],
    ["3", "E-E-A-T Signals at Scale", "Demonstrate Experience, Expertise, Authority, Trust", "Author bios + expert quotes + cited sources"],
    ["4", "Schema Markup Foundation", "Help AI parse Coffra content unambiguously", "12 schema types deployed (covered in docs/12)"],
    ["5", "Conversational Content", "Match how users ask AI engines (long-tail, natural)", "Prompt research + semantic-triple structure"],
    ["6", "Multi-Channel Reinforcement", "Reinforce brand identity across the web", "GBP + Wikipedia + LinkedIn + industry directories"],
]
story.append(create_table(pillars_data, col_widths=[0.8 * cm, 3.5 * cm, 5 * cm, 6.7 * cm]))

story.append(Spacer(1, 0.4 * cm))

# PRINCETON FINDINGS
story.append(Paragraph("Evidence-Based Tactics — Princeton GEO Research", styles["h1"]))

story.append(Paragraph(
    "The Princeton GEO research (2024) empirically tested 10,000 queries across major AI "
    "engines, measuring how content tactics impact LLM citation probability. The findings "
    "drive Coffra's content priorities:",
    styles["body"]))

princeton_data = [
    ["Tactic", "Impact on AI Citation Visibility"],
    ["Adding expert quotes to content", "+41% citation rate"],
    ["Including statistics with sources", "+30%"],
    ["Adding citations to authoritative sources", "+30%"],
    ["Adding fluency optimization", "Minimal impact"],
    ["Keyword stuffing", "Negative impact"],
]
story.append(create_table(princeton_data, col_widths=[8 * cm, 8 * cm]))

story.append(Paragraph(
    "These findings translate directly into Coffra's content guidelines. Every blog post should "
    "quote a roaster, barista, or coffee scientist. Every claim about Coffra products should "
    "include a specific statistic with attribution. Generic content (filler words, keyword "
    "stuffing) is actively harmful.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# SCHEMA STRATEGY
story.append(Paragraph("Schema Implementation Strategy", styles["h1"]))

story.append(Paragraph(
    "Schema markup is the structural foundation that allows AI engines to parse Coffra content "
    "unambiguously. The implementation guide (docs/12) provides copy-paste-ready JSON-LD for "
    "12 schema types covering every Coffra page type.",
    styles["body"]))

schema_priority = [
    ["Priority", "Schema", "Rationale"],
    ["1", "Organization (homepage)", "Foundation entity for AI knowledge graph"],
    ["2", "Person (founder bio)", "E-E-A-T signal — author authority"],
    ["3", "LocalBusiness (cafés)", "Local search dominance for Timișoara"],
    ["4", "Product (coffee products)", "Direct sales impact via product attributes"],
    ["5", "FAQPage (key pages)", "Highest AEO citation rate — AI quotes FAQ verbatim"],
    ["6", "Article (blog posts)", "Sustained content authority"],
    ["7", "Recipe (brewing guides)", "Niche traffic capture for technique queries"],
    ["8", "Service (Coffra Pass)", "Subscription positioning"],
    ["9", "Review (testimonials)", "Trust signal with aggregateRating"],
    ["10", "Event (cupping sessions)", "Community engagement, local relevance"],
]
story.append(create_table(schema_priority, col_widths=[1.5 * cm, 4.5 * cm, 10 * cm]))

story.append(Paragraph(
    "All schemas have been written with realistic Coffra-specific data: Strada Alba Iulia 1 "
    "Timișoara address, founder Sebastian Kradyel, Ethiopia Gelana Abaya as flagship product, "
    "Coffra Pass at 245 RON. Implementation requires only paste-and-publish.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# AUDIT METHODOLOGY
story.append(Paragraph("Audit Methodology", styles["h1"]))

story.append(Paragraph(
    "Traditional SEO tools cannot measure AEO performance. The audit notebook implements a "
    "multi-engine query battery that quantifies brand visibility across customer journey "
    "stages. Currently tested against the Anthropic Claude API; production version would test "
    "ChatGPT (OpenAI), Perplexity, Google AI Overviews (SerpAPI), Gemini, and Microsoft "
    "Copilot.",
    styles["body"]))

story.append(Paragraph("Query battery", styles["h2"]))

audit_battery = [
    ["Stage", "Example Query"],
    ["Discovery", "What are the best specialty coffee roasters in Romania?"],
    ["Discovery (RO)", "Care sunt cele mai bune cafenele de specialitate din Timișoara?"],
    ["Comparison", "Coffra vs Origo Coffee — which has better single-origin beans?"],
    ["Evaluation", "What are the best coffee subscriptions for V60 enthusiasts in Eastern Europe?"],
    ["Trust", "Is Coffra a reputable specialty coffee brand?"],
    ["Local", "Specialty coffee shops near Strada Alba Iulia Timișoara"],
    ["Product", "How do I brew a Coffra single-origin coffee using V60?"],
]
story.append(create_table(audit_battery, col_widths=[3 * cm, 13 * cm]))

story.append(Paragraph("Metrics computed", styles["h2"]))

story.append(Paragraph(
    "For each response, the audit detects: (1) brand mentioned by name, (2) cited as source URL, "
    "(3) sentiment of mention (positive / neutral / negative / no mention), (4) information "
    "accuracy (flagged for manual review). These aggregate into the AI Visibility Score, "
    "Citation Rate, and Sentiment Score — Coffra's core AEO KPIs.",
    styles["body"]))

story.append(Paragraph(
    "For an unlaunched fictional brand like Coffra, baseline visibility is expected near 0%. "
    "After 90 days of AEO content publication, expect 5-15% for niche queries. After 12-18 "
    "months of sustained investment, expect 25-40% for category-specific queries. The audit "
    "establishes the methodology for tracking this progress.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# STRATEGIC BETS
story.append(Paragraph("Coffra-Specific Strategic Bets", styles["h1"]))

story.append(Paragraph(
    "Beyond the universal AEO playbook, Coffra has specific advantages worth exploiting:",
    styles["body"]))

bets_data = [
    ["Bet", "Description"],
    ["Romanian specialty coffee niche", "Most AEO competition is English-language and US/UK-based. Romanian specialty coffee is under-served. Coffra can capture 60-80% citation share for category-specific Romanian queries within 12 months."],
    ["Founder narrative authority", "Sebastian's authentic story (marketing master's, transition to coffee, hands-on technical interest) is quotable. Building personal LinkedIn presence reinforces both brand and personal entity in AI knowledge graphs."],
    ["Bilingual content advantage", "Producing content in Romanian and English with proper inLanguage schema annotations doubles addressable AI query space — Romanian competition is essentially zero."],
    ["Specialty community endorsement", "Specialty coffee has tight active communities (Reddit r/Coffee, r/espresso). Earning organic mentions in these spaces is high-leverage. AI engines weight community discussions heavily."],
]
story.append(create_table(bets_data, col_widths=[4 * cm, 12 * cm]))

story.append(Spacer(1, 0.4 * cm))

# IMPLEMENTATION PRIORITIES
story.append(Paragraph("Implementation Priorities", styles["h1"]))

story.append(Paragraph(
    "Coffra has limited resources. Priorities are tiered to focus initial effort where AEO "
    "impact is highest:",
    styles["body"]))

priorities_data = [
    ["Tier", "Timeline", "Tasks"],
    ["1 — Must do", "Week 1-4", "Homepage Organization schema, Google Business Profile, founder bio, baseline audit"],
    ["2 — Should do", "Month 2-3", "Product schemas, FAQ pages, customer testimonials, 4 detailed blog posts"],
    ["3 — Nice to have", "Month 4-6", "Original photography, press outreach, recipe schemas, LinkedIn cadence"],
    ["4 — Long-term", "Month 7-12", "Wikipedia/Wikidata presence, industry partnerships, multi-language scaling"],
]
story.append(create_table(priorities_data, col_widths=[3.5 * cm, 3 * cm, 9.5 * cm]))

story.append(Spacer(1, 0.4 * cm))

# SKILLS DEMONSTRATED
story.append(Paragraph("Skills Demonstrated", styles["h1"]))

skills_data = [
    ["Category", "Specific Skills"],
    ["Strategic foresight", "Identified AEO/GEO trend before mainstream adoption; recognized 2026 AI search shift"],
    ["Research synthesis", "Aggregated 9+ industry sources into coherent strategic framework"],
    ["Schema.org expertise", "12 schema types implemented with proper @id linking and validation"],
    ["Content strategy", "Six-pillar AEO framework with 12-month content calendar"],
    ["Measurement design", "AI Visibility Score, Citation Rate, Sentiment Score — new KPI definitions"],
    ["API integration", "Anthropic Claude API for automated multi-query audit"],
    ["Production thinking", "Automated audit, scheduled refresh, dashboard integration"],
    ["Honest disclosure", "Princeton research cited, baseline expectations clear, limitations explicit"],
]
story.append(create_table(skills_data, col_widths=[4 * cm, 12 * cm]))

story.append(Spacer(1, 0.4 * cm))

# LIMITATIONS
story.append(Paragraph("Limitations and Future Work", styles["h1"]))

story.append(Paragraph("Known limitations", styles["h2"]))
story.append(Paragraph(
    "The audit currently tests Claude only; production version requires API access to "
    "ChatGPT, Perplexity, Gemini, Copilot. Sentiment classification uses keyword heuristic; "
    "production should use a proper sentiment model. Information accuracy detection is "
    "manual; ground truth fact base needed for automation. AEO is fluid — best practices "
    "evolve as AI engines change citation algorithms; the strategy must be revisited "
    "quarterly.",
    styles["body"]))

story.append(Paragraph("Future enhancements", styles["h2"]))
story.append(Paragraph(
    "Multi-engine audit expansion (test all 5 major AI engines monthly). Sentiment model "
    "trained on AI response sentiment specifically. Competitor benchmarking (Origo, Tucano) "
    "for relative AEO posture. Historical trend visualization in dashboard once 6+ months "
    "of audit data accumulate. Integration with Google Search Console for AI Overviews "
    "tracking. Schema validation CI/CD to catch regressions automatically.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# CLOSING
story.append(horizontal_rule())
story.append(Paragraph("Connection to Other Projects", styles["h1"]))

story.append(Paragraph(
    "P4 completes the discovery-layer of Coffra's marketing system. Where P1-P3 assumed "
    "customers had already discovered Coffra, P4 addresses how Coffra becomes discoverable "
    "in the AI search era. The four projects together cover the full marketing funnel:",
    styles["body"]))

connection_data = [
    ["Project", "Funnel Stage", "Concern"],
    ["P4 — AEO Strategy", "Discovery (top of funnel)", "How does Coffra become the answer when customers ask AI engines?"],
    ["P1 — Marketing Automation", "Engagement & nurture", "Once discovered, how does Coffra build relationships through emails?"],
    ["P3 — Customer Segmentation", "Retention & growth", "How does Coffra differentiate by customer behavior for higher retention?"],
    ["P2 — Marketing Dashboard", "Measurement & operations", "How does the marketing team see what is happening across all systems?"],
]
story.append(create_table(connection_data, col_widths=[4 * cm, 4 * cm, 8 * cm]))

story.append(Spacer(1, 0.4 * cm))
story.append(horizontal_rule())
story.append(Spacer(1, 0.3 * cm))

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
