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

sys.path.insert(0, str(ROOT_DIR))
from utils.rate_limiter import call_claude  # noqa: E402

load_dotenv()

MODEL = "claude-sonnet-5"
MAX_TOKENS = 16000

SYSTEM_PROMPT = """Ești Governance Reviewer pentru sistemul de outreach al Coffra.
Rolul tău NU e să scrii sau să îmbunătățești mesajul, ci să îl
EVALUEZI împotriva unei rubrici stricte și să apelezi tool-ul
governance_verdict cu rezultatul structurat. Ești ultimul filtru
înainte de review-ul uman.

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

Apelează OBLIGATORIU tool-ul governance_verdict cu rezultatul - nu
răspunde în text liber.

Reguli: orice claim din "claims_checked" cu supported=false generează
AUTOMAT un flag "hard" pe CLAIMS și verdict "REVISE" — nu poți da
APPROVE dacă există măcar un claim unsupported. Un singur flag "hard"
per total înseamnă verdict "REVISE". Doar flags "soft" pot rămâne
"APPROVE" dar le raportezi pentru omul care revizuiește. Nu inventezi
motive; dacă totul e curat, returnezi APPROVE cu flags gol. Fii strict
la descompunere — nu evalua propoziții per ansamblu."""

GOVERNANCE_VERDICT_TOOL = {
    "name": "governance_verdict",
    "description": (
        "Records the structured governance review result for an outreach "
        "draft: the claim-by-claim grounding check, any rubric flags, the "
        "final APPROVE/REVISE verdict, and a one-sentence summary."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "claims_checked": {
                "type": "array",
                "description": "Every individual claim extracted from the draft.",
                "items": {
                    "type": "object",
                    "properties": {
                        "claim": {"type": "string", "description": "Exact text of the claim."},
                        "supported": {"type": "boolean"},
                        "note": {
                            "type": "string",
                            "description": "Where it appears in sources, or why not - max 15 words.",
                        },
                    },
                    "required": ["claim", "supported", "note"],
                },
            },
            "verdict": {"type": "string", "enum": ["APPROVE", "REVISE"]},
            "flags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "criterion": {"type": "string"},
                        "severity": {"type": "string", "enum": ["hard", "soft"]},
                        "reason": {"type": "string"},
                    },
                    "required": ["criterion", "severity", "reason"],
                },
            },
            "summary": {"type": "string", "description": "One sentence about the decision."},
        },
        "required": ["claims_checked", "verdict", "flags", "summary"],
    },
}


def run_governance(draft: dict[str, Any], lead: dict[str, Any]) -> dict[str, Any]:
    """
    Review an Outreach Agent draft against the governance rubric.

    draft: the {"subject", "message", "personalization_basis"} dict
        returned by agents.outreach.run_outreach.
    lead: the lead dict the draft was written for.

    Returns the {"claims_checked", "verdict", "flags", "summary"} dict,
    taken directly from the model's governance_verdict tool call - no
    manual JSON text parsing involved.
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
    response = call_claude(
        client,
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[GOVERNANCE_VERDICT_TOOL],
        tool_choice={"type": "tool", "name": "governance_verdict"},
        messages=[{"role": "user", "content": user_message}],
    )

    if response.stop_reason == "max_tokens":
        raise RuntimeError(
            "Governance Reviewer response was truncated (stop_reason='max_tokens') - "
            "the claim decomposition for this draft was too long for MAX_TOKENS. "
            "Increase MAX_TOKENS or shorten the claims_checked 'note' field in the prompt."
        )

    for block in response.content:
        if block.type == "tool_use" and block.name == "governance_verdict":
            return block.input

    raise RuntimeError(
        f"Governance Reviewer did not call governance_verdict (stop_reason={response.stop_reason!r})."
    )


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
