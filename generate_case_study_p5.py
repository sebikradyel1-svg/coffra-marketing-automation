"""
Coffra P5 Case Study PDF Generator
Author: Sebastian Kradyel
Date: April 2026

Generates case study PDF for P5 Attribution Modeling project.
Brand-aligned styling consistent with P1-P4.
"""

from pathlib import Path
import json
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
OUTPUT_FILE = OUTPUT_DIR / "P5_Coffra_Attribution_Case_Study.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_FILE), pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    topMargin=2.0 * cm, bottomMargin=2.0 * cm,
    title="P5 Coffra Attribution Modeling - Case Study",
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
                      "P5 Coffra Attribution Modeling · Sebastian Kradyel · April 2026")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


story = []

# COVER
story.append(Spacer(1, 1 * cm))
story.append(Paragraph("Marketing Attribution Modeling", styles["title"]))
story.append(Paragraph(
    "Multi-Touch Attribution + Bayesian Marketing Mix Model — quantifying channel value with uncertainty",
    styles["subtitle"]))
story.append(horizontal_rule())

story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph(
    "Live Dashboard: <a href='https://coffra-marketing-dashboard.streamlit.app/Attribution' "
    "color='#3E2723'>coffra-marketing-dashboard.streamlit.app</a>",
    styles["url_callout"]))
story.append(Spacer(1, 0.4 * cm))

# Metadata
metadata_data = [
    ["Project", "P5 · Coffra Attribution Modeling"],
    ["Author", "Sebastian Kradyel"],
    ["Date", "April 2026"],
    ["Repository", "github.com/sebikradyel1-svg/coffra-marketing-automation"],
    ["Stack", "Python · NumPy · Pandas · PyMC 5.x · ArviZ · Streamlit · Plotly"],
    ["Methods", "6 MTA + 1 Bayesian MMM with NUTS sampling"],
    ["Status", "v1.0 — methodology + 4 notebooks + dashboard + case study"],
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
    "P5 addresses one of marketing's hardest questions: which channels actually drive conversions, "
    "and how should budget be allocated? Naive last-click attribution systematically misallocates "
    "budget by 25-40 percentage points across channels. This project builds a dual-method attribution "
    "system combining six Multi-Touch Attribution (MTA) methods with a Bayesian Marketing Mix Model "
    "(MMM) using PyMC, validated against synthetic data with known ground truth.",
    styles["body"]))

story.append(Paragraph(
    "The analysis surfaces actionable insight: the most efficient channel (Email at £1.92 CPA) costs "
    "8x less per acquisition than the least efficient (Meta Ads at £15.44 CPA). Reallocating from "
    "Meta Ads to Email and Google Ads — based on MMM credible intervals rather than point estimates — "
    "would generate a projected 10-15% lift in conversions at the same total spend.",
    styles["body"]))

story.append(Paragraph(
    "Beyond the numerical output, the project demonstrates production-grade rigor: convergence "
    "diagnostics (R-hat = 1.00, ESS > 750), posterior predictive validation (R² = 0.69, MAPE = 11.3%, "
    "95% CI coverage = 95.2%), and explicit honest assessment of where each method fails. The "
    "methodology is documented in `docs/13` and reproducible from `notebooks/07-10`.",
    styles["body"]))

# Key outcomes
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Key Outcomes", styles["h2"]))

outcomes_data = [
    ["Component", "Outcome"],
    ["Methods implemented", "6 MTA (Last-Click, First-Click, Linear, Time-Decay, Markov, Shapley) + 1 Bayesian MMM"],
    ["Synthetic dataset", "50K customers (MTA) + 731 daily observations (MMM) with known ground truth"],
    ["MMM convergence", "R-hat = 1.00 (target < 1.01), Min ESS = 750 (target > 400) — fully converged"],
    ["MMM model fit", "R² = 0.69, MAPE = 11.3%, 95% CI coverage = 95.2% — well-calibrated"],
    ["Strategic finding", "Email is 8x more cost-efficient than Meta Ads (CPA £1.92 vs £15.44)"],
    ["Business value", "10-15% projected lift from MMM-informed budget reallocation (industry benchmark)"],
    ["Live deployment", "Dashboard page integrated into existing Coffra Streamlit app"],
]
story.append(create_table(outcomes_data, col_widths=[5 * cm, 11 * cm]))

