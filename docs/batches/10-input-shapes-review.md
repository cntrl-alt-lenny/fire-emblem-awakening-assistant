# 10-input-shapes — independent Verifier review

## Scope and blind order

Reviewed `bffe0a39035e6e5735da661b6ab306e9b3966fd7` against baseline
`e78fa7bcc245071556a408f725105ac63ce7a8e9`; pinned plan
`ea5eb003d232f1e45a1c31e5ac2bb7412949b56e`.
Fetched Worker tip matched the literal reviewed commit. Review used a separate,
detached linked checkout.

After status/rules/plan, before reading changed production, tests, documentation
or Worker conclusions, I constructed synthetic 30-HP duels and recorded expected
UNKNOWN/null refusals for both sides: skills/weaknesses objects, strings,
non-string elements, missing/null fields, unsupported membership, and HP
types/bounds. Baseline had 18 leaks among 68 invalid cases; integer HP 1/30
controls remained supported. Production diff came next, then tests/reference,
summary and evidence.

## Findings and verdict

**PASS for this bounded input contract.** BLOCKER: 0; SHOULD FIX: 0;
UNPROVEN CLAIM: 0; NOTE: 0.

All 68 independent invalid cases refuse with UNKNOWN/null/false and side/field
diagnostics, preserve inputs, and match direct/public CLI results. Eighteen
baseline numeric leaks were independently reproduced through the CLI. All 293
complete supported assessments equal baseline; five distinct full CLI controls
also match. Ninety-two context/unsupported/unequipped checks pass. `known_weapon`
has identical AST; calculator/event code is unchanged.

Diff stays within the gate, new tests/reference and batch evidence. Public
attachments contain synthetic inputs and redacted historical failures; no home
paths or credential-pattern matches were found. Canonical/private regular-file
sets/content in primary and review checkouts were privately compared before/after
and preserved. Private paths, inventories and hashes are withheld.

Both changed documents were rendered to HTML/PNG and visually inspected: tables,
code and prose fit without clipping; local links resolve. No gameplay fact,
coverage, rebuild, player-run fixture or run mutation was introduced. Combined
batches, Brain re-derivation and owner approval remain outstanding.

## Independent evidence

Private command paths below are redacted for public portability. Outputs are
actual excerpts from the reviewed commit; the independent scripts remain private.

| Command | Relevant output | Exit |
|---|---|---:|
| `python3 tools/fw.py status` | `all project checks pass` | 0 |
| `python3 <private>/probe.py <review-checkout>` | `68 invalid cases; 18 contract failures; controls: ['attacker:1', 'attacker:30', 'defender:1', 'defender:30']` | 0 |
| `python3 <private>/regression.py <review-checkout> baseline` | `FAIL: defender skills object produced NO_MODELED_DEATH_IN_THIS_DUEL; expected UNKNOWN/null` | 1 |
| `python3 <private>/regression.py <review-checkout> tip` | `PASS: defender skills object refused UNKNOWN/null` | 0 |
| `python3 <private>/verify.py <review-checkout>` | `68/68 UNKNOWN/null/false with side/field; immutable; 68 CLI equality checks exit 0; 18 baseline CLI leaks reproduced` | 0 |
| Same independent probe | `Complete supported assessments equal baseline: 293 ; full CLI controls equal baseline: 5` | 0 |
| Same independent probe | `Existing context/unsupported/unequipped refusals: 92 ; known_weapon AST identical; canonical/private/calculator/event diff empty` | 0 |
| `make audit` | Three audits: `"passed": true`; `Ran 140 tests in 5.466s`; `OK` | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 -m unittest discover -s tests -p 'test_combat*.py' -v` | `Ran 31 tests in 4.879s`; `OK` | 0 |
| `git diff e78fa7bcc245071556a408f725105ac63ce7a8e9 bffe0a39035e6e5735da661b6ab306e9b3966fd7 --check` | No output | 0 |
| Private snapshots, primary and review checkout | `Protected regular-file sets/content preserved` (both) | 0 |
| `python3 <private>/render.py` | Both documents: `links resolved; HTML rendered; PNG generated; controlled browser cleanup` | 0 |

## Failed attempts

An initial baseline test-file lookup used a nonexistent filename (exit 128);
listing the baseline tree resolved it. Bundled Python lacked Markdown (exit 1);
system Python 3.9 Markdown rendered successfully. An early second-PNG inspection
preceded its creation; waiting for renderer completion resolved it. The baseline
regression failure above is intentional and demonstrates the original defect.

10-input-shapes · Verifier · DONE · report-only handoff; Brain reviews next.
