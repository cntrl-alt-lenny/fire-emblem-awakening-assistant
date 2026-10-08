# Fire Emblem Awakening Assistant

Instructions for every agent working on this project. Read
[the framework](docs/agents/FRAMEWORK.md), your [role card](docs/agents/roles/),
and [standing decisions](docs/state.md). Project rules take precedence.

Merge rule: owner-approves

## What this project is

An offline factual reference, supported calculation toolkit and playthrough
tracker for Fire Emblem Awakening. Its tactical claims must expose evidence
gaps; structural tests cannot certify every mechanic or complete map safety.

## Roles

| Seat | Card | Scope |
|---|---|---|
| Brain | `docs/agents/roles/brain.md` | GPT plans batches, writes prompts, reviews evidence and merges under the merge rule. |
| Worker | `docs/agents/roles/worker.md` | The other agent does one batch on its own branch and commits its summary in `docs/batches/`; never merges. |
| Verifier | `docs/agents/roles/verifier.md` | Independently reviews a Checked batch at one exact commit; never implements or merges. |

Every session starts with `python3 tools/fw.py status`, then follows the
prompt Brain supplied. Use `py -3` or `python` if appropriate on the machine.

## Tactical and data invariants

**Read and obey [the full tactical policy](docs/agents/local/tactical-policy.md)
before gameplay advice or changes to data, mechanics, tools, tests or tactical
documentation.** It preserves the project's original instructions, including
the Hard/Classic forensic precedence, quarantined records and unsupported
combat cases. This summary does not replace it.

- Actual player reports and `state/current_run.json` are authoritative. Never
  initialize a run without the player's request, restore a dead unit without
  an explicit correction, or erase the event/history ledger. Tests use
  temporary states and must not mutate a live run.
- Keep raw permanent stats separate from effective displayed battle stats.
  Apply bonuses once. Missing stats, skills, support or weaknesses stay unknown.
- No complete reinforcement schedule or whole-map safety guarantee is
  certified. Null/empty records never mean zero/absent threats. Difficulty
  datasets stay separate. Unsupported effects are refused, never stripped.
- Preserve claim-level sources, confidence, conflicts and quarantine. The
  Hard forensic records supersede legacy Hard slots; other modes remain separate.
- Default to Tactical spoilers unless the player says otherwise. Scope answers
  to the current map; reference commands may expose more than a reply should.
- Build and use remain offline, Python 3.9+, standard library only. Respect
  source access restrictions; no bulk crawls, whole guide pages or game assets.
- This repository is public. Keep credentials, personal paths and player runs
  out of commits. Git records project decisions; local run JSON records play.

Canonical data, mechanics claims and tactical advice tooling take the
**Checked** path: Worker, then blind Verifier, then Brain review and
independent re-derivation. Brain never implements those batches itself.
Other code is Normal; notes and framework updates are Small.

## Evidence

| Changed | Required evidence |
|---|---|
| Any project change | `make audit` and `python3 tools/fw.py check` |
| Without make | Run `tools/validate_data.py`, `tools/audit_phase2.py`, `tools/audit_hard.py`, then `python3 -m unittest discover -s tests -v` |
| Canonical data or rebuild code | Also `make rebuild`, rerun audit, compare canonical hashes across two rebuilds, and prove other-mode records and run state were preserved |
| External tactical/mechanics facts | Primary-source or independently scoped evidence, exact difficulty/phase/version and remaining uncertainty; tests alone are insufficient |
| Presentation/docs only | Resolve changed local links and inspect the rendered artifact; audits check repository hygiene, not appearance or source truth |

Paste real commands, relevant output and exit status at the reviewed commit.
Update `STATUS.md` and coverage counters when tactical coverage changes;
framework-only housekeeping does not create new verified gameplay coverage.

## What is actually enforced

GitHub Actions runs data validation and regressions on Linux and macOS; the CI badge links to actual runs. Framework tests check document
hygiene and `fw.py check` caps batch summaries; neither runs the tactical
audit. The full audit remains required evidence. No local pre-push hook is installed.
Branch protection and required-check settings are not configured by this
bootstrap. Roles and owner approval are agent rules; GitHub cannot distinguish
seats using the same account. Licensing remains the owner's decision.

## Where to look

- Decisions: [docs/state.md](docs/state.md); live workflow: `tools/fw.py status`.
- Batch summaries: [docs/batches/](docs/batches/); 3.x rounds stay in [docs/rounds/](docs/rounds/) as history.
- Tactical policy: [docs/agents/local/tactical-policy.md](docs/agents/local/tactical-policy.md).
- Coverage: [STATUS.md](STATUS.md), [map coverage](docs/map-coverage.md).
- Usage: [docs/usage.md](docs/usage.md); sources: [SOURCES.md](SOURCES.md).
