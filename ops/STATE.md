# Chartspur operating state

Updated 2026-10-30: experiment 001's 14-day window ended with no recorded paid order (see Experiment below). Updated 2026-10-15: card checkout is open and experiment 001 is running. Updated 2026-10-14: the repository is now `myrmitis/chartspur` (renamed from `myrmitis/appsignal`) and the site is at https://chartspur.com/. Earlier sections date from 2026-09-26. This file is the handoff. Chat history is not required to continue.

## Offer

Primary offer: a one-time **$19 US genre chart brief**. It shows, for one genre, who is on the latest US Top Free, Top Grossing, and Top Paid charts and who entered, left, or changed rank versus the stored snapshot at least 7 days earlier.

Buyer: an indie iOS developer or small studio checking a category before building.

The largest genre is published free at `brief.html`. The existing chart table on `index.html` stays free. Revenue figures are the rank heuristic in `data/METHOD.md` and sit in a labeled appendix.

Checkout is **open** since 2026-10-15 (commit 57fd7eb). `ops/payments.json` holds the live Stripe Payment Link. `brief.html` shows the Pay $19 button.

Experiment: `ops/experiments/001-category-brief.json` **ended** on 2026-10-29. The day-14 result (recorded 2026-10-30): no paid
order is recorded, so success is not shown. The zero is not reconciled with Stripe, because agents cannot read it (#12).
The experiment's stop-or-pivot rule applies: the owner chooses a new offer, audience or price in #13.

## Profit

See `ops/ledger.json`. Provisional net operating profit **$0**. Cash collected **$0**. Paying customers **0**. Retained customers **0**. Outstanding customer obligations **none**. Stripe is connected, but agents cannot read orders yet (owner ticket myrmitis/chartspur#12 asks for a read-only key). This is not a reconciled profit figure. Inherited revenue: no evidence in this repository.

New discretionary spend authorized in-repo: **none**. This operator's cap is **$0** of new discretionary spend (ads, new SaaS, contractors, paid APIs).

## What already ran without this session

GitHub Actions workflow `refresh` updates Apple charts daily at 13:00 UTC and pushes to `main`. Successful unattended runs include 2026-09-23, 2026-09-24, and 2026-09-25. Pages deploys `main` to https://myrmitis.github.io/chartspur/. The Cloudflare Worker in `edge/` serves that build at https://chartspur.com/ (see the README).

## Runtime after this change

- `refresh` rebuilds `brief.html`, `data/brief.json`, and `ops/summary.json`, then commits them. A push made with the workflow token does not start the Pages workflow, so the job then dispatches `pages.yml`. The 2026-09-26 17:01 UTC refresh committed new charts and the summary issue before that dispatch existed, so the public site stayed on the prior snapshot until the next Pages deploy.
- `operating-summary` posts or updates the GitHub issue "Chartspur daily operating summary" after `refresh` completes, and at 18:00 UTC if the refresh looks unhealthy. Configured, not yet unattended-tested.
- Stop the jobs from the GitHub Actions tab on `myrmitis/chartspur`. There is no separate always-on worker.

## Shared systems checked, not adopted

- `laqaer/agent-prompts` registry 1.2 was readable through the `laqaer` GitHub account. Its kit is not installed here. This repository stays the product record.
- `laqaer/junction` at `558986c52729971dfd48c4459477303554a0d1e7` is a local agent/model control plane. It is not the production runtime for this site.
- `laqaer/forge` is a separate product. It was not used.

## Fulfillment

`ops/RUNBOOK.md`. Do not send a brief as if it were paid until a processor payment is reconciled.

## Next action

Each weekday, check Stripe for paid orders on the Payment Link. For each paid order, deliver the brief and record it per `ops/RUNBOOK.md`. On 2026-10-29, record the experiment 001 result. The weekday check needs the read-only Stripe key from myrmitis/chartspur#12.