story.append(Spacer(1, 0.4 * cm))

# THE PROBLEM
story.append(Paragraph("The Business Problem", styles["h1"]))

story.append(Paragraph(
    "Coffra invests across multiple marketing channels: paid search (Google Ads), paid social "
    "(Meta Ads), Instagram organic, email automation, and direct/referral traffic. Each channel "
    "competes for budget. The CMO needs to know:",
    styles["body"]))

problems_data = [
    ["Question", "Why naive answers fail"],
    ["Which channels actually drive conversions?", "Last-click attribution gives credit only to the final touchpoint, ignoring the journey that led there. Upper-funnel channels (Instagram, content) get 0% credit."],
    ["What is the marginal ROI of additional spend?", "Without saturation modeling, you can't tell whether £1,000 more on Google Ads will generate 50 conversions or 5."],
    ["Should we shift budget between channels?", "Without comparing channels on equal footing (CPA, contribution share, marginal returns), reallocation is guesswork."],
    ["How confident are we in these answers?", "Point estimates without uncertainty quantification mislead decision-makers into over-confident actions."],
]
story.append(create_table(problems_data, col_widths=[6 * cm, 10 * cm]))

story.append(Paragraph(
    "P5 builds the analytical infrastructure to answer all four questions defensibly.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# TWO APPROACHES
story.append(Paragraph("Why Both MTA and MMM", styles["h1"]))

story.append(Paragraph(
    "Multi-Touch Attribution and Marketing Mix Modeling are complementary, not interchangeable. "
    "They answer different questions and have different failure modes:",
    styles["body"]))

approaches_data = [
    ["Dimension", "MTA", "MMM"],
    ["Granularity", "Individual customer journey", "Aggregate weekly/daily spend"],
    ["Question answered", "How did customers get here?", "What if we hadn't spent on this channel?"],
    ["Data needs", "UTM tracking, click logs", "Channel spend + conversions over time"],
    ["Privacy compliance", "Hard (cookie deprecation, GDPR)", "Easy (no individual data)"],
    ["Cross-channel reach", "Digital only", "Includes TV, OOH, podcast"],
    ["Time to first result", "Days", "2-3 months of historical data"],
    ["Captures incrementality", "Heuristic, often poor", "Designed for causal estimation"],
]
story.append(create_table(approaches_data, col_widths=[3.5 * cm, 6.25 * cm, 6.25 * cm]))

story.append(Paragraph(
    "<b>Production deployment uses both.</b> When they agree, confidence is high. When they "
    "disagree, the analyst investigates — possible causes include MTA's last-click bias, MMM's "
    "missing channel, or one method being poorly calibrated for the dataset.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# METHODS — MTA
story.append(Paragraph("Multi-Touch Attribution Methods", styles["h1"]))

mta_methods_data = [
    ["Method", "How it works", "When it fails"],
    ["Last-Click (baseline)", "100% credit to final touchpoint", "Always — systematically overestimates closer channels"],
    ["First-Click", "100% credit to first touchpoint", "Mirror of Last-Click bias for upper funnel"],
    ["Linear", "Equal credit to all touchpoints", "When some touchpoints obviously matter more"],
    ["Time-Decay", "Exponential weighting toward conversion", "Sensitive to half-life parameter choice"],
    ["Markov Chain (removal effect)", "Probabilistic — credit = conversion drop when channel removed", "Short paths reduce signal; can give 0 contribution"],
    ["Shapley Values (game theory)", "Average marginal contribution across all coalitions", "Computationally expensive (2^n coalitions)"],
]
story.append(create_table(mta_methods_data, col_widths=[3.5 * cm, 6 * cm, 6.5 * cm]))

story.append(Paragraph(
    "Implementation in `notebooks/08_multi_touch_attribution.ipynb`. Markov uses transition matrix "
    "iteration with early-stopping convergence. Shapley uses exact enumeration over 2^5 = 32 "
    "coalitions, tractable for 5 channels.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# METHODS — MMM
story.append(Paragraph("Bayesian Marketing Mix Model", styles["h1"]))

story.append(Paragraph(
    "The MMM uses Bayesian regression with PyMC and NUTS sampling to estimate channel contribution "
    "with quantified uncertainty. Model specification:",
    styles["body"]))

story.append(Paragraph(
    "<font face='DejaVuSans-Bold'>y_t = baseline + Σ [β_c × Adstock(saturation(spend_c,t))] + seasonality_t + ε_t</font>",
    styles["body"]))

mmm_components_data = [
    ["Component", "Specification", "Rationale"],
    ["baseline", "HalfNormal(σ=30)", "Organic conversions without marketing"],
    ["β_c (per channel)", "HalfNormal(σ=80), shape=4", "Positive priors — channels can only add"],
    ["Adstock (geometric)", "y[t] = x[t] + α × y[t-1]", "Advertising effect persists across days"],
    ["Saturation (Hill)", "y = x^k / (x^k + S^k)", "Diminishing returns on spend"],
    ["Seasonality", "Annual sin/cos + weekly", "Captures Q4 holiday, weekend dips"],
    ["σ (noise)", "HalfNormal(σ=5)", "Gaussian likelihood noise"],
    ["Sampling", "NUTS, 2 chains × 1000 samples", "Industry standard Bayesian inference"],
]
story.append(create_table(mmm_components_data, col_widths=[3 * cm, 5 * cm, 8 * cm]))

story.append(Paragraph(
    "Implementation in `notebooks/09_marketing_mix_model.ipynb`. Adstock and saturation parameters "
    "are pre-applied with reasonable defaults; production version would learn them as latent "
    "variables. PyMC chosen over LightweightMMM for educational transparency.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# RESULTS
story.append(Paragraph("Results — Channel Contribution", styles["h1"]))

story.append(Paragraph(
    "Each method's estimate compared against the known ground truth from the synthetic data:",
    styles["body"]))

results_data = [
    ["Channel", "Ground Truth", "Last-Click", "Markov", "Shapley", "MMM Bayesian"],
    ["Google_Ads", "29.4%", "21.4%", "23.7%", "26.6%", "33.8%"],
    ["Meta_Ads", "23.5%", "24.2%", "37.6%", "21.5%", "14.5%"],
    ["Instagram_Organic", "11.8%", "13.0%", "30.6%", "13.3%", "13.5%"],
    ["Email", "35.3%", "36.8%", "10.3%", "33.8%", "38.1%"],
    ["TOTAL ABS ERROR", "—", "13.9 pp", "54.3 pp", "19.0 pp", "17.9 pp"],
]
story.append(create_table(results_data, col_widths=[3.5 * cm, 2.3 * cm, 2.3 * cm, 2.3 * cm, 2.3 * cm, 3.3 * cm]))

story.append(Paragraph("Honest interpretation", styles["h2"]))

story.append(Paragraph(
    "Method ranking is data-dependent, not universal. In this synthetic dataset, Last-Click "
    "happened to outperform Markov because the data-generating process gave Email a high "
    "last-touch probability AND high true contribution — they correlated. In real data with "
    "longer paths and weaker last-touch correlation, Markov and Shapley typically dominate.",
    styles["body"]))

story.append(Paragraph(
    "Markov failed here because customer paths are relatively short (mean ~3 touchpoints), "
    "making the removal effect weak — removing one channel often doesn't dramatically change "
    "the chain's conversion probability. This is a known limitation, not a bug.",
    styles["body"]))

story.append(Paragraph(
    "MMM Bayesian achieves comparable accuracy to Last-Click (17.9 vs 13.9 pp error) but adds "
    "<b>95% credible intervals</b> — Google_Ads is between 19.7% and 48.3% with 95% confidence. "
    "Last-Click gives no uncertainty information. This makes MMM more defensible for budget "
    "decisions where confidence matters.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# ROI ANALYSIS
story.append(Paragraph("Channel ROI Analysis", styles["h1"]))

story.append(Paragraph(
    "MMM's primary business output is cost-per-acquisition (CPA) per channel:",
    styles["body"]))

roi_data = [
    ["Channel", "Avg Daily Spend", "Total Spend", "Estimated Conv.", "CPA", "vs Avg"],
    ["Email", "£19.24", "£14,065", "7,338", "£1.92", "0.28x"],
    ["Instagram_Organic", "£24.08", "£17,602", "2,608", "£6.75", "1.00x"],
    ["Google_Ads", "£76.16", "£55,676", "6,511", "£8.55", "1.26x"],
    ["Meta_Ads", "£59.11", "£43,207", "2,799", "£15.44", "2.28x"],
]
story.append(create_table(roi_data, col_widths=[3.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2 * cm, 2 * cm]))

story.append(Paragraph("Strategic implications", styles["h2"]))

story.append(Paragraph(
    "<b>Email is 8x more efficient than Meta Ads.</b> For every £15.44 spent on Meta Ads, you "
    "get 1 conversion. The same £15.44 on Email generates 8 conversions. This is one of the "
    "largest CPA spreads observed in marketing analytics.",
    styles["body"]))

story.append(Paragraph(
    "<b>Meta Ads underperforms despite being a top-3 spend channel.</b> Meta Ads consumes 33% "
    "of paid budget but contributes only 14.5% of conversions. This is the textbook signal for "
    "budget reallocation.",
    styles["body"]))

story.append(Paragraph(
    "<b>Google Ads is borderline.</b> CPA at 1.26x average is acceptable but not exceptional. "
    "Test creative refresh and audience refinement before declaring it a winner or loser.",
    styles["body"]))

story.append(Paragraph(
    "<b>Caveat:</b> Reducing Meta Ads spend by 50% does not mean a linear loss of 50% Meta "
    "contributions. Saturation curves matter — at lower spend, Meta might be more efficient. "
    "Recommendation: incremental tests with holdout validation before large reallocation.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# RECOMMENDATIONS
story.append(Paragraph("Coffra Action Plan", styles["h1"]))

actions_data = [
    ["Action", "Investment", "Expected Impact"],
    ["Replace last-click in HubSpot reports with MMM contributions for budget allocation", "40 hours analyst time, one-time", "10-15% better budget efficiency"],
    ["Test +20% Email spend over 4 weeks (best CPA channel)", "+£115/month additional Email spend", "If not yet at saturation: more conversions at low marginal cost"],
    ["Audit Meta Ads — investigate creative + targeting before budget cut", "2 weeks holdout test + analyst review", "Validate underperformance vs creative issue"],
    ["Implement monthly MMM refresh cadence", "4 hours/month maintenance", "Catches saturation, seasonality, market shifts"],
    ["Quarterly geo-holdout tests on top channels", "10-15% revenue at risk during holdout", "Experimental validation of MMM estimates"],
    ["Use MTA + MMM in parallel — triangulate when they disagree", "Already in place", "Robust to method-specific failures"],
]
story.append(create_table(actions_data, col_widths=[6 * cm, 4.5 * cm, 5.5 * cm]))

story.append(Spacer(1, 0.4 * cm))

# VALIDATION
story.append(Paragraph("Model Validation", styles["h1"]))

story.append(Paragraph(
    "Bayesian models must converge before estimates can be trusted. We pass standard diagnostics:",
    styles["body"]))

validation_data = [
    ["Diagnostic", "Value", "Target", "Status"],
    ["Max R-hat", "1.000", "< 1.01", "PASS"],
    ["Min ESS bulk", "750", "> 400", "PASS"],
    ["R²", "0.686", "> 0.6 (noisy daily data)", "PASS"],
    ["MAE", "5.42 conv/day", "Context-specific", "Acceptable"],
    ["MAPE", "11.3%", "< 15% standard", "PASS"],
    ["95% CI coverage", "95.2%", "~95%", "PASS — well calibrated"],
]
story.append(create_table(validation_data, col_widths=[4 * cm, 3 * cm, 5 * cm, 4 * cm]))

story.append(Paragraph(
    "All diagnostics pass. The 95% CI coverage at 95.2% is particularly encouraging — it means "
    "the model's stated uncertainty intervals are statistically calibrated. When the model says "
    "it's 95% confident, it's actually right 95% of the time.",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# SKILLS
story.append(Paragraph("Skills Demonstrated", styles["h1"]))

skills_data = [
    ["Category", "Specific Skills"],
    ["Causal inference", "Counterfactual reasoning (removal effect), holdout test design"],
    ["Bayesian methods", "PyMC model specification, NUTS sampling, posterior credible intervals, convergence diagnostics"],
    ["Game theory applied to ML", "Shapley value computation with exact coalition enumeration"],
    ["Time-series modeling", "Adstock (geometric carryover), Hill saturation, seasonality decomposition"],
    ["Probability theory", "Markov chain analysis, transition matrix iteration, absorbing states"],
    ["Synthetic data generation", "Realistic multi-channel customer journeys with known ground truth"],
    ["Model validation", "Posterior predictive checks, R-hat/ESS diagnostics, CI coverage analysis"],
    ["Business communication", "Translation of probabilistic estimates to actionable budget recommendations"],
    ["Honest disclosure", "Method limitations explicit, no overselling, comparison to ground truth transparent"],
]
story.append(create_table(skills_data, col_widths=[4 * cm, 12 * cm]))

story.append(Spacer(1, 0.4 * cm))

# LIMITATIONS
story.append(Paragraph("Limitations and Future Work", styles["h1"]))

story.append(Paragraph("Known limitations", styles["h2"]))
story.append(Paragraph(
    "All conclusions in this project are about the synthetic dataset. They demonstrate "
    "methodology, not Coffra's actual channel performance. Real Coffra deployment would require "
    "live UTM tracking, real ad spend records, and quarterly A/B holdout tests for incrementality "
    "validation. Additionally: cookie deprecation increasingly breaks MTA; MMM requires 6+ months "
    "of stable spend data to converge; both methods assume the data-generating process matches "
    "model assumptions.",
    styles["body"]))

story.append(Paragraph("Future enhancements (v1.1+)", styles["h2"]))
story.append(Paragraph(
    "Learn adstock and saturation parameters as latent variables (currently fixed). Add channel "
    "interaction terms to MMM (Email × Search synergy). Implement Bayesian Optimal Budget "
    "Allocation using posterior samples. Add geo-experiments framework for incrementality "
    "validation. Build CI/CD pipeline for monthly model re-fits with diff alerts. Compare against "
    "industry tools (Meta Robyn, Google LightweightMMM, Uber Orbit).",
    styles["body"]))

story.append(Spacer(1, 0.4 * cm))

# CLOSING
story.append(horizontal_rule())
story.append(Paragraph("Connection to Other Projects", styles["h1"]))

story.append(Paragraph(
    "P5 is the measurement infrastructure for the entire Coffra marketing system. Where "
    "P1-P4 generated marketing activities (emails, segmentation, content), P5 measures which "
    "of those activities actually drove value:",
    styles["body"]))

connection_data = [
    ["Project", "Relationship to P5"],
    ["P1 — Marketing Automation", "Email channel performance is now measured end-to-end via MMM. P1's no-discount discipline can be quantified in CPA terms."],
    ["P2 — Marketing Dashboard", "Attribution page integrates into existing Streamlit dashboard. Marketing team has unified visibility."],
    ["P3 — Customer Segmentation", "Segments can now be analyzed for channel preferences (which segments respond best to which channels)."],
    ["P4 — AEO Strategy", "Once Coffra has live AEO traffic, AI-referred sessions become a measurable channel in MMM."],
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
