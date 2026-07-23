# Coffra — Talking Points pentru Outreach

## Context
Coffra e un brand fictiv de cafea de specialitate D2C (Timișoara),
folosit ca sandbox pentru portofoliul de marketing automation al lui
Paul Sebastian Kradyel. Fictiv, deliberat — pentru rigoare
metodologică fără complicații de date reale.

## Segmentare de lead-uri (deja specificată în P1)
- Scor 80-100 → High / Sales-Ready → handoff imediat, email personal.
- Scor 40-80 → Medium / Warm MQL → nurture accelerat, contact săptămânal.
- Scor 0-40 → Low / Cold → nurture standard, cadență 2-4 săptămâni.

## Rezultate verificate (de citat exact)
- Model de lead scoring: XGBoost, test ROC-AUC 0.7843 (vs. 0.7643
  pentru baseline de regresie logistică), cu audit de data leakage
  și explicabilitate SHAP.
- Sistem de nurture: 13 emailuri de producție, pe două călătorii de
  persona (Connoisseur - engleză, Daily Ritualist - română).
- AI Subject Line Optimizer construit pe Claude API, pipeline în
  două etape (generator + critic), 5 variante scorate pe 4 dimensiuni.
- Implementare HubSpot: workflows vizualizate pentru nurture și
  recuperare coș abandonat.

## Ce NU spunem (evităm overclaiming)
- Nu promitem rezultate garantate.
- Nu inventăm cifre sau studii de caz care nu sunt în aceste surse.
- Limitările sunt documentate transparent, nu ascunse.