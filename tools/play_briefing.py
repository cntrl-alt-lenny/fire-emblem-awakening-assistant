#!/usr/bin/env python3
"""Read-only, current-map Hard/Classic evidence briefing (offline)."""
import argparse
import copy
import json
import re
from pathlib import Path

import map_info

SPOILERS = ('No spoilers', 'Tactical spoilers', 'Full information')
GENERAL_WARNING = ('Map and schedule evidence is incomplete. No empty result '
                   'or modeled outcome establishes whole-map safety.')
# Only exact, repeated boilerplate is abridged. Unrecognized notes, including
# conflicts and special event boundaries, are printed in full without a cap.
# The details view always retains original notes (subject to spoiler scope).
NOTE_SUMMARIES = {
    'Campaign objective catalog compared against Hard-default guide; verify displayed objective before declaring completion.':
        'Verify displayed objective before declaring completion.',
    'Pre-battle limit including Chrom; automatic NPC/allied arrivals are additional. Early chapters without preparation use initial army size.':
        'Includes Chrom; automatic arrivals additional. Without preparation: initial army size.',
    'Hard-default guide metadata; exact displayed stats and equipped skill rolls remain unknown. Weapon names do not establish proc skills.':
        'Exact stats/skills unknown; weapon names do not establish procs.',
    'Recruitment system conditions checked against current Hard reference. Unit must survive to retain recruit in Classic.':
        'Recruit must survive for retention in Classic.',
    'Exact Hard starting tiles not established; consult observed map.':
        'Starting tiles unknown; observe map.',
    'No complete Hard enemy roster, starting coordinates, numerical stats, enemy forges or random skill rolls certified. Observe actual enemies; Lunatic templates cannot substitute.':
        'Roster/positions/stats/forges/skills incomplete; observe enemies, never substitute Lunatic templates.',
    'World-map shops are separate; full in-map shop/event inventory not established.':
        'World-map shops separate; in-map shop/event inventory incomplete.',
    'Complete schedule not established. No matching fixed-turn wave does NOT mean no spawn. Conditional and unknown-time families are always retained as possible.':
        'Schedule incomplete; no fixed match is not no spawn. Conditional/unknown-time families remain possible.',
    'Exact positions, all enemy stats/equipment/skills and event boundaries are not complete. No empty list or zero modeled death chance certifies a move without observed inputs.':
        'Positions/stats/equipment/skills/events incomplete; empty results or zero modeled risk do not certify a move.',
    'Exact turn/count/equipment single indexed Hard subsection; western arrival corroborated by guide. Not a certified complete schedule.':
        'Turn/count/equipment single indexed Hard source; west corroborated. Schedule incomplete.',
    'Support applies to the supplied attributes only. Null class/count/equipment/level/location remains UNKNOWN, never absent. Skill rolls and exact enemy forge stats are not established.':
        'Only listed attributes supported; nulls UNKNOWN, never absent. Skills/exact forges unestablished.',
    'Ordinary Hard rule applied; map-specific scripted exceptions have not all been excluded.':
        'Rule applied conditionally; scripted exceptions not excluded.',
    'Conditional application of VERIFIED ordinary Hard rule: if this is an ordinary beginning-enemy-phase arrival it can move/attack and kill immediately. This wave was not independently observed; scripted phase/exception uncertainty remains.':
        'VERIFIED rule, conditional application: ordinary EP-beginning arrivals act/kill immediately. Wave not independently observed; scripted phase/exceptions uncertain.',
}


def _state_context(path):
    """Read only explicitly selected context; never inspect unit stats/history."""
    try:
        run = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('Cannot read selected state as UTF-8 JSON') from exc
    if not isinstance(run, dict):
        raise ValueError('Selected state must be a JSON object')
    if run.get('mode') != 'Classic':
        raise ValueError('Selected state must explicitly use Classic; this reference is Hard/Classic only')
    return {key: run.get(key) for key in ('chapter', 'difficulty', 'turn', 'spoiler_mode')}


def _chapter_id(chapter):
    if type(chapter) not in (str, int) or not str(chapter).strip():
        raise ValueError('Supply a known chapter')
    return map_info.resolve(chapter, map_info.load()[0])['chapter_id']


def _difficulty(value):
    if not isinstance(value, str) or value.lower() != 'hard':
        raise ValueError('This reference supports Hard only; other difficulties require separate datasets')
    return 'hard'


def _turn(value):
    if type(value) is not int or value < 1:
        raise ValueError('Supply a positive integer turn')
    return value


def _selected(explicit, recorded, name, validate):
    chosen = validate(explicit) if explicit is not None else None
    stored = validate(recorded) if recorded is not None else None
    if chosen is not None and stored is not None and chosen != stored:
        raise ValueError('Explicit ' + name + ' does not match selected state')
    if chosen is None and stored is None:
        raise ValueError('Supply ' + name + ' explicitly or in selected state')
    return chosen if chosen is not None else stored


def _scope(value, chapter_id):
    """Hide cross-map references in a current-map tactical reply, recursively."""
    if isinstance(value, str):
        def replace(match):
            kind = 'chapter' if match.group(1).lower().startswith('chapter') else 'paralogue'
            return match.group(0) if kind + '_' + str(int(match.group(2))) == chapter_id else 'another map'
        return re.sub(r'\b(chapter|paralogue)[ _]*(\d+)\b', replace, value, flags=re.I)
    if isinstance(value, list):
        return [_scope(item, chapter_id) for item in value]
    if isinstance(value, dict):
        return {key: _scope(item, chapter_id) for key, item in value.items()}
    return value


