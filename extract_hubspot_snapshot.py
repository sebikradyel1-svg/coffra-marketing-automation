"""
HubSpot Data Snapshot Extractor

Pulls a one-time snapshot of contacts, lists/segments, and persona property values
from HubSpot via the Private App API. Saves results as JSON files for the dashboard
to read locally — avoiding the need for live API calls (which would break after
trial expiry).

Usage:
    python extract_hubspot_snapshot.py

Output:
    data/snapshots/contacts.json
    data/snapshots/segments.json
    data/snapshots/persona_distribution.json
    data/snapshots/snapshot_metadata.json

Environment:
    Requires HUBSPOT_PRIVATE_APP_TOKEN in .env file.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# ============================================================
# CONFIG
# ============================================================
load_dotenv()

TOKEN = os.getenv("HUBSPOT_PRIVATE_APP_TOKEN")
if not TOKEN:
    raise RuntimeError(
        "HUBSPOT_PRIVATE_APP_TOKEN not found in .env. "
        "Generate one at: HubSpot Settings → Private Apps."
    )

BASE_URL = "https://api.hubapi.com"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

OUTPUT_DIR = Path("data/snapshots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# API HELPERS
# ============================================================

def get(endpoint, params=None):
    """GET wrapper with error handling."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params or {})
    response.raise_for_status()
    return response.json()


def post(endpoint, payload):
    """POST wrapper with error handling."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# ============================================================
# EXTRACT FUNCTIONS
# ============================================================

def extract_contacts():
    """Pull all contacts with their key properties."""
    print("Extracting contacts...")

    properties_to_pull = [
        "email", "firstname", "lastname",
        "lifecyclestage", "hs_lead_status",
        "hs_persona", "createdate",
        "hs_email_open", "hs_email_click",
    ]

    all_contacts = []
    after = None

    while True:
        params = {
            "limit": 100,
            "properties": ",".join(properties_to_pull),
        }
        if after:
            params["after"] = after

        result = get("/crm/v3/objects/contacts", params=params)

        for contact in result.get("results", []):
            all_contacts.append({
                "id": contact["id"],
                "properties": contact.get("properties", {}),
                "created_at": contact.get("createdAt"),
                "updated_at": contact.get("updatedAt"),
            })

        # Pagination
        paging = result.get("paging", {})
        next_page = paging.get("next")
        if not next_page:
            break
        after = next_page.get("after")

    print(f"  Found {len(all_contacts)} contacts.")
    return all_contacts


def extract_segments():
    """Pull all lists/segments with metadata."""
    print("Extracting segments (lists)...")

    # Use the v1 lists endpoint — more stable for lists/segments
    try:
        result = get("/contacts/v1/lists", params={"count": 100})
        lists_data = result.get("lists", [])
    except requests.HTTPError as e:
        print(f"  v1 lists endpoint failed: {e}. Trying v3 lists...")
        try:
            result = post("/crm/v3/lists/search", {"limit": 100})
            lists_data = result.get("lists", [])
        except requests.HTTPError as e2:
            print(f"  v3 lists also failed: {e2}. Returning empty.")
            return []

    segments = []
    for lst in lists_data:
        segments.append({
            "id": lst.get("listId") or lst.get("id"),
            "name": lst.get("name"),
            "type": lst.get("listType") or lst.get("processingType"),
            "size": lst.get("metaData", {}).get("size") or lst.get("additionalProperties", {}).get("hs_list_size"),
            "created_at": lst.get("createdAt"),
            "updated_at": lst.get("updatedAt"),
        })

    print(f"  Found {len(segments)} segments.")
    return segments


def compute_persona_distribution(contacts):
    """Aggregate persona property values across contacts."""
    print("Computing persona distribution...")

    distribution = {}
    for c in contacts:
        persona = c.get("properties", {}).get("hs_persona")
        if persona:
            distribution[persona] = distribution.get(persona, 0) + 1
        else:
            distribution["(unset)"] = distribution.get("(unset)", 0) + 1

    print(f"  Distribution: {distribution}")
    return distribution


def extract_persona_property_definition():
    """Pull the persona property definition (options, descriptions)."""
    print("Extracting persona property definition...")

    try:
        result = get("/crm/v3/properties/contacts/hs_persona")
        return {
            "name": result.get("name"),
            "label": result.get("label"),
            "type": result.get("type"),
            "field_type": result.get("fieldType"),
            "options": result.get("options", []),
        }
    except requests.HTTPError as e:
        print(f"  Property definition fetch failed: {e}")
        return {}


# ============================================================
# MAIN
# ============================================================

def main():
    print(f"\nHubSpot Snapshot Extraction — {datetime.now().isoformat()}")
    print("=" * 60)

    # Pull all data
    contacts = extract_contacts()
    segments = extract_segments()
    persona_distribution = compute_persona_distribution(contacts)
    persona_definition = extract_persona_property_definition()

    # Build metadata
    metadata = {
        "extracted_at": datetime.now().isoformat(),
        "extracted_at_human": datetime.now().strftime("%B %d, %Y at %H:%M"),
        "source": "HubSpot Marketing Hub trial via Private App API",
        "trial_expires": "2026-05-09",
        "counts": {
            "contacts": len(contacts),
            "segments": len(segments),
            "personas": len(persona_distribution),
        },
        "note": (
            "This is a one-time snapshot used by the Coffra Marketing Dashboard. "
            "In production, this script would be scheduled (e.g., daily cron job) "
            "to refresh data. For portfolio purposes, snapshot remains static "
            "post-trial-expiry."
        ),
    }

    # Save all to JSON
    files_saved = []

    contacts_path = OUTPUT_DIR / "contacts.json"
    with open(contacts_path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    files_saved.append(contacts_path)

    segments_path = OUTPUT_DIR / "segments.json"
    with open(segments_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)
    files_saved.append(segments_path)

    persona_path = OUTPUT_DIR / "persona_distribution.json"
    with open(persona_path, "w", encoding="utf-8") as f:
        json.dump({
            "distribution": persona_distribution,
            "property_definition": persona_definition,
        }, f, indent=2, ensure_ascii=False)
    files_saved.append(persona_path)

    metadata_path = OUTPUT_DIR / "snapshot_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    files_saved.append(metadata_path)

    print("\n" + "=" * 60)
    print("Snapshot complete. Files saved:")
    for fp in files_saved:
        size_kb = fp.stat().st_size / 1024
        print(f"  {fp} ({size_kb:.1f} KB)")
    print("\nReady for Streamlit dashboard.")


if __name__ == "__main__":
    main()
