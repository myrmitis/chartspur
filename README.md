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
