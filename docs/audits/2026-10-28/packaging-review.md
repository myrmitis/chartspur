# Independent CLI fixture-copy review

Provider: `OpenAI Codex subagent`.
Reviewer: `/root/agents_audit`.
Base: `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
Setup patch SHA-256: `5b7e6f1bd104106791d60d6fc0172cd9e1d122234c8719b3ba188c27969bffeb`.
Actual CLI test SHA-256: `b89d4dd59f403dbf7738d336ac7b88f8f703925eaf63aaca6beed925ba155dcc`.

The setup-only correction clears independent preservation review.
The estimate case now copies the complete current pipeline directory into its disposable workspace.
It excludes Python bytecode and no longer maintains a private two-module inventory.
An internal helper extraction can therefore preserve the same public command without breaking this test's setup.

I read the exact setup diff and actual shared source.
All assertion ASTs and both test declarations match the prior cleared case.
The synthetic SQL, input rows, subprocess command, output reads, and all following estimate assertions remain AST-identical.
The entire summary CLI case also remains AST-identical.
The other three Python candidate files still match the cleared v2 proposal exactly.

The test still creates synthetic persisted inputs in a fresh temporary workspace.
It still runs the real estimate script and checks actual exported JSON.
Copying source does not supply an output receipt, mock internal behavior, or access the real database.
The fixture retains the stored-time, screenshots, malformed-input, and velocity assertions.

The worker's isolated rerun reports both CLI cases passing.
I verified its log hash and read the actual result.
This review started no duplicate runner and made no source edit.
Frozen v2 patches and reviews remain byte-identical historical evidence.

`independent-review.json` records the exact content and AST comparisons.
The final combined candidate must still pass its normal offline and UI gates.

I applied all ten house-style checks and resolved at least eight applicable checks.
Exact source pins, hashes, identifiers, and authority boundaries retain their technical form.
