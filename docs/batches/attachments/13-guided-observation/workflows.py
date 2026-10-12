"""Reproduce public synthetic entry workflows and exact unchanged-gate equality."""
import copy
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
from test_observed_input import transcript, edit_transcript
from tactical_combat import assess
from tactical_enemy_phase import evaluate

BASELINE = '5c596d42adb3d2a5eeee460032ee20bdd4bb78ba'


def run(label, answers, args=(), expected=0, status=None):
    result = subprocess.run([sys.executable, 'tools/observed_input.py', *args], cwd=ROOT,
                            input=answers, text=True, capture_output=True)
    assert result.returncode == expected, (label, result.stderr)
    print('\nCASE:', label)
    print('COMMAND: python3 tools/observed_input.py' + (' [explicit synthetic draft/output selected]' if args else ''))
    print('STDIN (literal answers):\n' + answers, end='')
    print('EXIT:', result.returncode)
    if expected:
        assert result.stdout == '', label
        print('STDOUT: empty')
        print('DIAGNOSTIC:', result.stderr.strip())
        return None
    payload = json.loads(result.stdout)
    assessment = assess(payload)
    if status:
        assert assessment['status'] == status, (label, assessment)
    if assessment['status'] == 'UNKNOWN':
        assert 'probability=' not in result.stderr and 'displayed_hit' not in result.stderr
    print('PROMPTS:', result.stderr.count('[blank/? unknown; cancel stops]'))
    print('COMPLETENESS:', payload['observed_inputs_complete'])
    print('ASSESSMENT:', assessment['status'])
    print('JSON (actual stdout):\n' + result.stdout, end='')
    return payload


def keys(value):
    if isinstance(value, dict):
        return len(value) + sum(keys(item) for item in value.values())
    if isinstance(value, list):
        return sum(keys(item) for item in value)
    return 0


