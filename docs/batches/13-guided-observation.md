# 13-guided-observation — Worker summary

## Done

Added a standard-library terminal collector/editor for plain existing duels.
Grouped stats/bonuses and deliberate confirmations preserve unknowns, actual
forged values and unsupported effects. Prompts/assessment use stderr; stdout is
JSON. Optional files are create-only in ignored `state/observations`; runs,
incompatible/extra fields, duplicate keys, traversal, symlinks and overwrite are
refused. Editing renews each observation and the final confirmation.

Nested null/unknown/empty forge observations and malformed optional alive state
now stay present with completeness false. Known nonempty forge data remains
complete but engine-refused; literal boolean false still refuses a dead unit.
Supplied nested metadata and other observation fields are checked conservatively.
No engine, mechanics, canonical coverage or primary checkout changes.

| Anchor | Full commit |
|---|---|
| Fetched baseline origin/main | `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba` |
| Literal pushed planning commit | `7f4553587263772d9539e571c04abb18207704bf` |
| Preserved Verifier report tip | `517315b6f652c347c3c54dbf217e246c4cee8a63` |
| Audited revised implementation | `1b6e77ef786e806819b57088fd1a6a12f20a2b62` |

## Checked

[Evidence](attachments/13-guided-observation/) retains original failures and
revised `nested-*.log` commands, output and exits. The
[workflow runner](attachments/13-guided-observation/workflows.py) records 33
synthetic public cases spanning complete/custom/catalog, partial, real effects,
forge, paired/raw/context, mismatch, integer re-entry, unarmed, edit, renewed
confirmation, cancel/EOF, nested forge/alive and file boundaries. Both-side
public regressions challenge null/unknown/empty nested observations, malformed
alive values and known-forge/boolean controls without dropping data.

Complete/custom-forged/unarmed full assessments equal baseline (3/3). Forged
outputs pass the existing two-attacker sequence schema/outcome. Custom: 41
answers for 66 generated keys/75 formatted JSON lines; catalog: measured 27
answers; manual JSON edits: zero. Sixteen stat values use two answers.

| Command at audited revised implementation | Actual result | Exit |
|---|---|---:|
| `make audit` | All three audits pass; 181 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `python3 -m unittest discover -s tests -p 'test_observed_input.py' -v` | 15 tests OK | 0 |
| `python3 docs/batches/attachments/13-guided-observation/workflows.py` | All 33 cases; equality/preservation pass | 0 |
| `git diff 5c596d42adb3d2a5eeee460032ee20bdd4bb78ba --check` | Empty output | 0 |

Canonical/research/run file sets and content privately compared before/after in
primary and Worker: unchanged; no private values/hashes published. Verifier
report fast-forwarded before correction commits and remains untouched.
Reference/summary/attempts rendered, inspected and local links resolved.

## Not checked

Verifier recheck of this revised delivery, Brain re-derivation, combined Batch14
acceptance and owner merge approval remain pending. No human usability, native
Windows, new gameplay fact or whole-map safety validation. No rebuild needed.

## Failed or blocked

[Attempts](attachments/13-guided-observation/attempts.md) retains prompt-count,
zsh wrapper and exploratory failures; Brain's unknown-range failure; Verifier's
nested-null forge failure; and Brain-confirmed alive-string/empty-forge numeric
leaks at prior delivery. Revised public regressions preserve those values with
completeness false and no numbers. The prior catalog burden claim of 29 was
wrong; captured prompts and replay measure 27. Original evidence/history stays
available. Correction checks pass; independent recheck remains required.
