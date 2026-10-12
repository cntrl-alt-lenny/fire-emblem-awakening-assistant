# 11-observed-sequence — blind Verifier review

Reviewed delivery: `17d6a09e888fd82e3517d074224b1254b5ae7b55`.
Original main: `e78fa7bcc245071556a408f725105ac63ce7a8e9`.
Plan: `ea5eb003d232f1e45a1c31e5ac2bb7412949b56e`.
Fetched remote tip matched the literal delivery before inspection and after checks.

## Independent review

Read project/framework/Verifier/state/tactical rules and pinned plan. Before
new production, tests, reference, example or Worker conclusions, privately
derived baseline defaults, ordered HP kernels, death absorption, early kills
and conservative durability. Inspected production first, then built separate
synthetic controls; read Worker tests/docs/summary afterward. No new external
mechanics claims or formulas were introduced.

For HP 10, independent attacks dealing 6 and 5 with hit probabilities 1/2 and
1/4 give `{10:3/8, 5:1/8, 4:3/8, 0:1/8}`. Separately enumerating uniform
two-draw hit outcomes for displayed 50/25 produces 0.505/0.1275; the complete
implemented distribution matched the table below, rather than only death risk.

| Final HP | Independently expected and actual probability |
|---:|---:|
| 0 | 0.0643875 |
| 4 | 0.4406125 |
| 5 | 0.0631125 |
| 10 | 0.4318875 |

Controls also matched crit branches, certain death, interrupted enemy doubles,
newly active Vantage, sufficient/insufficient cumulative uses and legacy
supported results. Incomplete collections/HP/equipment, support, repeated
entities, conflicting turn/outdoors, unsupported/malformed lethal tails and
dynamic Sol overkill all returned UNKNOWN without numbers. Inputs remained
immutable; distances may vary and skill-required context is per entry.

## Checks at the literal delivery

| Real command or check | Relevant output | Exit |
|---|---|---:|
| `make audit` | Three audits: `passed: true`; `Ran 142 tests`; `OK`; zero certified schedules | 0 |
| `python3 tools/fw.py check` | `0 error(s), 0 warning(s)` | 0 |
| `python3 -m unittest discover -s tests -p test_tactical_enemy_phase.py -v` | `Ran 11 tests`; `OK` | 0 |
| `git diff --check e78fa7bcc245071556a408f725105ac63ce7a8e9 17d6a09e888fd82e3517d074224b1254b5ae7b55` | No output | 0 |
| `python3 /tmp/fea-verifier11-independent-controls.py` | `Independent controls: 50 PASS; all inputs immutable`; supported/UNKNOWN CLI exit 0 | 0 |
| Synthetic invalid-JSON CLI subprocess | `Cannot read sequence JSON: Expecting property name enclosed in double quotes`; input preserved | 2, expected |
| `python3 tools/tactical_enemy_phase.py examples/observed_enemy_sequence.json` | Conditional zero death; minimum HP 10; both survival flags false | 0 |
| Unchanged reference with example player HP/durability removed | Death 0, minimum HP 10; confirms baseline assumptions | 0 |
| Private SHA-256/file-set comparison | 161 linked canonical/research/private files unchanged; 2 primary private files unchanged | 0 |
| Baseline diff for canonical/research/state/coverage/shared engines | No output; only owned additions and evidence changed | 0 |
| Headless Markdown/JSON rendering and local-link checks | Reference, Worker summary and example inspected; links resolve; no overflow/clipping | 0 |

One initial private Sol control expected support but its critical overkill was
already refused. Corrected the synthetic fixture to isolate later HP-dependent
refusal; rerun passed. No product fix was made. Evidence/privacy diff inspection
found no player content, credentials, canonical changes or coverage increase.

## Findings and verdict

No BLOCKER, SHOULD FIX or new UNPROVEN CLAIM found. NOTE: conservative
durability/preflight may refuse feasible sequences, as documented; numerical
results remain conditional on a fixed order without intervening changes.

PASS within this batch's stated scope. Real gameplay/source accuracy,
whole-map safety and combined batch-10 integration remain unproved. Brain
integration review, independent re-derivation and owner approval remain required.
