"""
v3 — corrected after the first real run against your governance.py.

WHAT CHANGED FROM v2
---------------------
v2's real-run results showed 100% recall (never missed a real problem —
good) but only 68% precision (over-flagged 14 of 20 clean drafts).

Digging into WHY: most v2 "PASS" drafts included personalization language
like "you've opened our emails several times, so we moved you to weekly
contact." The eval harness passes an empty lead={} dict (no real lead
data), so the agent had nothing to verify that specific behavioral claim
against — and correctly flagged it. That's not a bug in your agent, it's
a confound in the test: I was testing brand-fact grounding, but some
drafts accidentally also asked the agent to verify lead-specific claims
it was never given data for. (I also mislabeled D01 in v2 — it repeated
the same ungrounded "personal ritual" phrase as D41 but I'd only checked
one of its two claims.)

v3 removes ALL lead-specific personalization claims. Every draft here is
a claim about Coffra's brand, product, or marketing system — the kind of
thing brand_sources.md actually documents. This isolates exactly one
question: does the agent correctly verify claims against approved brand
sources? Testing whether it correctly grounds PERSONALIZATION claims
against real lead data is a legitimate follow-on test, but it needs
drafts paired with matching lead dicts — a different, smaller exercise,
not this one.

Same labeling policy as before:
  - claim status: "supported" / "contradicted" / "ungrounded"
  - draft verdict: PASS only if every claim is "supported"
                   REVISE if any claim is "contradicted" or "ungrounded"
"""
import json

drafts = []

def add(id, persona, text, claims, notes=""):
    verdict = "PASS" if all(c["status"] == "supported" for c in claims) else "REVISE"
    drafts.append({
        "id": id, "persona": persona, "draft_text": text,
        "claims": claims, "ground_truth_verdict": verdict, "notes": notes
    })

# ---------- PASS: 20 drafts, brand/product/system facts only ----------

add("D01", "Connoisseur",
    "Coffra is a specialty coffee brand based in Timișoara — the whole project is deliberately fictional, built as a portfolio sandbox rather than a real business.",
    [{"text": "brand fictiv, sandbox, Timișoara", "status": "supported", "fact_id": "F01"}])

add("D02", "Daily Ritualist",
    "Lead-urile cu scor între 80 și 100 sar peste coada de nurture și primesc direct un email personal.",
    [{"text": "scor 80-100 = handoff imediat, email personal", "status": "supported", "fact_id": "F02"}])

add("D03", "Connoisseur",
    "The engine behind our recommendations is an XGBoost model, tested at 0.7843 ROC-AUC against a 0.7643 logistic regression baseline.",
    [{"text": "XGBoost, 0.7843 vs 0.7643", "status": "supported", "fact_id": "F05"}])

add("D04", "Daily Ritualist",
    "Secvența noastră de nurture are 13 emailuri, împărțite pe două parcursuri de persona.",
    [{"text": "13 emailuri, 2 parcursuri", "status": "supported", "fact_id": "F06"}])

add("D05", "Connoisseur",
    "We never promise guaranteed results in our outreach — every claim is grounded in what's actually been measured.",
    [{"text": "fără garanții de rezultate", "status": "supported", "fact_id": "F09_policy"}])

add("D06", "Daily Ritualist",
    "Lead-urile cu scor între 40 și 80 sunt tratate ca MQL calde și primesc contact accelerat, săptămânal.",
    [{"text": "scor 40-80 = MQL cald, contact săptămânal", "status": "supported", "fact_id": "F03"}])

add("D07", "Connoisseur",
    "Every subject line goes through a two-stage Claude API pipeline — a generator, then a critic scoring five candidate variants.",
    [{"text": "pipeline în 2 etape, 5 variante", "status": "supported", "fact_id": "F07"}])

add("D08", "Daily Ritualist",
    "Nu cităm cifre sau studii de caz care nu apar în sursele noastre aprobate — nimic de aici nu e inventat.",
    [{"text": "fără cifre/studii inventate", "status": "supported", "fact_id": "F10_policy"}])

add("D09", "Connoisseur",
    "Leads scoring below 40 go on a standard nurture cadence — contact every two to four weeks.",
    [{"text": "scor 0-40, cadență 2-4 săptămâni", "status": "supported", "fact_id": "F04"}])

add("D10", "Daily Ritualist",
    "Fluxurile de nurture și de recuperare a coșului abandonat sunt construite și vizualizate direct în HubSpot.",
    [{"text": "workflow-uri în HubSpot, nurture + cart recovery", "status": "supported", "fact_id": "F08"}])

add("D11", "Connoisseur",
    "Each of the five subject line candidates is scored across four separate dimensions before selection.",
    [{"text": "5 variante, 4 dimensiuni", "status": "supported", "fact_id": "F07"}])

add("D12", "Daily Ritualist",
    "Modelul de scoring a trecut printr-un audit complet de scurgere de date și e explicat prin SHAP, pentru transparență.",
    [{"text": "audit de leakage + SHAP", "status": "supported", "fact_id": "F05"}])

