# Chartspur frontend and Worker audit

The baseline has no offline test failure. The browser audit found a real metadata bug and one unused CSS rule.

## Source and scope

The source pin is `49453b586d9a854c942ea02a4b77c9b85e7ab382` in `chartspur--deep-test-audit`.
The primary checkout was not changed.
Other agents now have approved Python and documentation changes in the audit checkout.
No shared frontend or Worker file changed during these checks.

I read these complete files:

- `app.js`, `data.js`, `index.html`, `brief.html`, and `styles.css`.
- `pipeline/verify_ui.py` and all 18 methods in `pipeline/test_edge_seo.py`.
- `edge/worker.js`, `edge/wrangler.jsonc`, `edge/SEO.md`, and the CI and Pages workflows.
- Root instructions, README, `ops/STATE.md`, `ops/RUNBOOK.md`, and `docs/HUB.md`.

I traced entry points, all current frontend consumers, and relevant history.
I also read the brief producer's `render_page` branch to resolve its conditional controls.
The Python lane owns the complete pipeline producer review.

## Baseline evidence

| Check | Actual result | Evidence |
| --- | --- | --- |
| `node --check app.js` | Exit 0; no diagnostics. | `js-app-check.log` |
| `node --check data.js` | Exit 0; no diagnostics. | `js-data-check.log` |
| CI Python syntax and JSON parse | Passed without running pipeline writers. | `parse.log` |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s pipeline -p 'test_*.py' -v` | 36 tests passed; no failures; 8.659 seconds. | `unittest-baseline.log` |
| Original `verify_ui.py 8913` | Passed with 138 checked-in pipeline rows. | `baseline-public/verify-ui.log` |
| Original `verify_ui.py 8914` | Passed with 139 freshly ingested pipeline rows. | `public-pipeline/verify-ui.log` |

The local runtime was Python 3.14.7, Node 26.0.0, and Python Playwright 1.58.0.
Playwright used its installed matching Chromium revision 1208.
No dependency, browser, manifest, or global configuration changed.
Hosted CI specifies Python 3.12 and Node 22; this local run does not claim that runtime match.

The browser baseline used nine copied public files and the unchanged harness.
`baseline-public/copy-receipt.json` pins every copied file to the source commit.
All nine copied hashes remained unchanged after the baseline.
Browser screenshots went to separate output directories.
No shared `data/` byte changed.
`baseline-result.json` records the runtime, baseline, and concurrent authorized changes.

The Python lane generated the second data set in an independent public-only copy.
Its receipt records snapshot 1793164929, 150 chart rows, and 139 exported apps.
My second browser check used those frozen outputs without running a writer.
It did not open checkout, submit a form, send a message, or deploy a service.

## Confirmed metadata bug

Both live response mappings in `app.js` read `x.primaryGenre`.
The checked-in seed uses `primaryGenreName`.
The actual Apple metadata producer in `pipeline/ingest.py` also reads `primaryGenreName`.
The wrong mappings already existed in `fba951e` on 2026-09-17.

The reproduction derives one response from the copied public seed.
It changes only the app identity to avoid a local result match.
Playwright intercepts the public Apple search and lookup URLs with that JSON.
The browser blocks every other external request in this check.
No test imports implementation code or edits browser application state.

On the exact baseline, the public search action produced these visible failures:

- The Category cell was empty.
- The Genre selector contained only `All genres`.
- A direct `?id=900000001` lookup omitted `Health & Fitness` from the detail.

`genre-proof/red/receipt.json` records both request URLs, DOM text, and failures.
`genre-proof/red/search.png` and `lookup.png` preserve the browser output.
The separate `red.log` ends with the three intended assertion failures.
There was no browser page error.

The proposed fix replaces exactly two reads with `x.primaryGenreName`.
The proposed `verify_ui.py` extension drives search, selects the genre, and opens a direct lookup URL.
It asserts the visible Category, retained filtered row, and detail genre.
All 12 old assertions and every old harness line remain in order.
The candidate has 18 assertions.
No existing assertion, timeout, skip, or retry changed.

The same extended harness fails the baseline category assertion and passes the disposable fixed copy.
A separate capture also passes all three metadata outcomes on the fixed copy.
`genre-proof/run-results.json` records exact argument arrays, working directories, and exit codes.
`genre-proof/proposal-receipt.json` records assertion preservation and the patch hash.
The proposed patch SHA-256 is `5af3c40f980fdef6ea91936306656d49b0f9a76bd595f6dbe0a043b557b8e6ac`.
Shared frontend files remain unchanged pending review.

## Legacy candidate and retained frontend paths

The one unused source candidate is the `ol.steps li` rule at `styles.css:30`.
Commit `06bdce751195c449fcde8c8f8d7bc15a91eada79` removed `sampleOnboarding` and its `ol.steps` producer.
The same change replaced fake onboarding with Apple screenshots or an honest empty state.
A current source search finds `steps` only in that CSS rule.
No current HTML, dynamic template, brief producer, or script emits the class.
No named public CSS contract or frozen fixture requires it.

The existing browser harness guards the replacement through the Onboarding tab's screenshots or empty-state assertion.
Removing the rule cannot hide a baseline failure; the unchanged baseline already passes.
The candidate risk is an undocumented external consumer of the public stylesheet.
The repository has no such caller or supported selector contract.
A removal still needs the unchanged browser check and a source diff review.
This rule is not part of the metadata proposal patch.
No test deletion is proposed in this lane.

Retain `demoEstimate` in `data.js`.
`index.html` loads it before `app.js`, and `est` calls it for seed and live-search results.
The user interface labels those values as demo estimates.
It is an active fallback, despite the live pipeline's separate estimate fields.

Retain the Ads and Viral empty states and the screenshot URL filter.
Commit `06bdce7` removed fake content and established those honest source boundaries.
The browser assertions still distinguish real screenshot content from invented onboarding and ad spend.
Retain reduced-motion and decorative-mark assertions from `9b9f20e`.
They test visible animation and accessibility behavior through the browser.

Retain the brief's guarded genre listener.
The current open-checkout HTML has no `genre` or `request` control.
The producer still emits both controls when checkout is closed.
That branch is the named public interest-registration fallback.
The missing controls in one generated snapshot do not prove the handler obsolete.

## Worker disposition

Retain all 18 Worker tests and the current Worker source.
`wrangler.jsonc` names `worker.js` as the platform entry point.
The Pages workflow publishes the exact frontend assets that the Worker proxies.
The Node harness imports the real Worker and replaces only the external fetch boundary.
It asserts actual response status, headers, body, and outbound request arguments.
It makes no network or provider request.

The discovery tests enforce the exact two approved canonical URLs, valid XML, and no fabricated modification time.
They also preserve query exclusion, exact path matching, HEAD behavior, and bounded cache headers.
`edge/SEO.md` explicitly limits the map to the home page and free brief.
Those publication limits remain active contracts.

The method, alias, port, and encoded-query tests preserve real routing behavior.
Commit `000ddcbfeed77443acc406253a55972f1f0ca402` fixed HTTP redirects on 2026-10-17.
The tests guard that repair and intentionally retain existing HTTPS nondefault-port behavior.
The proxy cases preserve public data delivery, manual redirects, external destinations, and upstream failures.
The external payment redirect is inert JSON; no checkout occurs.

`test_managed_training_restrictions_survive_composition` is a narrow synthetic composition guard.
It combines the real application robots body with an explicit managed-policy fixture.
It does not prove the deployed Cloudflare composition or actual crawler access.
The adjacent exact-directive test is stronger against application-added policy directives.
However, managed crawler restrictions are a named security contract in `edge/SEO.md` and commit `59b6a86`.
This audit retains the composition case rather than removing that explicit contract for a small assertion overlap.

The Worker streams the upstream body and holds no mutable request state at module scope.
It uses no secrets, bindings, background tasks, body buffering, or dynamic destination host.
Its `cacheEverything` and `cacheTtl` options match the documented GET/HEAD request options.
These observations follow the current [Cloudflare request reference](https://developers.cloudflare.com/workers/runtime-apis/request/#the-cf-property-requestinitcfproperties)
and [Worker response guidance](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/#stream-request-and-response-bodies).

## Limits and final review

Offline Node tests do not execute Cloudflare's cache, zone policy, or network implementation.
This audit did not run Wrangler, change platform configuration, or inspect a deployed private account.
The repository has no local Wrangler dependency; the task forbids adding dependencies.
Live deployment acceptance and managed robots verification remain separate gates in `edge/SEO.md`.
They are not blockers for this local source audit.

The original UI harness does not cover search metadata or direct unknown-app lookup.
The proposed extension closes the demonstrated gap without replacing its existing coverage.
No claim depends on a green rerun alone: the exact baseline fails the new visible outcome.

I applied all ten documentation review checks to this report.
Exact identifiers, commands, hashes, and quoted UI text retain their required form.
Long table cells and exact test names are technical exceptions to the sentence-length target.
