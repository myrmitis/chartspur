# Frontend review addendum

The final proposal is `genre-proof/v2/proposed.patch`.
The v1 proposal and original report remain unchanged as historical evidence.
V2 uses the same two-field production repair and adds the approved CSS cleanup.

The regression names the genre cell by role and visible text.
It checks the seller-and-genre detail line in a fresh lookup page.
It records both exact public Apple request URLs at the local fixture boundary.
All 12 original assertions and lines remain; the candidate has 19 assertions.

The baseline fails the new search assertion.
The search-only old-field control fails the same assertion.
The lookup-only old-field control reaches its own lookup request and fails the new detail assertion.
The complete fix passes all original and new browser checks.
Each control differs from the fixed copy by exactly one production field read.
Every other copied file is byte-identical.

The unused CSS rule has no current producer or caller.
Its fake onboarding owner was removed in `06bdce751195c449fcde8c8f8d7bc15a91eada79`.
The unchanged Onboarding assertion still checks the replacement screenshot or empty state.
No test deletion is proposed in this lane.

See `genre-proof/v2/README.md`, `run-results.json`, and `preservation-receipt.json` for commands, hashes, and retained failure output.
No shared UI or Worker source changed before independent review.
No browser runner remains active.

All ten documentation checks were applied.
Exact technical identifiers and frozen evidence retain their required form.
