# 007-chapter20-evidence: Correct Chapter 20 evidence strength and provenance

Tier: 2
Mode: documentation
Supersedes: 006-chapter20-objective because the research assessment overstates unestablished source independence and its observation plan assumes a settings display.

## Goal

Deliver a traceable, conservatively scoped Chapter 20 research assessment that
distinguishes recoverable source wording, source dependency, reported play and
visible gameplay evidence. Correct the round 006 artifact without resolving
the canonical conflict or claiming new gameplay coverage.

## Context

Read `AGENTS.md`, the full tactical policy, your role card, `docs/state.md`,
relevant Chapter 20 parts of `STATUS.md`, `SOURCES.md`,
`research/UNCERTAINTIES.md`, `docs/hard-reinforcements.md`,
`docs/map-coverage.md`, and the canonical Chapter 20 records.
The round 006 brief supplies the original bounded question and source URLs.

Worker then reads round 006's reports, `attachments/objective-evidence.md` and
[Brain review](../006-chapter20-objective/attachments/brain-review.md).
The delivered research was rejected for its asserted source independence,
not because the absence of gameplay footage makes an unresolved result invalid.
Brain recovered the disputed MK completion sentence through indexed retrieval;
the correction must not label that sentence false simply because an earlier
Verifier could not access it. Direct access restrictions remain in force.

Verifier: before opening the round 007 Worker report, changed evidence
attachment, or round 006 reports/Brain review, independently inspect the
baseline records and bounded original source contexts. Record the blind pass
in a private temporary note. You may read the round 006 brief for URLs and
scope. Inspect the attachment diff only after that independent source pass;
then compare all material changes and earlier findings at one exact Worker
commit. Do not require a particular external conclusion to match Brain.

## Scope and non-goals

Worker may amend only round 006's `attachments/objective-evidence.md` and add
concise correction/evidence attachments under round 007, plus the new Worker
report. Mark the attachment's correction date and point to this superseding
round. Preserve round 006's stamped reports, original brief and Brain review.
Verifier writes only `docs/rounds/007-chapter20-evidence/verifier.md`.

No canonical data, registry, rebuild, tools, tests, coverage, `STATUS.md`,
standing decisions, framework, CI, settings or license changes. No other-map
research, reinforcement timing work, playthrough initialization, save/game
operations, game-file acquisition, downloaded footage or full-page archives.
Bounded reads may clarify existing Chapter 20 evidence and the specific
MK/Gamer Guides dependency lead. No broad new source hunt or assumption that
more guides will resolve gameplay. Suitable capture is not a prerequisite
for this correction; missing observation stays explicit.

## Invariants

- `AGENTS.md` and tactical policy: keep difficulties and versions separate;
  metadata and strategy do not establish an observed Hard/Classic transition.
  Preserve canonical conflict, source uncertainty, quarantine, incomplete
  schedules and zero new verified gameplay coverage.
- Source IDs, sites, languages and different named authors do not alone prove
  independent derivation. Wording overlap is a dependency lead, not proof of
  copying. An unresolved dependency is an acceptable stated result.
- Respect access restrictions. Do not retry definitely denied direct URLs,
  change routes to bypass restrictions, crawl broadly or archive guide prose.
  Existing indexed excerpts keep their original source family and limitations.
- Preserve `CURRENT_RUN.md` and every `state/` file. Keep private digests and
  contents out of public reports. Never reconstruct unavailable historical
  preservation or rendering evidence as though it was performed.
- Framework: Worker corrects, fresh Verifier reviews blindly, Brain re-derives
  at the exact delivered commit, and the owner controls merge approval.

## Acceptance criteria

1. Each retained source assertion has an exact URL, durable local heading or
   row/footnote locator, retrieval date and route (direct, indexed, or inherited
   unreproduced report), source family, difficulty/mode/version scope and gaps.
   Distinguish a quote actually recovered from a historical quote not recovered.
   Index snippets from other chapter sections cannot supply Chapter 20 context.
2. Audit all independence language, including the source trace, matrix,
   assessment and stopping-point narrative. Either substantiate source lineage
   with bounded recoverable evidence or explicitly leave independence unknown
   and remove the corresponding independent-corroboration claim. Document the
   MK/Gamer Guides overlap lead without asserting copying from similarity.
   Apply the same standard to other retained editorial contributions.
3. Assess the MK completion sentence neutrally: retain with supported local
   scope and retrieval limitations if recovered, otherwise label its exact
   wording unverified. Do not infer Walhart-alone completion merely from boss
   order or the condition metadata. A player report with unknown difficulty
   remains a reported observation, never verified Hard/Classic behavior.
4. Clearly separate original objective attribution from game-displayed
   objective and actual completion. Retain the unresolved gameplay result;
   do not amend canonical confidence or count this as gameplay verification.
5. Revise the single next observation task so Hard/Classic settings are visibly
   tied to the same save via a display that actually exposes them. Do not
   assume the preparation screen contains those settings. Require displayed
   objective, both Cervantes and Excellus alive through Walhart's defeat and
   continuous completion transition. Keep cuts, resets, hidden boss state and
   unknown region/version explicit. No capture or game operation is authorized
   in this correction round.
6. Preserve original stamped reports as historical evidence. A concise
   correction record maps each material finding to its disposition and states
   that new checks cannot recreate missing old private snapshots/rendering.
   Capture fresh preservation evidence for this round including CURRENT_RUN.
7. At the exact delivery, required checks pass, CLI still exposes the Chapter
   20 conflict and incomplete coverage, data JSON file sets/content including
   other-mode records are identical, and private file sets/content are preserved.
   Render and visually inspect changed Markdown and resolve local links.
8. Fresh Verifier records blind source/baseline work before comparison, judges
   every material retained claim and correction independently, and reruns checks
   and preservation comparisons. Report known model/settings honestly; unknown
   configuration remains unknown. Verifier commits only its report.

## Required evidence

At the reported full commit, provide actual OS/Python version, commands,
relevant outputs and exit statuses:

```sh
make audit
python3 tools/fw.py check
python3 tools/map_info.py --chapter 20 --difficulty hard
python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase player
python3 tools/map_info.py --chapter 20 --difficulty hard --turn 6 --phase enemy
git diff --check
```

Before work/checks, privately snapshot sorted `data/**/*.json` and separately
`CURRENT_RUN.md` plus every regular `state/` file; compare file sets and
SHA-256 content after work/checks. Report counts, equality and live-run presence
only. Compare data JSON sets/content with the round's starting commit and
`origin/main` to detect inherited or newly introduced changes. No rebuild is
authorized. If make is unavailable, run every equivalent in `AGENTS.md` and
record all exit statuses.

Record bounded source retrievals, locators, compliant short excerpts or
observations, inferred dependency limits, render command/result and visual
inspection, local-link results and blind-pass ordering. Repository tests do
not establish source truth. Commit Worker artifacts before stamping its report;
do not claim checks of uncommitted edits as checks of a full reported commit.

Finish even if blocked with:
`python3 tools/fw.py report --role worker --round 007-chapter20-evidence --push`.
Verifier substitutes `--role verifier`. Neither seat accepts or merges.
