# Applied Python preservation review

Provider: `OpenAI Codex subagent`.
Reviewer: `/root/agents_audit`.
Base: `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
Approved proposal SHA-256: `85ccc6ddb7f8149bff3e48b834bfdfe2c3d41714f318175f101fe2c8b9a6336a`.

The actual shared four-path Python candidate clears preservation review.
All four applied files match the independently reviewed v2 bytes exactly.
The earlier proposal reviews and controls therefore apply to this actual source.
Full final offline and browser gates remain required.

The actual diff removes only the unused clock import/read and repairs bare summary output paths.
It retires the two detached test methods after adding their real CLI keeper.
The existing keeper also protects stored snapshot timestamps.
No other formula, SQL, output field, guard, or retained assertion changed.

I reviewed the tracked diff and the new untracked `pipeline/test_cli.py` together.
The new file matches the exact cleared test hash, `a8960e6b2405f73340d08a888b1f96be9a08d2b12de629e75bab90765c91ae18`.
The file matches the existing CI discovery pattern.
Every other tracked pipeline file matches base.
All 15 tracked stored/public/operating files checked in the independent comparison also match base.

The worker retained an initial patch-check failure caused by missing new-file metadata in the frozen proposal.
It then copied only the four exact reviewed source files after baseline checks.
That transport change did not change the proposed content.
`application-v2.json` records the failure and the applied bytes.

`applied-python-preservation-review.json` records the four hashes, combined source digest, and complete preservation inventories.
`applied-python-tracked.patch` retains the existing-file diff; the new CLI file hash records the separate untracked file.
No new product test runner or Python source edit occurred in this independent review.

The separate two-file documentation application also matches its approved patch.
Both issue-form versions parse with system Ruby's safe YAML parser.
Their parsed structures differ only in the intended first markdown text.
The form URL identity, required inputs, privacy sentence, and local UI check requirement remain intact.

I applied all ten house-style checks and resolved at least eight applicable checks.
Exact source pins, paths, identifiers, and failure evidence retain their technical form.
