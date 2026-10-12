"""Brain public-CLI integration trial; run only in a disposable synthetic checkout."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

from brain_baseline import fixtures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path)
    args = parser.parse_args()
    root = args.checkout.resolve()
    observations = root / 'state' / 'observations'
    assert not observations.exists(), 'Use a fresh disposable checkout, never a live observation directory'
    assert not (root / 'state' / 'current_run.json').exists(), 'Never use an actual run'
    sys.path.insert(0, str(root / 'tools'))
    from tactical_combat import assess
    from tactical_enemy_phase import evaluate

    answers = ['Hard', 'Classic', 'effective_displayed', 'none', 'none',
               '20 0 0 0 0 0 0 0', '20', 'custom', 'tome', 'magical', 'E',
               '6 50 0', '1', 'none', 'no', 'none', 'E', 'none', 'none',
               'none', 'none', '10', '10 0 0 0 0 0 0 0', '10', 'unequipped',
               'E', 'none', 'none', 'none', 'none', '0', '1', 'yes']
    count = 0

    def command(tool, arguments=(), transcript=None, expected_exit=0):
        nonlocal count
        result = subprocess.run([sys.executable, 'tools/' + tool + '.py', *arguments],
                                cwd=root, input=transcript, text=True, capture_output=True)
        assert result.returncode == expected_exit, (tool, result.returncode, result.stderr)
        count += 1
        return result

    def collect(values, arguments=(), expected_exit=0):
        return command('observed_input', arguments, '\n'.join(values) + '\n', expected_exit)

    def unknown(result, engine):
        payload = json.loads(result.stdout)
        assert engine(payload)['outcome'] is None
        assert 'UNKNOWN' in result.stderr
        assert 'death probability=' not in result.stderr
        return payload

    first = collect(answers, ['--output', 'state/observations/one.json'])
    second = collect(answers, ['--output', 'state/observations/two.json'])
    original = json.loads(first.stdout)
    assert original == json.loads(second.stdout)
    baseline_duel, baseline_sequence = fixtures()
    assert assess(original) == assess(baseline_duel)
    assert (observations / 'one.json').read_text() == first.stdout
    selections = ['--player-id', 'observed_player', '--enemy', 'enemy_one',
                  'state/observations/one.json', '--enemy', 'enemy_two',
                  'state/observations/two.json']
    confirms = ['--confirm-order', '--confirm-unchanged', '--confirm-no-events']
    assembled = command('sequence_input', selections + confirms +
                        ['--output', 'state/observations/sequence.json'])
    sequence = json.loads(assembled.stdout)
    assert evaluate(sequence) == evaluate(baseline_sequence)
    expected = {10: 0.245025, 4: 0.49995, 0: 0.255025}
    assert {row['hp']: row['probability'] for row in
            evaluate(sequence)['outcome']['final_hp_distribution']} == expected
    guided = command('sequence_input', transcript='\n'.join([
        'observed_player', 'state/observations/one.json', 'enemy_one',
        'state/observations/two.json', 'enemy_two', '', 'yes', 'yes', 'yes']) + '\n')
    assert json.loads(guided.stdout) == sequence

    for index, value in ((6, '?'), (17, 'counter'), (11, '7 50 0'),
                         (2, 'raw_permanent'), (4, '?')):
        variant = answers.copy()
        variant[index] = value
        result = collect(variant)
        payload = json.loads(result.stdout)
        if index == 11:
            expected_duel = copy.deepcopy(baseline_duel)
            expected_duel['attacker']['weapon']['might'] = 7
            assert assess(payload) == assess(expected_duel)
        else:
            unknown(result, assess)
        if index in (6, 4):
            assert payload['observed_inputs_complete'] is False
    paired = answers.copy()
    paired[3:5] = ['paired', 'actual_partner']
    unknown(collect(paired), assess)

    cancelled = collect(['cancel'], ['--output', 'state/observations/cancelled.json'], 1)
    assert not cancelled.stdout and not (observations / 'cancelled.json').exists()
    eof = command('observed_input', transcript='Hard\n', expected_exit=1)
    assert not eof.stdout
    revised = collect(['keep'] * 26 + ['yes'], ['--edit', 'state/observations/one.json'])
    assert json.loads(revised.stdout) == original
    stale = collect(['keep'] * 26 + ['no'], ['--edit', 'state/observations/one.json'])
    assert unknown(stale, assess)['observed_inputs_complete'] is False
    marked = copy.deepcopy(original)
    marked['attacker']['weapon']['range'] = '?'
    (observations / 'marked.json').write_text(json.dumps(marked))
    edited = collect(['keep'] * 26 + ['yes'], ['--edit', 'state/observations/marked.json'])
    assert unknown(edited, assess)['observed_inputs_complete'] is False
    assert json.loads(edited.stdout)['attacker']['weapon']['range'] == '?'

    incomplete = command('sequence_input', selections)
    assert unknown(incomplete, evaluate)['observed_inputs_complete'] is False
    mismatched = copy.deepcopy(original)
    mismatched['defender']['current_hp'] = 9
    (observations / 'mismatch.json').write_text(json.dumps(mismatched))
    mismatch_args = selections.copy()
    mismatch_args[-1] = 'state/observations/mismatch.json'
    conflict = command('sequence_input', mismatch_args + confirms, expected_exit=2)
    assert not conflict.stdout and 'defender.current_hp' in conflict.stderr
    duplicate = selections.copy()
    duplicate[-1] = 'state/observations/one.json'
    refusal = command('sequence_input', duplicate + confirms, expected_exit=2)
    assert not refusal.stdout

    preserved = {p.name: p.read_bytes() for p in observations.iterdir() if p.is_file()}
    refusal = collect(answers, ['--output', 'state/observations/one.json'], 2)
    assert not refusal.stdout
    refusal = command('sequence_input', selections + confirms +
                      ['--output', 'state/observations/sequence.json'], expected_exit=2)
    assert not refusal.stdout
    assert preserved == {p.name: p.read_bytes() for p in observations.iterdir() if p.is_file()}
    print('Public CLI workflows:', count, 'PASS; complete full engine equality; independent distribution:', expected)
    print('Fresh custom/unarmed duel: 33 answers; two-duel guided assembly: 9 answers; manual JSON edits: 0')
    print('Unknown/effect/raw/paired/stale/mismatch/cancel/duplicate/create/no-overwrite checks PASS; sources preserved.')
    print('Only synthetic observations in disposable checkout; no gameplay or human usability claim. Exit 0')


if __name__ == '__main__':
    main()
