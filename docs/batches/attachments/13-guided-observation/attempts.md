# Attempts retained

Before the first implementation commit, focused tests exited 1:

```text
python3 -m unittest discover -s tests -p 'test_observed_input.py' -v
FAIL: test_complete_public_transcript_and_gate_equality
AssertionError: 39 != 40
Ran 12 tests in 0.525s
FAILED (failures=1)
exit: 1
```

The assertion counted 40 prompts but the initial custom flow had 39. Brain's
interchange inspection also identified the missing explicit weapon required-rank
prompt. Adding it on both sides brought the final measured count to 41; the
focused test now measures that count and checks existing sequence compatibility.
An explicitly unequipped edited draft now separately renews its supplied weapon
state; exact preservation is tested.

The first workflow capture completed its Python runner, but the surrounding zsh
wrapper attempted to assign the reserved read-only `status` variable:

```text
zsh:139: read-only variable: status
exit: 1
```

The workflow capture was rerun using `fea13_exit`; the final log contains its
actual exit. Initial exploratory lookups used absent guessed filenames
(`test_tactical_combat.py`, `input_shapes.py`, `observed_sequence.py`,
`observed_enemy_phase.py`) and exited 1/2; repository file search located the
actual `test_combat_gate.py`, `tactical_combat.py` and `tactical_enemy_phase.py`.
No source/private file was modified by these unsuccessful lookups.
