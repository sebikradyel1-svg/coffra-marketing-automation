"""
Coffra P1 Case Study PDF Generator
Author: Sebastian Kradyel
Date: April 2026

Generates a 6-7 page case study PDF documenting the P1 Coffra Marketing Automation
project. Brand-aligned styling with deep coffee brown accents.

Usage:
    python generate_case_study.py
    Output: case_study/P1_Coffra_Case_Study.pdf
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ============================================================
# FONT REGISTRATION (Unicode support for Romanian diacritics)
# ============================================================
# DejaVu Sans supports all Romanian characters: ă, â, î, ș, ț
# Comes bundled with matplotlib on most systems
import matplotlib
DEJAVU_PATH = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"

pdfmetrics.registerFont(TTFont("DejaVuSans", str(DEJAVU_PATH / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(DEJAVU_PATH / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", str(DEJAVU_PATH / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", str(DEJAVU_PATH / "DejaVuSans-BoldOblique.ttf")))

from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily(
    "DejaVuSans",
    normal="DejaVuSans",
    bold="DejaVuSans-Bold",
    italic="DejaVuSans-Oblique",
    boldItalic="DejaVuSans-BoldOblique",
)

# Font names for use in styles
FONT_REGULAR = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"
FONT_ITALIC = "DejaVuSans-Oblique"

# ============================================================
# BRAND COLORS
# ============================================================
COFFRA_BROWN = colors.HexColor("#3E2723")
COFFRA_BROWN_LIGHT = colors.HexColor("#6D4C41")
COFFRA_CREAM = colors.HexColor("#EFEBE9")
DARK_GRAY = colors.HexColor("#212121")
MEDIUM_GRAY = colors.HexColor("#616161")
LIGHT_GRAY = colors.HexColor("#E0E0E0")

# ============================================================
# DOCUMENT SETUP
# ============================================================
OUTPUT_DIR = Path("case_study")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "P1_Coffra_Case_Study.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE),
    pagesize=A4,
    leftMargin=2.2 * cm,
    rightMargin=2.2 * cm,
    topMargin=2.0 * cm,
    bottomMargin=2.0 * cm,
    title="P1 Coffra Marketing Automation - Case Study",
    author="Sebastian Kradyel",
)

# ============================================================
# STYLES
# ============================================================
base_styles = getSampleStyleSheet()

styles = {
    "title": ParagraphStyle(
        "title",
        parent=base_styles["Heading1"],
        fontName=FONT_BOLD,
        fontSize=28,
        textColor=COFFRA_BROWN,
        leading=34,
        spaceBefore=0,
        spaceAfter=8,
        alignment=TA_LEFT,
    ),
    "subtitle": ParagraphStyle(
        "subtitle",
        parent=base_styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=14,
        textColor=MEDIUM_GRAY,
        leading=18,
        spaceBefore=0,
        spaceAfter=20,
        alignment=TA_LEFT,
    ),
    "h1": ParagraphStyle(
        "h1",
        parent=base_styles["Heading1"],
        fontName=FONT_BOLD,
        fontSize=18,
        textColor=COFFRA_BROWN,
        leading=22,
        spaceBefore=18,
        spaceAfter=10,
    ),
    "h2": ParagraphStyle(
        "h2",
        parent=base_styles["Heading2"],
        fontName=FONT_BOLD,
        fontSize=13,
        textColor=COFFRA_BROWN_LIGHT,
        leading=17,
        spaceBefore=14,
        spaceAfter=6,
    ),
    "h3": ParagraphStyle(
        "h3",
        parent=base_styles["Heading3"],
        fontName=FONT_BOLD,
        fontSize=11,
        textColor=DARK_GRAY,
        leading=14,
        spaceBefore=10,
        spaceAfter=4,
    ),
    "body": ParagraphStyle(
        "body",
        parent=base_styles["BodyText"],
        fontName=FONT_REGULAR,
        fontSize=10,
        textColor=DARK_GRAY,
        leading=14,
        spaceBefore=2,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
    ),
    "body_small": ParagraphStyle(
        "body_small",
        parent=base_styles["BodyText"],
        fontName=FONT_REGULAR,
        fontSize=9,
        textColor=DARK_GRAY,
        leading=12,
        spaceAfter=6,
    ),
    "metadata": ParagraphStyle(
        "metadata",
        parent=base_styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=9,
        textColor=MEDIUM_GRAY,
        leading=12,
        spaceAfter=4,
    ),
    "callout": ParagraphStyle(
        "callout",
        parent=base_styles["BodyText"],
        fontName=FONT_ITALIC,
        fontSize=10,
        textColor=COFFRA_BROWN,
        leading=14,
        spaceBefore=8,
        spaceAfter=8,
        leftIndent=14,
        rightIndent=14,
        borderColor=COFFRA_BROWN_LIGHT,
        borderWidth=0,
        borderPadding=8,
    ),
    "screenshot_caption": ParagraphStyle(
        "screenshot_caption",
        parent=base_styles["Normal"],
        fontName=FONT_ITALIC,
        fontSize=8,
        textColor=MEDIUM_GRAY,
        leading=10,
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=14,
    ),
    "footer": ParagraphStyle(
        "footer",
        parent=base_styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=8,
        textColor=MEDIUM_GRAY,
        leading=10,
        alignment=TA_CENTER,
    ),
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def horizontal_rule(color=COFFRA_BROWN, width=1):
    return HRFlowable(
        width="100%", thickness=width, color=color,
        spaceBefore=4, spaceAfter=10
    )


def screenshot_placeholder(filename, caption, width_cm=15, height_cm=8):
    """
    Includes the actual screenshot if it exists in screenshots/hubspot/.
    Falls back to a placeholder box if the file is not found.

    The script auto-resolves the path relative to the script location, so it works
    when run from the repo root: python generate_case_study.py
    """
    # Resolve screenshot path relative to script location
    script_dir = Path(__file__).resolve().parent
    screenshot_path = script_dir / "screenshots" / "hubspot" / filename

    if screenshot_path.exists():
        # Real image — calculate proper height from aspect ratio
        from PIL import Image as PILImage
        with PILImage.open(screenshot_path) as img:
            aspect = img.height / img.width
        actual_width = width_cm * cm
        actual_height = actual_width * aspect

        # Cap maximum height to keep layout sane
        max_height = 11 * cm
        if actual_height > max_height:
            actual_height = max_height
            actual_width = actual_height / aspect

        elements = [
            Image(str(screenshot_path), width=actual_width, height=actual_height),
            Paragraph(caption, styles["screenshot_caption"]),
        ]

        # Wrap in a table to keep image + caption together on same page
        wrapper = Table([[el] for el in elements], colWidths=[actual_width])
        wrapper.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return wrapper

    # Fallback: placeholder box if screenshot is missing
    placeholder_table = Table(
        [[
            Paragraph(
                f"<b>[SCREENSHOT MISSING]</b><br/><br/>"
                f"Expected file: <font color='#6D4C41'>{filename}</font><br/>"
                f"Path: <font color='#6D4C41'>screenshots/hubspot/{filename}</font><br/>"
                f"Caption: {caption}",
                styles["body_small"]
            )
        ]],
        colWidths=[width_cm * cm],
        rowHeights=[height_cm * cm],
    )
    placeholder_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COFFRA_CREAM),
        ("BOX", (0, 0), (-1, -1), 1, COFFRA_BROWN_LIGHT),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))
    return placeholder_table


def create_table(data, col_widths=None, header=True, alt_rows=True):
    """Creates a styled table with brand colors. Wraps cell text in Paragraph for proper line breaking."""
    if col_widths is None:
        col_widths = [None] * len(data[0])

    # Cell text style for body cells (wraps automatically)
    cell_style = ParagraphStyle(
        "cell",
        fontName=FONT_REGULAR,
        fontSize=9,
        textColor=DARK_GRAY,
        leading=12,
        alignment=TA_LEFT,
    )
    header_cell_style = ParagraphStyle(
        "header_cell",
        fontName=FONT_BOLD,
        fontSize=9,
        textColor=colors.white,
        leading=12,
        alignment=TA_LEFT,
    )

    # Wrap each cell content in a Paragraph
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


# ============================================================
# PAGE FOOTER
# ============================================================

def add_page_number(canvas, doc):
    """Adds page number and brand to footer."""
    canvas.saveState()
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(MEDIUM_GRAY)
    canvas.drawString(
        2.2 * cm, 1.2 * cm,
        f"P1 Coffra Marketing Automation · Sebastian Kradyel · April 2026"
    )
    canvas.drawRightString(
        A4[0] - 2.2 * cm, 1.2 * cm,
        f"Page {doc.page}"
    )
    canvas.restoreState()


# ============================================================
# CONTENT BUILD
# ============================================================

story = []

# ===== PAGE 1: COVER + EXECUTIVE SUMMARY =====

story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Coffra Marketing Automation", styles["title"]))
story.append(Paragraph(
    "Full-funnel lead nurture and cart abandonment recovery for a fictional D2C specialty coffee brand",
    styles["subtitle"]
))

story.append(horizontal_rule())

# Metadata table
metadata_data = [
    ["Project", "P1 · Coffra Marketing Automation"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "April 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Status", "v1.0 — complete (live A/B testing deferred to v1.1)"],
    ["Project type", "Portfolio project — fictional brand, real methodology"],
]
metadata_table = Table(metadata_data, colWidths=[4 * cm, 12 * cm])
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

story.append(Spacer(1, 0.6 * cm))

# Executive summary
story.append(Paragraph("Executive Summary", styles["h1"]))

story.append(Paragraph(
    "This project takes a fictional specialty coffee brand (Coffra, Timișoara) from strategy to "
    "operational marketing automation. The deliverables include 13 production-ready emails across "
    "two persona-specific journeys (10 nurture + 3 cart recovery), a Romanian-and-English bilingual "
    "voice system, an XGBoost lead scoring model with SHAP explainability, an AI-powered Subject "
    "Line Optimizer built on the Anthropic Claude API, a HubSpot workflow implementation, and a "
    "full A/B testing methodology specification.",
    styles["body"]
))

story.append(Paragraph(
    "The project was scoped deliberately to demonstrate the full stack of skills required for an "
    "AI Marketing Specialist role: persona-driven copy craft, segmentation logic, marketing "
    "technology fluency, machine learning integration, AI tooling development, and statistical "
    "literacy. Where live execution was impractical (consent-based pilot list for A/B testing, "
    "production email sending on trial tooling), methodology and limitations are documented "
    "transparently rather than fabricated.",
    styles["body"]
))

story.append(Paragraph(
    "Coffra is fictional by design. This avoids privacy and legal complications of using real "
    "brand or customer data while preserving full methodological rigor. All datasets are public "
    "(Kaggle), all copy is original, and all strategic decisions are documented as fictional "
    "design choices.",
    styles["body"]
))

# Key outcomes box
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Persona system", "2 distinct personas (EN + RO journeys) with rhetorical separation by sender"],
    ["Email copy", "13 emails final, full versioning, copy decisions log, voice consistency"],
    ["Lead scoring model", "XGBoost; Test ROC-AUC 0.78; data leakage audit; SHAP explainability"],
    ["AI Subject Optimizer", "5 variants generated + scored on 4 dimensions; cached; Streamlit UI"],
    ["HubSpot implementation", "Brand setup, segments, workflows visualized; trial limitations disclosed"],
    ["A/B methodology", "Pre-registered design with chi-square analysis; deferred for live execution"],
]
story.append(create_table(outcomes_data, col_widths=[5 * cm, 11 * cm]))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 2: PROBLEM STATEMENT & APPROACH =====

story.append(Paragraph("Problem Statement and Approach", styles["h1"]))

story.append(Paragraph("The challenge", styles["h2"]))
story.append(Paragraph(
    "Specialty coffee brands face a structural marketing challenge: their target customers are "
    "fragmented across two psychographic poles. The 'Connoisseur' segment values technical "
    "transparency, micro-lot sourcing, roast freshness, and brewing rigor. The 'Daily Ritualist' "
    "segment values atmosphere, social context, accessibility, and aesthetic experience. A "
    "single voice cannot credibly serve both — the language that signals competence to a "
    "Connoisseur reads as gatekeeping to a Ritualist; the warmth that welcomes a Ritualist reads "
    "as fluff to a Connoisseur.",
    styles["body"]
))

story.append(Paragraph(
    "This project addresses that challenge by building two parallel marketing automation "
    "journeys, each with its own copy voice, sender identity, conversion model, and incentive "
    "structure — all sharing a common operational stack (segmentation, scoring, AI tooling).",
    styles["body"]
))

story.append(Paragraph("Scope decisions", styles["h2"]))

scope_data = [
    ["Decision", "Choice", "Rationale"],
    ["Persona count", "2 (Connoisseur + Daily Ritualist)", "Strategic differentiation > sample size"],
    ["Languages", "EN + RO (one per persona)", "Demonstrates multi-locale capability"],
    ["Sender identity", "Sebastian (Roaster) vs Ioana (Community Manager)", "Rhetorical separation"],
    ["Discount discipline", "Asymmetric: none for Connoisseur, modest for Ritualist", "Persona-true positioning"],
    ["AI tool integration", "Custom Claude API tool, not just chat", "Demonstrates programmatic AI"],
    ["Live A/B execution", "Deferred to v1.1", "No invented results without consent-based list"],
]
story.append(create_table(scope_data, col_widths=[3.5 * cm, 5.5 * cm, 7 * cm]))

story.append(Paragraph("Methodology principles", styles["h2"]))
story.append(Paragraph(
    "Five disciplines were enforced throughout the project to maintain professional rigor:",
    styles["body"]
))

principles = [
    "<b>Honest documentation.</b> Every limitation is disclosed. No invented metrics, no overstated claims, no fabricated test results.",
    "<b>Reproducibility.</b> Fixed random seeds, pinned dependencies, public datasets, JSON-cached API responses.",
    "<b>Versioning.</b> All copy, code, and decisions are versioned in Git with explicit change logs in each document.",
    "<b>Citation.</b> Industry benchmarks (Mailchimp 2025) cited with source attribution. No 'industry suggests' without source.",
    "<b>Transparency over persuasion.</b> Where the AI tool's claim cannot be validated (e.g., predicted open rates), the limitation is stated explicitly rather than packaged as a strength.",
]

for p in principles:
    story.append(Paragraph(f"• {p}", styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 3: PERSONA STRATEGY =====

story.append(Paragraph("Persona Strategy", styles["h1"]))

story.append(Paragraph(
    "The two personas are intentionally non-overlapping in psychographic profile, language "
    "preference, and decision criteria. This forces the marketing system to demonstrate "
    "sophisticated segmentation rather than shallow personalization.",
    styles["body"]
))

# Side-by-side comparison
comparison_data = [
    ["Dimension", "The Connoisseur (Andrei)", "The Daily Ritualist (Bianca)"],
    ["Age", "32", "30"],
    ["Profession", "Senior Software Engineer (Timișoara)", "Senior in NGO youth work (Reșița)"],
    ["Income", "8,000–20,000 RON/month", "~5,000 RON/month"],
    ["Brewing setup", "V60, Aeropress, Comandante grinder", "Nespresso at home, café-goer"],
    ["Information sources", "James Hoffmann, Sprudge, r/espresso", "Instagram, TikTok, lifestyle blogs"],
    ["Decision driver", "Process transparency, micro-lot sourcing", "Atmosphere, social context, aesthetics"],
    ["Conversion model", "Online beans purchase + subscription", "Foot traffic + aspirational Pass purchase"],
    ["Communication preference", "English (consumes global content)", "Romanian (local)"],
    ["Sender identity", "Sebastian, Roaster & Founder", "Ioana, Community Manager"],
    ["Tone register", "Technical-mentor, peer-to-peer", "Warm-conversational, invitational"],
]
story.append(create_table(comparison_data, col_widths=[3.5 * cm, 6.25 * cm, 6.25 * cm]))

story.append(Paragraph("Operational implications", styles["h2"]))
story.append(Paragraph(
    "These differences cascade into every operational layer of the marketing system. The "
    "Connoisseur receives a 14-day nurture sequence focused on roast date transparency, lot "
    "selection rigor, and brewing technique — followed by a no-discount comparison test offer. "
    "The Daily Ritualist receives a parallel 14-day sequence focused on staff personalities, "
    "ritual-by-time-of-day scenarios, and aspirational Coffra Pass positioning — with an "
    "asymmetric 5% discount available only in the late stage. Both sequences end with explicit "
    "graceful exit promises that respect subscriber autonomy.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 4: EMAIL DESIGN SYSTEM =====

story.append(Paragraph("Email Design System", styles["h1"]))

story.append(Paragraph(
    "Thirteen emails were written across three sequences: 5 Connoisseur nurture (English), 5 "
    "Daily Ritualist nurture (Romanian), and 3 Connoisseur cart recovery (English). Each email "
    "is documented with full copy decisions log, technical specs (subject length, character "
    "counts, mobile preview test), and operational notes for production deployment.",
    styles["body"]
))

# Email overview table
email_overview = [
    ["#", "Sequence", "Email", "Timing", "Strategic Move"],
    ["1", "C-Nurture", "Welcome + Sample Pack", "T+0", "Free Discovery Pack on first order"],
    ["2", "C-Nurture", "Origin Story (Gelana)", "T+3", "Demonstrate sourcing rigor"],
    ["3", "C-Nurture", "V60 Brewing Guide", "T+6", "Technical value delivery"],
    ["4", "C-Nurture", "Subscription Pitch", "T+10", "Risk-reversal trial"],
    ["5", "C-Nurture", "Comparison Test", "T+14", "Final no-discount value escalation"],
    ["6", "DR-Nurture", "Welcome + First Coffee", "T+0", "RO welcome, free first café visit"],
    ["7", "DR-Nurture", "Meet the People", "T+3", "Humanize via 3 named staff"],
    ["8", "DR-Nurture", "Three Rituals", "T+6", "Lifestyle scenario projection"],
    ["9", "DR-Nurture", "Coffra Pass", "T+10", "Aspirational, not transactional"],
    ["10", "DR-Nurture", "Community Invitation", "T+14", "Cupping + brunch event + graceful exit"],
    ["11", "C-Cart", "Saving Your Spot", "+1h", "Calm reminder, real scarcity"],
    ["12", "C-Cart", "Quick Thought", "+24h", "Free shipping + sample upgrade"],
    ["13", "C-Cart", "Comparison Test (final)", "+72h", "Risk reversal + graceful exit"],
]
story.append(create_table(email_overview, col_widths=[1 * cm, 2.5 * cm, 4.5 * cm, 1.5 * cm, 6.5 * cm]))

story.append(Paragraph("Voice consistency mechanism", styles["h2"]))
story.append(Paragraph(
    "Each email follows a strict voice protocol enforced via a copy decisions log:",
    styles["body"]
))

voice_table = [
    ["Persona", "Voice anchors", "Forbidden register"],
    ["Connoisseur", "Technical specifics, peer-tone, observational humor, founder accessibility", "Generic premium language, urgency manipulation, discount-driven pitches"],
    ["Daily Ritualist", "Permission framing, sensory detail, 'normalitate' as luxury, anti-pretentious", "Buzzwords ('wellness', 'family'), false intimacy, aggressive upsell"],
]
story.append(create_table(voice_table, col_widths=[3 * cm, 6 * cm, 7 * cm]))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 5: AI SUBJECT LINE OPTIMIZER =====

story.append(Paragraph("AI Subject Line Optimizer", styles["h1"]))

story.append(Paragraph(
    "A custom Python tool built on the Anthropic Claude API that generates 5 distinct subject "
    "line variants for a given email brief and scores each on 4 dimensions. The tool "
    "demonstrates programmatic AI integration — beyond chat-based prompting — with production "
    "patterns including caching, error handling, and structured outputs.",
    styles["body"]
))

story.append(Paragraph("Architecture", styles["h2"]))

story.append(Paragraph(
    "Two-stage pipeline (generator + critic) separated to reduce single-prompt bias:",
    styles["body"]
))

architecture_data = [
    ["Stage", "Function", "Output"],
    ["1. Generator", "Generates 5 variants using 5 distinct strategic angles (direct, curiosity, insider, counter-intuitive, invitation)", "List of variants with rationale"],
    ["2. Critic", "Independently scores each variant on 4 dimensions (clarity, intrigue, brand fit, mobile readability)", "Scores 0-10 per dimension, total /40"],
    ["Cache", "SHA-256 hashes (persona + brief + version + model) to avoid duplicate API calls", "JSON files in cache/"],
    ["UI", "Streamlit web app with persona selector, example briefs, live results display", "Browser at localhost:8501"],
]
story.append(create_table(architecture_data, col_widths=[2.5 * cm, 8 * cm, 5.5 * cm]))

story.append(Paragraph("Sample output", styles["h2"]))

story.append(screenshot_placeholder(
    filename="Coffra Subject Line Optimizer_2.png",
    caption="Subject Line Optimizer UI showing 5 generated variants with scores and winner",
    width_cm=15,
    height_cm=8
))

story.append(Paragraph("Honest framing of capabilities", styles["h2"]))
story.append(Paragraph(
    "The tool produces qualitative scoring grounded in persona constraints, not predicted open "
    "rates. A future v2 could add open rate prediction by integrating industry benchmarks "
    "(Mailchimp 2025: Food & Beverage avg 22.1%) — explicitly documented as next steps. The "
    "current scoring quality is bounded by the Claude model's understanding of persona-specific "
    "marketing copy, which the tool's prompts attempt to scaffold via explicit forbidden words "
    "and tone keyword lists.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 6: LEAD SCORING MODEL =====

story.append(Paragraph("Lead Scoring Model", styles["h1"]))

story.append(Paragraph(
    "A production-grade lead scoring model built in scikit-learn and XGBoost on the Kaggle "
    "Predict Conversion in Digital Marketing dataset (8,000 records). The model demonstrates "
    "the full ML lifecycle: data quality audit, feature engineering, baseline comparison, "
    "explainability, and saved artifacts for deployment.",
    styles["body"]
))

story.append(Paragraph("Critical move: data leakage audit", styles["h2"]))
story.append(Paragraph(
    "Before any modeling, the dataset was audited for data leakage — features that encode the "
    "target variable. Three columns were dropped before training: `ConversionRate` (direct "
    "leakage), `ClickThroughRate` (likely leakage), and `CustomerID` (identifier without "
    "predictive signal). Two zero-variance columns (`AdvertisingPlatform`, `AdvertisingTool`) "
    "were also removed. Documenting this audit explicitly is what separates a production-ready "
    "model from a notebook model.",
    styles["body"]
))

story.append(Paragraph("Results", styles["h2"]))

results_data = [
    ["Model", "CV ROC-AUC (mean ± std)", "Test ROC-AUC", "Test PR-AUC"],
    ["Logistic Regression (baseline)", "0.7671 ± 0.0148", "0.7643", "0.9441"],
    ["XGBoost (production candidate)", "0.7813 ± 0.0149", "0.7843", "0.9440"],
]
story.append(create_table(results_data, col_widths=[5 * cm, 4.5 * cm, 3 * cm, 3 * cm]))

story.append(Paragraph(
    "XGBoost outperforms the logistic baseline by approximately 2 ROC-AUC points. In the "
    "context of an 88/12 class imbalance (note: dataset reports atypically high conversion "
    "rate, documented as limitation), this is a modest but real improvement that justifies "
    "the additional complexity.",
    styles["body"]
))

story.append(Paragraph("SHAP explainability", styles["h2"]))

story.append(Paragraph(
    "SHAP values provide both global feature importance and per-prediction explanations. The "
    "top contributing features align with marketing intuition: engagement metrics "
    "(WebsiteVisits, EmailClicks, EmailOpens) and the engineered EngagementScore dominate the "
    "predictions. This validates that the model uses sensible signals rather than spurious "
    "patterns — essential for trust in production deployment and for regulatory compliance. "
    "Full SHAP analysis (global summary plot, beeswarm plot, individual prediction "
    "explanations) is available in the lead scoring notebook at "
    "<font color='#6D4C41'>notebooks/01_lead_scoring_eda_and_model.ipynb</font>.",
    styles["body"]
))

story.append(Paragraph("Coffra mapping", styles["h2"]))

mapping_data = [
    ["Lead Score", "Segment", "Action"],
    ["80-100", "High (Sales-Ready)", "Immediate handoff via internal task; personal email from Sebastian"],
    ["40-80", "Medium (Warm MQL)", "Accelerated nurture; weekly contact; activation incentive"],
    ["0-40", "Low (Cold)", "Standard nurture; 2-4 week cadence"],
]
story.append(create_table(mapping_data, col_widths=[3 * cm, 4 * cm, 9 * cm]))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 7: HUBSPOT IMPLEMENTATION + LIMITATIONS =====

story.append(Paragraph("HubSpot Implementation and Honest Limitations", styles["h1"]))

story.append(Paragraph(
    "HubSpot Marketing Hub trial (14 days) was used to implement the operational layer of the "
    "marketing system. Brand identity, custom property for persona segmentation, dynamic "
    "segments, marketing email drafts, and three workflows visualizing nurture and cart "
    "recovery timing logic were all built in HubSpot. Screenshots are committed to the "
    "repository and referenced in this case study.",
    styles["body"]
))

story.append(screenshot_placeholder(
    filename="workflow_connoisseur.png",
    caption="HubSpot Connoisseur Nurture workflow with 4 delays representing email cadence (T+3, T+6, T+10, T+14)",
    width_cm=15,
    height_cm=7
))

story.append(Paragraph("What was implemented", styles["h2"]))

implementation_data = [
    ["Layer", "Status"],
    ["Brand setup (account, currency, timezone, color)", "Complete"],
    ["Custom property: Persona (Connoisseur / Daily Ritualist)", "Complete"],
    ["Test contacts with persona values", "Complete (2 contacts)"],
    ["Active segments (filter on persona)", "Complete (2 segments)"],
    ["Marketing email drafts", "2 of 13 emails fully built; 11 specified in markdown"],
    ["Workflows: Connoisseur Nurture, DR Nurture, Cart Recovery", "Complete (visual logic, 3 workflows)"],
]
story.append(create_table(implementation_data, col_widths=[8 * cm, 8 * cm]))

story.append(Paragraph("Trial limitation: locked actions", styles["h2"]))
story.append(Paragraph(
    "The HubSpot trial provided was Sales Hub Pro, not Marketing Hub Pro. As a result, the "
    "'Send marketing email' action within workflows was locked behind upgrade. The pragmatic "
    "decision was to visualize the timing logic with Delay actions only, mark each delay's "
    "intended email recipient in the case study mapping, and document the production migration "
    "path. This is the right portfolio decision: it demonstrates strategic thinking and tool "
    "fluency without inventing capability.",
    styles["body"]
))

story.append(Paragraph(
    "Production migration would unlock email actions either by (a) upgrading to HubSpot "
    "Marketing Hub Pro, or (b) migrating the implementation to Brevo (free tier supports "
    "automation workflows with native email sends). Migration estimated at 4-6 hours including "
    "audience re-import and workflow rebuild.",
    styles["body"]
))

story.append(Paragraph("A/B testing methodology", styles["h2"]))
story.append(Paragraph(
    "A complete A/B testing methodology is documented in the repository (docs/08_ab_testing_"
    "methodology.md). It specifies the hypothesis (H1: AI-optimized variant > manual baseline), "
    "sample size (n=200 with power calculation), randomization protocol, statistical analysis "
    "(chi-square test of independence + Cramér's V effect size), decision rules, and "
    "limitations (Apple Mail Privacy Protection inflation, single-shot test caveats). Live "
    "execution is deferred to v1.1 pending a consent-based pilot list of sufficient size.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))

# ===== PAGE 8: SKILLS & NEXT STEPS =====

story.append(Paragraph("Skills Demonstrated and Next Steps", styles["h1"]))

story.append(Paragraph("Skills demonstrated by this project", styles["h2"]))

skills_data = [
    ["Category", "Skills"],
    ["Strategy", "Persona segmentation, JTBD reasoning, asymmetric incentive design, voice differentiation"],
    ["Copywriting", "Bilingual (EN/RO native), 13 emails versioned, copy decisions log, mobile preview testing"],
    ["Marketing Tech", "HubSpot configuration end-to-end (brand, segments, properties, workflows, emails)"],
    ["AI Engineering", "Anthropic Claude API integration, prompt engineering, two-stage pipeline, JSON caching"],
    ["Machine Learning", "XGBoost, Logistic Regression baseline, cross-validation, SHAP explainability, leakage audit"],
    ["Statistics", "Chi-square test, effect size (Cramér's V), power calculation, pre-registration discipline"],
    ["Software", "Python 3.11, pandas, scikit-learn, Streamlit, ReportLab, Git versioning"],
    ["Documentation", "Markdown specifications, PDF case study, README navigation, screenshot organization"],
]
story.append(create_table(skills_data, col_widths=[3.5 * cm, 12.5 * cm]))

story.append(Paragraph("Next steps (v1.1 and beyond)", styles["h2"]))
story.append(Paragraph(
    "The following extensions would deepen this project for v1.1:",
    styles["body"]
))

next_steps = [
    "<b>Live A/B test execution.</b> Run the methodology specified in docs/08 with a 200-person consent-based pilot list. Report results with full disclosure including effect size and limitations.",
    "<b>Production migration to Brevo.</b> Migrate workflows from HubSpot trial to Brevo free tier; enable native send actions; run end-to-end automation test.",
    "<b>v2 Subject Line Optimizer.</b> Add predicted open rate using industry benchmark anchoring; train a small custom regressor on labeled subject line performance data.",
    "<b>Lead scoring re-training.</b> When real Coffra subscriber data accumulates (500+ contacts with conversion labels), retrain monthly with feature drift monitoring via Evidently.",
    "<b>Multi-armed bandit testing.</b> Replace fixed A/B with Thompson sampling for dynamic allocation toward winning variant.",
]

for s in next_steps:
    story.append(Paragraph(f"• {s}", styles["body"]))

story.append(Paragraph("Project trajectory in portfolio", styles["h2"]))
story.append(Paragraph(
    "This is project 1 of 6 in a portfolio targeting AI Marketing Specialist roles. Project 2 "
    "(Customer Segmentation with RFM and clustering) builds on the lead scoring foundation "
    "with deeper data analysis. Project 3 (Marketing Analytics Dashboard) adds visualization "
    "and KPI monitoring. Projects 4-6 expand into recommendation systems, attribution "
    "modeling, and competitive SEO/content strategy. Each project deliberately demonstrates a "
    "non-overlapping skill cluster.",
    styles["body"]
))

story.append(Spacer(1, 0.6 * cm))
story.append(horizontal_rule())
story.append(Spacer(1, 0.4 * cm))

story.append(Paragraph("Contact", styles["h2"]))
story.append(Paragraph(
    "Sebastian Kradyel · Marketing Master's (9.54 GPA, Babeș-Bolyai University) · "
    "Reșița, Romania",
    styles["body_small"]
))
story.append(Paragraph(
    "GitHub: github.com/sebikradyel1-svg · LinkedIn link available on GitHub profile",
    styles["body_small"]
))

# ============================================================
# BUILD
# ============================================================

doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

print(f"PDF generated: {OUTPUT_FILE}")
print(f"Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
