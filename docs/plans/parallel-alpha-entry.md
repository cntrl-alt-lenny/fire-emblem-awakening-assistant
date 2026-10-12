# Parallel alpha-entry handoff — 2026-10-12

PRs 9 and 10 are merged. Baseline main:
`ec3bceca1d70a4da240a490601602e97c2466de2`.
These are the next two useful Checked batches, ready for owner relay together.
No Workers are dispatched by this planning handoff.

| Batch | Outcome | Exclusive product files |
|---|---|---|
| [15-duel-boundary](15-duel-boundary.md) | Direct duel callers cannot bypass honest unknown-state/effect refusal | tactical_combat.py; new dedicated tests/reference |
| [16-play-entry](16-play-entry.md) | One guided command starts the existing play tools | new play.py; new dedicated tests/reference |

Brain owns shared documentation, scope/API decisions, integration, review and
owner-approved main merge. Each Worker starts from recorded main in a separate
worker branch/linked checkout. Read the literal pushed plan with git show;
absence from main is not a blocker. Record actual baseline and plan hashes.

## Confirmed reason for the safety batch

Read-only synthetic probes at starting main use `examples/battle.json` and
`tactical_combat.assess`. Adding attacker alive `"?"`, alive `"false"`, forge
`{}`, or status_effects `["unknown"]` each returns POTENTIALLY_LETHAL and a
numeric outcome. The new editor blocks those inputs; direct API callers do not.
The [probe](attachments/2026-10-12-next/direct_gate_probe.py) and
[baseline output](attachments/2026-10-12-next/direct_gate_probe.log) are retained.
No run was read, initialized or changed by these probes. This is an observed
boundary gap, not a proposal to change combat formulas or expand mechanics.

## Independence and the genuine dependency

The duel CLI stays `tools/tactical_combat.py FILE`; supported output and the
public assess/known_weapon functions stay stable. The launcher delegates existing
tools and owns no shared engine. Both implementation and independent review can
therefore proceed against starting main. A planning merge, pending approval or
other review does not block either Worker.

Brain's final combined trial must use the hardened gate through the launcher,
collector and sequence engine; that acceptance gate waits for both deliveries.
The launcher may prove routing against baseline but must not claim hardened
input refusal before the combined trial. A genuine breaking contract discovery
goes to Brain; do not change another Worker's files.

## Acceptance and handoff continuity

Each delivery gets a fresh blind Verifier at a literal commit; failed attempts
and corrections remain recorded. Brain independently checks every finding,
full supported-result equality and at least ten combined CLI workflows.
No unknown-to-supported conversion, dropped effects, guessed phase/support,
spoilage, lost stdin or live-run mutation is acceptable. Full audit/framework/CI
and rendered-reference checks remain mandatory. Actual play-session usability,
complete maps/schedules, native Windows and new gameplay coverage remain separate.

Two Workers are useful here; no third occupancy batch is created. After a merge,
Brain supplies the next useful prompts or identifies the concrete missing
dependency, rather than treating merge completion as project completion.
