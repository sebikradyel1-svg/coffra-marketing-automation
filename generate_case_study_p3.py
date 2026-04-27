"""
Coffra P3 Case Study PDF Generator
Author: Sebastian Kradyel
Date: April 2026

Generates a 6-8 page case study PDF for P3 Customer Segmentation project.
Brand-aligned styling consistent with P1 and P2.

Usage:
    python generate_case_study_p3.py
    Output: case_study/P3_Coffra_Segmentation_Case_Study.pdf
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
    PageBreak, HRFlowable
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

registerFontFamily(
    "DejaVuSans",
    normal="DejaVuSans", bold="DejaVuSans-Bold",
    italic="DejaVuSans-Oblique", boldItalic="DejaVuSans-BoldOblique",
)

FONT_REGULAR = "DejaVuSans"
FONT_BOLD = "DejaVuSans-Bold"
FONT_ITALIC = "DejaVuSans-Oblique"

# Brand colors
COFFRA_BROWN = colors.HexColor("#3E2723")
COFFRA_BROWN_LIGHT = colors.HexColor("#6D4C41")
COFFRA_CREAM = colors.HexColor("#EFEBE9")
DARK_GRAY = colors.HexColor("#212121")
MEDIUM_GRAY = colors.HexColor("#616161")
LIGHT_GRAY = colors.HexColor("#E0E0E0")

# Document setup
OUTPUT_DIR = Path("case_study")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "P3_Coffra_Segmentation_Case_Study.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE), pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    topMargin=2.0 * cm, bottomMargin=2.0 * cm,
    title="P3 Coffra Customer Segmentation - Case Study",
    author="Sebastian Kradyel",
)

# Styles
base_styles = getSampleStyleSheet()
styles = {
    "title": ParagraphStyle("title", parent=base_styles["Heading1"],
        fontName=FONT_BOLD, fontSize=28, textColor=COFFRA_BROWN,
        leading=34, spaceBefore=0, spaceAfter=8, alignment=TA_LEFT),
    "subtitle": ParagraphStyle("subtitle", parent=base_styles["Normal"],
        fontName=FONT_REGULAR, fontSize=14, textColor=MEDIUM_GRAY,
        leading=18, spaceBefore=0, spaceAfter=20, alignment=TA_LEFT),
    "h1": ParagraphStyle("h1", parent=base_styles["Heading1"],
        fontName=FONT_BOLD, fontSize=18, textColor=COFFRA_BROWN,
        leading=22, spaceBefore=18, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=base_styles["Heading2"],
        fontName=FONT_BOLD, fontSize=13, textColor=COFFRA_BROWN_LIGHT,
        leading=17, spaceBefore=14, spaceAfter=6),
    "body": ParagraphStyle("body", parent=base_styles["BodyText"],
        fontName=FONT_REGULAR, fontSize=10, textColor=DARK_GRAY,
        leading=14, spaceBefore=2, spaceAfter=8, alignment=TA_JUSTIFY),
    "body_small": ParagraphStyle("body_small", parent=base_styles["BodyText"],
        fontName=FONT_REGULAR, fontSize=9, textColor=DARK_GRAY,
        leading=12, spaceAfter=6),
    "url_callout": ParagraphStyle("url_callout", parent=base_styles["Normal"],
        fontName=FONT_BOLD, fontSize=12, textColor=COFFRA_BROWN,
        leading=16, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4),
}


def horizontal_rule(color=COFFRA_BROWN, width=1):
    return HRFlowable(width="100%", thickness=width, color=color,
                      spaceBefore=4, spaceAfter=10)


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
                      "P3 Coffra Customer Segmentation · Sebastian Kradyel · April 2026")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


# Build story
story = []

# COVER
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Customer Segmentation", styles["title"]))
story.append(Paragraph(
    "RFM analysis with ML clustering, persona alignment, and Coffra deployment playbook",
    styles["subtitle"]))
story.append(horizontal_rule())

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Live Dashboard: <a href='https://coffra-marketing-dashboard.streamlit.app/Customer_Segments' "
    "color='#3E2723'>coffra-marketing-dashboard.streamlit.app</a>",
    styles["url_callout"]))
story.append(Spacer(1, 0.4 * cm))

# Metadata
metadata_data = [
    ["Project", "P3 · Coffra Customer Segmentation"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "April 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Dataset", "Online Retail II (UCI / Kaggle) — 1.07M transactions, ~5,900 customers"],
    ["Stack", "Python · pandas · scikit-learn · Plotly · Streamlit"],
    ["Status", "v1.0 — complete with live dashboard integration"],
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
    "P3 builds the analytical foundation for personalized customer marketing at Coffra by applying "
    "Recency-Frequency-Monetary (RFM) segmentation and unsupervised machine learning to a real "
    "e-commerce dataset (Online Retail II UCI, 1.07 million transactions). The output is "
    "deployment-ready: 11 actionable customer segments, a strategic playbook mapping each segment "
    "to specific Coffra marketing tactics, and an annual revenue uplift projection of £240,000 "
    "(+23% over untargeted baseline) supported by industry-anchored assumptions.",
    styles["body"]))

story.append(Paragraph(
    "The methodology applies professional standards: explicit data quality audit before analysis, "
    "comparison of K-Means against Hierarchical Clustering for robustness, log-transformation and "
    "scaling of skewed features, multi-metric evaluation of cluster quality, and explicit honest "
    "disclosure of all assumptions in financial projections. The analysis surfaces a non-trivial "
    "strategic insight: probable Connoisseur customers (high-frequency, high-value, recent) "
    "represent only 14.4% of the customer base but contribute 61.8% of revenue, validating P1's "
    "disproportionate investment in the Connoisseur email sequence with a 4.3x revenue "
    "concentration ratio.",
    styles["body"]))

story.append(Paragraph(
    "All findings integrate into the live Coffra dashboard from P2, where a new Customer Segments "
    "page renders segment economics, ML clustering metrics, persona alignment insights, and the "
    "strategic playbook. The deliverable is therefore not a standalone document but an active "
    "component of the Coffra marketing operations stack.",
    styles["body"]))

# Key outcomes
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Customers analyzed", "5,878 unique customers (after data quality audit and cleaning)"],
    ["Revenue scope", "£17.4M observed, £240K projected annual uplift from differentiated campaigns"],
    ["Segments produced", "11 rule-based RFM segments + 4 ML-clustered groups (cross-validated)"],
    ["Top revenue insight", "Connoisseur persona (14.4% customers) generates 61.8% revenue (4.3x concentration)"],
    ["ML rigor", "K-Means + Hierarchical compared (ARI = 0.61, substantial agreement)"],
    ["Deployment", "Live dashboard page + 4 production-ready notebooks + 2 strategic documents"],
]
story.append(create_table(outcomes_data, col_widths=[5 * cm, 11 * cm]))

story.append(Spacer(1, 0.4 * cm))

# PROBLEM & APPROACH
story.append(Paragraph("Problem and Approach", styles["h1"]))

story.append(Paragraph("The challenge", styles["h2"]))
story.append(Paragraph(
    "Coffra's marketing system from P1 (13 emails across two persona-specific journeys) and P2 "
    "(operational dashboard) was built on persona theory, not customer data. Without a customer "
    "base to segment, all marketing spend was effectively broadcast: every Connoisseur message "
    "to every Connoisseur subscriber, every Daily Ritualist message to every Daily Ritualist. "
    "This works at small scale but fails to differentiate between a 5-purchase Champion and a "
    "1-purchase recent customer. Different customers need different campaigns.",
    styles["body"]))

story.append(Paragraph("The approach", styles["h2"]))
story.append(Paragraph(
    "Segmentation is the standard solution. Two complementary approaches were applied: "
    "rule-based RFM (interpretable, marketing-actionable) and ML clustering (data-driven, "
    "validates rules). Both surface the same underlying behavioral structure, providing "
    "confidence the segmentation is real and not an artifact of method choice.",
    styles["body"]))

story.append(Paragraph(
    "The deliverable is structured to be operationally useful: each segment has an action, a "
    "channel, a cadence, and a reference to which P1 email content to deploy. A marketing manager "
    "could read this on Monday and configure HubSpot workflows by Wednesday.",
    styles["body"]))

story.append(Paragraph("Why this dataset", styles["h2"]))
story.append(Paragraph(
    "The Online Retail II UCI dataset was chosen because Coffra is fictional and has no real "
    "customer transactions. Online Retail II is a public, real e-commerce dataset (UK retailer, "
    "2009-2011) widely used in academic and industry RFM tutorials. RFM dynamics are universal "
    "across e-commerce verticals: a Champion in retail behaves like a Champion in coffee "
    "subscription, with the same retention strategies applying. The methodology transfers "
    "directly to Coffra once real customer data exists.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# DATA & CLEANING
story.append(Paragraph("Data Quality and Cleaning", styles["h1"]))

story.append(Paragraph(
    "Real e-commerce data has known quality issues. The first notebook performs an explicit data "
    "quality audit before any analysis. Five categories of issues were identified and addressed "
    "with documented decisions:",
    styles["body"]))

cleaning_data = [
    ["Issue", "Impact", "Decision"],
    ["Missing Customer ID (~22%)", "Cannot do customer-level analysis", "Drop, exclusion documented"],
    ["Cancellation invoices (C-prefix)", "Returns dilute purchase intent signal", "Drop (not net against purchases)"],
    ["Negative quantity / price", "Likely data errors", "Drop"],
    ["Zero price", "Promotional samples or errors", "Drop"],
    ["Exact duplicates", "Upload artifacts", "Drop"],
]
story.append(create_table(cleaning_data, col_widths=[5 * cm, 5 * cm, 6 * cm]))

story.append(Paragraph(
    "Net retention: 1.07M rows reduced to ~770K usable transactions (~72% retention). The 28% "
    "loss is dominated by missing-Customer-ID rows, consistent with public e-commerce datasets. "
    "Every cleaning step is logged in the EDA notebook with row counts before and after.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# RFM SCORING
story.append(Paragraph("RFM Scoring and Standard Segments", styles["h1"]))

story.append(Paragraph(
    "RFM scoring assigns each customer a 1-5 score on three dimensions (Recency, Frequency, "
    "Monetary) using quintile binning. Composite scores combine these into the industry-standard "
    "11-segment framework based on the 2D `R_Score × FM_Score` grid.",
    styles["body"]))

story.append(Paragraph("Pareto validation", styles["h2"]))
story.append(Paragraph(
    "Before applying segmentation, we validated that the dataset has the expected long-tail "
    "distribution. The result: top 20% of customers contribute approximately 70-80% of revenue. "
    "This Pareto pattern is the structural reason segmentation is valuable — differentiated "
    "investment per segment is justified by differential revenue contribution.",
    styles["body"]))

story.append(Paragraph("Segment economics", styles["h2"]))

segments_summary = [
    ["Segment", "Customers", "% of Customers", "% of Revenue"],
    ["Champions", "469", "8.0%", "27.5%"],
    ["Loyal Customers", "1,111", "18.9%", "31.5%"],
    ["Cannot Lose Them", "445", "7.6%", "12.7%"],
    ["Potential Loyalists", "565", "9.6%", "8.4%"],
    ["At Risk", "417", "7.1%", "5.6%"],
    ["About to Sleep", "528", "9.0%", "3.4%"],
    ["Hibernating + Lost", "~2,000", "~34%", "~6%"],
    ["Other (mid-tier)", "~340", "~5.8%", "~5%"],
]
story.append(create_table(segments_summary, col_widths=[4 * cm, 3 * cm, 4 * cm, 5 * cm]))

story.append(Paragraph(
    "Note: The top 3 segments (Champions, Loyal Customers, Cannot Lose Them) account for ~35% "
    "of customers but ~71% of revenue. This concentration is the strategic foundation for the "
    "playbook: differentiated investment in these segments yields disproportionate uplift.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# ML CLUSTERING
story.append(Paragraph("Machine Learning Clustering", styles["h1"]))

story.append(Paragraph(
    "Two unsupervised algorithms were applied to validate that any structure adopted is "
    "algorithm-robust: K-Means (fast, scalable, requires k upfront) and Agglomerative "
    "Hierarchical Clustering (no k assumption, dendrogram for visual inspection, slower). "
    "Cross-validation via the Adjusted Rand Index (ARI) measures algorithm agreement.",
    styles["body"]))

story.append(Paragraph("Methodology choices", styles["h2"]))
story.append(Paragraph(
    "Frequency and Monetary were log-transformed (`np.log1p`) to compress long tails. All three "
    "features were then z-score normalized via StandardScaler so that distance computations are "
    "not dominated by features with larger raw scales. K=4 was selected via the elbow method and "
    "silhouette analysis: lower k loses meaningful distinctions, higher k over-fragments.",
    styles["body"]))

story.append(Paragraph("Cluster quality", styles["h2"]))

quality_data = [
    ["Metric", "K-Means (k=4)", "Hierarchical (k=4)"],
    ["Silhouette score", "0.362 (acceptable, > 0.3 threshold)", "Comparable"],
    ["Davies-Bouldin", "0.894 (lower is better)", "Comparable"],
    ["Adjusted Rand Index", "ARI = 0.613 (substantial agreement)", "—"],
]
story.append(create_table(quality_data, col_widths=[5 * cm, 6 * cm, 5 * cm]))

story.append(Paragraph(
    "An ARI above 0.5 indicates substantial agreement between methods, providing confidence "
    "that the clusters represent real structure in customer behavior rather than algorithmic "
    "artifacts. The 4 clusters that emerge — Best Customers, Engaged Mid-Value, Light Buyers, "
    "Inactive — are interpretable and actionable.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# PERSONA ALIGNMENT
story.append(Paragraph("Persona Alignment", styles["h1"]))

story.append(Paragraph(
    "Coffra's two personas (Connoisseur and Daily Ritualist) were defined in P1. The "
    "segmentation analysis assigns probable persona to each customer based on RFM signature: "
    "high-frequency + high-value + recent → Connoisseur; moderate-frequency + moderate-value "
    "+ moderately-recent → Daily Ritualist; otherwise Unaligned.",
    styles["body"]))

story.append(Paragraph("The critical insight", styles["h2"]))

story.append(Paragraph(
    "<b>Probable Connoisseurs are 14.4% of customers but generate 61.8% of revenue — a 4.3x "
    "revenue concentration ratio.</b> This empirically validates P1's disproportionate "
    "investment in the Connoisseur email sequence (5 carefully crafted English emails plus "
    "3-email cart recovery). The premium positioning, no-discount discipline, and technical "
    "messaging are justified by the data: this small subset of customers carries the majority "
    "of revenue.",
    styles["body"]))

persona_data = [
    ["Persona", "Customers", "% Customers", "% Revenue", "Avg Monetary"],
    ["Connoisseur (probable)", "845", "14.4%", "61.8%", "£12,711"],
    ["Daily Ritualist (probable)", "1,343", "22.8%", "10.5%", "£1,358"],
    ["Unaligned", "3,690", "62.8%", "27.7%", "£1,303"],
]
story.append(create_table(persona_data, col_widths=[4 * cm, 2 * cm, 3 * cm, 3 * cm, 3 * cm]))

story.append(Paragraph(
    "Daily Ritualists are a volume segment: more customers, lower revenue per customer. The "
    "strategy implication is opposite to Connoisseurs — optimize for retention and frequency, "
    "use accessible price points (Coffra Pass), and prioritize community and ritual over "
    "technical content. Unaligned customers represent an opportunity for explicit persona "
    "discovery via signup survey in production deployment.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# STRATEGIC PLAYBOOK
story.append(Paragraph("Strategic Playbook", styles["h1"]))

story.append(Paragraph(
    "Each segment has a specific marketing tactic, channel, cadence, and reference to which "
    "P1 email content to reuse. The playbook is HubSpot-deployment-ready.",
    styles["body"]))

playbook_summary = [
    ["Tier", "Segments", "Approach"],
    ["Tier 1 — Retain & Amplify", "Champions, Loyal Customers", "Personal touch, exclusivity, no discounts; subscription upsell"],
    ["Tier 2 — Develop & Convert", "Potential Loyalists, Recent, Promising", "Full nurture sequence; persona discovery survey; trial offers"],
    ["Tier 3 — Re-engage & Recover", "Customers Needing Attention, About to Sleep, At Risk, Cannot Lose Them", "Differentiated win-back: personal email for Cannot Lose Them; light re-engagement for others"],
    ["Tier 4 — Suppress & Reset", "Hibernating, Lost", "Single last-chance email; suppress non-engagers to protect sender reputation"],
]
story.append(create_table(playbook_summary, col_widths=[4 * cm, 5 * cm, 7 * cm]))

story.append(Paragraph(
    "The full playbook (in `docs/10_segment_strategies.md`) details specific tactics per segment "
    "with watch-outs and expected impact. Cross-cutting principles are also documented: "
    "persona consistency, discount discipline (asymmetric per persona), frequency hygiene "
    "(max 2 emails/week), suppression as a feature, and a measurement loop for continuous "
    "improvement.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# FINANCIAL IMPACT
story.append(Paragraph("Financial Impact Projection", styles["h1"]))

story.append(Paragraph(
    "Total projected annual uplift: <b>£240,367 (+23.2% over untargeted baseline)</b>. The "
    "projection is computed per segment using customer counts, average monthly orders, AOV "
    "(£20 Coffra assumption), and segment-specific lift assumptions anchored to Klaviyo and "
    "Bloomreach 2024 industry benchmarks for differentiated marketing programs.",
    styles["body"]))

story.append(Paragraph("Top 3 uplift segments", styles["h2"]))

uplift_data = [
    ["Segment", "Customers", "Lift", "Annual Uplift"],
    ["Loyal Customers", "1,111", "25%", "£99,990"],
    ["Cannot Lose Them", "445", "40%", "£64,080"],
    ["Champions", "469", "15%", "£33,768"],
]
story.append(create_table(uplift_data, col_widths=[5 * cm, 3 * cm, 3 * cm, 5 * cm]))

story.append(Paragraph(
    "These three segments alone account for £197,838 in projected uplift — 82% of the total. "
    "This Pareto in uplift mirrors the Pareto in revenue, confirming where marketing "
    "investment yields the highest returns.",
    styles["body"]))

story.append(Paragraph("Honest disclosure", styles["h2"]))
story.append(Paragraph(
    "All projections are scenario-based, not measurements. They represent reasonable "
    "expectations for differentiated segment campaigns vs. a no-personalization baseline, "
    "assuming campaigns are designed and executed competently. Actual lifts in real "
    "deployment would vary based on creative quality, customer base composition, channel mix, "
    "and competitive context. A real Coffra deployment would measure actual lifts via "
    "per-segment A/B testing and refine the assumption table iteratively.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# DEPLOYMENT
story.append(Paragraph("Production Deployment Roadmap", styles["h1"]))

story.append(Paragraph(
    "The full segmentation system can be operationalized at Coffra in approximately 10 weeks "
    "across six phases:",
    styles["body"]))

roadmap_data = [
    ["Phase", "Duration", "Tasks"],
    ["1. Data Foundation", "Weeks 1-2", "HubSpot + Shopify integration, Customer ID consistency"],
    ["2. RFM Pipeline", "Weeks 3-4", "Adapt scoring notebook, schedule weekly refresh, persist scores in HubSpot"],
    ["3. Segment Workflows", "Weeks 5-6", "Configure HubSpot workflows, map segments to P1 emails, suppression rules"],
    ["4. Persona Survey", "Week 6", "1-question survey for Recent Customers, populate `hs_persona` property"],
    ["5. Measurement", "Ongoing", "Monthly dashboard refresh, segment migration matrix tracking"],
    ["6. Iteration", "Quarterly", "Re-cluster, validate definitions, adjust playbook with measured rates"],
]
story.append(create_table(roadmap_data, col_widths=[4 * cm, 2.5 * cm, 9.5 * cm]))

story.append(Spacer(1, 0.4 * cm))

# SKILLS
story.append(Paragraph("Skills Demonstrated", styles["h1"]))

skills_data = [
    ["Category", "Specific Skills"],
    ["Data analysis", "Real-world data cleaning, missing data handling, audit trail discipline"],
    ["RFM segmentation", "Quintile scoring, 11-segment framework, snapshot date conventions"],
    ["Unsupervised ML", "K-Means + Hierarchical Clustering, log-transformation, scaling, PCA visualization"],
    ["Cluster validation", "Silhouette, Davies-Bouldin, Calinski-Harabasz, Adjusted Rand Index"],
    ["Statistical literacy", "Pareto analysis, distribution diagnostics, scenario-based projection"],
    ["Strategic mapping", "Segment-to-action playbook with channel, cadence, and KPIs"],
    ["Production thinking", "Roadmap, A/B testing protocols, suppression rules, measurement loops"],
    ["Honest disclosure", "Transparent labelling of assumptions, limitations, and scenarios"],
]
story.append(create_table(skills_data, col_widths=[4 * cm, 12 * cm]))

story.append(Spacer(1, 0.4 * cm))

# LIMITATIONS
story.append(Paragraph("Limitations and Future Work", styles["h1"]))

story.append(Paragraph("Known limitations", styles["h2"]))
story.append(Paragraph(
    "This is a snapshot analysis on a static dataset, not a longitudinal study of customer "
    "migration. Persona inference is heuristic — real Coffra deployment requires explicit "
    "persona signal capture. Financial projections are scenarios anchored to public benchmarks, "
    "not measurements. RFM uses 3 dimensions; richer features (product diversity, channel "
    "behavior, demographics) would surface additional structure.",
    styles["body"]))

story.append(Paragraph("Future enhancements (v1.1+)", styles["h2"]))
story.append(Paragraph(
    "Time-series segmentation to track customer migration patterns. Margin-weighted Monetary "
    "to align with profitability. Predictive churn model trained on segment-migration history. "
    "Multi-armed bandit campaigns replacing fixed segment-strategy mapping with adaptive "
    "allocation. Density-based clustering (DBSCAN, HDBSCAN) to surface non-spherical "
    "behavioral patterns missed by K-Means.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# CLOSING
story.append(horizontal_rule())
story.append(Paragraph("Connection to P1, P2, and Future Projects", styles["h1"]))

story.append(Paragraph(
    "P3 completes the analytical layer of the Coffra marketing stack. P1 built the strategic "
    "and operational layer (personas, emails, HubSpot workflows, lead scoring, AI subject "
    "optimizer). P2 added the visualization layer (live dashboard with operational visibility). "
    "P3 now adds the analytical depth: customer behavior segmentation that drives "
    "differentiated campaign allocation.",
    styles["body"]))

story.append(Paragraph(
    "Future projects build on this foundation. P4 (Recommendation Systems) will use cluster "
    "membership as a feature for product recommendations. P5 (Attribution Modeling) will "
    "measure channel effectiveness across the full segmented marketing program. P6 (Content "
    "Strategy with AEO) will explore answer-engine-optimized content, completing a 2026-relevant "
    "portfolio.",
    styles["body"]))

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
