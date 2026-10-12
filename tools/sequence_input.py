#!/usr/bin/env python3
"""Assemble selected plain observed duels into the existing sequence contract."""
import argparse
import copy
import json
import os
from pathlib import Path
import sys

from tactical_enemy_phase import evaluate

ROOT = Path(__file__).resolve().parents[1]
RULES = {'difficulty': 'Hard', 'mode': 'Classic', 'stats_basis': 'effective_displayed'}
SHARED = ('difficulty', 'mode', 'stats_basis', 'support_state', 'partners')
DUEL_KEYS = set(SHARED) | {'observed_inputs_complete', 'attacker', 'defender', 'context', 'note'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON object key: ' + key)
        result[key] = value
    return result


def source_path(filename):
    selected = Path(filename)
    path = selected.resolve()
    if selected.name == 'current_run.json' or path.name == 'current_run.json':
        raise ValueError('live run files are not duel observations')
    live = ROOT / 'state' / 'current_run.json'
    if live.exists() and path.samefile(live):
        raise ValueError('live run file aliases are not duel observations')
    return path


def read_duel(filename):
    path = source_path(filename)
    with path.open(encoding='utf-8') as stream:
        return json.load(stream, object_pairs_hook=unique_object,
                         parse_constant=lambda value: invalid_constant(value))


def invalid_constant(value):
    raise ValueError('non-JSON numeric constant: ' + value)


def difference(left, right, path):
    """Type-sensitive first mismatch; missing and null are distinct observations."""
    if type(left) is not type(right):
        return path
    if type(left) is dict:
        for key in sorted(set(left) | set(right)):
            child = path + '.' + key
            if key not in left or key not in right:
                return child
            mismatch = difference(left[key], right[key], child)
            if mismatch:
                return mismatch
    elif type(left) is list:
        if len(left) != len(right):
            return path
        for index, (a, b) in enumerate(zip(left, right)):
            mismatch = difference(a, b, path + '[' + str(index) + ']')
            if mismatch:
                return mismatch
    elif left != right:
        return path
    return None


def entity_id(value, path):
    if type(value) is not str or not value.strip() or value != value.strip():
        raise ValueError(path + ': requires a nonempty entity ID without outer whitespace')


def assemble(player_id, selected, confirm_order=False, confirm_unchanged=False,
             confirm_no_events=False):
    """Copy observations verbatim; refuse conflicts, never repair or infer them."""
    entity_id(player_id, 'player_id')
    if not selected:
        raise ValueError('enemies: select at least one duel')
    seen = {player_id}
    first = None
    entries = []
    complete = all(flag is True for flag in
                   (confirm_order, confirm_unchanged, confirm_no_events))
    for index, (identity, source) in enumerate(selected):
        path = 'entries[' + str(index) + ']'
        entity_id(identity, path + '.id')
        if identity in seen:
            raise ValueError(path + '.id: repeated entity or player identity')
        seen.add(identity)
        if type(source) is not dict:
            raise ValueError(path + ': requires a plain duel object')
        extras = set(source) - DUEL_KEYS
        if extras:
            raise ValueError(path + ': unsupported duel fields: ' + ', '.join(sorted(extras)))
        if 'note' in source and type(source['note']) is not str:
            raise ValueError(path + '.note: only a nonmechanical text comment is supported')
        for field, required in RULES.items():
            if source.get(field) != required:
                raise ValueError(path + '.' + field + ': requires explicit ' + required)
        # No absence is converted to {} or filled from another file.
        for field in ('attacker', 'defender', 'context'):
            if field not in source:
                raise ValueError(path + '.' + field + ': observation missing')
        if first is None:
            first = source
        else:
            for field in ('support_state', 'partners', 'defender'):
                if (field in source) != (field in first):
                    mismatch = field
                else:
                    mismatch = difference(first.get(field), source.get(field), field)
                if mismatch:
                    raise ValueError(path + '.' + mismatch + ': conflicts with entries[0] observation; '
                                     'refresh the source rather than choose a snapshot')
        complete = complete and source.get('observed_inputs_complete') is True
        entries.append({'id': identity, 'unit': copy.deepcopy(source['attacker']),
                        'context': copy.deepcopy(source['context'])})
    result = {field: copy.deepcopy(first[field]) for field in SHARED if field in first}
    result.update(observed_inputs_complete=complete, player_id=player_id,
                  player=copy.deepcopy(first['defender']), enemies=entries)
    return result


def create_output(filename, payload, root=ROOT):
    """Create only under ignored observations, with descriptor-relative no-follow IO."""
    path = Path(filename)
    parts = path.parts
    if (path.is_absolute() or len(parts) < 3 or parts[:2] != ('state', 'observations')
            or '..' in parts or path.suffix != '.json' or path.name == 'current_run.json'):
        raise ValueError('--output requires state/observations/NAME.json without traversal')
    if not hasattr(os, 'O_NOFOLLOW') or not hasattr(os, 'O_DIRECTORY'):
        raise ValueError('protected output requires a platform supporting no-follow directory IO')
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    descriptor = os.open(str(root), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            try:
                os.mkdir(part, mode=0o700, dir_fd=descriptor)
            except FileExistsError:
                pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        output = os.open(parts[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=descriptor)
        try:
            with os.fdopen(output, 'wb') as stream:
                stream.write(encoded)
        except BaseException:
            os.unlink(parts[-1], dir_fd=descriptor)
            raise
    finally:
        os.close(descriptor)


def prompt(message):
    print(message, end=' ', file=sys.stderr, flush=True)
    answer = input().strip()
    if answer.lower() == 'cancel':
        raise EOFError('cancelled')
    return answer


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guided', action='store_true', help='prompt for selections and renew confirmations')
    parser.add_argument('--player-id')
    parser.add_argument('--enemy', nargs=2, action='append', metavar=('ID', 'DUEL_JSON'),
                        help='repeat in supplied attack order; attacker is enemy, defender is player')
    parser.add_argument('--confirm-order', action='store_true')
    parser.add_argument('--confirm-unchanged', action='store_true')
    parser.add_argument('--confirm-no-events', action='store_true')
    parser.add_argument('--output', help='create-only state/observations/NAME.json')
    args = parser.parse_args(argv)
    guided = args.guided or (args.player_id is None and args.enemy is None)
    try:
        player_id = args.player_id
        selections = args.enemy or []
        confirmations = (args.confirm_order, args.confirm_unchanged, args.confirm_no_events)
        if guided:
            print('Attacker = distinct enemy; defender = same player. Type cancel to stop. '
                  'Never rename a repeated entity to obtain numbers.', file=sys.stderr)
            if player_id is None:
                player_id = prompt('Player entity ID:')
            if not selections:
                while True:
                    filename = prompt('Next plain duel JSON path (blank finishes ordered list):')
                    if not filename:
                        break
                    identity = prompt('Distinct observed enemy entity ID:')
                    selections.append((identity, filename))
        sources = []
        source_files = set()
        for index, (identity, filename) in enumerate(selections):
            try:
                path = source_path(filename)
                metadata = path.stat()
                file_id = (metadata.st_dev, metadata.st_ino)
                if file_id in source_files:
                    raise ValueError('same source file selected again; do not rename a repeated entity')
                source_files.add(file_id)
                source = read_duel(filename)
            except (OSError, ValueError) as exc:
                raise ValueError('entries[' + str(index) + ']: cannot read duel: ' + str(exc)) from exc
            sources.append((identity, source))
        # Validate identity and snapshot compatibility before asking confirmations.
        payload = assemble(player_id, sources)
        if guided:
            print('Supplied order: ' + ' -> '.join(identity for identity, _ in sources), file=sys.stderr)
            confirmations = tuple(prompt(question).lower() == 'yes' for question in (
                'Confirm this exact supplied attack order? (yes/no)',
                'Confirm all supplied observations are complete and still unchanged? (yes/no)',
                'Confirm no healing, levels, equipment/skill swaps or other events intervene? (yes/no)'))
        payload = assemble(player_id, sources, *confirmations)
        result = evaluate(payload)
        print(result['status'] + (': ' + result['reason'] if result.get('reason') else '')
              + '; supplied sequence only; no map survival guarantee.', file=sys.stderr)
        if args.output:
            create_output(args.output, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (EOFError, KeyboardInterrupt):
        print('Cancelled; no sequence emitted or saved.', file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError) as exc:
        print('Cannot assemble sequence: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
