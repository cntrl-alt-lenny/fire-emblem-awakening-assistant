# 004-chapter17-research: Establish Hard Chapter 17 first-arrival evidence

Tier: 2
Mode: research
Supersedes: none

## Goal

Establish whether accessible, difficulty-specific evidence can resolve Hard
Chapter 17's first reinforcement staircase and warning-to-arrival relationship.
Deliver a traceable account of what the sources establish, what remains
disputed and what observations would distinguish the alternatives. An honestly
unresolved result is valid; no canonical adoption occurs in this round.

## Context

Read the project rules, full tactical policy, your role card, `docs/state.md`,
`STATUS.md`, `SOURCES.md`, `research/UNCERTAINTIES.md`,
`docs/hard-reinforcements.md`, `docs/map-coverage.md`,
`research/hard_verification/manual_audit.md`, and the Chapter 17 records in
`research/hard_verification/reviewed.json`,
`data/chapters/hard_tactics.json` and `hard_reinforcements.json`.
Inspect `tools/map_info.py` only as needed to understand current output.

Start with source IDs `hr_fandom17`, `hr_jp_17`, `p2_guide_16_2` and their
registry URLs. `p2_survey_16_2` shares a publisher/URL with the guide; duplicate
registry entries are not independent evidence. Inspect exact local section
headings rather than inheriting guide-wide difficulty assumptions.

The repository preserves eastern versus left/western first-staircase accounts.
Its Japanese summary cites a Hard-labelled 2012-04-27 warning-relative report;
indexed turns 8/9/10 remain conditional reports, not guaranteed fixed arrivals.
A separate 2014-09-06 Hard summary concerns activation of initial enemies in
the upper six rows. These are inherited summaries to investigate, not facts
to endorse. Initial activation must not become a reinforcement trigger by
association. Later excerpt rows with a lost difficulty boundary are excluded.
Do not choose either side from the existing record's confidence label.

Chapter 5 is parked pending observable gameplay evidence. The previous round
also showed why map labels, section boundaries, source families and event
phase must be checked directly. Its Brain review records a provenance erratum;
neither the Chapter 5 findings nor another chapter's reports settle this map.

## Scope and non-goals

Research the first Hard Chapter 17 arrival's staircase, timing, event phase,
warning occurrence and possible triggering conditions. Trace nearby second
and central arrivals only as needed to identify ordering or a source boundary.
Inventory reported first-wave class/count attributes without expanding to a
complete enemy roster, combat forecast or full reinforcement schedule.

Allowed changes: your report and concise supporting research artifacts under
this round's folder. A justified canonical amendment may be proposed as an
unapplied attachment with exact record/field, provenance and confidence; Brain
will review before a separate adoption round. No canonical data, source
registry, rebuild code, tools, tests, coverage counters, standing decisions,
framework, CI, licensing or player state changes are authorized.

Do not reopen Chapter 5, research the whole campaign, create or control a new
playthrough, initialize a run, acquire/extract game files, download footage
or archive full guides/game assets. Use accessible public contexts and short
factual observations. No paid access or account/settings changes are needed.

## Invariants

- `AGENTS.md` and tactical policy: Hard and other difficulties stay separate;
  null, empty and missing remain unknown. Preserve conflict, claim-level
  sources and quarantine. No full-map safety or complete schedule guarantee.
- Tactical policy: respect paywalls, authentication, challenges, robots
  restrictions and rate limits. No bypass, bulk crawl or full-page archive.
  Search-index retrieval belongs to the originating source, not a new family.
- `AGENTS.md`: tests do not certify external facts. State difficulty, mode,
  region/version, phase convention, source wording, translation and inference
  separately. Language/date do not by themselves prove region/version.
- Tactical policy: the general ordinary Hard rule does not observe this
  scripted event's phase. Warning-relative timing must not become a fixed turn
  without independent evidence. Source silence does not establish no arrivals.
- Tactical policy: distinguish initial movement, warning dialogue, new units
  appearing and those units acting. Unobserved trigger, staircase occupancy
  effect and boss-defeat censoring remain unknown.
