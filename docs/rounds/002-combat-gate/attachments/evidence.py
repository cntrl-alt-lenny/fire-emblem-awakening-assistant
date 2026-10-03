"""Reproduce baseline failures, numerical comparisons, CLI and preservation."""
import copy
import hashlib
import io
import json
import platform
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
BASE='0af85f83df6e372ff0c03853968eca4921be840f'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tests')]
import test_combat_gate as tests
from tactical_combat import assess
from test_hard import battle

def main():
    source=subprocess.check_output(['git','show',BASE+':tools/tactical_combat.py'],cwd=ROOT,text=True)
    old=types.ModuleType('baseline_gate');exec(compile(source,'baseline_gate','exec'),old.__dict__)
    suite=unittest.TestSuite(tests.CombatGateTests(name) for name in
                            ('test_missing_properties_both_sides','test_certain_death_both_sides'))
    tests.assess=old.assess
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    tests.assess=assess
    public_output=stream.getvalue().replace(str(ROOT)+'/', '')
    (OUT/'baseline-failures.txt').write_text('Baseline '+BASE+'; new complete fixtures and new assertions, old wrapper.\nRepository root removed from traceback paths.\n'+public_output+'expected_test_exit_status: 1\n')
    assert len(result.failures)==8 and not result.errors,stream.getvalue()
    fixtures={'ordinary':battle(),'certain_attacker':tests.lethal('attacker'),'certain_defender':tests.lethal('defender')}
    p=battle();p['attacker']['weapon']['crit']=1;p['defender']['current_hp']=20;fixtures['possible']=p
    p=battle();p['attacker']['weapon']['effectiveness']=['flying'];p['defender']['weaknesses']=['flying'];fixtures['effective']=p
    p=battle();p['defender']['weapon']=None;p['defender']['weapon_state']='unequipped';p['defender']['remaining_uses']=0;fixtures['unequipped']=p
    p=battle();p['attacker']['weapon'].update(might=8,hit=110,crit=3);fixtures['forged']=p
    fixtures['canonical']=json.loads((ROOT/'examples/battle.json').read_text())
    p=battle();p['attacker'].update(weapon='brave_sword',weapon_rank='A');fixtures['canonical_brave']=p
    p=battle();p['attacker']['skills']=['ignis'];p['attacker']['stats']['skl']=20;fixtures['proc']=p
    comparisons={}
    for name,p in fixtures.items():
        before,after=old.assess(p),assess(p)
        assert before.get('outcome') is not None and after.get('outcome') is not None,name
        assert before['forecast']==after['forecast'] and before['outcome']==after['outcome'],name
        comparisons[name]={'input':p,'forecast_and_outcome_equal':True,'old_status':before['status'],'new_output':after}
    (OUT/'numerical-comparison.json').write_text(json.dumps(comparisons,indent=2)+'\n')
    cli={}
    fixtures['missing_effect']=battle();del fixtures['missing_effect']['defender']['weapon']['effect']
    with tempfile.TemporaryDirectory() as tmp:
        file=Path(tmp)/'battle.json'
        for name in ('canonical','forged','unequipped','certain_attacker','certain_defender','possible','missing_effect'):
            file.write_text(json.dumps(fixtures[name]))
            r=subprocess.run(['python3','tools/tactical_combat.py',str(file)],cwd=ROOT,capture_output=True,text=True)
            assert r.returncode==0,r.stderr
            cli[name]={'command':'python3 tools/tactical_combat.py TEMP_INPUT.json','input':fixtures[name],
                       'exit_status':r.returncode,'output':json.loads(r.stdout)}
    (OUT/'cli.json').write_text(json.dumps(cli,indent=2)+'\n')
    paths=sorted((ROOT/'data').rglob('*.json'))+[ROOT/'CURRENT_RUN.md']+sorted(p for p in (ROOT/'state').rglob('*') if p.is_file())
    after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    before=json.loads((OUT/'preservation-before.json').read_text())
    preservation={'before':before,'after':after,'added':sorted(set(after)-set(before)),
                  'deleted':sorted(set(before)-set(after)),
                  'changed':sorted(p for p in set(before)&set(after) if before[p]!=after[p]),
                  'live_run_exists':(ROOT/'state/current_run.json').exists()}
    assert not any(preservation[k] for k in ('added','deleted','changed'))
    (OUT/'preservation.json').write_text(json.dumps(preservation,indent=2)+'\n')
    print('OS/Python:',platform.system(),platform.release(),platform.python_version())
    print('Baseline: 8 expected assertion failures, 0 errors (test exit 1)')
    print('Numerical comparison: 10 complete fixtures, identical forecasts/outcomes')
    print('CLI: 7 temporary inputs, all exit 0')
    print('Preservation: %s files; added/deleted/changed: []/[]/[]; live run: %s'%(len(after),preservation['live_run_exists']))

if __name__=='__main__':main()