add("D13", "Connoisseur",
    "This project is intentionally fictional, built to demonstrate marketing-automation methodology without using any real customer data.",
    [{"text": "brand fictiv, deliberat, fără date reale", "status": "supported", "fact_id": "F01"}])

add("D14", "Daily Ritualist",
    "Parcursul de persona Connoisseur e scris în engleză, iar Daily Ritualist e scris în română — împreună formează secvența de 13 emailuri.",
    [{"text": "Connoisseur=EN, Daily Ritualist=RO, 13 emailuri", "status": "supported", "fact_id": "F06"}])

add("D15", "Connoisseur",
    "Abandoned-cart recovery is one of the workflows we've built and visualized directly in HubSpot.",
    [{"text": "cart recovery în HubSpot", "status": "supported", "fact_id": "F08"}])

add("D16", "Daily Ritualist",
    "Un lead cu scor de 80 sau peste sare peste coada automată și primește direct un email personal.",
    [{"text": "scor 80+ = email personal, fără secvență", "status": "supported", "fact_id": "F02"}])

add("D17", "Connoisseur",
    "Our model outperforms a logistic regression baseline by two points of ROC-AUC — 0.7843 versus 0.7643.",
    [{"text": "0.7843 vs 0.7643", "status": "supported", "fact_id": "F05"}])

add("D18", "Daily Ritualist",
    "Nu promitem rezultate specifice garantate — ce putem spune e exact ce am testat și validat.",
    [{"text": "fără promisiuni de rezultate", "status": "supported", "fact_id": "F09_policy"}])

add("D19", "Connoisseur",
    "The critic stage of our subject line pipeline evaluates every variant before anything reaches an inbox.",
    [{"text": "etapa de critic evaluează variantele", "status": "supported", "fact_id": "F07"}])

add("D20", "Daily Ritualist",
    "Lead-urile reci, cu scor sub 40, sunt contactate pe o cadență mai lentă, de 2-4 săptămâni, nu săptămânal.",
    [{"text": "scor sub 40 = cadență 2-4 săptămâni", "status": "supported", "fact_id": "F04"}])

# ---------- REVISE: 20 drafts, one contradicted claim each ----------

add("D21", "Connoisseur",
    "Our lead scoring model is a Random Forest, tuned to 0.91 ROC-AUC on the test set.",
    [{"text": "Random Forest, 0.91 ROC-AUC", "status": "contradicted", "fact_id": "F05"}],
    notes="Real model is XGBoost at 0.7843.")

add("D22", "Daily Ritualist",
    "Secvența noastră de nurture are 20 de emailuri, distribuite pe trei parcursuri de persona.",
    [{"text": "20 emailuri, 3 parcursuri", "status": "contradicted", "fact_id": "F06"}])

add("D23", "Connoisseur",
    "We guarantee a measurable lift in engagement within your first two weeks on this track.",
    [{"text": "garanție de creștere a engagementului", "status": "contradicted", "fact_id": "F09_policy"}])

add("D24", "Daily Ritualist",
    "Coffra este un brand real, cu magazine fizice în trei orașe din România.",
    [{"text": "brand real, magazine fizice", "status": "contradicted", "fact_id": "F01"}])

add("D25", "Connoisseur",
    "Our subject lines are generated in a single pass, with no review or critic stage before sending.",
    [{"text": "generare într-un singur pas, fără critic", "status": "contradicted", "fact_id": "F07"}])

add("D26", "Daily Ritualist",
    "Fluxurile noastre de nurture și recuperare coș sunt construite direct în Salesforce, nu în HubSpot.",
    [{"text": "construit în Salesforce", "status": "contradicted", "fact_id": "F08"}])

add("D27", "Connoisseur",
    "Any lead scoring above 60 receives an immediate personal handoff from the team.",
    [{"text": "scor peste 60 = handoff imediat", "status": "contradicted", "fact_id": "F02"}])

add("D28", "Daily Ritualist",
    "Un client similar a văzut o creștere de 340% în vânzări după prima lună de nurture.",
    [{"text": "creștere de 340% citată ca fapt", "status": "contradicted", "fact_id": "F10_policy"}])

add("D29", "Connoisseur",
    "Each subject line candidate is scored across seven separate evaluation dimensions.",
    [{"text": "7 dimensiuni de scorare", "status": "contradicted", "fact_id": "F07"}])

add("D30", "Daily Ritualist",
    "Parcursul Daily Ritualist e disponibil în engleză, franceză și română, pentru acoperire mai largă.",
    [{"text": "3 limbi pentru Daily Ritualist", "status": "contradicted", "fact_id": "F06"}])

add("D31", "Connoisseur",
    "Leads scoring under 40 still receive weekly contact to maximize conversion odds.",
    [{"text": "scor sub 40 = contact săptămânal", "status": "contradicted", "fact_id": "F04"}])

add("D32", "Daily Ritualist",
    "Modelul nostru de scoring nu a trecut printr-un audit formal de scurgere de date, deși performanța pe test e solidă.",
    [{"text": "fără audit de leakage", "status": "contradicted", "fact_id": "F05"}])

