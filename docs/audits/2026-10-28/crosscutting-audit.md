# Chartspur CI and operating-contract audit

Provider: `OpenAI Codex subagent`.
Reviewer: `/root/agents_audit`.
Canonical source: `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
Checkout: `/Users/andyzhou/dev/chartspur--deep-test-audit`.
Date: 2026-10-28.

## Result and scope

Keep both operational shell entrypoints and the existing summary deduplication marker.
No operational code or test deletion is proved by this lane.
The public genre-interest form contains one proved stale checkout statement.
The repository testing instructions also overstate the hosted CI gate.
Both findings admit narrow documentation corrections without lowering the UI check requirement.

I completely read all five workflows, dependency routing, both shell entrypoints, the issue form, and the named operating documents.
`crosscutting-source-hashes.json` records 20 complete reads and four caller-reference reads.
It records exact hashes, line counts, and the clean canonical checkout state.
I traced relevant caller and rename history without duplicating the other lanes' complete current test reads.
The Python reviewer supplied exact summary keeper names after its full test read.

This lane started no test, syntax check, pipeline, provider call, deployment, message, payment, or database write.
Baseline execution belongs to the web lane.
Historical operating figures and workflow claims below describe source contracts, not newly observed live state.

## Actual CI and operational routing

| Entrypoint | Actual owner and behavior | Preservation boundary |
| --- | --- | --- |
| `.github/workflows/ci.yml` | Pull requests and main pushes run pinned Python 3.12/Node 22 setup, JS syntax checks, Python AST/JSON parsing, and offline unittest discovery. | It does not run `verify_ui.py`, ingest, estimate, or a live refresh. It checks tracked-byte and untracked-data preservation afterward. |
| `refresh.yml` | Daily 13:00 UTC or manual execution runs ingest, estimate, brief, and summary in sequence. It commits only named generated products. | It writes the committed SQLite history and generated public sample. Failure stops the chained pipeline before publication. Do not invoke it during this audit. |
| `operate.yml` | Refresh completion, daily 18:00 UTC, or manual execution calls `post_summary.sh`. It checks out trusted main with persisted credentials disabled. | Its token can read Actions and write issues. The configured job posts messages; offline helper tests do not exercise live GitHub posting. |
| `pages.yml` | Main pushes and manual execution package an explicit site asset list and deploy Pages. Refresh dispatches it explicitly after token-authored pushes. | SQLite, ledger, operating state, payment configuration, and customer reports are outside the publication allowlist. |
| `documentation-receipts.yml` | Main pushes write a source-revision receipt through the GitHub Contents API. Receipt-only changes do not retrigger this workflow. | The receipt explicitly proves source history only. It is not CI, deployment, revenue, or customer evidence. |

The Pages and read-only validation jobs have separate event routing.
The Pages job does not depend on the validation job.
A main push therefore has an automatic publication effect that must be considered before delivery.
This read-only audit did not trigger either job.

The refresh needs `contents: write` for its commit and `actions: write` for Pages dispatch.
The operating-summary job needs `issues: write` for its existing message loop.
Read-only CI has only `contents: read`.
The documentation job's write token stays in its existing repository receipt owner.
No new loop, permission, dependency, or publishing surface is proposed.

## Proved instruction mismatch

`AGENTS.md` says the hosted gate includes both unittest discovery and `verify_ui.py`.
The complete current workflow has no browser command, server, Playwright installation, or UI step.
History introduces the E2E instruction in `54c7af9`; CI did not acquire that claimed step.
The read-only gate originated in `97d32af` and was extended for brief generation in `503c812`.

Correct the statement to distinguish hosted offline checks from the required local browser check.
Keep the local real-site command and the requirement to extend UI verification for visible changes.
Do not remove a check, lower an assertion, or add a dependency stack merely to match inaccurate documentation.
The final audit must report the actual offline and browser results separately.

## Proved stale public issue-form text

Exact location: `.github/ISSUE_TEMPLATE/genre-brief.yml:8`.
The current text says card checkout is not open.
`ops/STATE.md` records checkout opening in `57fd7eb` on 2026-10-15.
The checked-in public `brief.html` shows the Pay $19 link.
This source evidence establishes the intended current checkout configuration; it does not prove a live payment succeeds.

The stale form remains reachable in the product flow.
`pipeline/brief.py::request_url` targets `genre-brief.yml`.
The catalog renderer emits a Register interest link for every genre, including when checkout is open.
The checked-in public brief contains 22 such form links.
The form also remains available through the repository's issue chooser.

History created this form in `503c812`, when checkout was deliberately closed.
The form has no later change.
`57fd7eb` opened checkout and updated the offer documentation.
`7e6ccba` updated current state, the experiment window, and the issue title without changing the form.
The obsolete sentence therefore survived an actual state transition.

The exact old sentence has no meaningful keeper contract.
The form's interest, privacy, and non-payment boundaries remain live and must stay.
The experiment treats interest as a secondary observation, never a paid success or revenue.
The runbook requires processor reconciliation before fulfillment.

Proposed replacement:

> This issue records genre interest only. It is not a payment or proof of purchase.
> When checkout is open, use the card-checkout link on the brief page for paid briefs.
> Do not include payment card numbers, bank details, or a full Stripe receipt.

This changes the stale message while preserving the form and its public URL.
Validate its YAML and visible text, then run the normal offline and local browser gates.
No new unit test is needed for this reversible copy edit.
No issue, payment, receipt, or order should be created to verify it.
`documentation-corrections-proposal.patch` contains both narrow corrections without applying them.
Its JSON receipt records the preserved instructions, form identity, required fields, and privacy text.

`ops/ENABLEMENT.md` is explicitly dated 2026-09-26 and contains the earlier blocked-connection history.
Preserve that historical evidence and use `ops/STATE.md` for current operating handoff.
This audit does not rewrite the dated record as if it were a fresh provider observation.

## Retained candidate ledger

### Old summary marker

- Exact test: `SummaryTest.test_decide_posts_once` in `pipeline/test_summary.py`.
- Actual detected failure: none claimed in this read-only lane. The current test asserts the exact dated `appsignal-summary` marker.
- Non-test callers: `summary.py::render_body` emits the marker; `post_summary.sh` reads issue bodies and comments for that exact marker.
- Named contract: the marker identifies an existing posted UTC-day summary and suppresses a duplicate message.
- Keeper: the same test checks first workflow posting, repeated-post suppression, quiet healthy schedule, and unhealthy scheduled posting/suppression.
- History: `503c812` introduced producer, consumer, and keeper together. The later Chartspur title change preserved the marker.
- Deletion unlocked: none. Renaming or removing it without a persisted-message migration can break deduplication.
- Risk and validation: preserve producer/consumer agreement. Live GitHub pagination, permissions, and posting were not tested here.

Current visible summary branding is already Chartspur.
Do not confuse the retained storage marker with obsolete public copy.

### `pipeline/run.sh`

- Exact tests: none call this executable wrapper.
- Actual detected failure: none; this lane did not run its live ingestion path.
- Non-test callers: none found in current repository references, workflows, the portfolio loop table, or shared script pointers.
- Current entrypoint: the executable itself runs ingest and estimate, matching the README's local chart-only pipeline recipe.
- Stronger current owner: the scheduled refresh directly runs all four Python commands, including brief and summary.
- History: `fba951e` introduced this wrapper. `503c812` expanded scheduled refresh outputs without retiring the local two-command recipe.
- Deletion unlocked: only the two-line wrapper. No production Python method or test would become removable.
- Risk and validation: absence of repository callers does not prove that nobody invokes this public CLI path. No retirement contract or deletion control was established.
- Disposition: retain. The wrapper's narrow recipe is not proved obsolete merely because the daily job has more steps.

### `pipeline/post_summary.sh`

- Exact keepers: `SummaryTest.test_decide_posts_once`, the four health cases, and `test_next_action_tracks_checkout` guard its Python decision owner.
- Actual detected failure: no shell or live-provider result is claimed in this lane.
- Non-test caller: `operate.yml` invokes this executable directly for all configured triggers.
- Named contracts: one UTC-day message, stable marker, unhealthy exit status, token-bound posting, and no posting outside Actions.
- History: `503c812` introduced the script and workflow. `7e6ccba` changed only the target issue title to Chartspur.
- Deletion unlocked: none. It remains the actual operational owner of external summary delivery.
- Validation limit: helper tests do not prove shell/GitHub integration. Do not run the posting owner with real Actions credentials during this audit.

## Other named contracts retained

The committed SQLite database holds prior Apple snapshots needed for velocity and week-over-week movement.
It is product history, not a disposable fixture or legacy cache.
The pipeline reviewer owns its full schema, mutation, and retention assessment.

The free table, public largest-genre sample, and paid single-genre report remain distinct product surfaces.
Rank-derived downloads and revenue remain labeled estimates under `data/METHOD.md`.
Interest issues are not payments, and only reconciled non-owner paid orders can satisfy experiment 001.
The dated experiment window is 2026-10-15 through 2026-10-29 in source.
No result evaluation or order reconciliation occurred here.

The public SEO map is limited to the apex and `brief.html`.
Keep private paths, customer reports, payment URLs, queries, and data files out of that map.
Worker source tests and deployment acceptance have separate owners and evidence.
This audit changed no DNS, Pages domain, crawler policy, Worker, or live deployment.

## Remaining review boundary

The other lanes own full test reads and baseline executions.
This report makes no invented pass count or live operational claim.
Later source/test deletion proposals require a separate review of their actual diff and preservation controls.
No candidate quota justifies removing a reachable owner, persistent history, or meaningful assertion.

I applied all ten documentation checks and resolved at least eight applicable checks.
Exact commands, paths, identifiers, source pins, and accepted authority boundaries keep their technical form.
