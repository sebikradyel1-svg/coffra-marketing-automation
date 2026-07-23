"""
Coffra P6 Case Study PDF Generator
Author: Sebastian Kradyel
Date: April 2026

Generates case study PDF for P6 Technical SEO + GEO Audit project.
Brand-aligned styling consistent with P1-P5, P7. Content sourced from the
existing case_study/P6_Coffra_SEO_Audit.pdf, docs/14_seo_methodology.md,
and dashboard/pages/9_Technical_SEO_GEO_Audit.py (all three verified
consistent before this script was written).
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
OUTPUT_FILE = OUTPUT_DIR / "P6_Coffra_SEO_Audit.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE), pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    topMargin=2.0 * cm, bottomMargin=2.0 * cm,
    title="P6 Coffra Technical SEO + GEO Audit - Case Study",
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
                      "P6 Coffra Technical SEO + GEO Audit · Sebastian Kradyel · April 2026")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


story = []

# COVER
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Technical SEO + GEO Audit", styles["title"]))
story.append(Paragraph(
    "Search Console diagnostics, Core Web Vitals, Schema.org coverage & AI citation "
    "monitoring across 4 platforms",
    styles["subtitle"]))
story.append(horizontal_rule())

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Live Dashboard: <a href='https://coffra-marketing-dashboard.streamlit.app/Technical_SEO_GEO_Audit' "
    "color='#3E2723'>coffra-marketing-dashboard.streamlit.app</a>",
    styles["url_callout"]))
story.append(Spacer(1, 0.4 * cm))

# Metadata
metadata_label_style = ParagraphStyle("metadata_label", fontName=FONT_BOLD, fontSize=9,
                                       textColor=COFFRA_BROWN, leading=12)
metadata_value_style = ParagraphStyle("metadata_value", fontName=FONT_REGULAR, fontSize=9,
                                       textColor=DARK_GRAY, leading=12)
metadata_data = [
    ["Project", "P6 · Coffra Technical SEO + GEO Audit"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "April 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Stack", "Python · Google Search Console API · PageSpeed Insights · Schema.org Validator · Streamlit · Pandas"],
    ["Methods", "Technical SEO audit (6 categories, 15 checks) · Core Web Vitals (5 metrics) · Schema validation (12 templates) · GEO citation monitoring (4 platforms)"],
    ["Status", "v1.0 — audit complete + dashboard page + methodology doc + case study"],
]
metadata_data = [
    [Paragraph(label, metadata_label_style), Paragraph(value, metadata_value_style)]
    for label, value in metadata_data
]
metadata_table = Table(metadata_data, colWidths=[3.5 * cm, 12.5 * cm])
metadata_table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(metadata_table)

story.append(Spacer(1, 0.5 * cm))

# Executive Summary
story.append(Paragraph("Executive Summary", styles["h1"]))

story.append(Paragraph(
    "P6 closes the Coffra portfolio's technical foundation by adding a full technical SEO and "
    "generative engine optimization (GEO/AEO) audit layer. It addresses two questions that "
    "regularly appear in AI Marketing and Marketing Operations roles: are Coffra's pages "
    "technically sound enough for Google to index and rank them, and are they structured well "
    "enough for AI engines (Google AI Overviews, Perplexity, ChatGPT, Bing Copilot) to cite them "
    "in generated answers?",
    styles["body"]))

story.append(Paragraph(
    "The audit finds that all five Core Web Vitals pass Google's Good threshold, 11 of 12 Schema "
    "templates pass validation, and GEO citation rates have increased 10-15x across all four AI "
    "platforms following Schema.org implementation in November 2025. The most significant finding "
    "is the +41.6 percentage point citation rate increase on Google AI Overviews (4.2% baseline "
    "to 45.8% post-Schema), consistent with the Princeton GEO benchmark study.",
    styles["body"]))

story.append(Paragraph(
    "The page also introduces a Looker Studio export layer — five CSV datasets structured for "
    "direct connector compatibility — demonstrating production-grade BI tool integration, a "
    "capability that appears in the majority of Marketing Operations job descriptions reviewed "
    "during the portfolio research phase.",
    styles["body"]))

# Key outcomes
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Methods implemented", "Technical SEO audit (15 checks, 6 categories) + CWV (5 metrics) + Schema validation (12 templates) + GEO monitoring (4 platforms)"],
    ["SEO Health Score", "74 / 100 — composite (CWV 30% + Schema 25% + GSC 25% + GEO 20%)"],
    ["Core Web Vitals", "5/5 metrics pass Good threshold — LCP 1.84s, INP 88ms, CLS 0.04"],
    ["Schema coverage", "11/12 templates valid; 1 VideoObject warning (duration format — fix queued)"],
    ["GEO: Google AI Overviews", "+41.6pp citation rate (4.2% baseline → 45.8% post-Schema)"],
    ["GEO: Perplexity", "+36.5pp (3.1% → 39.6%)"],
    ["GEO: ChatGPT Browse", "+30.5pp (2.8% → 33.3%)"],
    ["GEO: Bing Copilot", "+31.3pp (3.1% → 34.4%)"],
    ["Technical audit", "13/15 checks pass; 2 partial items with clear remediation path"],
    ["Looker Studio layer", "5 CSVs downloadable from dashboard; connection guide included"],
    ["Live deployment", "Dashboard page integrated into existing Coffra Streamlit app"],
]
story.append(create_table(outcomes_data, col_widths=[4.5 * cm, 11.5 * cm]))

story.append(Spacer(1, 0.4 * cm))

# THE BUSINESS PROBLEM
story.append(Paragraph("The Business Problem", styles["h1"]))

story.append(Paragraph(
    "Coffra's P1-P5 projects generate marketing activities — email automation, customer "
    "segmentation, content strategy, attribution modeling. P6 addresses a prerequisite that "
    "underpins all of them: is the site technically visible to search engines and AI platforms?",
    styles["body"]))

problems_data = [
    ["Question", "Why naive answers fail"],
    ["Is Google indexing all pages?", "Without GSC monitoring, crawl errors and noindex tags silently block pages from appearing in search results for months."],
    ["Are pages fast enough to rank?", "Google's Core Web Vitals are a confirmed ranking signal since 2021. Pages in the Needs Improvement or Poor range are algorithmically penalized."],
    ["Are AI engines citing our content?", "AI Overviews and Perplexity now generate answers directly from web content. Pages without Schema markup have 10-15x lower citation rates (Princeton GEO study)."],
    ["Can the marketing team track SEO in Looker Studio?", "Marketing Operations roles require BI tool fluency. A Looker Studio-ready data layer demonstrates production-grade workflow integration."],
]
story.append(create_table(problems_data, col_widths=[6 * cm, 10 * cm]))

story.append(Paragraph("Data transparency", styles["h2"]))
story.append(Paragraph(
    "Consistent with the rest of the portfolio, every data point on this page is explicitly "
    "labeled by provenance rather than presented uniformly as fact:",
    styles["body"]))

data_types_data = [
    ["Component", "Type", "Rationale"],
    ["GSC Queries", "Snapshot", "Real GSC data extracted April 2026"],
    ["Core Web Vitals", "Simulated", "Coffra (Streamlit-hosted) has no real CrUX data; benchmarks used"],
    ["Schema Coverage", "Real", "12 templates validated via Schema.org Validator + Rich Results Test"],
    ["GEO Citations", "Simulated", "No real organic traffic; Princeton GEO benchmark methodology applied"],
    ["Technical Audit", "Real", "Manual checks via GSC, PageSpeed Insights, Validator"],
]
story.append(create_table(data_types_data, col_widths=[4 * cm, 3 * cm, 9 * cm]))

story.append(Spacer(1, 0.4 * cm))

# CORE WEB VITALS
story.append(Paragraph("Core Web Vitals Results", styles["h1"]))

story.append(Paragraph(
    "Google's CWV thresholds define three zones: Good, Needs Improvement, Poor. A page must pass "
    "all five metrics to qualify for CWV-related ranking boosts. Coffra passes all five as of "
    "April 2026.",
    styles["body"]))

cwv_data = [
    ["Metric", "Value", "Good Threshold", "Status", "Priority"],
    ["LCP — Largest Contentful Paint", "1.84s", "< 2.5s", "Good", "Monitor"],
    ["INP — Interaction to Next Paint", "88ms", "< 200ms", "Good", "Monitor"],
    ["CLS — Cumulative Layout Shift", "0.04", "< 0.1", "Good", "Monitor"],
    ["FCP — First Contentful Paint", "0.92s", "< 1.8s", "Good", "Monitor"],
    ["TTFB — Time to First Byte", "320ms", "< 800ms", "Good", "Monitor"],
]
story.append(create_table(cwv_data, col_widths=[5.5 * cm, 2.5 * cm, 3 * cm, 2.5 * cm, 2.5 * cm]))

story.append(Paragraph(
    "<i>Note: INP replaced FID (First Input Delay) as a Core Web Vital in March 2024. CWV values "
    "are simulated using realistic benchmarks for Streamlit Cloud-hosted apps (see "
    "docs/14_seo_methodology.md, Section 8.2). Real deployment would use CrUX field data.</i>",
    styles["body_small"]))

story.append(Spacer(1, 0.4 * cm))

# SCHEMA MARKUP
story.append(Paragraph("Schema.org Markup Coverage", styles["h1"]))

story.append(Paragraph(
    "12 JSON-LD templates were implemented in P4 (AEO Content Strategy). P6 adds validation "
    "tracking and GEO impact measurement. A template passes only if it clears three layers: "
    "Schema.org Validator, Google Rich Results Test, and GSC Rich Results report.",
    styles["body"]))

schema_data = [
    ["Schema Type", "Pages", "Validation", "Rich Result", "GEO Impact"],
    ["Product", "8", "Valid", "Yes", "High"],
    ["Organization", "1", "Valid", "No", "Medium"],
    ["WebSite", "1", "Valid", "No", "Low"],
    ["BreadcrumbList", "24", "Valid", "Yes", "Low"],
    ["FAQPage", "6", "Valid", "Yes", "High"],
    ["HowTo", "4", "Valid", "Yes", "High"],
    ["Article", "12", "Valid", "Yes", "High"],
    ["Review", "5", "Valid", "Yes", "Medium"],
    ["SiteLinksSearchBox", "1", "Valid", "Yes", "Low"],
    ["LocalBusiness", "1", "Valid", "No", "Medium"],
    ["VideoObject", "3", "Warning", "Yes", "Medium"],
    ["Recipe", "2", "Valid", "Yes", "High"],
]
story.append(create_table(schema_data, col_widths=[4.5 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm]))

story.append(Paragraph(
    "<b>VideoObject warning:</b> the <font face='DejaVuSans-Bold'>duration</font> property "
    "requires ISO 8601 format (<font face='DejaVuSans-Bold'>PT2M30S</font>), not plain integer "
    "seconds. One-line fix per template; queued for next sprint. All other templates pass full "
    "three-layer validation.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# GEO / AEO CITATION RESULTS
story.append(Paragraph("GEO / AEO Citation Results", styles["h1"]))

story.append(Paragraph(
    "Citation monitoring follows the Princeton GEO benchmark (Aggarwal et al., 2023): 48 "
    "representative queries per platform, binary citation recording, weekly sampling. The "
    "before/after delta is the primary metric — without a baseline, citation rates are "
    "meaningless.",
    styles["body"]))

geo_results_data = [
    ["Platform", "Queries", "Citations", "Citation Rate", "Baseline", "Uplift"],
    ["Google AI Overviews", "48", "22", "45.8%", "4.2%", "+41.6pp"],
    ["Perplexity", "48", "19", "39.6%", "3.1%", "+36.5pp"],
    ["ChatGPT (Browse)", "48", "16", "33.3%", "2.8%", "+30.5pp"],
    ["Bing Copilot", "32", "11", "34.4%", "3.1%", "+31.3pp"],
]
story.append(create_table(geo_results_data, col_widths=[4 * cm, 2 * cm, 2.2 * cm, 2.8 * cm, 2.5 * cm, 2.5 * cm]))

story.append(Paragraph("Citation rate trend (post-Schema implementation)", styles["h2"]))
story.append(Paragraph(
    "Schema.org implementation deployed November 2025. Citation rates across all four platforms "
    "have increased 10-15x in six months. Trajectory modeled as logistic growth; Google AI "
    "Overviews shows fastest adoption, consistent with Princeton study findings.",
    styles["body"]))

trend_data = [
    ["Month", "Google AI Overviews", "Perplexity", "ChatGPT Browse"],
    ["Nov 2025", "5%", "3%", "3%"],
    ["Dec 2025", "12%", "9%", "7%"],
    ["Jan 2026", "22%", "17%", "13%"],
    ["Feb 2026", "31%", "26%", "21%"],
    ["Mar 2026", "38%", "33%", "28%"],
    ["Apr 2026", "46%", "40%", "33%"],
]
story.append(create_table(trend_data, col_widths=[3.5 * cm, 4.5 * cm, 3.5 * cm, 4.5 * cm]))

story.append(Spacer(1, 0.4 * cm))

# TECHNICAL AUDIT CHECKLIST
story.append(Paragraph("Technical Audit Checklist", styles["h1"]))

story.append(Paragraph(
    "15 checks across 6 categories. Data type: real — all checks performed manually using Google "
    "Search Console, PageSpeed Insights, Schema.org Validator, and Google Rich Results Test, "
    "April 2026.",
    styles["body"]))

checklist_data = [
    ["Category", "Check", "Status", "Notes"],
    ["Crawlability", "XML Sitemap submitted to GSC", "Pass", "24/24 pages indexed"],
    ["Crawlability", "robots.txt configured correctly", "Pass", "Disallow: /admin, /staging"],
    ["Crawlability", "No crawl errors in GSC Coverage", "Pass", "0 errors as of April 2026"],
    ["Indexability", "Canonical tags on all pages", "Pass", "Self-referencing on all 24 pages"],
    ["Indexability", "No unintended noindex tags", "Pass", "All pages indexable"],
    ["Indexability", "Hreflang (EN/RO bilingual)", "Partial", "EN done; RO pending 3 pages"],
    ["Page Speed", "LCP < 2.5s", "Pass", "1.84s average"],
    ["Page Speed", "No render-blocking resources", "Pass", "CSS/JS deferred"],
    ["Page Speed", "Images with width/height (CLS)", "Pass", "All img tags include dimensions"],
    ["Schema", "JSON-LD on all key pages", "Pass", "12 templates, 68 instances"],
    ["Schema", "No errors in Rich Results Test", "Partial", "1 VideoObject warning — fix queued"],
    ["Mobile", "Google Mobile-Friendly Test", "Pass", "Pass"],
    ["Mobile", "Viewport meta tag present", "Pass", "Correct on all pages"],
    ["Security", "HTTPS enforced sitewide", "Pass", "SSL/TLS A+ rating"],
    ["Security", "No mixed content warnings", "Pass", "0 issues"],
]
story.append(create_table(checklist_data, col_widths=[3 * cm, 6 * cm, 2 * cm, 5 * cm]))

story.append(Paragraph(
    "Audit score: 13/15 checks pass (87%). Two partial items have clear remediation: (1) RO "
    "hreflang — 3 pages need tags added; (2) VideoObject duration — one-line format fix per "
    "template. Both completable in under 2 hours.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# LOOKER STUDIO
story.append(Paragraph("Looker Studio Export Layer", styles["h1"]))

story.append(Paragraph(
    "Looker Studio is the most frequently required BI tool in Marketing Operations job "
    "descriptions. P6 includes a production-grade export layer: five CSVs downloadable directly "
    "from the dashboard, structured for Google Sheets connector compatibility.",
    styles["body"]))

looker_data = [
    ["Dataset", "File", "Shape", "Looker Studio Use"],
    ["GSC Queries", "gsc_queries.csv", "10 rows x 5 cols", "Time-series: impressions, CTR, position"],
    ["CWV Diagnostics", "cwv_diagnostics.csv", "5 rows x 5 cols", "Scorecard: metric vs threshold"],
    ["Schema Coverage", "schema_coverage.csv", "12 rows x 5 cols", "Table: validation status by type"],
    ["GEO Citation Trend", "geo_citation_trend.csv", "6 rows x 4 cols", "Line chart: citation rate by platform"],
    ["Technical Audit", "seo_audit_checklist.csv", "15 rows x 4 cols", "Table: pass/fail by category"],
]
story.append(create_table(looker_data, col_widths=[3.5 * cm, 4.5 * cm, 3 * cm, 5 * cm]))

story.append(Paragraph(
    "Recommended Looker Studio dashboard structure: Page 1 — GSC Performance (impressions, "
    "clicks, CTR, position trend); Page 2 — Technical Health (CWV scorecard, audit checklist); "
    "Page 3 — GEO/AEO Monitoring (citation rate by platform, trend). Full connection guide in "
    "docs/14_seo_methodology.md, Section 7.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# SKILLS DEMONSTRATED
story.append(Paragraph("Skills Demonstrated", styles["h1"]))

skills_data = [
    ["Category", "Specific Skills"],
    ["Technical SEO", "Crawlability audit, indexability, hreflang, canonical tags, sitemap management"],
    ["Core Web Vitals", "LCP/INP/CLS/FCP/TTFB measurement, PageSpeed Insights API, CrUX interpretation"],
    ["Schema / Structured Data", "JSON-LD authoring, Schema.org Validator, Google Rich Results Test, three-layer validation pipeline"],
    ["GEO / AEO", "Citation rate measurement, Princeton GEO benchmark methodology, multi-platform sampling (Google AI Overviews, Perplexity, ChatGPT, Bing)"],
    ["Google Search Console", "API integration, snapshot architecture, query/page performance analysis"],
    ["Looker Studio", "Export schema design, Google Sheets connector, BI dashboard structure"],
    ["Python / Streamlit", "Multi-page dashboard, st.download_button, st.line_chart, st.progress, data_disclosure component"],
    ["Data transparency", "Explicit real/snapshot/simulated labeling throughout; honest limitations documented"],
]
story.append(create_table(skills_data, col_widths=[4 * cm, 12 * cm]))

story.append(Spacer(1, 0.4 * cm))

# LIMITATIONS
story.append(Paragraph("Limitations and Future Work", styles["h1"]))

story.append(Paragraph("Known limitations", styles["h2"]))
story.append(Paragraph(
    "CWV values are simulated using PageSpeed Insights lab benchmarks; real CrUX field data "
    "requires sufficient real-user traffic, which Coffra (fictional brand) does not have. GEO "
    "citation monitoring is based on manual query sampling — inherently noisy, with "
    "approximately ±14% margin of error at 48 queries per platform. No official Google AI "
    "Overviews citation API exists as of April 2026; monitoring requires manual spot-checking. "
    "Citation rate improvement may be partially attributable to factors beyond Schema (content "
    "freshness, concurrent backlink acquisition).",
    styles["body"]))

story.append(Paragraph("Future enhancements (v1.1+)", styles["h2"]))
story.append(Paragraph(
    "Automate GSC extraction via GitHub Actions + Google Cloud Run (weekly refresh). Replace CWV "
    "simulation with live CrUX API data as traffic grows. Automate Perplexity citation sampling "
    "via API. Increase query sample to 100 per platform (±10% margin of error). Design holdout "
    "experiment: Schema on test pages, withhold from matched control pages, measure citation rate "
    "difference — proper experimental GEO attribution. Add competitive benchmarking: Coffra "
    "citation rates vs 3 competitor coffee brands.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# CLOSING
story.append(horizontal_rule())
story.append(Paragraph("Connection to Other Projects", styles["h1"]))

story.append(Paragraph(
    "P6 closes the technical foundation loop across the entire Coffra portfolio:",
    styles["body"]))

connection_data = [
    ["Project", "Relationship to P6"],
    ["P1 — Marketing Automation", "Email content drives organic traffic; GEO citations of email topics feed back into subject line testing (high-citation angles = higher open rates)"],
    ["P2 — Marketing Dashboard", "P6 is integrated into the same Streamlit app; snapshot architecture identical to P2"],
    ["P3 — Customer Segmentation", "GSC query data can be segmented by persona (Connoisseur vs Daily Ritualist search behavior)"],
    ["P4 — AEO Content Strategy", "P4 built the Schema templates; P6 validates them, monitors their GEO impact, and measures the +41.6pp citation rate uplift"],
    ["P5 — Attribution Modeling", "As GEO-referred traffic grows, AI Overview / Perplexity becomes a measurable channel in P5's MMM — closing the attribution loop"],
]
story.append(create_table(connection_data, col_widths=[4 * cm, 12 * cm]))

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
