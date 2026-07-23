"""
Governance Reviewer for the Coffra outreach system.

Last automated filter before human approval: evaluates an Outreach
Agent draft against a strict rubric (grounding, brand voice, banned
patterns, compliance, personalization) and returns a structured
APPROVE/REVISE verdict. Does not rewrite the message.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
BRAND_SOURCES_PATH = ROOT_DIR / "data" / "brand_sources.md"

load_dotenv()

MODEL = "claude-sonnet-5"
MAX_TOKENS = 4096

SYSTEM_PROMPT = """Ești Governance Reviewer pentru sistemul de outreach al Coffra.
Rolul tău NU e să scrii sau să îmbunătățești mesajul, ci să îl
EVALUEZI împotriva unei rubrici stricte și să returnezi un verdict
structurat. Ești ultimul filtru înainte de review-ul uman.

Primești: (a) mesajul de outreach draftat, (b) contextul lead-ului,
(c) sursele de brand aprobate (talking points).

PASUL 1 — Descompune mesajul în afirmații individuale (claims).
O propoziție poate conține mai multe afirmații distincte, unite prin
virgulă sau conjuncție — separă-le. Tratează fiecare afirmație
descriptivă despre brand, produs sau rezultate ca pe un claim de
verificat separat, chiar dacă e atașată lângă un fapt real (ex:
"Coffra e un brand D2C de cafea de specialitate" + "gândit pentru
ritual personal, nu standardizat" = DOUĂ claims distincte, nu unul).

PASUL 2 — Pentru fiecare claim, verifică dacă apare, literal sau
parafrazat fără adăugiri, în sursele de brand aprobate. Dacă nu
apare → unsupported.

PASUL 3 — Evaluează și celelalte criterii:
2. BRAND VOICE — tonul respectă vocea de brand (profesional, direct,
   fără hype gol)? Superlative nefondate → FLAG.
3. BANNED PATTERNS — fraze interzise, presiune agresivă, "act now /
   limited time" nepotrivit B2B? → FLAG.
4. COMPLIANCE — overpromising, garanții absolute, afirmații
   potențial înșelătoare? → FLAG.
5. PERSONALIZATION — personalizare reală (bazată pe context) sau
   generică? Generică → FLAG (soft).

Returnează STRICT în acest format JSON:
{
  "claims_checked": [
    {"claim": "text exact al afirmației", "supported": true|false,
     "note": "unde apare în surse, sau de ce nu apare"}
  ],
  "verdict": "APPROVE" | "REVISE",
  "flags": [
    {"criterion": "...", "severity": "hard" | "soft", "reason": "..."}
  ],
  "summary": "o frază despre decizie"
}

Reguli: orice claim din "claims_checked" cu supported=false generează
AUTOMAT un flag "hard" pe CLAIMS și verdict "REVISE" — nu poți da
APPROVE dacă există măcar un claim unsupported. Un singur flag "hard"
per total înseamnă verdict "REVISE". Doar flags "soft" pot rămâne
"APPROVE" dar le raportezi pentru omul care revizuiește. Nu inventezi
motive; dacă totul e curat, returnezi APPROVE cu flags gol. Fii strict
la descompunere — nu evalua propoziții per ansamblu."""


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


def run_governance(draft: dict[str, Any], lead: dict[str, Any]) -> dict[str, Any]:
    """
    Review an Outreach Agent draft against the governance rubric.

    draft: the {"subject", "message", "personalization_basis"} dict
        returned by agents.outreach.run_outreach.
    lead: the lead dict the draft was written for.

    Returns the parsed {"verdict", "flags", "summary"} dict.
    """
    brand_sources = BRAND_SOURCES_PATH.read_text(encoding="utf-8")

    user_message = (
        "MESAJ DE OUTREACH DRAFTAT:\n"
        + json.dumps(draft, ensure_ascii=False, indent=2)
        + "\n\nCONTEXTUL LEAD-ULUI:\n"
        + json.dumps(lead, ensure_ascii=False, indent=2)
        + "\n\nSURSE DE BRAND APROBATE:\n"
        + brand_sources
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
            f"Governance Reviewer returned no text (stop_reason={response.stop_reason!r})."
        )
    return _extract_json(final_text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    hot_lead = {
        "Age": 43, "Income": 30558, "AdSpend": 2076.535113910116, "WebsiteVisits": 9,
        "PagesPerVisit": 7.818844717795544, "TimeOnSite": 14.229981592378053, "SocialShares": 83,
        "EmailOpens": 11, "EmailClicks": 4, "PreviousPurchases": 2, "LoyaltyPoints": 951,
        "Gender_Male": False, "CampaignChannel_PPC": False, "CampaignChannel_Referral": False,
        "CampaignChannel_SEO": False, "CampaignChannel_Social Media": False,
        "CampaignType_Consideration": False, "CampaignType_Conversion": True, "CampaignType_Retention": False,
    }

    outreach_draft = {
        "subject": "Continuăm experiența ta cu Coffra?",
        "message": (
            "Bună, am observat că ai petrecut timp semnificativ explorând site-ul Coffra "
            "și ai parcurs mai multe pagini într-o singură vizită, semn că ceva din oferta "
            "noastră de cafea de specialitate ți-a atras atenția. Vii dintr-o campanie "
            "orientată spre conversie și ai deja două achiziții anterioare, ceea ce ne spune "
            "că nu ești la prima interacțiune cu brandul. Coffra este un brand D2C de cafea "
            "de specialitate, gândit pentru cei care tratează ritualul cafelei ca pe ceva "
            "personal, nu standardizat. Aș vrea să înțeleg mai bine ce cauți acum, ca să "
            "vedem dacă are sens o experiență adaptată nevoilor tale. Ai 10 minute pentru "
            "un schimb scurt pe email sau telefon în această săptămână?"
        ),
        "personalization_basis": (
            "Lead provine dintr-o campanie CampaignType_Conversion, are TimeOnSite ridicat "
            "și PagesPerVisit mare (semnal de engagement activ), plus 2 achiziții anterioare, "
            "ceea ce indică un client existent cu interes reactivat, nu un prim contact rece."
        ),
    }

    verdict = run_governance(outreach_draft, hot_lead)
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