add("D33", "Connoisseur",
    "Our subject line system runs on GPT-4, chosen specifically for its creative writing strength.",
    [{"text": "sistem pe GPT-4", "status": "contradicted", "fact_id": "F07"}])

add("D34", "Daily Ritualist",
    "HubSpot gestionează doar campaniile de achiziție — recuperarea coșului abandonat se face printr-un alt tool.",
    [{"text": "HubSpot nu acoperă cart recovery", "status": "contradicted", "fact_id": "F08"}])

add("D35", "Connoisseur",
    "Every recommendation we've shipped this quarter converted at over 90%.",
    [{"text": "90%+ conversie citată ca fapt", "status": "contradicted", "fact_id": "F10_policy"}])

add("D36", "Daily Ritualist",
    "Coffra funcționează din Cluj-Napoca, unde se află producția și logistica noastră.",
    [{"text": "sediul în Cluj-Napoca", "status": "contradicted", "fact_id": "F01"}])

add("D37", "Connoisseur",
    "Our model beat baseline by a wide margin — 0.7843 versus just 0.58 for logistic regression.",
    [{"text": "baseline de 0.58", "status": "contradicted", "fact_id": "F05"}],
    notes="Subtler swap — real baseline is 0.7643, not 0.58.")

add("D38", "Daily Ritualist",
    "Toate cele 13 emailuri din secvența de nurture sunt scrise în română, indiferent de persona.",
    [{"text": "toate 13 emailurile în română", "status": "contradicted", "fact_id": "F06"}])

add("D39", "Connoisseur",
    "We can promise visible results within 30 days, or we'll revise the strategy at no extra cost.",
    [{"text": "promisiune de rezultate în 30 zile", "status": "contradicted", "fact_id": "F09_policy"}])

add("D40", "Daily Ritualist",
    "Lead-urile cu scor între 40 și 80 primesc un singur email, fără niciun follow-up.",
    [{"text": "scor 40-80 = un singur email", "status": "contradicted", "fact_id": "F03"}])

# ---------- Ungrounded: 10 drafts, plausible but unverifiable ----------

add("D41", "Daily Ritualist",
    "Coffra e gândit pentru oameni care tratează ritualul cafelei ca pe ceva personal, nu standardizat.",
    [{"text": "cadru de brand: ritual personal, nu standardizat", "status": "ungrounded"}],
    notes="Fraza exactă folosită ca exemplu în system prompt-ul propriu al governance.py. Nu apare literal în brand_sources.md — doar faptul brut că Coffra e un brand de cafea de specialitate. Cel mai important draft din tot setul.")

add("D42", "Daily Ritualist",
    "Echipa noastră de marketing analizează manual fiecare lead înainte ca sistemul automat să intervină.",
    [{"text": "review manual înainte de automatizare", "status": "ungrounded"}])

add("D43", "Connoisseur",
    "Our model gets retrained every month to stay accurate as customer behavior shifts.",
    [{"text": "retraining lunar", "status": "ungrounded"}])

add("D44", "Daily Ritualist",
    "Emailurile noastre au o rată medie de deschidere de 42%, peste media industriei.",
    [{"text": "rată de deschidere de 42%", "status": "ungrounded"}])

add("D45", "Connoisseur",
    "Every stage of our lead-scoring pipeline is fully GDPR-compliant.",
    [{"text": "conformitate GDPR", "status": "ungrounded"}])

add("D46", "Daily Ritualist",
    "Acest sistem a fost construit de o echipă de trei specialiști în marketing și AI.",
    [{"text": "echipă de 3 specialiști", "status": "ungrounded"}])

add("D47", "Connoisseur",
    "Every A/B test we run requires 95% statistical significance before we act on the result.",
    [{"text": "prag de semnificație statistică 95%", "status": "ungrounded"}])

add("D48", "Daily Ritualist",
    "Acest sistem poate fi extins ușor la alte branduri de retail, nu doar la cafea.",
    [{"text": "extensibil la alte branduri", "status": "ungrounded"}])

add("D49", "Connoisseur",
    "We benchmark against three competing specialty coffee subscriptions every quarter.",
    [{"text": "benchmarking trimestrial cu 3 competitori", "status": "ungrounded"}])

add("D50", "Daily Ritualist",
    "Fiecare decizie a modelului trece printr-un audit uman săptămânal, separat de review-ul de guvernanță.",
    [{"text": "audit uman săptămânal separat", "status": "ungrounded"}])

with open("calibration_set.json", "w", encoding="utf-8") as f:
    json.dump({
        "_policy": "PASS only if every claim is 'supported'. REVISE if any claim is 'contradicted' or 'ungrounded'.",
        "_note": "v3 — no lead-specific personalization claims. Isolates brand-source grounding only.",
        "drafts": drafts
    }, f, indent=2, ensure_ascii=False)

n_pass = sum(1 for d in drafts if d["ground_truth_verdict"] == "PASS")
print(f"Built {len(drafts)} drafts -> {n_pass} PASS / {len(drafts) - n_pass} REVISE")
