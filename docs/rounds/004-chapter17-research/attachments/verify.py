#!/usr/bin/env python3
"""Round-local checks. Protected hashes stay in a private output directory.

Run from checkout root with: python3 <this-file> /tmp/fea-worker004-checks
Baseline must be the private pre-work snapshot made at session start. A later
reviewer may supply their independently created baseline as the second argument.
No rebuilds, network calls, run initialization or production writes occur.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path.cwd()
OUT = Path(sys.argv[1])
BASE = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('/tmp/fea-worker004-protected-before.json')
OUT.mkdir(parents=True, exist_ok=True)


def snapshot():
    files = sorted(Path('data').rglob('*.json')) + [Path('CURRENT_RUN.md')]
    files += sorted(p for p in Path('state').rglob('*') if p.is_file())
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


before = json.loads(BASE.read_text())
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
commands = [['make', 'audit'], ['python3', 'tools/fw.py', 'check']]
commands += [['python3', 'tools/map_info.py', '--chapter', '17', '--difficulty', 'hard',
              '--turn', str(turn), '--phase', phase]
             for turn, phase in [(8, 'player'), (8, 'enemy'), (9, 'player'), (10, 'player')]]
commands += [['git', 'diff', '--check']]
lines = ['HEAD: ' + head, 'OS: ' + platform.platform(),
         'Python: ' + sys.version.replace('\n', ' '),
         'Audit output: checkout prefix sanitized to <worktree>.',
         'CLI output below: parsed JSON excerpts, full stdout stays private.']
failed = False
for number, command in enumerate(commands):
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output = result.stdout.replace(str(ROOT), '<worktree>')
    (OUT / ('command-%d.txt' % number)).write_text(output)
    if 'tools/map_info.py' in command and result.returncode == 0:
        d = json.loads(result.stdout)
        keys = ['chapter_id', 'difficulty', 'mode', 'current_turn', 'current_phase',
                'target_enemy_phase_turn', 'map_confidence', 'reinforcement_status',
                'absence_reasonably_supported', 'safe_to_conclude_no_reinforcements']
        excerpt = {k: d[k] for k in keys}
        # Preserve exact uncertainty fields without reproducing all map content.
        waves = d.get('reinforcement_candidates', [])
        if not waves:
            for value in d.values():
                if isinstance(value, list) and any(isinstance(w, dict) and w.get('id') == 'hard_chapter_17_first' for w in value):
                    waves = value
                    break
        excerpt['wave_excerpts'] = [{k: w[k] for k in
                                    ['id', 'confidence', 'timing', 'location', 'spawn_phase', 'schedule_completeness']}
                                   for w in waves]
        output = json.dumps(excerpt, ensure_ascii=False, indent=2)
    lines += ['', '$ ' + ' '.join(command), output.rstrip(), 'exit: ' + str(result.returncode)]
    failed |= result.returncode != 0
    print(' '.join(command) + ' -> exit ' + str(result.returncode), flush=True)
after = snapshot()
# Never commit private manifests, including player paths or hashes.
(OUT / 'protected-after-private.json').write_text(json.dumps(after, indent=2))
added, removed = set(after) - set(before), set(before) - set(after)
changed = [p for p in before.keys() & after.keys() if before[p] != after[p]]
summary = {'protected_file_count': len(after),
           'canonical_json_count': sum(p.startswith('data/') for p in after),
           'state_file_count': sum(p.startswith('state/') for p in after),
           'added_count': len(added), 'removed_count': len(removed),
           'changed_hash_count': len(changed),
           'live_run_exists': Path('state/current_run.json').exists()}
status = int(bool(added or removed or changed))
failed |= bool(status)
lines += ['', '$ protected SHA-256 and file-set comparison',
          json.dumps(summary, indent=2), 'exit: ' + str(status)]
(OUT / 'checks.txt').write_text('\n'.join(lines) + '\n')
print(json.dumps(summary), flush=True)
sys.exit(int(failed))
