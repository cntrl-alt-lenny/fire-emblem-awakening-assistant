# Direct observed duel boundary

Run `python3 tools/tactical_combat.py FILE` with a plain observed battle JSON.
The public `assess(payload)` and `known_weapon(unit, side)` signatures remain
unchanged. This gate validates observations before the existing calculator;
it adds no combat formulas or gameplay coverage.

## Accepted observations

Supply explicit `Hard`, `Classic`, `effective_displayed`,
`observed_inputs_complete: true`, `support_state`, `partners`, `attacker`,
`defender` and `context`. For a supported duel, support is `none` and partners
are `[]`, confirming no paired or adjacent supporting combatant. Optional
root `note` is a string. Other root fields, including run/event/roster data,
are refused.

Each unit requires all eight effective displayed stats (`hp`, `str`, `mag`,
`skl`, `spd`, `lck`, `def`, `res`), current HP, exact weapon, weapon rank,
all skills, weaknesses, terrain, combat bonuses and remaining uses. Stats are
nonnegative integers; maximum HP is positive and current HP is within
1..maximum. Uses are nonnegative integers. Booleans, floats and numeric strings
are not numbers. Rank must be exactly E/D/C/B/A, including on an unarmed side.

Optional `alive` must be `true`; false and unknown states are refused. Optional
`weapon_state` must be `equipped` or `unequipped`, consistent with the weapon.
Only a defender explicitly unequipped may supply `weapon: null`, with zero
remaining uses. Optional unit/weapon `id` and `name` are known nonempty strings.
Omitting these optional fields adds no inferred state.

Terrain accepts only integer `def`, `res`, `avoid`; combat bonuses accept only
integer `hit`, `avoid`, `crit`, `crit_avoid`, `attack`. Signed modifiers are
preserved. Empty objects confirm no extra modifiers. Context requires positive
integer `distance`; optional `turn` is a positive integer and `outdoors` is a
boolean even when no equipped skill uses them. Relevant skills require their
[explicit context](combat-context.md).

## Exact weapons and effects

Canonical weapon IDs resolve catalog metadata internally. Caller-supplied
objects accept only `id`, `name`, `weapon_type`, `damage_type`, `rank`, `might`,
`hit`, `crit`, `range`, `effect`, `brave`, `effectiveness`. All mechanical fields
are required. Might/hit/crit are nonnegative integers; range is a positive
integer or positive ascending range string such as `1-2` or `1~2`.

No effect is explicit `"–"`; no Brave is `false`; no effectiveness is `[]`.
Brave text and boolean must agree. Exact custom or forged values remain
supported. Any separate `forge` marker, including `{}`, `null`, `[]`, or a
suffix, is refused: supply actual complete weapon numbers instead. Extra
mechanical fields such as `status_effects` are refused at every level rather
than stripped. Catalog metadata is not permission to add effect fields to a
custom object.

## Refusals and file handling

Semantic unknowns return JSON `UNKNOWN` with a reason or missing-field list,
`outcome: null`, and `safe_to_claim_survival: false`; the CLI exits 0. No numeric
forecast or partial probability distribution accompanies a refusal. Supported
results retain the existing full distribution, probabilities, worst HP and
classification. Counter, drain, unsupported procs, paired outcomes and possible
weapon breakage remain refused. See [supported formulas](combat-formulas.md)
and [input shape rules](combat-input-shapes.md).

Malformed/unreadable JSON exits 2 with a controlled diagnostic. Duplicate keys
and NaN/Infinity constants are rejected. Named `current_run.json`, resolved
symlink names and hard links to the checkout's standard run are refused before
reading. Run-shaped data never becomes a duel. Files are read-only; the gate
never creates or updates a run. Structural tests do not verify source facts,
actual RNG, complete maps, or whole-map survival.
