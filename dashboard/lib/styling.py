"""
Coffra Dashboard - Shared styling and theme.

Brand colors and CSS injection helpers used across all dashboard pages.
Keeps visual consistency without per-page duplication.
"""

import streamlit as st

# Brand colors (consistent with case study PDF and email design)
COFFRA_BROWN = "#3E2723"
COFFRA_BROWN_LIGHT = "#6D4C41"
COFFRA_CREAM = "#EFEBE9"
COFFRA_ACCENT = "#A1887F"
DARK_GRAY = "#212121"
MEDIUM_GRAY = "#616161"
LIGHT_GRAY = "#E0E0E0"


def inject_custom_css():
    """Inject custom CSS for Coffra branding across all pages."""
    st.markdown(
        f"""
        <style>
        /* Hide default Streamlit chrome where appropriate */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Brand-aligned headers */
        h1 {{
            color: {COFFRA_BROWN};
            font-weight: 700;
        }}
        h2 {{
            color: {COFFRA_BROWN_LIGHT};
            font-weight: 600;
            border-bottom: 2px solid {COFFRA_CREAM};
            padding-bottom: 0.3em;
        }}
        h3 {{
            color: {DARK_GRAY};
            font-weight: 600;
        }}

        /* Metric containers */
        [data-testid="stMetric"] {{
            background-color: {COFFRA_CREAM};
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid {COFFRA_BROWN};
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #FAFAFA;
        }}

        /* Buttons */
        .stButton button {{
            background-color: {COFFRA_BROWN};
            color: white;
            border: none;
            border-radius: 4px;
        }}
        .stButton button:hover {{
            background-color: {COFFRA_BROWN_LIGHT};
            color: white;
        }}

        /* Rename main page in sidebar (streamlit_dashboard -> Overview) */
        [data-testid="stSidebarNav"] ul li:first-child a span {{
            visibility: hidden;
            position: relative;
        }}
        [data-testid="stSidebarNav"] ul li:first-child a span::before {{
            content: "Overview";
            visibility: visible;
            position: absolute;
            left: 0;
        }}

        /* Info/warning boxes brand color */
        [data-testid="stNotificationContentInfo"] {{
            border-left-color: {COFFRA_BROWN_LIGHT};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = None):
    """Render a consistent page header across all dashboard pages."""
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(
            f"<p style='color: {MEDIUM_GRAY}; font-size: 1.1rem; margin-top: -0.5rem;'>{subtitle}</p>",
            unsafe_allow_html=True,
        )
    st.markdown("---")


def data_disclosure(level: str, message: str):
    """
    Render a clear data disclosure banner.

    level: 'real', 'snapshot', or 'simulated'
    """
    icon_color = {
        "real": COFFRA_BROWN,
        "snapshot": COFFRA_BROWN_LIGHT,
        "simulated": "#D84315",  # Distinct orange-red so simulated data is visually clear
    }.get(level, MEDIUM_GRAY)

    label = {
        "real": "REAL DATA",
        "snapshot": "SNAPSHOT (April 2026)",
        "simulated": "SIMULATED DATA",
    }.get(level, "DATA")

    st.markdown(
        f"""
        <div style='background-color: {COFFRA_CREAM};
                    border-left: 4px solid {icon_color};
                    padding: 0.8rem 1rem;
                    border-radius: 4px;
                    margin: 1rem 0;'>
            <strong style='color: {icon_color};'>{label}</strong>
            <span style='color: {DARK_GRAY}; margin-left: 0.5rem;'>{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
