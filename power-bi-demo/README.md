# Power BI rendering — P5 attribution method comparison

P5's attribution comparison table (`attribution_unified_comparison.csv` —
Ground Truth vs 7 attribution methods, per channel) already exists as a
static Plotly chart on the live dashboard. This folder rebuilds the same
underlying data as an interactive Power BI report, as a second BI-tool
demonstration of the same result.

## What it shows

A clustered bar chart — **Method × Channel × Percent** — with a Method
slicer, so a reviewer can isolate any subset of attribution methods
(e.g. Last-Click vs MMM Bayesian vs Ground Truth) and see how each
channel's attributed share compares.

## Files

- `Coffra_Attribution_PowerBI_P5_Attribution_Method_Comparison.pbix` — the Power BI Desktop file, importable directly
- `attribution_powerbi_chart.png` — screenshot of the finished report

## Notes on the build

Getting from the raw CSV to this chart involved three real Power Query
fixes, not just a straightforward import:

1. **Aggregation** — the first version of the chart used `Count of Percent`
   instead of `Average`, producing identical-looking bars regardless of
   the actual attribution values.
2. **Locale parsing** — Power Query's default type detection, running on a
   Central European Windows locale, silently corrupted decimal values on
   import (`29.4` became `294`) by misreading the CSV's US-style decimal
   points. Fixed by re-importing with `Data Type Detection: Do not detect`,
   then explicitly setting `Change Type → Using Locale → English (United
   States)` on the numeric columns before any further transformation.
3. **Header promotion** — disabling auto type-detection also skipped
   automatic header promotion, so the first data row briefly became the
   column headers; fixed with an explicit `Use First Row as Headers` step.

None of these are Power BI's fault exactly — they're the kind of
environment-specific data-import issues (regional settings, type
inference order) that only show up when actually building a report, not
when reading documentation about it.
