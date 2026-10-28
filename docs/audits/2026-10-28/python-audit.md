# Chartspur Python test audit

Source: `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
Reviewer: `/root/python_audit`.
Date: 2026-10-28.

The audit proved two detached test cases and one genuine CLI output bug. The shared source remains unchanged.

The proposed patch replaces the detached cases with one real estimate CLI case. A second CLI case guards the relative-output repair.

The proposal is ready for independent review. Shared application and final gates remain pending.

## Exact read scope

The reviewer fully read three test files and five production owners, totaling 977 lines:

- `pipeline/test_pipeline.py`: 25 lines and four cases.
- `pipeline/test_brief.py`: 129 lines and eight cases.
- `pipeline/test_summary.py`: 76 lines and six cases.
- `pipeline/db.py`, `ingest.py`, `estimate.py`, `brief.py`, and `summary.py`: 747 lines.

The reviewer also read the root instructions, README, documentation hub, method, operating state, and runbook.
The workflow and shell reads established Python entrypoints; the cross-cutting lane owns their complete audit.

`python-inventory.json` records every source hash and all 18 exact method names. The shared checkout was clean before and after the controls.

## Live entrypoints and contracts

The refresh workflow invokes ingest, estimate, brief, and summary directly. The README also names the ingest and estimate commands.
The runbook exposes `brief.py --genre ... --out ...` for fulfillment. The summary job invokes `summary.py --decide` before any external posting.

No Python package manifest, installed SDK, or named external helper API exists in the tracked repository. The documented contracts are standalone commands and persisted outputs.
This repository search does not prove that no unknown external consumer exists.

The production helpers remain live:

- `db.conn` creates and migrates the store used by ingest and estimate.
- `ingest.get` reads public Apple feeds and lookup details.
- `estimate.dl_day` and `keywords` populate the exported rows.
- The brief helpers load read-only snapshots, compare charts, render observed data, and write the public or requested report.
- The summary helpers build operating data, assess refresh health, and decide whether the posting wrapper should act.

The audit proposes no production helper deletion. It preserves the intentionally old `appsignal-summary` deduplication marker.

## Candidate ledger

| Candidate | Existing assertion and detectable failure | Production reach and keeper | Origin, risk, and disposition |
| --- | --- | --- | --- |
| `T.test_shots_parse` | It decodes its own literal with `json.loads` and catches a standard-library decode error. It cannot detect an estimate-owner regression. | The live decoder is inside `estimate.main`. The new CLI case checks valid, malformed, and absent screenshots in actual `data/live.json`. | Commit `06bdce751195c449fcde8c8f8d7bc15a91eada79` added the case. No later edit or named test consumer exists. Remove only after the CLI keeper lands. Keep the production decoder. |
| `T.test_velocity_none_without_prev` | It evaluates a copied expression with local `prev=None`. It detects changes to that copied expression, not the production owner. | The live expression is inside `estimate.main`. The new CLI case observes null velocity without a prior snapshot and 5.0/day with a two-day prior snapshot. | The same commit added this case. It has no non-test caller or named API contract. Remove only after the CLI keeper lands. Keep the production velocity behavior. |

The existing brief roundtrip checks `brief._rows` velocity. It does not exercise `estimate.main`, so the audit does not claim duplicate ownership.

The proposal retains `T.test_dl_curve` and `T.test_keywords` unchanged. They call live production helpers and guard the documented curve and exported keyword limits.

## Estimate CLI keeper and mutation controls

The keeper invokes `python pipeline/estimate.py` in a disposable source workspace. Its only inputs are synthetic SQLite rows in the public schema.
It uses 40 distinct apps to satisfy the unchanged minimum-output guard. It imports no production internals for setup or assertions.

The keeper checks the persisted `data/live.json` file. It covers valid screenshot preservation, malformed and absent screenshot fallback, first-snapshot null velocity, and an actual prior-snapshot delta.

| Actual owner mutation | All four old pipeline cases | New CLI keeper | Intended observation |
| --- | --- | --- | --- |
| Discard decoded screenshots. | Four pass. | Fails. | The valid screenshot list becomes empty. |
| Rethrow the malformed screenshot decode error. | Four pass. | Fails. | The real command exits with `JSONDecodeError`. |
| Emit zero velocity without a previous snapshot. | Four pass. | Fails. | Persisted velocity is zero instead of null. |

The baseline keeper passes. Each mutation runs in its own source copy and fails its intended assertion, without setup errors.
`proposal-control-results.json` pins the commands, paths, exits, and log hashes.

## Genuine bug: relative summary output

The public command accepts `--out summary.json`. The current owner calls `os.makedirs('')` for that filename and exits 1.
With identical synthetic inputs, `--out nested/summary.json` succeeds. This positive control isolates the missing directory fallback.

The one-line repair uses `os.path.dirname(out_path) or "."`. The existing brief writer already uses this pattern.
The repair retains atomic temporary-file replacement and the existing summary format.

The new summary CLI case fails before the repair at the actual `FileNotFoundError` for the empty directory.
After the repair, it reads the persisted output and verifies the snapshot, genre, app count, checkout state, and zero cash default.
The separate CLI probe also confirms that relative and nested output documents are equal.

## Proposal and measured results

The isolated proposal is `proposal/source/pipeline`. The patch is `proposal/proposal.patch`.

Patch SHA256: `f0684a8d0e8271161f529973d700fef19b13ca55f23bc0e3f8d03575a176a592`.
New CLI file SHA256: `9b9c7aa04c413e7813d029130d3c69f1759d5185342825ca591320f14229f8ff`.

The patch changes only `summary.py`, `test_pipeline.py`, and the new `test_cli.py`.
It removes the two proved cases and their unused `json` import. Every other existing test body and assertion remains unchanged.

The unchanged source with both new CLI cases runs 20 Python-lane cases. Only the genuine summary regression fails.
The final isolated proposal runs 18 Python-lane cases successfully. This count excludes the edge suite owned by the web lane.
Both executions use local Python 3.14; the repository CI specifies Python 3.12.

The runner made no network request, external post, payment action, or change to tracked data. Synthetic ledgers contain no customer data.

## Remaining work and limits

Independent preservation review must precede application. The web lane owns shared baseline and final runners.
The native offline gate, browser harness, and real public-Apple pipeline run are reported separately.
No paid pipeline, Stripe call, mail, issue post, fulfillment, deployment, or production-data write is part of this lane.

The reviewer applied all ten house-style checks and resolved at least eight. Exact identifiers, commands, hashes, and frozen results remain unchanged.