def briefing(chapter=None, difficulty=None, turn=None, phase=None, spoilers=None, state=None):
    """Return a spoiler-filtered query copy; state is an opt-in path, never a default."""
    context = _state_context(state) if state is not None else {}
    chapter = _selected(chapter, context.get('chapter'), 'chapter', _chapter_id)
    difficulty = _selected(difficulty, context.get('difficulty'), 'difficulty', _difficulty)
    turn = _selected(turn, context.get('turn'), 'turn', _turn)
    if phase not in ('player', 'enemy'):
        raise ValueError('Supply current phase player or enemy; selected state does not establish phase')
    recorded_spoilers = context.get('spoiler_mode')
    if recorded_spoilers is not None and recorded_spoilers not in SPOILERS:
        raise ValueError('Selected state has an invalid spoiler mode')
    # An intentional explicit preference overrides the stored preference.
    spoilers = spoilers if spoilers is not None else recorded_spoilers or 'Tactical spoilers'
    if spoilers not in SPOILERS:
        raise ValueError('Invalid spoiler mode')
    result = copy.deepcopy(map_info.query(chapter, difficulty, turn, phase, spoilers))
    if spoilers == 'No spoilers':
        # Even the underlying warning contains a tactical rule: do not print it.
        result.pop('map_confidence', None)
        result['warning'] = GENERAL_WARNING + ' Detailed material withheld under No spoilers.'
    elif spoilers == 'Tactical spoilers':
        result = _scope(result, chapter)
        result['warning'] += ' Tactical view abridges other-map references; Full information retains the original reference.'
    return result


def _value(value):
    if value is None:
        return 'UNKNOWN'
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    if isinstance(value, dict):
        return '; '.join(str(key) + ': ' + _value(item) for key, item in value.items()) or '(empty record; not absence)'
    if isinstance(value, list):
        return ' / '.join(_value(item) for item in value) or '(empty list; not absence)'
    # Keep one physical line per claim; no limit or truncation of unique dangers.
    return ' '.join(str(value).split())


def _claim(claim, provenance):
    line = '  [' + claim['confidence'] + '] ' + claim['label'] + ': ' + _value(claim['value'])
    if claim.get('notes'):
        note = claim['notes']
        if not provenance and claim['confidence'] != 'CONFLICTED':
            note = NOTE_SUMMARIES.get(note, note)
        line += ' — ' + _value(note)
    if provenance:
        line += ' [sources: ' + (', '.join(claim.get('source_ids', [])) or 'none recorded') + ']'
    return line


def render(result, provenance=False):
    """Render all returned claims; confidence remains attached to each attribute."""
    lines = [result['chapter_id'] + ' | ' + result['difficulty'] + ' / ' + result['mode'],
             'Current: ' + str(result['current_phase']) + ' phase ' + str(result['current_turn']) +
             ' -> target: enemy phase ' + str(result['target_enemy_phase_turn']),
             result['warning']]
    if 'candidate_reinforcements' not in result:
        return '\n'.join(lines) + '\n'
    lines.append('Map completeness: ' + result['map_confidence'] + '; complete schedule: no; move safety certified: no.')
    lines.append('Candidates are reports, not predictions that an event condition is satisfied.')
    lines.append('Arrival status: ' + result['reinforcement_status'] +
                 '; absence reasonably supported: ' + _value(result['absence_reasonably_supported']) +
                 '; absence certain: ' + _value(result['safe_to_conclude_no_reinforcements']))
    claims = result['known_verified_supported'] + result['uncertain_partial_conflicted_unknown']
    lines.append('Current-map facts, hazards and uncertainty:')
    for claim in claims:
        if claim['kind'] != 'reinforcement':
            # Include kind so numbered hazard/conflict labels remain meaningful.
            labelled = dict(claim, label=claim['kind'] + ' / ' + claim['label'])
            lines.append(_claim(labelled, provenance))
    if not result['candidate_reinforcements']:
        lines.append('No matching candidate records; this does not establish no arrivals.')
    for wave in result['candidate_reinforcements']:
        lines.append('Candidate ' + wave['id'] + ' [' + wave['confidence'] +
                     ']; schedule completeness: ' + wave['schedule_completeness'])
        for claim in claims:
            if claim['kind'] == 'reinforcement' and claim['label'].startswith(wave['id'] + ':'):
                labelled = dict(claim, label=claim['label'][len(wave['id']) + 1:])
                lines.append(_claim(labelled, provenance))
    lines.append('Use --provenance for claim source IDs; --details for the full spoiler-filtered query.')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter')
    parser.add_argument('--difficulty')
    parser.add_argument('--turn', type=int)
    parser.add_argument('--phase', choices=['player', 'enemy'])
    parser.add_argument('--spoilers', choices=SPOILERS)
    parser.add_argument('--state', help='Explicit existing JSON state; context only, read-only')
    view = parser.add_mutually_exclusive_group()
    view.add_argument('--provenance', action='store_true')
    view.add_argument('--details', action='store_true', help='Full spoiler-filtered query JSON')
    args = parser.parse_args()
    try:
        result = briefing(args.chapter, args.difficulty, args.turn, args.phase, args.spoilers, args.state)
    except ValueError as exc:
        parser.exit(2, str(exc) + '\n')
    if args.details:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result, args.provenance), end='')


if __name__ == '__main__':
    main()
