# 15-duel-boundary — Worker delivery

## Done

Hardened the direct `assess` API and unchanged `tools/tactical_combat.py FILE`
CLI. Unknown/dead alive state, every separate forge marker, unrecognized fields,
malformed stats/ranks/ranges/modifiers/context and incomplete weapon effects
are refused without stripping information. Catalog lookup metadata remains
internal; complete supported catalog/custom/forged/unarmed results are unchanged.
JSON rejects duplicate keys and non-JSON constants. Read failures are controlled;
named/resolved run paths and standard-run hard links are refused before opening.
No run initialization or mutation; no formula, canonical or shared-tool changes.

Baseline: `ec3bceca1d70a4da240a490601602e97c2466de2`.
Literal fetched plan: `b9fffaeeea149470e7892106d9e6c6060f104c17`.
Checked code: `6c16c873214b198e113e03fb69da0745182798e0`.

## Checked

| Command/evidence at code commit | Result | Exit |
|---|---|---:|
| `make audit` — [output](attachments/15-duel-boundary/audit.log) | Three audits pass; 200 tests OK | 0 |
| `python3 tools/fw.py check` — [output](attachments/15-duel-boundary/checks.log) | 0 errors, 0 warnings | 0 |
| Dedicated discovery — [output](attachments/15-duel-boundary/focused.log) | 7 tests; both-side/nested API and CLI matrices, no numeric UNKNOWN leakage | 0 |
| [Compatibility replay](attachments/15-duel-boundary/controls.py), [output](attachments/15-duel-boundary/controls.log) | Full baseline equality: ten supported controls, collector custom/catalog, sequence; immutable inputs | 0 |
| [Preservation replay](attachments/15-duel-boundary/preservation.py), [before](attachments/15-duel-boundary/preservation-before.log), [after](attachments/15-duel-boundary/preservation-after.log) | 161 protected files equal baseline; private checksum unchanged | 0 |
| [Branch diff](attachments/15-duel-boundary/diff.log) | Exclusive ownership; whitespace check passes | 0 |
| [Reference render/links](attachments/15-duel-boundary/visual-qa.log) | Readable, no overflow; local links resolve | 0 |

Independent synthetic arithmetic checks six guaranteed damage leaving 24 HP,
then certain defender death with 30 damage. Existing refusal controls include
Counter, drain, unsupported procs, paired combat and breakage. A mocked read
proves run-path protection happens before file content access.

## Not checked

Actual gameplay/RNG/source verification, new tactical coverage, whole-map safety,
AI/path/order prediction, native Windows, human usability and rebuild are not
claimed. Canonical data/rebuild code are untouched. Blind Verifier, Brain
independent re-derivation and combined Worker 16 launcher trial, CI and owner
merge approval remain outstanding.

## Failed or blocked

[Baseline probes](attachments/15-duel-boundary/baseline.log) reproduce all eight
reported numeric bypasses. [Initial failures](attachments/15-duel-boundary/initial-failure.log)
retain diagnostic-order regressions, a public-log path hygiene failure, an
unused nonexistent collector import and exploratory nonexistent paths.
Restored side-specific diagnostics, sanitized local paths and corrected the
replay import. All final checks pass. No merge or reviewer spawned.
