"""Reproduce read-only CLI acceptance using only synthetic run context."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import map_info


def run(tool, args, expected=0):
    command = [sys.executable, 'tools/' + tool + '.py', *args]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    # State paths remain temporary/private and are not printed.
    shown = ['<synthetic-state>' if str(arg).endswith('/synthetic.json') else str(arg) for arg in args]
    print('$ python3 tools/' + tool + '.py ' + ' '.join(shown))
    print('exit', result.returncode)
    assert result.returncode == expected, result.stderr
    return result


def snapshot(base, names):
    files = []
    for name in names:
        path = base / name
        files.extend(path.rglob('*') if path.is_dir() else [path])
    return {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in files if p.is_file()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path, help='Private preservation baseline; never committed')
    args = parser.parse_args()
    output = Path(__file__).parent
    current = ['--chapter', '7', '--difficulty', 'hard', '--turn', '5', '--phase', 'player']
    before = run('map_info', current).stdout
    after = run('play_briefing', current).stdout
    (output / 'before.json').write_text(before)
    (output / 'after.txt').write_text(after)
    print('Before/after physical lines:', len(before.splitlines()), '/', len(after.splitlines()))
    print('After words:', len(after.split()), '; characters:', len(after))
    assert len(after.splitlines()) <= 30
    detail = json.loads(run('play_briefing', current + ['--spoilers', 'Full information', '--details']).stdout)
    assert detail == map_info.query(7, 'hard', 5, 'player', 'Full information')
    print('Full information details exactly equal raw query: PASS')
    for chapter in ['7', '11', '16', '19', 'para10', 'para14', '17', '15', '22']:
        for turn in ['2', '3', '4', '5', '6', '99']:
            for phase in ['player', 'enemy']:
                argv = ['--chapter', chapter, '--difficulty', 'hard', '--turn', turn, '--phase', phase,
                        '--spoilers', 'Full information', '--details']
                # Quiet matrix; individual outputs remain independently reproduced
                # by the focused test and by the commands printed above/below.
                p = subprocess.run([sys.executable, 'tools/play_briefing.py', *argv], cwd=ROOT,
                                   text=True, capture_output=True)
                assert p.returncode == 0
                assert json.loads(p.stdout) == map_info.query(chapter, 'hard', int(turn), phase, 'Full information')
    print('108 CLI raw-query comparisons (phase/fixed/family/event/conflict/absence): PASS')
    enemy = run('play_briefing', [arg if arg != 'player' else 'enemy' for arg in current])
    assert 'target: enemy phase 6' in enemy.stdout and 'Candidate hard_chapter_7_t5' not in enemy.stdout
    print('EP5 query targets EP6; fixed EP5 candidate omitted, incompleteness retained: PASS')
    for view in [[], ['--details'], ['--provenance']]:
        no = run('play_briefing', current + ['--spoilers', 'No spoilers', *view])
        assert all(x not in no.stdout for x in ['Cordelia', 'Vasto', 'source_ids', 'p2_guide', 'can_attack'])
        assert 'incomplete' in no.stdout and 'withheld' in no.stdout
    print('No-spoiler text/provenance/details contain context + general warning only: PASS')
    for argv in [current[:-2], [arg if arg != 'hard' else 'Lunatic' for arg in current]]:
        p = run('play_briefing', argv, 2)
        assert not p.stdout
        print(p.stderr.strip())
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / 'synthetic.json'
        state = {'chapter': 'chapter_7', 'difficulty': 'Hard', 'mode': 'Classic', 'turn': 5,
                 'spoiler_mode': 'No spoilers', 'units': {'synthetic': {'alive': False, 'stats': None}},
                 'events': [{'synthetic': True}], 'history': ['synthetic only']}
        path.write_text(json.dumps(state) + '\n')
        original = snapshot(Path(temp), ['synthetic.json'])
        p = run('play_briefing', ['--state', str(path), '--phase', 'player'])
        assert 'withheld' in p.stdout
        p = run('play_briefing', ['--state', str(path), '--chapter', '7', '--phase', 'player',
                                 '--spoilers', 'Tactical spoilers'])
        assert 'Western map edge' in p.stdout
        p = run('play_briefing', ['--state', str(path), '--phase', 'player', '--turn', '6'], 2)
        assert not p.stdout
        print(p.stderr.strip())
        assert snapshot(Path(temp), ['synthetic.json']) == original
        assert sorted(p.name for p in Path(temp).iterdir()) == ['synthetic.json']
        print('Synthetic state/death/history bytes and file set preserved; no lock/initialization: PASS')
    if args.baseline:
        before = json.loads(args.baseline.read_text())
        gitdir = subprocess.check_output(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, text=True).strip()
        primary = (ROOT / gitdir).resolve().parent
        after = {'data': snapshot(ROOT, ['data']), 'reports': snapshot(ROOT, ['research']),
                 'local': snapshot(ROOT, ['state', 'CURRENT_RUN.md']),
                 'primary_local': snapshot(primary, ['state', 'CURRENT_RUN.md'])}
        assert before == after
        print('Canonical, research and both private file sets/content preserved:', {k: len(v) for k, v in after.items()})
        print('No private paths, filenames, hashes or run values emitted.')


if __name__ == '__main__':
    main()
