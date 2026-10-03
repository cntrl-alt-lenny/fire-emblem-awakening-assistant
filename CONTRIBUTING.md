# Contributing

Read [AGENTS.md](AGENTS.md) before changing anything. Preserve source provenance,
difficulty separation, explicit uncertainty and the live-run event history.
Never initialize or edit a player run while testing.

## Checks

From the repository root, run `make audit`. Without make:

```sh
python3 tools/validate_data.py
python3 tools/audit_phase2.py
python3 tools/audit_hard.py
python3 -m unittest discover -s tests -v
```

Python 3.9+ on Linux/macOS and its standard library are sufficient. Native
Windows tracking uses an unavailable `fcntl` module, and some data readers
assume UTF-8; use WSL for the full toolkit until portability is reviewed.
Audit warnings describe real coverage gaps; green
checks do not certify all mechanics or a complete tactical route.

`make rebuild` regenerates canonical records from retained factual extracts
and reviewed enrichment. Review the diff and rerun `make audit` afterwards.
Never fetch sources as part of a build. Do not store whole guide prose, game
assets, credentials or personal playthrough files in this public repository.

## Agent workflow

Brain plans and reviews; Worker executes a pushed brief; Verifier reviews Tier 2
work independently. Begin with the command from your role card. Run
`python3 tools/fw.py check` alongside the audit, use `fw.py report --push` on
every Worker/Verifier exit, and leave merging to Brain after owner approval.
Framework-owned copies are pinned; put project policy in `AGENTS.md` or
`docs/agents/local/`, and use the upstream installer for updates.

## Changes and evidence

Use focused branches and pull requests. Explain the problem, the resulting
behavior, the exact checks and their output, and what remains unverified.
Canonical data and external factual claims require independent source review.
The owner chooses licensing and repository access policy.
