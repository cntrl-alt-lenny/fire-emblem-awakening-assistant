# Chapter 20 correction: Brain review

Reviewed 2026-10-08 at delivered commit
`1165be06aa8b6af6c2755f642d3a2e02df195291`. Worker evidence is at
`7747d2ee79044eaa6f18a2673c26325e3b8e344a`; its report-only delivery is
`07357188ae2b841a704e0e5e0e7fb4866cc3bded`. The final delivery adds only the
Verifier report. Review applies to the corrected research, not gameplay truth.

## Decision

Accept the bounded correction, subject to owner merge approval and integration
checks. No demonstrated blocker. Round 006 remains superseded; its stamped
reports and rejected assessment history remain available. Chapter 20 completion
and source independence remain unresolved. Zero new gameplay coverage.

## Independent re-derivation

Bounded web-reader retrievals on 2026-10-08 reproduced the catalog Chapter 20
objective column, Gamer Guides Chapter 20 Condition field and separate Hard
default, and Vandal's Victoria field. Original-URL indexed MK retrieval reproduced
the completion footnote in Chapter 20 `[WM20]` after Excellus's skills. A second
bounded indexed introductory lookup reproduced the Hard-default overlap with
Gamer Guides. Direct GameFAQs access remains denied; no direct retry, bypass,
mirror, crawl or full-page archive was used. Unrelated search hits were excluded.
Exact source URLs and durable locators are in the
[corrected assessment](../../006-chapter20-objective/attachments/objective-evidence.md).

The source fields genuinely disagree; boss order is not completion evidence.
Introductory overlap establishes a dependency lead, not source lineage. MK's
broad editorial Classic assumption does not tie its completion assertion to
observed Hard/Classic gameplay. The inherited forum account was not freshly
retrieved here and remains explicitly unreproduced. The Verifier's no-blocker
finding agrees with this re-derivation. Its blind ordering is reported evidence;
private historical actions cannot be independently reconstructed.

## Checks at the delivered commit

Environment: macOS 27.0.1 arm64, Python 3.9.6. Commands ran in the exact delivery
checkout, before writing this review.

| Command | Actual relevant output | Exit |
|---|---|---:|
| `make audit` | Three audits `passed: true`; 44 campaign maps, 29 reinforcement records, 217 sources; `Ran 118 tests in 0.668s`, `OK`; zero verified safe schedules | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 tools/map_info.py --chapter 20 --difficulty hard` | Objective/map CONFLICTED; target phase null; schedule complete false; move safety false | 0 |
| Same command with `--turn 6 --phase player` | Target enemy phase 6; conflict and incomplete coverage retained | 0 |
| Same command with `--turn 6 --phase enemy` | Target enemy phase 7; conflict and incomplete coverage retained | 0 |
| Sorted JSON path/SHA-256 comparison using `git ls-tree` / `git show` against round starting commit and `origin/main` | Both equal; 28 canonical JSON files, including all other-mode records | 0 |

[CI at this exact delivery](https://github.com/cntrl-alt-lenny/fire-emblem-awakening-assistant/actions/runs/37299324080)
succeeded on Linux Python 3.9/3.13 and macOS Python 3.13.
Integration preservation, rendered review and final checks are recorded in
[the refresh record](../../../plans/2026-10-08-refresh.md).

## Limits

No observed objective/completion, complete schedule, source independence or
region/version equivalence was established. Fresh preservation and rendering
cannot recreate missing round 006 snapshots. The next observation remains
parked until suitable continuous capture is available; no game/save operation
or player-run initialization is authorized.
