# Parallel observed-input entry — 2026-10-12

The owner authorized easier observed-input entry and selected guided prompts
first. These two Checked batches build against the existing stable payloads;
no planning merge or other Worker review blocks starting.

| Batch | User outcome | Exclusive product ownership |
|---|---|---|
| [13-guided-observation](13-guided-observation.md) | Collect/edit a duel without hand-written nested JSON | observed_input; new dedicated tests/reference |
| [14-sequence-entry](14-sequence-entry.md) | Assemble supplied attackers from saved duel observations | sequence_input; new dedicated tests/reference |

Starting main: `5c596d42adb3d2a5eeee460032ee20bdd4bb78ba`.
Workers read the literal pushed planning commit and use separate worker branches
and linked checkouts. Brain owns integration, shared documentation and any API
question. A new shared helper is not assigned; neither imports the other's code.
Existing state/* ignore coverage protects local observation drafts. Output is
create-only in state/observations; live run/ledger writes are prohibited.

## Frozen interchange and confirmations

Default stdout is only a plain existing duel/sequence payload; prompts and
concise assessment are stderr. Thus files produced by batch13 can be consumed
by batch14, while batch14 can implement/review using existing synthetic duel
files. No new envelope, source-state import, automatic raw/effective conversion,
observed completeness or empty-effect defaults are permitted.

Unknown/blank remains unknown. Explicit none and deliberate reuse are different
from omission. A compatible existing draft is an observation, not proof it is
still current. Whole-input confirmations must be renewed. Unsupported observed
effects remain present even when engines refuse them. No actual run is started.

Selected draft/source loaders reject duplicate JSON keys and run-shaped inputs.
They never open current_run.json, including a symlink resolving to that file.
The duel gate's tolerance of an extra observation/effect field is not permission
to drop it: preserve it with refusal, or reject the incompatible input shape.

Both deliver independently with fresh blind Verifiers at exact commits. Brain's
combined end-to-end trial genuinely waits for both accepted deliveries: collect
and save synthetic duels, assemble them, compare strict results and preservation.
This release gate does not prevent either development or its own review.
Use two Workers plus pipelined Verifiers; do not invent a third occupancy batch.

## Acceptance targets

Complete a representative duel and a two-attacker sequence without manually
editing JSON. Exercise at least ten synthetic workflows spanning incomplete,
unsupported, forged, unarmed, paired, edited, cancelled and mismatched inputs.
Record prompts/steps and JSON editing eliminated; scripted success is not human
usability or gameplay validation. Require zero unknown-to-supported conversions,
no stale automatic completeness, no lost effects and no overwritten/private run.
Full audit, framework hygiene, CI, exact-source comparison and rendering remain
required. Canonical coverage remains unchanged; owner approves final merge.
