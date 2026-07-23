"""
Outreach Agent for Coffra.

Drafts a first-touch message for a HOT-qualified lead, grounded in
data/brand_sources.md via RAG (rag/brand_index.py) so product/brand
claims come only from approved sources rather than being invented.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag.brand_index import get_relevant_chunks  # noqa: E402

load_dotenv()

MODEL = "claude-sonnet-5"
MAX_TOKENS = 4096
RETRIEVAL_K = 3

SYSTEM_PROMPT = """Ești Outreach Agent pentru Coffra. Sarcina: redactezi un mesaj de prim
contact (first-touch) personalizat pentru un lead calificat HOT.

Primești: (a) datele și contextul lead-ului, (b) rezultatul calificării
(de ce e HOT), (c) SURSE DE BRAND aprobate — talking points și propuneri
de valoare, retrase prin RAG.

Grounding (prioritate zero):
- Orice afirmație despre produs, beneficii sau rezultate trebuie să vină
  DIN sursele aprobate. Dacă un lucru nu e în surse, NU îl afirma.
- Nu inventa cifre, studii de caz sau garanții.

Stil:
- Ton B2B profesional, direct, cald — fără hype, fără superlative goale,
  fără presiune ("act now", "limited offer").
- Text simplu, fără formatare decorativă, fără emoji.
- Scurt: 4-6 propoziții. Un singur call-to-action clar, low-friction.
- Personalizare REALĂ: leagă mesajul de contextul specific al lead-ului
  (rol, companie, semnalul care l-a făcut HOT), nu o formulă generică.

Structură:
1. Deschidere personalizată (ancorată în contextul lead-ului).
2. Relevanță: de ce îl contactezi, legat de nevoia lui probabilă.
3. Valoarea (doar din surse aprobate).
4. Un singur CTA low-friction.

Returnează STRICT JSON:
{
  "subject": "linie de subiect scurtă și specifică",
  "message": "corpul mesajului, text simplu",
  "personalization_basis": "ce element de context ai folosit"
}

Draftul tău merge apoi la Governance Reviewer și la aprobare umană —
scrie ca și cum ar fi verificat, pentru că va fi."""


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()
    # Claude occasionally escapes apostrophes as \' inside JSON strings;
    # that's not a valid JSON escape (apostrophes never need escaping)
    # and breaks json.loads, so strip it before parsing.
    cleaned = cleaned.replace("\\'", "'")
    return json.loads(cleaned)


def _build_retrieval_query(lead: dict[str, Any], qualification_result: dict[str, Any]) -> str:
    parts = [qualification_result.get("reasoning", "")]
    parts += [str(f) for f in qualification_result.get("top_factors", [])]
    return " ".join(p for p in parts if p)


def run_outreach(lead: dict[str, Any], qualification_result: dict[str, Any]) -> dict[str, Any]:
    """
    Draft a first-touch outreach message for a HOT-qualified lead.

    Retrieves the most relevant approved brand talking points for this
    lead's specific qualification signal, then asks Claude to draft the
    message using only that retrieved context plus the lead/qualification
    data - per SYSTEM_PROMPT's grounding rule.
    """
    query = _build_retrieval_query(lead, qualification_result)
    brand_chunks = get_relevant_chunks(query, k=RETRIEVAL_K)
    brand_context = "\n\n".join(f"- {chunk}" for chunk in brand_chunks)

    user_message = (
        "DATE LEAD:\n"
        + json.dumps(lead, ensure_ascii=False, indent=2)
        + "\n\nREZULTAT CALIFICARE:\n"
        + json.dumps(qualification_result, ensure_ascii=False, indent=2)
        + "\n\nSURSE DE BRAND APROBATE (retrase prin RAG):\n"
        + brand_context
    )

    client = Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    final_text = "".join(block.text for block in response.content if block.type == "text")
    if not final_text.strip():
        raise RuntimeError(
            f"Outreach Agent returned no text (stop_reason={response.stop_reason!r}); "
            "likely ran out of max_tokens during thinking - increase MAX_TOKENS."
        )
    return _extract_json(final_text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    from agents.qualification import run_qualification

    hot_lead = {
        "Age": 43, "Income": 30558, "AdSpend": 2076.535113910116, "WebsiteVisits": 9,
        "PagesPerVisit": 7.818844717795544, "TimeOnSite": 14.229981592378053, "SocialShares": 83,
        "EmailOpens": 11, "EmailClicks": 4, "PreviousPurchases": 2, "LoyaltyPoints": 951,
        "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False, "CampaignType_Conversion": True, "CampaignType_Retention": False,
    }

    qualification_result = run_qualification(hot_lead)
    print("=== Qualification result ===")
    print(json.dumps(qualification_result, ensure_ascii=False, indent=2))

    outreach_result = run_outreach(hot_lead, qualification_result)
    print("\n=== Outreach draft ===")
    print(json.dumps(outreach_result, ensure_ascii=False, indent=2))
