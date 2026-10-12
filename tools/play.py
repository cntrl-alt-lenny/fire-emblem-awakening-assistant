#!/usr/bin/env python3
"""Choose one existing offline play tool; prompts stay on stderr."""
import json
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]


def prompt(message):
    print(message + ' [cancel stops]', file=sys.stderr, flush=True)
    line = sys.stdin.readline()
    if not line or line.strip().lower() == 'cancel':
        raise EOFError
    return line.strip()


def assessment_path(filename, kind):
    """Refuse run aliases before opening, then require the selected observation kind."""
    selected = Path(filename)
    # Resolve aliases without opening the selected file or the standard run.
    if selected.name == 'current_run.json':
        raise ValueError('Player run files cannot be assessed.')
    resolved = selected.resolve()
    live = ROOT / 'state' / 'current_run.json'
    if resolved.name == 'current_run.json' or (live.exists() and os.path.samefile(resolved, live)):
        raise ValueError('Player run files and aliases cannot be assessed.')
    # Only navigation/run boundaries live here; combat observations are never repaired.
    try:
        payload = json.loads(resolved.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        # Let the selected CLI own malformed/missing-file diagnostics and exit status.
        return filename
    required = {'attacker', 'defender'} if kind == 'duel' else {'player', 'enemies'}
    run_keys = {'roster', 'units', 'events', 'history', 'inventory', 'current_chapter',
                'chapter', 'gold', 'spoiler_mode', 'run_id'}
    if not isinstance(payload, dict) or not required <= payload.keys() or run_keys & payload.keys():
        raise ValueError('Select plain ' + kind + ' observations; run-shaped JSON is refused.')
    return filename


def selection():
    print('One action, then exit. No run is selected or changed.\n'
          '1 Current-map briefing\n2 New duel collection\n3 Deliberate duel draft editing\n'
          '4 Sequence assembly\n5 Assess selected duel\n6 Assess selected sequence\n7 Quit',
          file=sys.stderr)
    action = prompt('Action (1-7):')
    if action == '7':
        return None
    if action == '1':
        args = []
        for flag, question in (('--chapter', 'Actual current chapter:'),
                               ('--difficulty', 'Actual difficulty:'),
                               ('--turn', 'Actual current turn:'),
                               ('--phase', 'Actual current phase (player/enemy):')):
            answer = prompt(question)
            if not answer:
                raise ValueError('Actual map context is required.')
            args += [flag, answer]
        spoilers = prompt('Spoilers: No spoilers / Tactical spoilers / Full information '
                          '(blank = Tactical spoilers):') or 'Tactical spoilers'
        args += ['--spoilers', spoilers]
        view = prompt('View: text / provenance / details (blank = text):') or 'text'
        if view not in ('text', 'provenance', 'details'):
            raise ValueError('Invalid briefing view.')
        if view != 'text':
            args += ['--' + view]
        return 'play_briefing.py', args
    if action in ('2', '3', '4'):
        args = []
        if action == '3':
            filename = prompt('Existing plain duel draft path (fresh confirmation required):')
            if not filename:
                raise ValueError('A draft path is required.')
            args += ['--edit', filename]
        output = prompt('Optional new state/observations/NAME.json output (blank = stdout only):')
        if output:
            args += ['--output', output]
        return ('sequence_input.py' if action == '4' else 'observed_input.py'), args
    if action in ('5', '6'):
        kind = 'duel' if action == '5' else 'sequence'
        filename = prompt('Selected plain ' + kind + ' JSON path (read only):')
        return ('tactical_combat.py' if action == '5' else 'tactical_enemy_phase.py'), [assessment_path(filename, kind)]
    raise ValueError('Invalid action; nothing was started.')


def main():
    try:
        chosen = selection()
    except (EOFError, KeyboardInterrupt):
        print('Cancelled; no action started.', file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print('Cannot start action: ' + str(exc), file=sys.stderr)
        return 2
    if chosen is None:
        return 0
    script, args = chosen
    # Share the same TextIO stream: a subprocess/exec would lose buffered pipe answers.
    # Delegate outside the selection handler, preserving tool exits/errors verbatim.
    previous = sys.argv
    try:
        sys.argv = [str(ROOT / 'tools' / script)] + args
        runpy.run_path(sys.argv[0], run_name='__main__')
    finally:
        sys.argv = previous
    return 0


if __name__ == '__main__':
    sys.exit(main())
