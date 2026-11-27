# Chartspur

iOS chart intelligence prototype: Apple Top Charts ingested daily, enriched with iTunes lookup data, and scored with transparent, labeled estimates.

**Live:** https://chartspur.com/

## Run locally

```sh
python3 -m http.server 8903
```

Open http://localhost:8903

## Domain

GitHub Pages builds and hosts the site (`pages.yml`) at https://myrmitis.github.io/chartspur/. The Cloudflare Worker in `edge/` serves that build at https://chartspur.com/ and sends `www.chartspur.com` to the apex. The Worker owns the DNS records for both names. Do not set a custom domain on the Pages site: Pages would then redirect back to chartspur.com and make a loop.

Deploy the Worker again only when `edge/` changes:

```sh
wrangler deploy -c edge/wrangler.jsonc
```

## Pipeline

```sh
python3 pipeline/ingest.py && python3 pipeline/estimate.py
```

`ingest.py` pulls Apple RSS feeds (topfree / topgrossing / toppaid, limit=50) plus iTunes lookup into `data/appintel.db`. `estimate.py` writes `data/live.json`. Velocity uses rating-count deltas between sqlite snapshots, so the db is committed.

## Method

`dl_day = 20000 * (50/rank)^0.7`; paid revenue = `price * dl * 0.7`; free revenue = grossing x `0.12`, others x `0.04`; velocity = rating-count delta per day. See `data/METHOD.md`.

## Genre brief

`brief.html` is a one-time $19 offer for a single US genre: who entered, left, or moved across Top Free, Top Grossing, and Top Paid since the snapshot at least 7 days earlier. The largest genre is published free. Card checkout uses the live Stripe Payment Link in `ops/payments.json` (created by `stripe-setup` from `stripe.json`; ids in `stripe.lock.json`). Estimates stay in a labeled appendix (`data/METHOD.md`). Operating state: `ops/STATE.md`.

## Real vs estimated vs demo

- **Real:** chart ranks, app metadata, and App Store screenshots from Apple's public RSS + iTunes lookup.
- **Est:** all download/revenue/velocity numbers (labeled `est`), derived from the method above.
- **Keywords:** title/genre tokens. Not ranked search volume.
- **Empty:** Ads (Meta Ad Library token) and Viral (YouTube Data API key).

Not affiliated with appkittie.

## Verification

Run the offline gate:

```sh
python3 -m unittest discover -s pipeline -p 'test_*.py' -v
```

Serve the checkout with the local command above. In a second terminal, run the existing browser check:

```sh
python3 pipeline/verify_ui.py 8903
```

The browser check writes `data/verify.png`. Hosted CI runs the offline and syntax checks; run Playwright locally as well.
Use a disposable copy for pipeline verification so the committed snapshot stays intact.
See [the test audit](docs/audits/2026-10-28/README.md) for retirement proof and actual checks.

### Frontend maintenance — 2026-11-13

The draft pass follows [Modern Web Guidance v1.0.0](https://github.com/GoogleChrome/modern-web-guidance/tree/4dd968349e54ca45a05dd5c818fb035c9054b022)
from [main revision 62ef0ae8c5d9b4b88ed62c15c66a6106aeb61935](https://github.com/myrmitis/chartspur/commit/62ef0ae8c5d9b4b88ed62c15c66a6106aeb61935).
Search now uses native form submission, so composition-confirmation keys
are not intercepted. Each result has a native keyboard button; opening it
focuses the detail heading, and detail choices expose their pressed state.
The results table's scroll region is keyboard focusable.
Controls inherit the reader's text size and the loading spinner stays still
under reduced motion. Data, estimates, brief copy and payment state are unchanged.

Verification: 37 existing pipeline tests and JavaScript/Python syntax checks
pass; the pinned legacy scan has zero findings. A fixture-driven DOM check
passes search submission, composition-event handling, result selection,
detail focus and pressed-state updates. `pipeline/verify_ui.py` adds browser
checks for those interactions and 320px reflow with enlarged text. Its actual
browser run remains blocked by Chromium startup in the validation environment;
DOM checks do not establish rendering or real IME acceptance. Run that browser
gate before merging. This source change has not been deployed.

Review: [frontend comparison](https://github.com/myrmitis/chartspur/compare/main...codex/modern-web-guidance-20261113).
