# 14-sequence-entry — Worker delivery

## Done

Added guided/explicit assembly of selected plain duel observations using the
existing sequence contract and unchanged `tactical_enemy_phase.evaluate`.
Attacker/defender roles, explicit entity IDs and argument/prompt order remain
visible. Three independent confirmations plus complete sources are required.
Player/shared ruleset conflicts reject with entry/field diagnostics; missing
values and unsupported unit/context/effect tails remain unchanged and refused.
Unknown top-level fields and duplicate JSON keys reject before assembly.
Sources are read-only; no run is imported or updated. Optional output creates
only new ignored observation JSON with no-follow protection. Run-like paths,
live symlink/hardlink aliases, overwrites and output escapes are rejected.

Baseline main: `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba`.
Literal pushed plan: `7f4553587263772d9539e571c04abb18207704bf`.
Reviewed code: `7b6cc0d74357abba53312dd217c1b9317a0271ec`.

## Checked

| Command/evidence at code commit | Result | Exit |
|---|---|---:|
| `make audit` — [output](attachments/14-sequence-entry/audit.log) | Three audits pass; 178 tests OK | 0 |
| `python3 tools/fw.py check` — [checks](attachments/14-sequence-entry/checks.log) | 0 errors, 0 warnings | 0 |
| Focused discovery; baseline-to-HEAD `git diff --check` in checks | 12 tests OK; no whitespace errors | 0 |
| [CLI workflows](attachments/14-sequence-entry/controls.log), [replay](attachments/14-sequence-entry/controls.py) | 15 workflows; supported payload/result equality; unknowns retained; sources unchanged | 0 |
| [Preservation](attachments/14-sequence-entry/preservation.log), [comparison](attachments/14-sequence-entry/preservation.py) | 324 canonical/research/private/pointer files unchanged across both checkouts; exclusive branch scope | 0 |
| [Rendered reference/link inspection](attachments/14-sequence-entry/visual-qa.log) | Readable full-page render; all local links resolve | 0 |

Two saved duels take nine guided answers with zero JSON edits or retyped
observation values. Nested sequence construction and repeated player/ruleset
copying are eliminated. EOF at every prompt boundary emits no artifact.
Tests additionally cover duplicate IDs/files/keys, malformed/run-shaped inputs,
unarmed/paired/forged observations, output protection and cancelled saving.

## Not checked

No human usability, actual gameplay/source verification, whole-map safety,
AI/path/order prediction, between-duel events, repeated enemy support, native
Windows output, new canonical coverage or rebuild. Identity and freshness
remain explicit player observations. Blind Verifier, Brain re-derivation,
collector integration and owner merge approval remain outstanding. Batch 13
files, shared engines and planning/framework files were not edited.

## Failed or blocked

[Initial attempts](attachments/14-sequence-entry/initial-failure.log) preserve
one test-fixture error, discovery of nonexistent filenames and a strengthened
forged-fixture control. Canonical weapon IDs/metadata were incorrectly treated
as plain full objects by synthetic tests; corrected fixtures now require a
supported exact-forged outcome. Initial successful logs remain alongside final
checks. No production filtering was added. No merge or reviewer spawned.
