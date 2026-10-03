"""Run from repository root. Optional private baseline; never print run hashes."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE = 'a97ee2d8a528d7f8fef62b06978a3c3861599e69'
root = Path.cwd()
files = sorted(str(p) for p in Path('data').rglob('*.json'))
base_files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'data'], text=True).splitlines()
base_files = sorted(p for p in base_files if p.endswith('.json'))
assert files == base_files
changes = []

def diff(a, b, path):
    if a == b:
        return
    if isinstance(a, dict) and isinstance(b, dict):
        assert a.keys() == b.keys(), path
        for key in a:
            diff(a[key], b[key], path + '/' + key)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (old, new) in enumerate(zip(a, b)):
            locator = str(old['id']) if isinstance(old, dict) and 'id' in old else str(i)
            diff(old, new, path + '/' + locator)
    else:
        changes.append(path)

for filename in files:
    old = json.loads(subprocess.check_output(['git', 'show', BASE + ':' + filename], text=True))
    new = json.loads(Path(filename).read_text())
    diff(old, new, filename)
expected = set()
for wave in ('first', 'second', 'central'):
    for field in ('source_ids', 'notes'):
        expected.add('data/chapters/hard_reinforcements.json/records/hard_chapter_17_' + wave + '/units/' + field)
for field in ('value', 'confidence'):
    expected.add('data/chapters/hard_reinforcements.json/records/hard_chapter_17_central/units/' + field)
for source in ('hr_fandom17', 'hr_jp_17'):
    for field in ('accessed', 'limitations'):
        expected.add('data/sources.json/' + source + '/' + field)
assert set(changes) == expected, (set(changes) - expected, expected - set(changes))
print('Canonical file set:', len(files), 'unchanged')
print('Exactly', len(changes), 'approved canonical field changes:')
for path in changes:
    print(path)
print('Other chapters/modes, mixed-mode JSON, Chapter 17 non-unit claims/conflict, Hard tactics and quarantine: unchanged')
old_review = json.loads(subprocess.check_output(['git', 'show', BASE + ':research/hard_verification/reviewed.json'], text=True))
new_review = json.loads(Path('research/hard_verification/reviewed.json').read_text())
for review in (old_review, new_review):
    for m in review['maps']:
        if m['id'] == 'chapter_17':
            for wave in m['waves']:
                wave.pop('units')
    for source in review['additional_sources']:
        if source['id'] in ('hr_jp_17', 'hr_fandom17'):
            source.pop('accessed')
            source.pop('limitations')
assert old_review == new_review
print('Reviewed inputs outside approved inventory/source fields: unchanged')
if len(sys.argv) == 2:
    before = json.loads(Path(sys.argv[1]).read_text())
    private_before = {p: digest for p, digest in before.items() if not p.startswith('data/')}
    paths = [Path('CURRENT_RUN.md')] + sorted(p for p in Path('state').rglob('*') if p.is_file())
    now = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert now == private_before
    print('Private run file set/content preserved:', len(now), 'files; live run exists:', Path('state/current_run.json').exists())
else:
    print('Private preservation not checked: supply private pre-work baseline as sole argument')
