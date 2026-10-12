# One guided play entry

From this checkout, run:

```sh
python3 tools/play.py
```

Choose one action: current-map briefing, new duel collection, deliberate duel
draft editing, sequence assembly, assessment of a selected duel, assessment of a
selected sequence, or quit. Each invocation performs one action and exits.
Menus and context questions go to stderr. Stdout remains the existing tool's
normal text or plain JSON, suitable for redirection. The same buffered input
stream serves the launcher and delegated helper, including assistant-supplied
batched stdin. No shell command is constructed.

Map entry asks for actual chapter, difficulty, turn and phase, then discloses
Tactical spoilers as the blank-answer default. Choose No spoilers or Full
information explicitly to override it, and text, provenance or details for the
view. The [briefing](play-briefing.md) owns scope filtering, supported modes and
phase interpretation. The launcher never selects a run or guesses context.

[Collection and editing](guided-observation.md) ask for an optional new local
output before delegating. Blank means stdout only. Existing values need deliberate
reuse and a fresh overall confirmation; catalog weapons also need a fresh exact
match confirmation. The existing helper refuses overwrites and unsafe destinations.
[Sequence assembly](sequence-entry.md) retains its distinct-entity selection and
three independent confirmations. No observations, effects or unsupported fields
are rewritten to obtain numbers.

Assessments explicitly select either a duel or a sequence JSON file. Named
`current_run.json` paths, symlinks resolving to that name and hardlinks to this
checkout's standard run are refused before opening. Run-shaped JSON and selecting
the wrong observation kind are also refused. The launcher does not open a live
run or ledger, initialize an army, import state or update tracking. The selected
[duel gate](../tools/tactical_combat.py) or
[sequence engine](../tools/tactical_enemy_phase.py) owns calculations and warnings.
Exit 0 and valid JSON do not establish supported input or map safety: inspect
UNKNOWN, limitations and conditional results.

Type `cancel`, send EOF or press Ctrl-C at a launcher prompt to exit 2 without
starting an action. Invalid selections also exit 2; quit exits 0. Once delegated,
the selected helper owns cancellation, errors and its actual exit status
(the duel collector cancels with 1, sequence assembly with 2). No second action
or automatic retry follows. Redirected stdout can be empty after cancellation.

The [dedicated tests](../tests/test_play_entry.py) compare public CLI outputs and
exit codes across synthetic workflows, including complete/partial/unsupported
observations, spoilers, phase refusal, editing, sequences and protected output.
A custom duel still requires 41 observation answers; the launcher adds two
navigation answers and removes choosing the helper filename and optional output
flag. A map briefing moves four required flags, the spoiler flag and optional
view flag into seven guided answers including action selection. Two-file sequence
assembly retains nine helper answers plus two navigation answers. Assessments
replace choosing one of two helper filenames with one explicit action and a file
selection. All workflows require zero additional manual JSON edits; this launcher
does not reduce the existing helpers' observation questions.

Scripted replay and terminal-stream tests are not human UAT or gameplay proof.
Batch 15's hardened duel boundary requires a later combined acceptance trial.
No new source facts, mechanics, formulas or verified tactical coverage are added.
Read the [tactical policy](agents/local/tactical-policy.md) before live advice.
