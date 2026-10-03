#!/usr/bin/env python3
"""Round-local evidence runner; never rebuilds or writes protected files.

Run from the worktree root. Supply an output directory (for example /tmp) when
rechecking an already committed artifact set. Outputs contain full command
results, with this checkout's absolute prefix replaced by <worktree>.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
OUT.mkdir(parents=True, exist_ok=True)


def snapshot():
    files = sorted(ROOT.glob('data/**/*.json')) + [ROOT / 'CURRENT_RUN.md']
    files += sorted(p for p in (ROOT / 'state').rglob('*') if p.is_file())
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in files}


before = json.loads((HERE / 'preservation-before.json').read_text())
commands = [
    ['make', 'audit'],
    ['python3', 'tools/fw.py', 'check'],
    ['python3', 'tools/map_info.py', '--chapter', '5', '--difficulty', 'hard',
     '--turn', '3', '--phase', 'player'],
    ['python3', 'tools/map_info.py', '--chapter', '5', '--difficulty', 'hard',
     '--turn', '3', '--phase', 'enemy'],
    ['python3', 'tools/map_info.py', '--chapter', '5', '--difficulty', 'hard',
     '--turn', '5', '--phase', 'player'],
    ['git', 'diff', '--check'],
]
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
lines = ['HEAD: ' + head, 'OS: ' + platform.platform(),
         'Python: ' + sys.version.replace('\n', ' '),
         'Output sanitation: checkout prefix replaced with <worktree>.']
failed = False
for command in commands:
    result = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    output = result.stdout.replace(str(ROOT), '<worktree>')
    lines += ['', '$ ' + ' '.join(command), output.rstrip(),
              'exit: ' + str(result.returncode)]
    failed |= result.returncode != 0
    print(' '.join(command) + ' -> exit ' + str(result.returncode), flush=True)
after = snapshot()
(OUT / 'preservation-after.json').write_text(json.dumps(after, indent=2) + '\n')
added = sorted(after.keys() - before.keys())
removed = sorted(before.keys() - after.keys())
changed = sorted(p for p in before.keys() & after.keys() if before[p] != after[p])
result = {'protected_files': len(after), 'canonical_json_files':
          sum(p.startswith('data/') for p in after), 'added': added,
          'removed': removed, 'changed': changed,
          'live_run_exists': (ROOT / 'state/current_run.json').exists(),
          'state_files': sorted(p for p in after if p.startswith('state/'))}
failed |= bool(added or removed or changed)
lines += ['', '$ protected file-set / SHA-256 comparison',
          json.dumps(result, indent=2), 'exit: ' + str(int(bool(added or removed or changed)))]
(OUT / 'checks.txt').write_text('\n'.join(lines) + '\n')
print(json.dumps(result), flush=True)
sys.exit(int(failed))
