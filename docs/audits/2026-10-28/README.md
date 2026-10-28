# Chartspur test audit

The audit starts at canonical main `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
The primary checkout remains unchanged.

## Proven obsolete checks

`test_shots_parse` exercises Python's JSON decoder without calling Chartspur.
`test_velocity_none_without_prev` evaluates a copied expression without calling the estimator.
Both arrived in `06bdce7` and never gained a production owner call.
All four old helper tests pass when the actual screenshot and first-snapshot velocity branches break.

The replacement invokes the real estimate CLI with synthetic persisted inputs.
It checks valid, malformed, and absent screenshots plus missing/prior snapshot velocity in `data/live.json`.
Actual owner mutations fail those output assertions for the intended reasons.
The CLI fixture copies the complete pipeline directory, so sibling helper extraction does not require a source-file inventory update.
No test-only production seam was added.
See [the ledger](python-audit.md), [preservation review](python-preservation-review-v2.md), and [setup correction review](packaging-review.md).

## Genuine repairs

A valid bare output filename made `summary.py --out summary.json` fail at `os.makedirs("")`.
Nested output already worked with the same inputs.
The repair uses the current directory when the output has no parent directory.
It preserves temporary output and atomic replacement.
A subprocess CLI regression fails before the repair and checks the written JSON afterward.

The estimator's unused clock local and import have no caller or named contract.
Exported freshness still comes from the stored snapshot timestamp.
The same CLI keeper checks that public field.

The genre-interest form still claimed checkout was closed after `57fd7eb` opened it.
The correction retains the interest-only purpose, required fields, URL identity, and existing privacy sentence.
The agent guide now distinguishes hosted offline checks from the required local browser check.
It does not remove or weaken that local requirement.
See [the cross-cutting audit](crosscutting-audit.md).

The public `--now 0` clock override parsed successfully but silently used the current date.
The explicit `None` fallback now honors epoch zero while retaining the same default clock expression.
A public CLI regression checks both epoch zero and one.
See [the clock review](epoch-clock-review.md) and [original reproduction](epoch-clock-reproduction.json.txt).

App Store search and direct app lookup read `primaryGenre` instead of the supplied `primaryGenreName`.
Both mappings now retain the public category field.
The extended browser check uses local API fixtures and visible category, filter, and seller/genre outcomes.
Each old field mapping fails independently at its intended visible assertion.
Every original browser assertion remains.
The new request witness requires both endpoints without locking private call order or counts.
See [the browser review](browser-preservation-review.md) and [proof](browser-proof.md).

The removed `ol.steps li` rule belonged to fake onboarding removed in `06bdce7`.
Current onboarding displays real App Store screenshots or an honest empty state.
All original onboarding assertions remain.
The Worker and all 18 named HTTP/discovery/security tests stay unchanged.

## Final qualification stage

The [combined applied-source review](final-combined-source-review.md) clears the source for the final offline and browser gates.
Final discovery passed 37 tests: two detached cases removed and three public CLI cases added.
JavaScript syntax, all Python files, seven checked-in JSON inputs, and whitespace checks passed.
The full extended browser harness passed with 138 checked-in apps and 139 refreshed apps.
All 88 frozen project/document files and all four stored data files stayed unchanged during execution.
Both nine-file public copies stayed unchanged, and all temporary servers stopped.
See [the final receipt](final-receipt.json.txt) and [command record](final-README.md).

The [final delivery review](final-delivery-review.md) confirms the source, checks, and retained contracts.

The implementation changes no pipeline formula, stored schema, committed snapshot, Worker behavior, payment configuration, or workflow permissions.

## Baseline and real pipeline proof

All 36 existing offline tests passed.
JavaScript syntax and Python/checked-in JSON parsing passed.
The unchanged browser harness passed on the canonical public copy with 138 rows.
The existing local Python Playwright runtime and its matching Chromium were used without installation.

The unchanged ingest and estimate commands also ran in an isolated public-data copy.
Free Apple endpoints produced 150 chart rows and 139 distinct apps.
That fresh output passed the existing browser harness.
The candidate estimator then reproduced `live.json` and `METHOD.md` byte-for-byte from the same stored snapshot without another network ingest.
The shared database, data, ledger, payment state, and public outputs stayed unchanged.
See [the pipeline receipt](public-pipeline-receipt.json.txt) and [candidate replay receipt](public-export-receipt.json.txt).

## Boundaries

No payment, order reconciliation, issue post, customer delivery, Worker deployment, or new spending occurred.
Offline Worker contracts do not establish the deployed Cloudflare zone's managed policy.
Pages publication and live-site source verification remain separate delivery facts.
The source change is prepared for a pull request; final merge and deployment receipts will identify the delivered revision.
Full logs and disposable copies remain under the owner's `.audit-evidence/2026-10-28/chartspur` directory.
Frozen JSON receipts use a `.txt` suffix to preserve their bytes.
Frozen failure logs and patch context retain their original paths and whitespace.
Source and test whitespace checks pass.
The full staged evidence tree reports whitespace in frozen artifacts; [the receipt](staged-whitespace-results.json.txt) records that exception.

The prose was reviewed against all ten house-style checks and satisfies at least eight.
Exact identifiers, commands, and frozen evidence retain their technical form.
