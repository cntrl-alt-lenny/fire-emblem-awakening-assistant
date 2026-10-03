# 003-chapter5-research: Establish the evidence for Hard Chapter 5 arrivals

Tier: 2
Mode: research
Supersedes: none

## Goal

Establish whether accessible, difficulty-specific evidence can resolve the
conflicting Hard Chapter 5 reinforcement reports. Deliver a traceable account
of what is supported, what remains disputed and what observations would settle
the remaining questions. An honestly unresolved finding is a valid outcome.

## Context

Read the project rules, full tactical policy, your role card, `docs/state.md`,
`STATUS.md`, `SOURCES.md`, `research/UNCERTAINTIES.md`,
`docs/hard-reinforcements.md`, `research/hard_verification/manual_audit.md`,
and the Chapter 5 records in `research/hard_verification/reviewed.json`,
`data/chapters/hard_tactics.json` and `hard_reinforcements.json`. Inspect
`tools/map_info.py` only as needed to understand the current output.

The inherited `hard_chapter_5_disputed_schedule` preserves alternatives rather
than selecting a schedule. The stored western report separates foot arrivals,
northwestern Wyverns and a mixed group across turns 3/4/5; an explicitly Hard
Japanese observation describes a different turn-3 mixture and a tentative
turn-5 group. The western table/prose also disagree about one class. These are
repository summaries to investigate, not instructions to endorse either side.
Region differences, phase conventions, transcription errors and difficulty
conflation are hypotheses, not established explanations.

Start from source IDs `reinforcements_early_0`, `hr_jp_5`, `p2_guide_04_2`
and their registry URLs/applicability. A separate Lunatic table can establish
only what that source says about Lunatic; it cannot supply missing Hard values.
The general ordinary Hard arrival rule does not observe this map's event phase.

Rounds 001/002 audited the foundation and repaired live combat input handling.
This round returns to factual research; no full reinforcement schedule or
safe route was certified by those rounds.

## Scope and non-goals

Research Hard Chapter 5 reinforcement turns, phase, unit classes/counts,
spawn areas, activation conditions and any reported suppression. Separate
initial enemies moving from actual new arrivals. Inspect adjacent mechanics
or other difficulties only when necessary to identify a source boundary or
explain a possible conflation, clearly labeling the comparison.

Allowed changes: report and concise supporting research artifacts under this
round's folder. Include proposed canonical amendments, if justified, as an
attachment with precise source IDs/confidence; do not apply them here. Brain
will review evidence before authorizing a separate canonical-data adoption.

Do not modify canonical data, source registry, rebuild code, tools, tests,
coverage counters, instructions, framework, CI, licensing or player state.
Do not research Chapter 17 or the whole campaign, expand mechanics, initialize
a run, or acquire/extract game files. Do not archive full guides, footage or
game assets. Record URLs, timestamps and short factual observations instead.

## Invariants

- `AGENTS.md` and tactical policy: difficulties remain separate; missing,
  null and empty records are unknown, not absence. Preserve conflicts,
  provenance and quarantine; no complete-map survival guarantee.
- Tactical policy: maintain source access restrictions. No bypass of paywalls,
  authentication, challenges, robots restrictions or rate limits; no bulk
  crawl, full-guide archive or unsupported inference from a search snippet.
- `AGENTS.md`: source agreement can reflect copying. Claims require scoped
  evidence beyond structural tests; record difficulty, phase convention,
  region/version and remaining uncertainty separately.
- Tactical policy: generic Hard timing does not certify a scripted event's
  phase. Do not invent a grace turn, last wave or effective fort-blocking rule.
- Framework: Worker researches; Verifier independently reviews at one exact
  commit, blind first pass; Brain re-derives and judges. Neither seat merges.
- Project rules: offline use/build remains Python 3.9+, standard library only;
  research retrieval may use accessible sources, but the delivered artifacts
  introduce no runtime network requirement or live-run mutation.

## Acceptance criteria

1. Reconstruct the exact existing disagreement from accessible original
   source contexts. Identify table versus prose, section difficulty boundaries,
   dated observations and turn/phase wording. Distinguish the site's words,
   your translation and your inference. Log unavailable sources without
   treating access failure as contradictory evidence or absence.
2. Make a bounded attempt to obtain independent, preferably game-derived
   evidence specifically for this map: a clearly Hard-labelled recorded
   playthrough with observable setup and relevant arrival phases, a scoped
   controlled observation already publicly available, or an independently
   authored firsthand report. Do not require a new source to exist. Record
   why each inspected candidate can or cannot support a claim, including
   missing difficulty, cuts, resets, mode, region/version and missing turns.
3. Deliver a claim-by-claim matrix for timing, phase, unit group, location,
   trigger and suppression. Each row has source IDs/URLs, short factual
   observations or compliant excerpts, difficulty, mode if established,
   region/version if established, confidence, alternatives and limitations.
   Keep unknown attributes unknown even when another attribute is supported.
   Group copied/mirrored/credited material by evidence family.
4. State whether the evidence resolves any part of the conflict, and why.
   Different descriptions need not represent the same event. Do not select
   a complete schedule from one observed wave or convert source silence into
   proof of no further arrivals. Explain tactical implications only for
   Chapter 5 and with the required uncertainty, not as a guaranteed route.
5. If justified, provide a proposed, unapplied canonical amendment specifying
   the exact record/fields, provenance, confidence and retained conflict.
   Otherwise provide a precise follow-up observation plan: which turns/phases,
   difficulty/region and trigger conditions must be visible to distinguish
   the alternatives. Recommend exactly one bounded next task based on the
   results, rather than automatically proceeding to campaign expansion.
6. Reports distinguish external factual evidence from passed repository
   checks. No new certified gameplay coverage or canonical changes are
   claimed. Prove canonical JSON, current-run pointer and all state files
   preserved by file-set/SHA-256 comparison; tests use temporary state.
7. Verifier independently inspects original source contexts and searches for
   contrary or insufficient evidence before opening the Worker report or
   results attachments. Then compare every material research claim, recording
   failures to reproduce and unsupported leaps as findings. An unavailable
   source is unverified, never assumed to agree.

## Required evidence

At the reported full commit, paste OS/Python version, actual commands,
relevant output and exit statuses:

```sh
make audit
python3 tools/fw.py check
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase player
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 3 --phase enemy
python3 tools/map_info.py --chapter 5 --difficulty hard --turn 5 --phase player
git diff --check
```

Record the protected-file hash/file-set comparison command and results,
including whether any live run exists. No rebuild is required or authorized:
canonical data and rebuild code stay unchanged. If make is unavailable, run
the audit equivalents in `AGENTS.md` and record each exit status.

Source evidence must include retrieval date, exact URL, section/comment date
or video timestamp, short compliant excerpt or factual summary, applicability,
translation/inference where relevant and limitations. Record focused search
attempts and access failures; do not save whole pages. Existing CLI output is
evidence of current behavior, not proof of the game's actual schedule.

Inspect rendered research Markdown and resolve any local links. Commit
artifacts before producing the framework-stamped report, and push even on an
early exit:
`python3 tools/fw.py report --role worker --round 003-chapter5-research --push`
(Verifier substitutes `--role verifier`). Neither seat implements or merges.
