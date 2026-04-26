"""
HubSpot CRM Page - Snapshot data from HubSpot Marketing Hub trial.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from lib.styling import inject_custom_css, page_header, data_disclosure
from lib.data_loaders import (
    load_hubspot_contacts,
    load_hubspot_segments,
    load_hubspot_personas,
    load_hubspot_metadata,
    map_persona_label,
)
from lib.plots import donut_chart


st.set_page_config(page_title="HubSpot CRM | Coffra", layout="wide")
inject_custom_css()

page_header(
    "HubSpot CRM Snapshot",
    "Contacts, segments, and persona distribution from the HubSpot trial deployment"
)

metadata = load_hubspot_metadata()
extracted_at = metadata.get("extracted_at_human", "(not recorded)")
trial_expires = metadata.get("trial_expires", "2026-05-09")

data_disclosure(
    "snapshot",
    f"Data captured on {extracted_at}. HubSpot trial expires {trial_expires}. "
    "After expiry, this snapshot remains stable while the live API access is revoked."
)


# ============================================================
# LOAD DATA
# ============================================================
contacts = load_hubspot_contacts()
segments = load_hubspot_segments()
personas_data = load_hubspot_personas()


# ============================================================
# OVERVIEW METRICS
# ============================================================
st.markdown("## Snapshot Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Contacts", len(contacts))
with c2:
    st.metric("Active Segments", len(segments))
with c3:
    distribution = personas_data.get("distribution", {})
    persona_count = len([k for k in distribution.keys() if k != "(unset)"])
    st.metric("Personas Used", persona_count)


# ============================================================
# PERSONA DISTRIBUTION
# ============================================================
st.markdown("## Persona Distribution")

distribution = personas_data.get("distribution", {})

if distribution:
    # Map internal values to friendly labels
    labels = [map_persona_label(k) for k in distribution.keys()]
    values = list(distribution.values())

    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.plotly_chart(
            donut_chart(
                labels=labels,
                values=values,
                title="Contacts per persona",
                height=320,
            ),
            use_container_width=True,
        )

    with col_r:
        st.markdown("### Persona Property")
        prop_def = personas_data.get("property_definition", {})
        if prop_def:
            st.markdown(f"**Property name:** `{prop_def.get('name', 'N/A')}`")
            st.markdown(f"**Label:** {prop_def.get('label', 'N/A')}")
            st.markdown(f"**Field type:** {prop_def.get('field_type', 'N/A')}")

            options = prop_def.get("options", [])
            if options:
                st.markdown("**Options configured:**")
                for opt in options:
                    if opt.get("hidden"):
                        continue
                    st.markdown(f"- {opt.get('label', opt.get('value', 'N/A'))}")
        else:
            st.caption("Property definition not available in snapshot.")
else:
    st.info("No persona data in snapshot.")


# ============================================================
# CONTACTS TABLE
# ============================================================
st.markdown("## Contacts")

if contacts:
    rows = []
    for c in contacts:
        props = c.get("properties", {})
        rows.append({
            "Email": props.get("email", "—"),
            "First Name": props.get("firstname", "—"),
            "Last Name": props.get("lastname", "—"),
            "Persona": map_persona_label(props.get("hs_persona", "(unset)")),
            "Lifecycle Stage": props.get("lifecyclestage", "—"),
            "Created": (c.get("created_at", "")[:10] if c.get("created_at") else "—"),
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No contacts in snapshot.")


# ============================================================
# SEGMENTS TABLE
# ============================================================
st.markdown("## Active Segments")

if segments:
    rows = []
    for s in segments:
        rows.append({
            "Name": s.get("name", "—"),
            "Type": s.get("type", "—"),
            "Size": s.get("size") or "—",
            "ID": s.get("id", "—"),
        })
    df_seg = pd.DataFrame(rows)
    st.dataframe(df_seg, use_container_width=True, hide_index=True)
else:
    st.info("No segments in snapshot. (Segments may have failed to extract.)")


# ============================================================
# WORKFLOWS NOTE
# ============================================================
st.markdown("## Workflows")

st.markdown(
    """
    Three workflows were configured in HubSpot to visualize automation logic:

    - **Connoisseur Nurture Sequence** — 5 emails over 14 days (T+0, T+3, T+6, T+10, T+14)
    - **Daily Ritualist Nurture Sequence** — 5 emails RO over 14 days, parallel to Connoisseur
    - **Cart Recovery Sequence (Connoisseur)** — 3 emails at T+1h, T+24h, T+72h

    Note: HubSpot trial allows visualizing workflow logic but locks the "Send marketing email"
    action behind Marketing Hub Pro. Workflow screenshots are in
    `screenshots/hubspot/` and full specs are in `docs/07_hubspot_workflow_specs.md`.

    Production deployment would migrate to either Marketing Hub Pro (paid) or Brevo (free
    tier supports automation workflows with native email sends).
    """
)


# ============================================================
# RAW JSON ACCESS (for transparency)
# ============================================================
with st.expander("Raw snapshot data"):
    st.markdown("**Metadata**")
    st.json(metadata)

    if contacts:
        st.markdown("**First contact (raw)**")
        st.json(contacts[0])
