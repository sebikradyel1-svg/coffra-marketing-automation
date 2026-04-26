"""
Coffra Dashboard - Shared plotting utilities.

Plotly charts with brand-aligned styling. All charts use the Coffra color
palette and consistent typography.
"""

import plotly.graph_objects as go
import plotly.express as px

from .styling import (
    COFFRA_BROWN, COFFRA_BROWN_LIGHT, COFFRA_CREAM, COFFRA_ACCENT,
    DARK_GRAY, MEDIUM_GRAY, LIGHT_GRAY,
)

# Categorical color sequence for multi-series charts
COFFRA_PALETTE = [
    COFFRA_BROWN,
    COFFRA_ACCENT,
    "#8D6E63",
    "#A1887F",
    "#BCAAA4",
    COFFRA_BROWN_LIGHT,
]


def apply_brand_layout(fig, title=None, height=400):
    """Apply consistent layout settings to a Plotly figure."""
    fig.update_layout(
        title=title,
        title_font_color=COFFRA_BROWN,
        title_font_size=16,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="sans-serif", color=DARK_GRAY, size=12),
        height=height,
        margin=dict(l=40, r=40, t=60 if title else 30, b=40),
        xaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY, zeroline=False),
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=LIGHT_GRAY,
            borderwidth=1,
        ),
    )
    return fig


def bar_chart(x, y, title=None, color=None, horizontal=False, height=400):
    """Brand-styled bar chart."""
    if color is None:
        color = COFFRA_BROWN

    if horizontal:
        fig = go.Figure(data=[go.Bar(
            x=y, y=x, orientation="h",
            marker_color=color,
            hovertemplate="%{y}: %{x}<extra></extra>",
        )])
    else:
        fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            marker_color=color,
            hovertemplate="%{x}: %{y}<extra></extra>",
        )])

    return apply_brand_layout(fig, title=title, height=height)


def grouped_bar_chart(df, x, y, color, title=None, height=400):
    """Multi-series bar chart."""
    fig = px.bar(
        df, x=x, y=y, color=color,
        color_discrete_sequence=COFFRA_PALETTE,
        barmode="group",
    )
    return apply_brand_layout(fig, title=title, height=height)


def donut_chart(labels, values, title=None, height=400):
    """Brand-styled donut chart."""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=COFFRA_PALETTE[:len(labels)],
        textinfo="label+percent",
        textposition="outside",
    )])
    return apply_brand_layout(fig, title=title, height=height)


def line_chart(x, y, title=None, height=400, name=None):
    """Brand-styled line chart."""
    fig = go.Figure(data=[go.Scatter(
        x=x, y=y, mode="lines+markers",
        line=dict(color=COFFRA_BROWN, width=2.5),
        marker=dict(color=COFFRA_BROWN, size=8),
        name=name or "value",
    )])
    return apply_brand_layout(fig, title=title, height=height)


def funnel_chart(stages, values, title=None, height=500):
    """Brand-styled funnel chart for marketing pipeline visualization."""
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        marker=dict(
            color=[COFFRA_BROWN, COFFRA_BROWN_LIGHT, COFFRA_ACCENT, "#8D6E63"][:len(stages)],
        ),
    ))
    apply_brand_layout(fig, title=title, height=height)
    # Hide x/y axis grids for funnel - they look noisy
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=True, showgrid=False),
    )
    return fig


def histogram(values, bins=30, title=None, x_label="Value", height=400):
    """Brand-styled histogram."""
    fig = go.Figure(data=[go.Histogram(
        x=values,
        nbinsx=bins,
        marker_color=COFFRA_BROWN,
        opacity=0.85,
    )])
    fig.update_layout(xaxis_title=x_label, yaxis_title="Count")
    return apply_brand_layout(fig, title=title, height=height)


def gauge_chart(value, max_value=100, title=None, label="Score", height=300):
    """Brand-styled gauge for single metric display (e.g., model AUC)."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": label, "font": {"size": 14, "color": DARK_GRAY}},
        gauge={
            "axis": {"range": [0, max_value], "tickcolor": MEDIUM_GRAY},
            "bar": {"color": COFFRA_BROWN},
            "bgcolor": "white",
            "borderwidth": 1,
            "bordercolor": LIGHT_GRAY,
            "steps": [
                {"range": [0, max_value * 0.5], "color": "#FAFAFA"},
                {"range": [max_value * 0.5, max_value * 0.75], "color": COFFRA_CREAM},
                {"range": [max_value * 0.75, max_value], "color": "#D7CCC8"},
            ],
        },
        number={"font": {"color": COFFRA_BROWN, "size": 32}},
    ))
    return apply_brand_layout(fig, title=title, height=height)
