# Final metadata proposal

This v3 proposal supersedes v2.
V1 and v2 remain frozen as prior evidence.

The only v2 change replaces the request list comparison with a set comparison.
The permanent check requires search and lookup to occur.
It permits repeated calls and either order.
The visible Category, genre filter, and seller-plus-genre assertions are unchanged.

The production change still fixes two Apple genre-field reads and removes one unused CSS rule.
Both production files are byte-identical to v2.
All 12 original browser assertions and lines remain in order.
The complete candidate has 19 assertions.
No timeout, retry, skip, or production test seam changed.

The independent one-field controls remain in `../v2/`.
Each fails its intended visible outcome before the request-presence check.
This change does not alter those control paths.
`fixed.log` records the final positive browser run.
`preservation-receipt.json` records the exact diff and source preservation.

The full patch SHA-256 is `70ac902ec9167943c2f5f6ef0489793607d77ef7a3768d177067c8b71ba1873b`.
Shared source remains unchanged pending independent review.

All ten documentation checks were applied.
Exact identifiers, hashes, and frozen evidence retain their required form.
