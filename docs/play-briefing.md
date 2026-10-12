# Current-map play briefing

`play_briefing.py` presents the existing [Hard/Classic query](hard-reinforcements.md)
as readable text, without initializing a run or making a deployment decision.
It uses only the offline reference; it adds no gameplay facts or verified coverage.

```sh
python3 tools/play_briefing.py --chapter 7 --difficulty hard --turn 5 --phase player
```

The selected map, current phase and target enemy phase lead the answer. Player
phase 5 targets enemy phase 5; enemy phase 5 targets enemy phase 6. Chapter 7's
fixed turn-5 candidate appears in the first case, not the second. A missing
candidate never proves no arrivals. Chapter 11's fort family remains a possible
candidate from target turn 3 onward, without predicting arrivals every turn;
its separate northwest report is fixed at target turn 4. Unknown, event,
warning-relative and repeating families follow `map_info.query` unchanged.

Every returned claim keeps its value and confidence. Repeated standard caveats
are shortened in the text view; unique notes and all conflicted notes remain
unabridged. Unknown attributes inside a supported group remain UNKNOWN.
Supported absence remains distinct from certainty. A general immediate-action
rule is applied conditionally, with map-specific scripted uncertainty visible.
No complete threat map, arrival schedule or move safety is certified.

## Evidence views

```sh
python3 tools/play_briefing.py --chapter 7 --difficulty hard --turn 5 --phase player --provenance
python3 tools/play_briefing.py --chapter 7 --difficulty hard --turn 5 --phase player --details
python3 tools/play_briefing.py --chapter 15 --difficulty hard --turn 5 --phase player --spoilers "Full information" --details
```

`--provenance` adds each claim's source IDs and restores full notes.
`--details` emits the entire spoiler-filtered query as JSON, including candidate
families, confidence, source IDs and completeness flags. Neither view bypasses
spoiler settings. Source IDs can be traced in the local [source registry](../data/sources.json)
and [source reference](../SOURCES.md).

Tactical spoilers is the default. Tactical output stays on the selected map:
references to other numbered maps in inherited caveats become “another map,”
with the caveat retained. This abridgment is disclosed in the warning.
Explicit Full information preserves the original query and its cross-map
provenance notes; it still does not query additional maps.

```sh
python3 tools/play_briefing.py --chapter 7 --difficulty hard --turn 5 --phase player --spoilers "No spoilers"
```

No spoilers emits only selected context, the current/target phases, a general
incomplete-map warning and notice that detailed material is withheld. It
contains no tactical claims, recruit/event labels or source IDs/titles, even
with `--details` or `--provenance`. It makes no map-specific threat assertion.

## Optional existing run context

```sh
python3 tools/play_briefing.py --state state/current_run.json --phase player
```

Only a deliberately selected existing JSON file is read. The default command
never opens a live run. State may supply chapter, difficulty, turn and
`spoiler_mode`; it must explicitly record Classic. This forensic reference
supports Hard/Classic only and refuses other difficulties or a Casual run.
No phase is stored by the tracker: `--phase` is required even if a selected
JSON file happens to contain a phase field. Establish the actual phase first.

Explicit chapter aliases are normalized before comparison. Chapter, difficulty
and turn must agree with known state context; mismatches fail with exit 2 and
no briefing. Missing context can be supplied explicitly. An intentional
`--spoilers` option overrides the recorded preference; an omitted option uses
that preference, then the Tactical default. Malformed or missing state and
unknown context are refused. No file is initialized, rewritten or locked.
Unit stats, inventory, deaths and history are never used or converted.

## Before and after

The baseline Chapter 7 command prints 333 JSON lines. The new default prints
27 physical text lines (363 words); terminal wrapping can increase display
lines. It retains the western three-Wyvern turn-5 report, flying hazard,
recruitment condition, conditional immediate action and all material unknowns.

```text
chapter_7 | Hard / Classic
Current: player phase 5 -> target: enemy phase 5
...
Candidate hard_chapter_7_t5 [SUPPORTED]; schedule completeness: UNKNOWN
  [SUPPORTED] location: Western map edge
...
  [UNKNOWN] coordinates: UNKNOWN
  [UNKNOWN] skills: UNKNOWN
  [UNKNOWN] suppression: UNKNOWN
```

These ellipses are documentation excerpts; the CLI never truncates claims to
meet a line budget. Chapter 17 and other complex records may exceed 30 lines
or include long lines because material disagreements and dangers take priority.
See the complete [before JSON](batches/attachments/12-play-briefing/before.json),
[after text](batches/attachments/12-play-briefing/after.txt), and
[CLI acceptance evidence](batches/attachments/12-play-briefing/acceptance.log).

Presentation and context tests protect the existing evidence boundary. They
do not establish source truth, actual event conditions, a complete reinforcement
schedule, or real play-session usability.
