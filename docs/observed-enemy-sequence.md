# Observed enemy attack sequence

Use this read-only entry point for a **fixed supplied order of distinct observed
attackers** against one player unit in Hard/Classic. It carries possible player
HP across supported duels. It does not select enemy targets, order, paths or
threat ranges, or establish whole-map safety.

```sh
python3 tools/tactical_enemy_phase.py examples/observed_enemy_sequence.json
```

The [synthetic example](../examples/observed_enemy_sequence.json) returns
`NO_MODELED_PLAYER_DEATH_IN_THIS_SEQUENCE`, minimum player HP 10 and modeled
player death probability 0. Both survival flags remain false. Actual unknown
attackers, reinforcements, triggers or paths still prevent a safety guarantee.
Read the [tactical policy](agents/local/tactical-policy.md) before live advice.
The [existing reference calculator](../tools/enemy_phase.py) retains its
assumptions; it can infer maximum HP and sufficient durability from omitted
inputs. This observed entry point refuses those omissions.

## Observations required

Supply an object with exactly these fields:

| Field | Required value |
|---|---|
| `difficulty`, `mode` | `"Hard"`, `"Classic"` |
| `observed_inputs_complete` | `true`, confirming every supplied observation |
| `stats_basis` | `"effective_displayed"`; include active stat bonuses once |
| `support_state`, `partners` | `"none"`, `[]`, confirming neither paired nor adjacent supporting combatants on any side |
| `player_id` | Observed entity ID, nonempty string without outer whitespace |
| `player` | Complete observed unit described below |
| `enemies` | Nonempty ordered list of objects with exactly `id`, `unit`, `context` |

Enemy IDs identify actual distinct entities, not generic enemy types. IDs must
be distinct from each other and the player. Repeated-entity attacks are
unsupported; do not rename the same entity to obtain numbers.

Each unit requires `stats` containing exactly `hp`, `str`, `mag`, `skl`, `spd`,
`lck`, `def`, `res` as nonnegative integers (maximum HP positive), `current_hp`
as an integer from 1 through maximum HP, `weapon`, `weapon_rank` as one of
E/D/C/B/A, `skills`, `weaknesses`, `terrain`, `combat_bonuses`, and
`remaining_uses` as a nonnegative integer. Booleans are not integers here.
Skills and weaknesses are distinct nonempty string lists; `[]` confirms none.
All equipped skills and innate weaknesses remain required after reclassing.

`terrain` accepts integer `def`, `res`, `avoid`; `combat_bonuses` accepts integer
`hit`, `avoid`, `crit`, `crit_avoid`, `attack`. `{}` confirms no additional
active effects. Optional `alive` must be `true`. Optional `weapon_state` is
`"equipped"` or `"unequipped"`. Other unit fields/effects are refused.

A weapon is either a known canonical ID confirming exact **unforged** catalog
values, or a full object with actual `weapon_type`, `rank`, `might`, `hit`,
`crit`, `range`, `damage_type`, `effect`, `brave`, `effectiveness`. Full objects
may also have `id`, `name`; other keys are refused. Supply actual forged
might/hit/crit directly, never offsets or `+` markers. Range is a positive
integer or string such as `"1"`, `"1-2"`, `"1~2"`. No special effect uses
explicit `"–"`, `brave: false`, `effectiveness: []`. Eligibility must still be
checked independently. Only the player may be explicitly unequipped:
`weapon: null`, `weapon_state: "unequipped"`, `remaining_uses: 0`.

Each context requires positive integer `distance`. Optional positive integer
`turn` and boolean `outdoors` become mandatory when equipped skills depend
on them. Other context keys are refused. Confirm that no healing, EXP-triggered
level/stat/skill changes, equipment swaps, events or other changes intervene
between the supplied duels. Such changes require a new observation, rather
than an unrepresented sequence effect.

## Results and refusal limits

Every attacker is validated and preflighted, including a tail after modeled
certain player death. Any missing, malformed or unsupported entry produces
`UNKNOWN`, `outcome: null`, diagnostic entry/side/field and false survival
flags. Unsupported effects are retained as refusals, never removed.

Supported results compose the existing [duel gate](../tools/tactical_combat.py)
state distributions using its independent uniform RNG model. Every surviving
player HP branch is assessed again for the next duel, including HP-dependent
skills. Dead-player probability is absorbing; a dead enemy cannot finish its
duel. Enemy HP is not carried forward because attackers are distinct. Any
unsupported reachable HP branch invalidates the entire numerical sequence.

Player durability must cover the **sum of maximum scheduled retaliation hits**
across every preflighted duel. This conservative bound counts even strikes that
an early kill or death could prevent; it can refuse a feasible sequence. It does
not claim actual uses spent. Enemy durability must cover its own scheduled
maximum. Possible breakage is refused; no weapon swapping is modeled.

`outcome` contains final HP probabilities, player death probability, minimum
and expected player HP, the maximum scheduled retaliation budget and per-step
player/enemy death probabilities. Per-step enemy death is unconditional,
including zero chance of engaging when the player is already dead.
`LETHAL` means only dead-player states remain; `POTENTIALLY_LETHAL` means
some death probability; `NO_MODELED_PLAYER_DEATH_IN_THIS_SEQUENCE` remains
conditional on complete supported observations. Expected HP is not a guarantee.

For direct callers, import `evaluate(payload)` from
[the wrapper](../tools/tactical_enemy_phase.py). It does not mutate the input.
CLI JSON results, including `UNKNOWN`, exit 0; unreadable/invalid JSON exits 2
with a diagnostic on stderr. Neither interface opens or updates a player run.

These synthetic controls demonstrate composition and uncertainty handling,
not new source-verified gameplay coverage or real play-session acceptance.
