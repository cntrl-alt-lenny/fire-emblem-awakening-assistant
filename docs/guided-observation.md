# Guided observed duel entry

Run from this checkout:

```sh
python3 tools/observed_input.py
python3 tools/observed_input.py --output state/observations/new-duel.json
python3 tools/observed_input.py --edit state/observations/new-duel.json
```

The collector asks for actual observations and prints a plain existing duel JSON
payload on stdout. Prompts and a concise assessment go to stderr. The default
writes no files. `--output` creates a new `.json` under this checkout's ignored
`state/observations`; it refuses existing files, traversal and symlinks. Editing
never overwrites the selected draft. Cancellation, EOF or Ctrl-C emits no payload
and creates no file. Player runs and run-shaped input are refused.

## What to enter

Blank or `?` means unknown, including current HP. Enter an actual integer:
`1.5`, `true` and `1e2` are refused. Stats use the shown order:
`hp str mag skl spd lck def res`. Within a group, `?` preserves an unknown value.
Terrain uses `def res avoid`; combat bonuses use `hit avoid crit crit_avoid attack`.
Enter `none` explicitly to confirm no skills, weaknesses, partners or bonuses.
Numeric zero must be entered as `0`; blank never supplies it.

Choose `effective_displayed` or `raw_permanent` explicitly. No bonus conversion
occurs. The existing live gate requires effective displayed stats with active
stat bonuses already applied once. Combat bonus fields remain separate. Enter
all real effects, even when unsupported. Counter, drain effects and paired full
outcomes remain UNKNOWN. UNKNOWN diagnostics contain no partial forecast numbers.

Choose `custom` for an observed custom/forged weapon: enter its actual type,
damage type, required rank, might/hit/crit, range, effect, brave status and
effectiveness. Required weapon rank differs from the unit's weapon proficiency.
`catalog iron_sword` displays exact battle values and requires a fresh `yes`
confirming an exact unforged match. Unknown names are never guessed. Catalog
values do not establish equipment eligibility. An explicitly `unequipped`
defender still needs observed stats, current HP, rank, skills, weaknesses,
bonuses and explicit zero remaining uses.

Support `none` confirms neither side has paired or adjacent support. Otherwise,
enter actual partner IDs. Optional `turn`/`outdoors` are omitted when unobserved
and irrelevant to supplied skills; they are explicitly requested when needed.
Edited supplied context fields remain present, including unknown/null values.
An unobserved required skill condition prevents completeness.

## Revising a draft

Every loaded value is shown with `keep=...`; type `keep` deliberately or re-enter
it. Blank clears that value to unknown. `keep` never accepts a previous overall
confirmation. Confirm current, complete observations again at the final prompt.
Incomplete values keep `observed_inputs_complete` false even after `yes`.
Unknown, zero, malformed or reversed weapon ranges and unknown effectiveness
categories also prevent completeness; keeping them preserves the supplied value.
Supplied forge data with nested null, `?`, `unknown` or empty observations remains
incomplete. Empty forge markers never confirm absence. Known nonempty forge
markers remain present and unsupported. Supplied `alive` must be a boolean;
malformed strings stay incomplete, and an explicitly dead unit refuses combat.
Supplied forge markers and real effects survive deliberate reuse; an incompatible
shape, extra field or duplicate JSON key is refused before collection rather
than silently dropping observations. Existing custom weapon objects are reused
as a whole; choose `custom` to re-enter their actual values.

## Synthetic replay

The [deterministic workflow runner](batches/attachments/13-guided-observation/workflows.py)
records complete, partial, forged, unsupported, unarmed, paired, edit, context,
cancellation and file-boundary cases without using a player run. Its
[output](batches/attachments/13-guided-observation/nested-workflows.log) contains literal
input transcripts and results. A complete custom duel uses 41 answers and zero
manual JSON edits; a catalog duel uses 27. Scripted replay is not human usability
testing or gameplay validation.

These drafts use the [existing live gate](../tools/tactical_combat.py) and supported
[sequence schema](../tools/tactical_enemy_phase.py). A duel describes supplied
combat roles only. It cannot establish whole-map safety, AI order, unseen threats
or complete reinforcement schedules. See the [tactical policy](agents/local/tactical-policy.md).
