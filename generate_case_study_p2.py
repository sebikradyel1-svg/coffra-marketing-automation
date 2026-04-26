"""
Coffra P2 Case Study PDF Generator
Author: Sebastian Kradyel
Date: April 2026

Generates a 4-5 page case study PDF documenting the P2 Coffra Marketing
Analytics Dashboard project. Brand-aligned styling consistent with P1.

Usage:
    python generate_case_study_p2.py
    Output: case_study/P2_Coffra_Dashboard_Case_Study.pdf
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
    PageBreak, Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ============================================================
# FONT REGISTRATION (Romanian diacritics support)
# ============================================================
DEJAVU_PATH = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"

pdfmetrics.registerFont(TTFont("DejaVuSans", str(DEJAVU_PATH / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(DEJAVU_PATH / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", str(DEJAVU_PATH / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", str(DEJAVU_PATH / "DejaVuSans-BoldOblique.ttf")))

registerFontFamily(
    "DejaVuSans",
    normal="DejaVuSans",
    bold="DejaVuSans-Bold",
    italic="DejaVuSans-Oblique",
    boldItalic="DejaVuSans-BoldOblique",
)

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
OUTPUT_FILE = OUTPUT_DIR / "P2_Coffra_Dashboard_Case_Study.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE),
    pagesize=A4,
    leftMargin=2.2 * cm,
    rightMargin=2.2 * cm,
    topMargin=2.0 * cm,
    bottomMargin=2.0 * cm,
    title="P2 Coffra Marketing Dashboard - Case Study",
    author="Sebastian Kradyel",
)

# ============================================================
# STYLES
# ============================================================
base_styles = getSampleStyleSheet()

styles = {
    "title": ParagraphStyle(
        "title", parent=base_styles["Heading1"],
        fontName=FONT_BOLD, fontSize=28, textColor=COFFRA_BROWN,
        leading=34, spaceBefore=0, spaceAfter=8, alignment=TA_LEFT,
    ),
    "subtitle": ParagraphStyle(
        "subtitle", parent=base_styles["Normal"],
        fontName=FONT_REGULAR, fontSize=14, textColor=MEDIUM_GRAY,
        leading=18, spaceBefore=0, spaceAfter=20, alignment=TA_LEFT,
    ),
    "h1": ParagraphStyle(
        "h1", parent=base_styles["Heading1"],
        fontName=FONT_BOLD, fontSize=18, textColor=COFFRA_BROWN,
        leading=22, spaceBefore=18, spaceAfter=10,
    ),
    "h2": ParagraphStyle(
        "h2", parent=base_styles["Heading2"],
        fontName=FONT_BOLD, fontSize=13, textColor=COFFRA_BROWN_LIGHT,
        leading=17, spaceBefore=14, spaceAfter=6,
    ),
    "body": ParagraphStyle(
        "body", parent=base_styles["BodyText"],
        fontName=FONT_REGULAR, fontSize=10, textColor=DARK_GRAY,
        leading=14, spaceBefore=2, spaceAfter=8, alignment=TA_JUSTIFY,
    ),
    "body_small": ParagraphStyle(
        "body_small", parent=base_styles["BodyText"],
        fontName=FONT_REGULAR, fontSize=9, textColor=DARK_GRAY,
        leading=12, spaceAfter=6,
    ),
    "footer": ParagraphStyle(
        "footer", parent=base_styles["Normal"],
        fontName=FONT_REGULAR, fontSize=8, textColor=MEDIUM_GRAY,
        leading=10, alignment=TA_CENTER,
    ),
    "screenshot_caption": ParagraphStyle(
        "screenshot_caption", parent=base_styles["Normal"],
        fontName=FONT_ITALIC, fontSize=8, textColor=MEDIUM_GRAY,
        leading=10, alignment=TA_CENTER, spaceBefore=2, spaceAfter=14,
    ),
    "url_callout": ParagraphStyle(
        "url_callout", parent=base_styles["Normal"],
        fontName=FONT_BOLD, fontSize=12, textColor=COFFRA_BROWN,
        leading=16, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4,
    ),
}

# ============================================================
# HELPERS
# ============================================================

def horizontal_rule(color=COFFRA_BROWN, width=1):
    return HRFlowable(width="100%", thickness=width, color=color,
                      spaceBefore=4, spaceAfter=10)


def screenshot_placeholder(filename, caption, width_cm=15, height_cm=8):
    """Image insertion or placeholder fallback."""
    script_dir = Path(__file__).resolve().parent
    screenshot_path = script_dir / "screenshots" / "dashboard" / filename

    if screenshot_path.exists():
        from PIL import Image as PILImage
        with PILImage.open(screenshot_path) as img:
            aspect = img.height / img.width
        actual_width = width_cm * cm
        actual_height = actual_width * aspect

        max_height = 11 * cm
        if actual_height > max_height:
            actual_height = max_height
            actual_width = actual_height / aspect

        return Image(str(screenshot_path), width=actual_width, height=actual_height)

    # Fallback placeholder
    placeholder_table = Table(
        [[Paragraph(
            f"<b>[SCREENSHOT MISSING]</b><br/><br/>"
            f"Expected file: <font color='#6D4C41'>{filename}</font><br/>"
            f"Path: <font color='#6D4C41'>screenshots/dashboard/{filename}</font><br/>"
            f"Caption: {caption}",
            styles["body_small"]
        )]],
        colWidths=[width_cm * cm], rowHeights=[height_cm * cm],
    )
    placeholder_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COFFRA_CREAM),
        ("BOX", (0, 0), (-1, -1), 1, COFFRA_BROWN_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))
    return placeholder_table


def create_table(data, col_widths=None, header=True, alt_rows=True):
    """Brand-styled table with text wrapping in cells."""
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


# ============================================================
# PAGE FOOTER
# ============================================================

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(MEDIUM_GRAY)
    canvas.drawString(
        2.2 * cm, 1.2 * cm,
        "P2 Coffra Marketing Dashboard · Sebastian Kradyel · April 2026"
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

# ===== COVER + EXECUTIVE SUMMARY =====
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Coffra Marketing Dashboard", styles["title"]))
story.append(Paragraph(
    "A live, branded marketing analytics dashboard with transparent data provenance",
    styles["subtitle"]
))

story.append(horizontal_rule())

# Live URL callout
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Live Demo: <a href='https://coffra-marketing-dashboard.streamlit.app/' color='#3E2723'>"
    "coffra-marketing-dashboard.streamlit.app</a>",
    styles["url_callout"]
))
story.append(Spacer(1, 0.4 * cm))

# Metadata
metadata_data = [
    ["Project", "P2 · Coffra Marketing Analytics Dashboard"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "April 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Live URL", "coffra-marketing-dashboard.streamlit.app"],
    ["Status", "v1.0 — deployed to Streamlit Cloud"],
    ["Stack", "Streamlit · Plotly · pandas · HubSpot Private App API"],
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
    "P2 builds on P1's strategic and operational foundation by delivering a live, deployable "
    "marketing analytics dashboard. The dashboard provides operational visibility across five "
    "domains: lead quality (XGBoost model insights), AI subject line optimization performance, "
    "HubSpot CRM snapshot data, simulated campaign funnel analytics, and a methodology page "
    "with full data provenance disclosure.",
    styles["body"]
))

story.append(Paragraph(
    "The deliverable solves a specific portfolio problem: most marketing portfolios are "
    "static documents (PDFs, presentations, screenshots). A recruiter scanning ten portfolios "
    "remembers the one with a clickable link to a working application. This dashboard is "
    "that link.",
    styles["body"]
))

story.append(Paragraph(
    "The technical approach prioritizes honesty over impressiveness. Rather than fabricating "
    "live campaign data for a fictional brand, the dashboard layers real data (model outputs, "
    "AI tool cache, HubSpot snapshot) with simulated funnel metrics that are clearly labeled "
    "and grounded in published industry benchmarks. The methodology page documents this "
    "approach explicitly.",
    styles["body"]
))

# Quick metrics
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Pages built", "5 (Lead Quality, Subject Optimizer, HubSpot CRM, Campaign Funnel, Methodology)"],
    ["Data sources integrated", "3 real (model artifacts, optimizer cache, HubSpot snapshot) + 1 simulated (clearly labeled)"],
    ["Deployment", "Streamlit Cloud free tier with auto-rebuild on git push"],
    ["Brand consistency", "Light theme + Coffra brown across all pages, matching P1 case study and email design"],
    ["Honest disclosure", "Methodology page documents what is real, snapshot, simulated for every metric shown"],
]
story.append(create_table(outcomes_data, col_widths=[5 * cm, 11 * cm]))

story.append(Spacer(1, 0.4 * cm))

# ===== SECTION: PROBLEM & APPROACH =====
story.append(Paragraph("Problem and Approach", styles["h1"]))

story.append(Paragraph("The portfolio differentiation challenge", styles["h2"]))
story.append(Paragraph(
    "The AI Marketing Specialist job market in 2026 has converged on a familiar set of "
    "portfolio artifacts: persona documents, email copy samples, ML notebooks, and PDF "
    "case studies. These are necessary but no longer differentiating. Recruiters scanning "
    "GitHub repositories of qualified candidates increasingly look for live, deployable "
    "applications that demonstrate production readiness.",
    styles["body"]
))

story.append(Paragraph("Strategic decisions", styles["h2"]))

decisions_data = [
    ["Decision", "Choice", "Rationale"],
    ["Data strategy", "Snapshot over live API", "Stable demo post-trial-expiry; recruiter sees consistent state"],
    ["Real vs simulated data", "Mix with explicit labeling", "Honesty signals senior judgment; fabrication signals junior overreach"],
    ["Theme", "Force light theme via config", "Recruiter sees branded version regardless of system preference"],
    ["Deployment", "Streamlit Cloud free tier", "Zero-cost public URL; auto-rebuild on git push"],
    ["Pages structure", "Multi-page sidebar nav", "Mirrors enterprise dashboards; supports separate concerns per page"],
]
story.append(create_table(decisions_data, col_widths=[3.5 * cm, 5 * cm, 7.5 * cm]))

story.append(Spacer(1, 0.4 * cm))

# ===== SECTION: ARCHITECTURE =====
story.append(Paragraph("Architecture", styles["h1"]))

story.append(Paragraph(
    "The dashboard is a multi-page Streamlit application following standard separation of "
    "concerns. Shared utilities live in <font name='DejaVuSans-Bold'>dashboard/lib/</font> "
    "and individual pages live in <font name='DejaVuSans-Bold'>dashboard/pages/</font>, "
    "auto-discovered by Streamlit's page registry.",
    styles["body"]
))

story.append(Paragraph("File structure", styles["h2"]))

structure_data = [
    ["Path", "Purpose"],
    ["dashboard/streamlit_dashboard.py", "Main entry point, overview page with cross-section metrics"],
    ["dashboard/lib/styling.py", "CSS injection, brand colors, page headers, data disclosure banners"],
    ["dashboard/lib/data_loaders.py", "Cached file I/O for snapshots, model artifacts, optimizer cache"],
    ["dashboard/lib/plots.py", "Brand-styled Plotly chart factories (bar, donut, funnel, gauge, line, histogram)"],
    ["dashboard/pages/1_Lead_Quality.py", "XGBoost model performance, baseline comparison, sample predictions"],
    ["dashboard/pages/2_Subject_Optimizer.py", "Cache analysis, persona coverage, character distribution"],
    ["dashboard/pages/3_HubSpot_CRM.py", "Contacts, segments, persona distribution from snapshot"],
    ["dashboard/pages/4_Campaign_Funnel.py", "Per-persona funnels, engagement decay, cart recovery (simulated)"],
    ["dashboard/pages/5_Methodology.py", "Data provenance disclosure, production roadmap"],
    [".streamlit/config.toml", "Theme configuration (light theme, Coffra brand colors)"],
    ["extract_hubspot_snapshot.py", "One-time HubSpot Private App API extraction script"],
]
story.append(create_table(structure_data, col_widths=[6.5 * cm, 9.5 * cm]))

story.append(Paragraph("Data flow", styles["h2"]))
story.append(Paragraph(
    "All data is read from local files committed to the repository. The HubSpot snapshot is "
    "captured once via the extraction script and stored as JSON. The lead scoring model "
    "artifacts come from the P1 notebook output. The Subject Optimizer cache is generated "
    "during normal use of the P1 tool. No runtime API calls are made by the dashboard, "
    "ensuring it remains functional after the HubSpot trial expires.",
    styles["body"]
))

story.append(Paragraph(
    "This architecture is deliberately simple. A production system would add: scheduled "
    "snapshot refresh, fallback to live API on staleness, authentication, role-based access "
    "control, and a proper data warehouse layer. These extensions are documented in the "
    "Methodology page's production roadmap.",
    styles["body"]
))

# ===== SCREENSHOT =====
story.append(Spacer(1, 0.2 * cm))

story.append(screenshot_placeholder(
    filename="dashboard_overview.png",
    caption="Dashboard overview page with cross-section metrics and navigation",
    width_cm=15,
    height_cm=8,
))

story.append(Spacer(1, 0.4 * cm))

# ===== SECTION: PAGES WALKTHROUGH =====
story.append(Paragraph("Pages Walkthrough", styles["h1"]))

story.append(Paragraph("Lead Quality", styles["h2"]))
story.append(Paragraph(
    "Visualizes the XGBoost lead scoring model from P1. Top section shows ROC-AUC and PR-AUC "
    "as gauge charts for at-a-glance performance. Comparison table below contrasts Logistic "
    "Regression baseline vs XGBoost across cross-validation and held-out test metrics. The "
    "class imbalance disclosure (88% positive class — atypical) is shown explicitly with "
    "mitigations applied (class_weight, scale_pos_weight, PR-AUC reporting). Sample "
    "predictions table shows 20 test set rows mapped to Coffra lead segments (Cold / Warm "
    "MQL / Sales-Ready). Feature engineering section discloses dropped leakage columns and "
    "engineered features.",
    styles["body"]
))

story.append(Paragraph("Subject Optimizer", styles["h2"]))
story.append(Paragraph(
    "Reads the local cache from the P1 Subject Line Optimizer (Claude API responses). Shows "
    "total generations, evaluations, variant count, and estimated USD cost based on token "
    "usage. Persona coverage donut indicates whether the tool has been exercised across both "
    "personas. Strategic angle distribution shows whether the prompt's 5 angles (direct, "
    "curiosity, insider, counter-intuitive, invitation) are balanced. Character length analysis "
    "validates mobile preview compliance (under 50 chars). Recent variants table and selected "
    "winners section provide qualitative review.",
    styles["body"]
))

story.append(Paragraph("HubSpot CRM", styles["h2"]))
story.append(Paragraph(
    "Renders the snapshot extracted from HubSpot Marketing Hub trial via the Private App API. "
    "Includes contact count, segment count, persona distribution donut, and tables of "
    "individual contacts and segments. Persona internal values from HubSpot (persona_1, "
    "persona_2) are mapped to human-readable labels (Connoisseur, Daily Ritualist) in the "
    "loader. A workflows section documents the three workflows configured in HubSpot, with a "
    "note on the 'Send marketing email' lock-out and migration path. Raw snapshot JSON is "
    "available in an expander for transparency.",
    styles["body"]
))

story.append(Paragraph("Campaign Funnel", styles["h2"]))
story.append(Paragraph(
    "The only page using simulated data, clearly labeled with an orange-red disclosure banner. "
    "Two parallel funnels (Connoisseur and Daily Ritualist) model a 14-day nurture campaign "
    "with 500 starting subscribers each. Conversion rates are anchored to Mailchimp 2025 "
    "Food &amp; Beverage benchmarks (22.1% open rate, 2.3% CTR) with a 1.15x premium-brand "
    "uplift factor. Engagement decay charts show realistic open/click trajectories across the "
    "5-email sequence. Cart recovery section models the 3-email recovery sequence with "
    "industry-standard recovery rates (15-25% range). All assumptions are documented inline.",
    styles["body"]
))

story.append(Paragraph("Methodology", styles["h2"]))
story.append(Paragraph(
    "The transparency layer of the dashboard. Documents data provenance per page (real, "
    "snapshot, simulated), data age (when each source was captured and when it goes stale), "
    "what the dashboard does NOT include and why (no real campaign data, no fabricated ROI), "
    "and the production roadmap describing how to scale this into a live system. Designed to "
    "be the page a senior recruiter opens first to assess judgment.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))

# ===== SECTION: TECHNICAL DECISIONS =====
story.append(Paragraph("Notable Technical Decisions", styles["h1"]))

story.append(Paragraph("Snapshot data over live API", styles["h2"]))
story.append(Paragraph(
    "Initially the plan was to query HubSpot API on every page load. After consideration, "
    "this was rejected because: (1) the trial expires in 14 days, after which API calls fail; "
    "(2) recruiters viewing the demo months later would see broken errors; (3) live API adds "
    "latency on every page interaction; (4) snapshot data is reproducible — the extraction "
    "script is committed to the repo and runnable by anyone with their own token.",
    styles["body"]
))

story.append(Paragraph("Theme forcing via config.toml", styles["h2"]))
story.append(Paragraph(
    "Streamlit defaults to user's system theme preference. For a portfolio deliverable, "
    "this is unacceptable — a recruiter on dark mode would see invisible text on light "
    "metric containers. The solution is a <font name='DejaVuSans-Bold'>.streamlit/config.toml"
    "</font> file that forces light theme and applies Coffra brand colors. This file is "
    "committed and applies on Streamlit Cloud automatically.",
    styles["body"]
))

story.append(Paragraph("Cached data loaders", styles["h2"]))
story.append(Paragraph(
    "All file I/O wrapped in Streamlit's <font name='DejaVuSans-Bold'>@st.cache_data</font> "
    "decorator. This avoids re-reading JSON files on every page interaction. For static "
    "snapshot data this is purely a performance optimization with no correctness implications. "
    "For a live system with frequently-updating data, the cache decorator would need TTL "
    "configuration.",
    styles["body"]
))

story.append(Paragraph("Honest disclosure as a feature", styles["h2"]))
story.append(Paragraph(
    "The Methodology page is not a footer afterthought — it is a featured page in the sidebar "
    "navigation. The data disclosure banner pattern (real / snapshot / simulated colored by "
    "type) appears on every relevant page. This signals to a senior reviewer that the author "
    "has thought about data provenance and trustworthiness as a first-class concern, not as "
    "a compliance checkbox.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))

# ===== SECTION: SKILLS DEMONSTRATED =====
story.append(Paragraph("Skills Demonstrated", styles["h1"]))

skills_data = [
    ["Category", "Specific Skills"],
    ["Production deployment", "Streamlit Cloud setup, secrets management, requirements.txt, auto-rebuild on push"],
    ["Multi-page Streamlit", "Page registry, sidebar navigation, shared utilities, config.toml theming"],
    ["Data visualization", "Plotly figure factories, brand-aligned palettes, gauge/funnel/donut/histogram patterns"],
    ["API integration", "HubSpot Private App API, scoped permissions, pagination, error handling"],
    ["Data architecture", "Snapshot vs live trade-off analysis, cached loaders, JSON-based portable artifacts"],
    ["Documentation", "Methodology page, provenance tables, production roadmap, inline assumptions"],
    ["Brand consistency", "Cross-deliverable styling (case study PDF, dashboard, email design), light theme forcing"],
    ["Software hygiene", "Secret management, gitignore discipline, environment templates, dependency pinning"],
]
story.append(create_table(skills_data, col_widths=[4 * cm, 12 * cm]))

story.append(Paragraph("Trade-offs accepted for portfolio scope", styles["h2"]))

tradeoffs = [
    "<b>No authentication.</b> The dashboard is public. A real production deployment would require login.",
    "<b>No automated tests.</b> Manual testing only. Production system would have unit tests for data loaders and integration tests for page rendering.",
    "<b>Single-snapshot.</b> No scheduled refresh. Production would have a cron-based refresh or webhook trigger from HubSpot.",
    "<b>No alerting or monitoring.</b> If a data source breaks, the dashboard fails silently or shows empty visuals. Production would have observability.",
]

for t in tradeoffs:
    story.append(Paragraph(f"• {t}", styles["body"]))

story.append(Paragraph("Production roadmap", styles["h2"]))
story.append(Paragraph(
    "The Methodology page enumerates next steps for promoting this from portfolio to "
    "production: scheduled HubSpot refresh, GA4 integration, attribution model, multi-environment "
    "deployment, role-based access control. None of these were attempted in v1.0 — the goal "
    "was to ship a working demo with honest scope, not to build production infrastructure for "
    "a fictional brand.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))

# ===== CLOSING =====
story.append(horizontal_rule())
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph("Connection to P1 and Future Projects", styles["h1"]))

story.append(Paragraph(
    "P2 demonstrates that the P1 deliverables (lead scoring model, AI subject optimizer, "
    "HubSpot configuration) are not isolated artifacts — they integrate into a coherent "
    "operational system. Future projects in the portfolio will continue this pattern:",
    styles["body"]
))

story.append(Paragraph(
    "P3 (Customer Segmentation) will add RFM analysis and clustering to the lead scoring "
    "foundation. P4 (Recommendation Systems) will use clustering output to drive personalized "
    "product recommendations. P5 (Attribution Modeling) will close the loop by measuring "
    "channel effectiveness across the full marketing system. Each project deliberately "
    "demonstrates a non-overlapping skill cluster while building on prior infrastructure.",
    styles["body"]
))

story.append(Spacer(1, 0.4 * cm))
story.append(horizontal_rule())
story.append(Spacer(1, 0.3 * cm))

story.append(Paragraph("Contact", styles["h2"]))
story.append(Paragraph(
    "Sebastian Kradyel · Marketing Master's (9.54 GPA, Babeș-Bolyai University) · "
    "Reșița, Romania",
    styles["body_small"]
))
story.append(Paragraph(
    "Live demo: <a href='https://coffra-marketing-dashboard.streamlit.app/' color='#3E2723'>"
    "coffra-marketing-dashboard.streamlit.app</a> · "
    "GitHub: github.com/sebikradyel1-svg",
    styles["body_small"]
))

# ============================================================
# BUILD
# ============================================================

doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

print(f"PDF generated: {OUTPUT_FILE}")
print(f"Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