def main():
    complete = run('complete custom', transcript(), status='NO_MODELED_DEATH_IN_THIS_DUEL')
    run('complete catalog exact confirmed', transcript(weapon='catalog iron_sword'))
    partial = run('unknown one stat', transcript(stats='40 10 ? 0 10 0 5 5'), status='UNKNOWN')
    assert partial['attacker']['stats']['mag'] is None and partial['observed_inputs_complete'] is False
    run('blank skills', transcript(skills=''), status='UNKNOWN')
    counter = run('actual Counter preserved', transcript(skills='counter'), status='UNKNOWN')
    assert counter['attacker']['skills'] == ['counter']
    drain = run('actual drain preserved', transcript(effect='Drains HP'), status='UNKNOWN')
    assert drain['attacker']['weapon']['effect'] == 'Drains HP'
    forged = run('actual forged values', transcript().replace('5 100 0', '8 110 3'))
    run('paired observations', transcript(support='paired'), status='UNKNOWN')
    run('raw observations no conversion', transcript().replace('effective_displayed', 'raw_permanent'), status='UNKNOWN')
    run('explicit skill condition', transcript(skills='odd_rhythm'))
    mismatch = run('support mismatch', transcript().replace('none\n40 ', 'observed_partner\n40 ', 1), status='UNKNOWN')
    assert mismatch['observed_inputs_complete'] is False
    run('integer float refused then re-entry', transcript().replace('\n40\n', '\n1.5\n40\n', 1))
    unarmed_answers = transcript()
    start = unarmed_answers.find('custom', unarmed_answers.find('custom') + 1)
    unarmed_answers = unarmed_answers[:start] + unarmed_answers[start:].replace(
        'custom\nsword\nphysical\nE\n5 100 0\n1\nnone\nno\nnone', 'unequipped', 1).replace('50\n', '0\n', 1)
    unarmed = run('explicit unarmed defender', unarmed_answers)
    assert unarmed['defender']['weapon_state'] == 'unequipped'
    with tempfile.TemporaryDirectory(prefix='fea13-synthetic-') as temp:
        draft = Path(temp) / 'synthetic.json'
        draft.write_text(json.dumps(counter), encoding='utf-8')
        before = draft.read_bytes()
        edited = run('edit real effect deliberate keep', edit_transcript(counter), ('--edit', str(draft)), status='UNKNOWN')
        assert edited == counter and draft.read_bytes() == before
        stale = run('edit blank final confirmation', edit_transcript(counter, ''), ('--edit', str(draft)), status='UNKNOWN')
        assert stale['observed_inputs_complete'] is False and draft.read_bytes() == before
        for field, value in (('range', '?'), ('effectiveness', ['?'])):
            unknown = copy.deepcopy(complete)
            unknown['attacker']['weapon'][field] = value
            draft.write_text(json.dumps(unknown), encoding='utf-8')
            before_unknown = draft.read_bytes()
            kept = run('edit unknown weapon ' + field, edit_transcript(unknown), ('--edit', str(draft)), status='UNKNOWN')
            assert kept['observed_inputs_complete'] is False
            assert kept['attacker']['weapon'][field] == value and draft.read_bytes() == before_unknown
        draft.write_bytes(before)
        for field, value, is_complete in (('forge', {'might': None}, False), ('forge', [], False),
                                       ('forge', {}, False), ('forge', {'might': 3}, True),
                                       ('alive', '?', False), ('alive', 'false', False),
                                       ('alive', False, True), ('alive', True, True)):
            supplied = copy.deepcopy(complete)
            supplied['attacker'][field] = value
            draft.write_text(json.dumps(supplied), encoding='utf-8')
            before_supplied = draft.read_bytes()
            kept = run('edit supplied ' + field + '=' + json.dumps(value), edit_transcript(supplied),
                       ('--edit', str(draft)), status='NO_MODELED_DEATH_IN_THIS_DUEL' if field == 'alive' and value is True else 'UNKNOWN')
            assert kept['attacker'][field] == value and kept['observed_inputs_complete'] is is_complete
            assert draft.read_bytes() == before_supplied
        draft.write_bytes(before)
        run('cancel draft after observations', edit_transcript(counter, 'cancel'), ('--edit', str(draft)), 1)
        run('EOF during draft', 'keep\nkeep\n', ('--edit', str(draft)), 1)
        assert draft.read_bytes() == before
        draft.write_text(json.dumps(unarmed), encoding='utf-8')
        edited = run('edit explicit unarmed state keep', edit_transcript(unarmed), ('--edit', str(draft)))
        assert edited == unarmed
        draft.write_text('{"attacker":{},"attacker":{},"defender":{}}', encoding='utf-8')
        run('duplicate draft rejected', '', ('--edit', str(draft)), 2)
        draft.write_text(json.dumps(dict(complete, events=[])), encoding='utf-8')
        run('run-shaped extra fields refused', '', ('--edit', str(draft)), 2)
        run('outside output refused', transcript(), ('--output', str(Path(temp) / 'outside.json')), 2)
        assert not (Path(temp) / 'outside.json').exists()
    destination = ROOT / 'state/observations/batch13-synthetic-evidence.json'
    assert not destination.exists()
    try:
        saved = run('public create observation', transcript(), ('--output', 'state/observations/batch13-synthetic-evidence.json'))
        before = destination.read_bytes()
        assert json.loads(before) == saved
        run('existing output refused', transcript(), ('--output', 'state/observations/batch13-synthetic-evidence.json'), 2)
        assert destination.read_bytes() == before
    finally:
        if destination.exists():
            destination.unlink()
    # Archive only baseline public engine/data, never the primary checkout's run.
    archive = subprocess.run(['git', 'archive', BASELINE, 'tools', 'data'], cwd=ROOT, capture_output=True, check=True)
    with tempfile.TemporaryDirectory(prefix='fea13-baseline-') as temp:
        baseline = Path(temp)
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as source:
            source.extractall(baseline)
        for index, payload in enumerate((complete, forged, unarmed)):
            selected = baseline / ('synthetic-' + str(index) + '.json')
            selected.write_text(json.dumps(payload), encoding='utf-8')
            result = subprocess.run([sys.executable, str(baseline / 'tools/tactical_combat.py'), str(selected)],
                                    text=True, capture_output=True, check=True)
            assert json.loads(result.stdout) == assess(payload)
        print('\nBASELINE: complete/custom-forged/unarmed full assessment equality, 3/3.')
    sequence = {key: forged[key] for key in ('difficulty', 'mode', 'stats_basis', 'support_state', 'partners', 'observed_inputs_complete')}
    sequence.update(player_id='observed_player', player=forged['defender'], enemies=[
        {'id': 'one', 'unit': forged['attacker'], 'context': forged['context']},
        {'id': 'two', 'unit': copy.deepcopy(forged['attacker']), 'context': forged['context']}])
    assert evaluate(sequence)['outcome'] is not None
    print('EXISTING SEQUENCE: two actual forged attackers schema/outcome accepted.')
    print('BURDEN: complete custom ' + str(len(transcript().splitlines())) + ' answers, catalog '
          + str(len(transcript(weapon='catalog iron_sword').splitlines())) + ' answers, manual JSON edits 0.')
    print('GENERATED JSON: ' + str(keys(complete)) + ' object keys, ' + str(len(json.dumps(complete, indent=2).splitlines())) + ' formatted lines.')
    print('GROUPS: 16 stat values collected in 2 answers; 10 bonus values in 2 answers when supplied.')
    print('Unknown-to-number conversion: 0; unsupported effects removed: 0; existing files overwritten: 0.')


if __name__ == '__main__':
    main()
