# 006-chapter20-objective: Establish Chapter 20 victory-condition evidence

Tier: 2
Mode: research
Supersedes: none

## Goal

Establish whether accessible, properly scoped evidence can resolve the Hard
Chapter 20 victory-condition disagreement: defeating Walhart versus defeating
every boss. Distinguish displayed objective, observed completion condition and
strategy wording. Deliver a traceable conclusion or an explicit unresolved
result, with any canonical amendment proposed but unapplied.

## Context

Read `AGENTS.md`, the full tactical policy, your role card, `docs/state.md`,
`STATUS.md`, `SOURCES.md`, `research/UNCERTAINTIES.md`,
`docs/hard-reinforcements.md` and `docs/map-coverage.md`.
Inspect only the relevant Chapter 20 portions of
`research/hard_verification/manual_audit.md`, `author_review.py`,
`reviewed.json`, `data/chapters/chapters.json`, `hard_tactics.json` and
`hard_reinforcements.json`, plus their source registry entries. Trace the
catalog and guide extraction/history as needed; inspect `tools/map_info.py`
to understand how the current conflict is exposed.

The stored objective is CONFLICTED. Its catalog value says `Defeat Walhart`;
the conflict summary attributes `Defeat every boss` to the guide. These are
inherited summaries to investigate, not facts to endorse. The guide record
lists Cervantes, Excellus and Walhart; a boss list alone does not establish
that all are required for completion. Determine whether the disputed wording
occurs in objective metadata, strategy, a scoped section or extraction error.

Start with registry IDs `chapter_catalog` and `p2_guide_20_1` and their exact
URLs. Repeated guide extracts, mirrors or registry IDs are one source family.
Read local difficulty headings; a guide-wide Hard default cannot override an
explicit local scope. Seek independently authored, normally accessible
Chapter 20 evidence only as needed to judge this particular objective.

Chapter 5/17 actual gameplay disputes remain parked pending observable
evidence. The [round 005 Brain review](../005-chapter17-provenance/attachments/brain-review.md)
records why narrowing attribution is different from resolving gameplay. Its
conclusions do not settle Chapter 20.

## Scope and non-goals

Research Chapter 20's displayed objective and actual map-ending condition.
Assess whether defeating Walhart can end the map while another named boss
remains alive, and whether credible evidence instead requires multiple bosses.
An unresolved outcome is acceptable. Research adjacent details only to
establish the observation's setup and completion sequence.

Allowed changes: Worker/Verifier reports and concise research attachments
under this round's folder. A proposed amendment must name the exact existing
record/field, sources, confidence, limitations and any affected duplicate
claims; leave it unapplied for a separate reviewed adoption round.

No canonical/source-registry/rebuild/tool/test/coverage/standing-decision
changes. Do not research reinforcement warning timing, the complete map,
other chapters or combat outcomes. No new playthrough, run initialization,
game-file acquisition/extraction, downloaded footage, full-guide archives,
framework/CI/license/settings changes or safety guarantee. Keep lookup bounded
to original contexts and a small set of directly relevant independent leads;
log a stopping point when searches stop adding useful evidence.

## Invariants

- `AGENTS.md` and tactical policy: difficulties stay separate. Unknown and
  source silence never mean absent threats. Preserve conflict, claim-level
  provenance and quarantine; no complete schedule or whole-map safety claim.
- Tactical policy: displayed objective, guide shorthand and actual completion
  behavior are different evidence. Do not infer a boss requirement from a
  boss table, or declare a catalog value correct merely because it is stored.
- `AGENTS.md`: external facts require scoped evidence, not passing tests.
  Record difficulty/mode, phase, region/version where established; language,
  date and title alone do not establish setup or regional equivalence.
- Tactical policy: respect robots restrictions, challenges, authentication,
  paywalls and rate limits. No bypass, bulk crawl or full-prose/asset archive.
  Indexed retrieval is attributed to its original family and limited context.
- `AGENTS.md`: preserve `CURRENT_RUN.md` and every local `state/` file;
  actual player state remains private. Never publish player contents/hashes.
- Framework: Worker researches; a fresh Verifier independently checks sources
  before Worker conclusions, then reviews one exact commit; Brain re-derives
  and judges. Neither seat merges. Offline use remains Python 3.9+ and stdlib.

## Acceptance criteria

1. Trace both existing objective summaries to their recoverable source and
   extraction context. Provide exact URL, local heading/row/paragraph locator,
   retrieval date, source family and difficulty scope. Distinguish quoted
   wording, translation, interpretation and historical repository assertions.
   Record unavailable contexts without treating failed access as agreement.
2. Build a concise claim matrix for displayed objective, Walhart-alone
   completion, any all-boss requirement and difficulty/version/mode limits.
   Each row needs short observations, locators, confidence, alternatives and
   gaps. Copied summaries cannot provide independent corroboration.
3. Seek a bounded independent source or observable gameplay sequence relevant
   to the disagreement. For footage, visible Chapter 20 Hard setup and the
   relevant completion transition matter; a title alone is insufficient.
   Record timestamps and what is actually visible. If all other bosses are
   already defeated, completing after Walhart does not distinguish the two
   hypotheses. Cuts, resets and hidden boss status remain explicit limitations.
   Do not require suitable footage to exist or download it.
4. State whether the evidence resolves source attribution only, supports a
   displayed objective, establishes completion behavior, or leaves the dispute
   unresolved. Do not promote one into another. Supply either a precise
   unapplied amendment or a discriminating observation plan with required
   visible setup, remaining-boss state, completion transition and limitations.
5. Prove canonical `data/` JSON file-set/content preservation before/after,
   including other-mode records, and separately prove private run file-set/
   content preservation. Report counts/results and live-run presence only.
   Current CLI must still expose Chapter 20's conflict and incomplete coverage.
   No new verified gameplay coverage results from this research-only delivery.
6. Verifier starts in a fresh session and records a blind source/baseline pass
   before opening Worker results or comparison attachments. Inspect contrary
   or insufficient evidence independently, then compare every material claim
   and proposed amendment at the exact Worker commit. Reproduce required
   checks and preservation comparisons without implementing changes.
7. Render research Markdown and resolve local links. Recommend exactly one
   bounded next task based on the findings, naming any unavailable input.
   Record the model/reasoning/speed settings used if known; label owner-reported
   settings as such rather than claiming to inspect unavailable configuration.
   Follow the evidence requirements regardless of model or speed setting.

## Required evidence

At the reported full commit, paste OS/Python version, real commands, relevant
output and exit statuses:

```sh
make audit
python3 tools/fw.py check
python3 tools/map_info.py --chapter 20 --difficulty hard
python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase player
python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase enemy
git diff --check
```

Record preservation comparison commands/results from your pre-work baseline,
including canonical file sets/SHA-256 equality and private run preservation.
Keep private digests outside public attachments. No rebuild is authorized:
canonical records and generation remain unchanged. If make is unavailable,
run every audit equivalent in `AGENTS.md` and record each exit status.
CLI output establishes repository behavior, not actual victory conditions.

External evidence needs precise locators/timestamps, short compliant excerpts
or observations, scope, translations/inferences and uncertainty. Do not retry
definitely denied sources. Missing observation input is a valid research
limitation, not permission to invent a result or weaken review.

Commit artifacts before producing the stamped report. Push even on an early
exit: `python3 tools/fw.py report --role worker --round 006-chapter20-objective --push`
(Verifier substitutes `--role verifier`). Neither seat implements or merges.
