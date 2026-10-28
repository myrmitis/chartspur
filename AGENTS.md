# AGENTS.md — Chartspur

Shared rules live in `~/.agents/AGENTS.md` and load every session. This file
holds only what is specific to this repo. Start with `README.md`, then
`ops/STATE.md` and `ops/RUNBOOK.md`.

## Testing — E2E over unit

Follow the shared policy: do not add unit or integration tests on your own,
and no TDD unless asked. Prove a change by driving the site the way a
visitor does.

- Web E2E: `python3 -m http.server 8903 & python3 pipeline/verify_ui.py 8903`
  (Playwright: rows render, detail opens, no console errors). A change to
  `index.html`, `brief.html`, `app.js` or `styles.css` extends `verify_ui.py`
  or adds a sibling `pipeline/verify_<flow>.py`; a brief/checkout change walks
  the real `brief.html` → Stripe Payment Link path in a browser.
- Pipeline: run it for real — `python3 pipeline/ingest.py && python3
  pipeline/estimate.py` — and check `data/live.json` and the rendered site.
- Hosted gate: `.github/workflows/ci.yml` runs offline unittest discovery
  and syntax checks. Run the local Web E2E command above as a separate
  required check. Existing `pipeline/test_*.py` are a contract: never delete,
  skip, weaken or loosen an assertion to go green.
- Exception, ask first: pure logic with a clear spec (the estimate formulas
  in `data/METHOD.md`, brief diffing).

## Documentation hub

Read [docs/HUB.md](docs/HUB.md) before material changes. Update the affected canonical documentation in the same PR/commit and link the issue, exact revision, tests and deployment boundary. Automatic `docs/updates/` receipts prove only source pushes. Follow the [shared standard](https://github.com/laqaer/agent-config/blob/main/docs/documentation-hub.md); never copy secrets or customer data into documentation.
