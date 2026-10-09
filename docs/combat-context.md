# Live combat skill context

The strict [live combat gate](../tools/tactical_combat.py) requires observed
context for equipped skills on either combatant. Unknown skill conditions return
`UNKNOWN` with `outcome: null`; the gate does not default or coerce those inputs.
This is an input contract, not new verification of game mechanics.

## Required context

Use canonical skill IDs in each combatant's `skills` list. The same battle
`context` applies to attacker and defender, including an explicitly unequipped
defender whose skills still affect the forecast.

| Equipped skill on either side | Required field | Accepted JSON values |
|---|---|---|
| `indoor_fighter`, `outdoor_fighter` | `context.outdoors` | `true` or `false` |
| `lucky_seven`, `even_rhythm`, `odd_rhythm` | `context.turn` | A positive integer, starting at `1` |

Missing fields, `null`, strings, arrays and objects are refused when the equipped
skill needs the field. Outdoors also refuses numbers; turn also refuses zero,
negative numbers, decimals and booleans. For example, `true` is not turn `1`.
There is no conversion of `"false"` to `false` or `"8"` to `8`.

If neither combatant has an Indoor/Outdoor Fighter skill, `outdoors` may be
omitted. If neither has a turn-dependent skill, `turn` may be omitted. A relevant
skill requires its context even when it would be inactive on the supplied turn.
Keep every actually equipped skill; removing a skill to obtain a number is not a
valid workaround.

## Supplying context

This fragment shows the context portion of an otherwise complete observed battle
input; it is not a complete battle or a default for an unobserved location:

```json
{
  "context": {
    "distance": 1,
    "outdoors": false,
    "turn": 8
  }
}
```

The public command reads a JSON file and prints the assessment:

```sh
python3 tools/tactical_combat.py observed-battle.json
```

For a defender with `lucky_seven` and a missing or invalid turn, the diagnostic
identifies both the combatant and the field:

```json
{
  "status": "UNKNOWN",
  "reason": "defender:context.turn requires an explicit positive integer (not boolean) for lucky_seven",
  "safe_to_claim_survival": false,
  "outcome": null
}
```

`UNKNOWN` is returned as JSON with process exit status `0` for these semantic
input refusals. Inspect `status` and `outcome`; a successful process alone does
not mean the duel was supported.

## Scope and limits

Well-formed supported input preserves the calculator's existing forecasts and
outcomes. Synthetic regressions cover both sides, indoors/outdoors, turns
`1`, `2`, `7`, `8`, optional omissions, public JSON output and unchanged inputs.
They check the contract and numerical preservation, not source truth, all game
mechanics or complete tactical coverage.

All other requirements in the [tactical policy](agents/local/tactical-policy.md)
and [usage guide](usage.md) still apply: explicit Hard/Classic, complete observed
effective stats, equipment, support and skills. Paired/adjacent full outcomes and
unsupported effects remain refused. No duel outcome establishes whole-map
survival, enemy order or reinforcement safety. Never strip a real effect or
assume unknown information to obtain reassurance.