- Framework: Worker researches; Verifier independently reviews one exact
  commit with a blind first pass; Brain re-derives and judges. Neither seat
  merges. Offline build/use stays Python 3.9+, standard library only.

## Acceptance criteria

1. Reconstruct the existing disagreement from accessible original contexts:
   exact section difficulty boundaries, table versus prose, dated comment,
   source-relative left/right/east/west and turn/phase/warning wording. Explain
   what is reported, translated or inferred. Log unavailable contexts without
   interpreting failure as agreement, contrary evidence or absent threats.
2. Make a bounded search for independent evidence specifically for Chapter 17
   Hard: normally accessible observable gameplay with setup and relevant
   phases, a scoped public controlled observation or independently authored
   firsthand report. Do not require such evidence to exist. Record the focused
   searches, inspected candidates and each exclusion's actual chapter/scope;
   check opening context before calling a candidate map-unscoped. Keep cuts,
   resets, hidden phase/setup and unavailable frames explicit.
3. Deliver a claim matrix covering first staircase, first arrival turn/phase,
   warning timing/trigger, warning-to-arrival interval, first-wave class/count,
   initial activation versus spawning, and ordering needed to compare reports.
   Rows need source IDs/URLs and locators, retrieval date, short observations,
   difficulty/mode, region/version when established, confidence, alternatives
   and limitations. Group copied/mirrored/credited reports by source family.
4. State whether any part is resolved and explain why. Distinguish ordinal
   first wave from a numbered turn and screen-relative directions from mapped
   coordinates. A warning-relative statement alone cannot establish an
   invariant fixed turn or causal trigger. Do not use different-mode/unlabelled
   tables to fill Hard gaps or certify later rows lost at a mode boundary.
5. Provide either a precise unapplied amendment supported by the evidence or
   a discriminating observation plan. Specify visible setup, phase boundaries,
   warning position/time, relevant staircase identities and conditions needed
   to distinguish hypotheses. A recording with no controlled comparison cannot
   prove a trigger; do not pretend missing matched trials exist. Recommend
   exactly one bounded next task based on the result, with unavailable inputs
   stated. No automatic adoption or campaign expansion.
6. Keep actual gameplay evidence separate from repository checks. Prove all
   canonical JSON under `data/`, `CURRENT_RUN.md` and all `state/` files are
   unchanged using file-set and SHA-256 comparisons before/after. A live run,
   if present, stays private and unchanged; never commit its contents or hashes.
   Report preservation/counts without exposing player data. No new certified
   coverage is claimed. Render artifacts and resolve changed local links.
7. Verifier independently inspects original source contexts and looks for
   contrary/insufficient evidence before opening the Worker report or results
   attachments. Record the blind findings first, then compare every material
   claim and proposed amendment at the exact Worker commit. Document failures
   to reproduce; unavailable source material remains unverified. Review the
   observation plan's ability to distinguish alternatives without implementing.

## Required evidence

At the reported full commit, paste OS/Python version, actual commands, relevant
output and exit statuses:

```sh
make audit
python3 tools/fw.py check
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase player
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 8 --phase enemy
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 9 --phase player
python3 tools/map_info.py --chapter 17 --difficulty hard --turn 10 --phase player
git diff --check
```

Record your protected-file comparison command and results, including whether
a live run exists, while respecting its privacy. No rebuild is authorized or
required: canonical data and rebuild code stay unchanged. If make is
unavailable, run every audit equivalent in `AGENTS.md` and record exit statuses.
CLI output proves present software behavior, not actual game event timing.

Source evidence includes exact URL, retrieval date, section/comment locator or
observed video timestamp, short compliant excerpt or factual summary, scope,
translation/inference and uncertainty. Titles alone do not establish visible
gameplay. Do not keep retrying a definitely denied source or collect unrelated
guides after the bounded candidate search stops producing useful evidence.

Inspect rendered research Markdown and check local links. Commit artifacts
before producing the stamped report. Push even on an early exit:
`python3 tools/fw.py report --role worker --round 004-chapter17-research --push`
(Verifier substitutes `--role verifier`). Neither seat implements or merges.
