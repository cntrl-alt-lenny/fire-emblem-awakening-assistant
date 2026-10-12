# Observed combat input shapes

The [live duel gate](../tools/tactical_combat.py) requires explicit observations
for both `attacker` and `defender`. This boundary strengthens input validation;
it adds no supported mechanic or verified gameplay coverage.

| Field on either combatant | Required observation | Refused examples |
|---|---|---|
| `skills` | List of string skill IDs, at most five; every ID must be supported | Missing, null, `""`, `{}`, `[null]`, `[0]`, an unknown ID |
| `weaknesses` | List of string categories: `beast`, `dragon`, `armour`, `flying` | Missing, null, `""`, `{}`, `[true]`, nested lists, unknown category |
| `current_hp` | Integer within 1 through observed `stats.hp`, inclusive | Missing, null, boolean, float (including `1.0`), string, zero, negative, above maximum |

Explicit `[]` means the player confirmed there are no skills or weaknesses.
It does not mean inspection was omitted. Never convert an object/string to a
list, round HP, or remove an equipped effect to obtain an outcome. Both sides
are checked even when the defender is explicitly unequipped.

A malformed observation returns `status: "UNKNOWN"`, `outcome: null` and
`safe_to_claim_survival: false`. Its `reason` identifies the side and field;
missing/null required fields appear in `missing`. For example, an empty object
for defender skills reports:

```json
{
  "status": "UNKNOWN",
  "reason": "defender:skills requires an explicit list of strings; [] means confirmed none",
  "safe_to_claim_survival": false,
  "outcome": null
}
```

The Python entry point remains `assess(payload)`. The offline JSON CLI remains:

```sh
python3 tools/tactical_combat.py synthetic-battle.json
```

`UNKNOWN` is a valid JSON response with CLI exit 0. Callers must inspect status
and outcome, rather than treating a successful process exit as a supported duel.
Inputs are preserved, including refused inputs; tests use temporary synthetic
files and never initialize or alter a player run.

Legal lists and integer HP preserve the full supported assessment. Existing
[skill-context requirements](combat-context.md), explicit weapon observation,
unsupported Counter/drain/proc refusals and paired outcome limits still apply.
See the [tactical policy](agents/local/tactical-policy.md) and
[usage guide](usage.md) for the complete observation contract. A supported duel
still cannot establish whole-map survival.
