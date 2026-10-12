# 13-guided-observation — Worker summary

## Done

Added a standard-library terminal collector/editor for plain existing duel
payloads. Stats and bonuses are grouped; prompts/assessment use stderr and JSON
uses stdout. Unknown stays null; absence, catalog values, reuse and overall
completeness require deliberate confirmation. Actual forged/unsupported effects
survive. Fresh optional context is omitted unless relevant; edited supplied
unknown context remains present. Run files, incompatible/extra fields and
duplicate keys are refused. Optional files are create-only inside ignored
`state/observations`, with traversal/symlink/overwrite refusal.

Only assigned product files and batch evidence changed. No new mechanics or
coverage; shared engines remain unchanged.

| Anchor | Full commit |
|---|---|
| Fetched baseline origin/main | `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba` |
| Literal pushed planning commit | `7f4553587263772d9539e571c04abb18207704bf` |
| Audited implementation | `80d50e43da32b769c988de1d9f2ec116238a03fa` |

## Checked

[Evidence](attachments/13-guided-observation/) retains real commands, output,
exits and failures. The [workflow runner](attachments/13-guided-observation/workflows.py)
records 23 synthetic public CLI cases: complete/custom/catalog, partial, Counter,
drain, forged, paired, raw, context, mismatch, integer re-entry, unarmed, deliberate
edit, stale confirmation, cancel/EOF, malformed draft and file creation/refusal.
Complete/custom-forged/unarmed full assessments exactly equal baseline (3/3).
Forged outputs pass the existing two-attacker sequence schema/outcome. Custom:
41 answers for 66 generated keys/75 formatted JSON lines; catalog: 29 answers;
manual JSON edits: zero. Sixteen stat values use two answers. Scripted burden
measurement does not prove human usability.

| Command at audited implementation | Actual result | Exit |
|---|---|---:|
| `make audit` | All three audits pass; 178 tests OK | 0 |
| `python3 tools/fw.py check` | 0 errors, 0 warnings | 0 |
| `python3 -m unittest discover -s tests -p 'test_observed_input.py' -v` | 12 tests OK | 0 |
| `python3 docs/batches/attachments/13-guided-observation/workflows.py` | All 23 cases; equality and preservation pass | 0 |
| `git diff 5c596d42adb3d2a5eeee460032ee20bdd4bb78ba --check` | Empty output | 0 |

Privately compared canonical/research/run file sets and content before/after in
primary and Worker checkouts: unchanged; published no private values/hashes.
Reference, summary and failed-attempt record rendered and visually inspected;
changed local links resolve. No run was initialized or selected as observation.

## Not checked

Fresh blind Verifier, Brain re-derivation, combined Batch14 entry and owner merge
approval remain pending. No human terminal trial, native Windows verification,
new gameplay fact or whole-map safety validation. No rebuild was needed.

## Failed or blocked

[Attempts](attachments/13-guided-observation/attempts.md) preserves the first
focused failure (prompt count 39 versus expected 40), zsh wrapper failure and
missing exploratory filenames. Explicit required weapon rank now brings custom
entry to 41 prompts and meets sequence requirements. Edited unequipped state
gets deliberate confirmation. Corrected checks pass; no shared-contract blocker.
