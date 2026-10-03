# Documentation inspection

Changed Markdown was rendered using bundled `marked` and Playwright with
installed Chrome, at a 1100 by 900 viewport. The initial default Playwright
launch could not find its bundled browser; using installed Chrome succeeded
(exit 0). No project runtime dependency was added.

Inspected `render-usage.png`, `render-formulas.png`, `render-status.png` and
`render-counts.png`: input fields, absence declarations, labels, conditional
scope and current test count are readable, with no clipped changed content.
Screenshots cover the changed sections rather than claiming a full redesign.
The temporary rendering script was outside the repository and is not a
production asset.

A Python standard-library link check parsed Markdown link targets in
`docs/usage.md`, `docs/combat-formulas.md` and `STATUS.md`, resolved local
paths relative to each document and checked existence. Result: 11 local
links resolved, exit 0; targets/results are in `link-check.json`.
