# Independent bounded v2 preservation review

Provider: `OpenAI Codex subagent`.
Reviewer: `/root/agents_audit`.
Base: `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
V2 patch SHA-256: `85ccc6ddb7f8149bff3e48b834bfdfe2c3d41714f318175f101fe2c8b9a6336a`.
V2 CLI test SHA-256: `a8960e6b2405f73340d08a888b1f96be9a08d2b12de629e75bab90765c91ae18`.

The exact bounded v2 clears independent preservation review.
It retains the already cleared summary repair, two CLI cases, and two detached-case retirements.
Relative to v1, it removes only the unused estimate clock import and assignment.
It adds one stored-timestamp assertion to the existing estimate CLI case.
No formula, exported field, minimum guard, SQL, ordering, fallback, or output write changes.

The original v1 patch remains frozen with SHA-256 `f0684a8d0e8271161f529973d700fef19b13ca55f23bc0e3f8d03575a176a592`.
The earlier `python-preservation-review.md` retains its complete review and original controls.
This report covers only the bounded extension and its refreshed controls.

## Dead clock candidate ledger

- Exact location: `pipeline/estimate.py`, the `time` import and `main`'s local `now = int(time.time())` assignment.
- Exact original test: none reaches or reads that local value.
- Actual detected failure through this local: none. It has one assignment and zero loads.
- Non-test callers: the README, `run.sh`, and refresh workflow invoke the exporter; none reads this local or imported module attribute.
- Reflection: repository searches find no `locals`, `globals`, frame-local, inspection, tracing, or attribute consumer of the candidate.
- Named contract: none exposes the unused local or requires `estimate.time` as a public library API.
- History: `fba951e` introduced the unread clock assignment. `06bdce7` retained it when adding screenshots and guards.
- Current owner: exported `updated_ts` uses the stored snapshot row's `ts`, which the web client consumes for freshness display.
- Keeper: `PipelineCLITest.test_estimate_exports_screenshots_and_snapshot_velocity` now requires every exported timestamp to equal the fixture's stored snapshot time.
- Deletion unlocked: only the unused import item and local assignment. Keep the exporter's `updated_ts` field and ingest's separate live clock use.
- Risk and validation: accidental substitution of wall-clock time would change public freshness semantics. The stored-time assertion and its real owner mutation protect that boundary.

The AST comparison independently confirms the bounded production edit.
After removing exactly the old import item and assignment, the estimate AST matches v2 completely.
Every other v1 production file and retained test file matches byte for byte.
The new CLI file differs only by the one timestamp assertion.
No additional test, helper, mock, or production seam appears.

## Refreshed execution evidence

I read and verified the actual v2 control logs and their hashes.
The baseline plus both new CLI cases runs 20 Python-lane cases.
Its sole failure remains the genuine bare-output summary exception.
The final v2 proposal runs 18 Python-lane cases successfully.

All four actual estimate-owner mutants preserve the old four tests and the exact v2 CLI keeper bytes.
The old tests pass under all four mutants.
The new keeper fails for discarded screenshots, rethrown malformed JSON, zero first-snapshot velocity, and a wall-clock export timestamp.

The timestamp mutant explicitly restores its required `time` import.
It then changes the actual exported field to `int(time.time())`.
Its real subprocess succeeds and the new persisted timestamp-set assertion fails against `2000000`.
This is the intended data mismatch, not a missing-import or setup failure.

No new runner or shared edit occurred in this independent review.
`python-preservation-review-v2.json` records source, AST, keeper, and log checks.
Apply the exact reviewed patch, then inspect the actual combined diff and run the full relevant gates.
The final exporter can reuse a previously fetched public database copy to compare output without another Apple request.
Do not run against or write the tracked database for this comparison.

I applied all ten house-style checks and resolved at least eight applicable checks.
Exact identifiers, source pins, hashes, and accepted authority boundaries retain their technical form.
