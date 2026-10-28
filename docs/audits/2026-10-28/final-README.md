# Final Chartspur local verification

All requested local gates passed on the frozen candidate.
No runner changed source, documentation, or stored data.

| Gate | Actual result | Log |
| --- | --- | --- |
| `node --check app.js` | Exit 0. | `js-app.log` |
| `node --check data.js` | Exit 0. | `js-data.log` |
| Exact CI Python syntax and seven JSON parses | Exit 0; no pipeline entry point executed. | `syntax-json.log` |
| `python3 -m unittest discover -s pipeline -p 'test_*.py' -v` | 37 tests passed in 8.754 seconds. | `offline.log` |
| `git diff --check` | Exit 0. | `whitespace.log` |
| Full extended browser harness with checked-in public data | Exit 0; 138 rows and all original plus metadata checks passed. | `checked-in/verify-ui.log` |
| Full extended browser harness with frozen refreshed public data | Exit 0; 139 rows and all original plus metadata checks passed. | `refreshed/verify-ui.log` |

Both browser runs used copied candidate assets and the exact candidate harness.
The refreshed copy used the earlier verified 139-app export.
No new ingest or refresh ran.
The new metadata checks intercepted Apple search and lookup requests locally.
No checkout, provider mutation, deployment, or message occurred.
Screenshots remain in each copy's `output/data/verify.png`.
No screenshot entered the shared checkout.

`native-results.json` and `browser-results.json` record exact argument arrays, working directories, times, and exit codes.
`runtime.json` records Python 3.14.7, Node 26.0.0, Playwright 1.58.0, and its matching Chromium revision 1208.
Hosted CI specifies Python 3.12 and Node 22.
These local results do not claim execution on the hosted runtime.

`before.json` and `after.json` pin all 88 frozen project files and all four stored data files.
Every hash remained unchanged across the runners.
HEAD also remained unchanged at `49453b586d9a854c942ea02a4b77c9b85e7ab382`.
The planned working changes were part of the frozen candidate.
The read-only comparison used that frozen state rather than rejecting its legitimate precommit diff.

`copy-receipt.json` pins all nine files in each public copy.
All copied source, harness, and data hashes remained unchanged.
`final-receipt.json` records those comparisons and screenshot hashes.
The candidate harness SHA-256 is `6484974136a29c116771b403af34bb1c98186f6cf14f7c96f615a61a97828388`.

Both task-owned HTTP servers stopped with exit 0.
All task-owned runners ended.
There is no remaining local verification blocker.
Hosted CI and release acceptance remain separate observations for the coordinating agent.

All ten documentation checks were applied.
Exact commands, identifiers, runtime versions, hashes, and frozen evidence retain their required form.
