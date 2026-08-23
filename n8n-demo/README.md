# n8n side-by-side demo — P7 notification step

The full Lead Intelligence Agent (P7) is code-first: Python + the Claude API,
with an XGBoost scoring tool, RAG-grounded outreach, and a claim-by-claim
Governance Reviewer. That's a deliberate choice — a pipeline with real
decisioning logic and a compliance rubric needs the auditability and control
of code, not a low-code canvas.

But not every step in a real deployment needs that. Once a lead has been
scored and approved, routing it to a notification channel is pure
orchestration — exactly what tools like n8n are built for, and a repeated
"nice to have" across several roles filtered from recent job postings.

This folder is a small, honest demo of that boundary: the **notification
step only**, rebuilt natively in n8n, running side-by-side with the Python
version — not a reimplementation of qualification, scoring, or governance.

## What it does

```
Webhook (POST /lead-qualified)
   → IF node: tier == "HOT"?
       → HTTP Request: POST to a Slack Incoming Webhook
         "🔥 New HOT lead: {{ lead_name }} (score: {{ score }})"
```

A lead payload (`{lead_name, score, tier}` — the shape P7's Qualification
Agent already outputs) triggers a webhook. If the tier is HOT, n8n posts a
formatted alert to Slack. WARM/COLD leads are silently dropped, matching
the same routing logic as the Python pipeline.

## Files

- `Coffra_Lead_Alert__n8n_demo_.json` — the exported n8n workflow, importable directly into any n8n instance (Workflows → Import from File). The Slack webhook URL in the HTTP Request node is replaced with a placeholder (`https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK`) — swap in your own Incoming Webhook URL to run it live.
- `n8n_Lead_Alert.png` — screenshot of the working canvas (all three nodes green after a successful test run)

## Why this scope, and not more

The Skills Gap Tracker behind this project explicitly ruled out a full P7
rebuild in n8n — the technical build skill is already demonstrated in
Python; the gap was platform breadth, not capability. This piece is sized
to close that gap honestly: enough to show working knowledge of triggers,
conditional logic, and third-party integrations in a low-code tool, without
pretending n8n replaces the governance-critical parts of the pipeline.
