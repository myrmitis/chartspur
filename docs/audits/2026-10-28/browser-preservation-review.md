# Independent metadata v3 authoring review

Provider: `OpenAI Codex subagent`.
Reviewer: `/root/agents_audit`.
Base: `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
V3 patch SHA-256: `70ac902ec9167943c2f5f6ef0489793607d77ef7a3768d177067c8b71ba1873b`.

The exact v3 proposal clears independent review.
Its sole v2 change checks presence of both public request paths as a set.
It no longer requires one call per path in a fixed order.
No named public contract imposes that order or cardinality.
The new check still fails if either endpoint is absent.

The app mappings, one-line CSS deletion, fixture, and visible assertions remain identical to cleared v2.
All 12 original assertions remain intact.
This correction changes an unlanded test's private ordering assumption; it does not hide a failing visible outcome.
V2's positive control already passed before the correction.

The separate v2 search-old and lookup-old controls remain frozen evidence.
Both fail before the request-presence assertion that v3 changes.
Their production mapping and preceding visible assertion bytes remain unchanged in v3.
This review does not claim new v3 negative-control executions.

The actual v3 positive run passed with 138 rows and both exact Apple fixture URLs recorded.
Its server exited successfully and no browser runner remains.
I read that result and independently verified the exact one-line source and patch delta.
No duplicate execution or shared source edit occurred in this review.

The complete mapping and pre-edit CSS ledger remains in `../v2/independent-review.md`.
Apply the exact latest patch, then review the actual combined source and run the final gates.

I applied all ten house-style checks and resolved at least eight applicable checks.
Exact identifiers, source pins, hashes, and execution boundaries retain their technical form.
