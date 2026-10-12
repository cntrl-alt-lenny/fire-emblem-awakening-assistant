# Assemble an observed enemy sequence

Select existing **plain duel JSON** files, supply actual entity IDs and confirm
a fixed attack order. Each file's attacker becomes one distinct enemy; its
defender must be the same unchanged player observation. The command copies
observations into the [existing sequence contract](observed-enemy-sequence.md)
and delegates assessment unchanged to
[the sequence engine](../tools/tactical_enemy_phase.py).

```sh
python3 tools/sequence_input.py
```

The guided command asks for the player ID, then each duel path and enemy ID.
Enter paths in the intended attack order; a blank next-path answer finishes
the list. It displays that order and asks three separate questions:

1. Is this the exact supplied attack order?
2. Are all supplied observations complete and still unchanged?
3. Do no healing, levels, equipment/skill swaps or other events intervene?

Only `yes` confirms each question. Blank or other answers leave sequence
completeness false. A source duel's completeness must also be explicitly true;
confirmations never repair incomplete sources. `cancel`, EOF or Ctrl-C stops
without emitting or saving a sequence. IDs identify actual entities: never
rename a repeated enemy to obtain numbers. Identical stats do not prove two
units are the same; entity identity remains the user's explicit observation.

Prompts, order and concise assessment status go to **stderr**. **stdout** is
only plain sequence JSON, allowing redirection or use by the existing engine.
The command writes no files by default. Redirected output may be empty after
cancellation; check the exit status before using it.

## Explicit selections and protected saving

```sh
python3 tools/sequence_input.py --player-id player_robin \
  --enemy enemy_west state/observations/west-duel.json \
  --enemy enemy_east state/observations/east-duel.json \
  --confirm-order --confirm-unchanged --confirm-no-events
```

Repeated `--enemy ID FILE` arguments define order. Omitting any confirmation
produces incomplete JSON and `UNKNOWN`, without numerical reassurance. Add
`--guided` to renew all three confirmations interactively for supplied arguments.

Optional `--output state/observations/sequence.json` also saves a new local
draft inside this checkout's ignored observations subtree. Relative `.json`
paths only: no overwrite, traversal, symlink components or `current_run.json`.
Saving uses create-only, descriptor-relative no-follow operations; supported
on Linux/macOS (use WSL on Windows). A protection failure exits 2 and emits
no JSON. No command initializes, imports or updates a run or ledger.

## Conflicts and unknowns

Sources must explicitly agree on Hard/Classic/effective displayed rules.
Defender snapshots must match field-for-field, including missing versus null
and value types. Shared support/partner observations must match too; a conflict
exits 2 with entry/field diagnostics. Refresh conflicting sources instead of
choosing whichever snapshot produces a preferable number. Selecting the same
file twice, including aliases, is refused even with different IDs.

Only documented duel keys are recognized: `difficulty`, `mode`,
`observed_inputs_complete`, `stats_basis`, `support_state`, `partners`,
`attacker`, `defender`, `context` and optional nonmechanical text `note`.
The note does not enter the sequence. Unknown top-level keys, duplicate JSON
object keys, malformed JSON, run-shaped inputs and live run paths are refused.
Run-like selected basenames, symlinks resolving to them and hardlink aliases
to this checkout's standard live run are rejected before decoding any contents.

Unit, weapon, support and context observations are copied without filling
missing values, converting raw stats, resolving weapon IDs, removing effects
or borrowing context from another entry. Unsupported skills/effects, paired
outcomes, unknown tails and fixed-context conflicts remain `UNKNOWN` through
the unchanged engine. Successful assembly exits 0 even for `UNKNOWN`; inspect
the assessment before interpreting a payload. A valid source file does not
establish freshness, sequence completeness, enemy AI order or map safety.

## Synthetic effort check

Two saved duels require nine guided answers: one player ID, two path/ID pairs,
one blank list terminator and three confirmations. This eliminates manual
creation of the nested player/enemies structure and repeated defender and
ruleset copying. Zero observation values are typed again and zero JSON edits
are required. Scripted transcripts verify this input count and exact equality
with the [synthetic sequence](../examples/observed_enemy_sequence.json);
they do not establish human usability or gameplay accuracy.

Read the [tactical policy](agents/local/tactical-policy.md) before live advice.
This remains a conditional calculation for the supplied distinct attackers,
with both survival guarantees withheld. Canonical tactical coverage is unchanged.
