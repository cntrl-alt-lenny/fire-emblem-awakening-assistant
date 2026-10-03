"""Temporary in-memory probes using the existing battle fixture; no run writes."""
import copy
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tests')]
from test_hard import battle
from tactical_combat import assess
from map_info import query
from tactical_query import query as legacy

def main():
    results = {}
    for n, turn, phase in [(7,5,'player'),(7,5,'enemy'),(15,5,'player'),(5,5,'player'),(17,5,'player'),(7,99,'player'),(3,5,'player')]:
        q = query(n, turn=turn, phase=phase)
        results['chapter_%s_%s_%s' % (n,turn,phase)] = {k:q[k] for k in ('target_enemy_phase_turn','reinforcement_status','candidate_reinforcements','safe_to_conclude_no_reinforcements','uncertain_partial_conflicted_unknown')}
    results['chapter_15_legacy'] = {str(t):legacy('chapter_15','Hard',t)['possible_reported_waves'] for t in (3,4,5)}
    cases = {'baseline':battle()}
    for key in ('support_state','partners'):
        p = battle(); del p[key]; cases['missing_'+key] = p
    p=battle();p['support_state']='adjacent';cases['adjacent_support']=p
    for skill in ('counter','dragonskin','aether'):
        p=battle();p['defender']['skills']=[skill];cases[skill]=p
    p=battle();p['attacker']['weapon']['effect']='Drains HP';cases['explicit_drain']=p
    p=battle();p['attacker']['weapon'].pop('effect');p['defender']['weapon'].pop('effect');cases['missing_weapon_effect']=p
    p=battle();p['attacker']['weapon']['brave']=True;p['attacker']['skills']=['hawkeye'];p['defender']['current_hp']=20;cases['certain_death']=p
    results['combat']={name:{'input':p,'output':assess(p)} for name,p in cases.items()}
    (Path(__file__).resolve().parent / 'scenarios.json').write_text(json.dumps(results, indent=2)+'\n')
    for name, p in cases.items():
        r=results['combat'][name]['output']
        print(name, json.dumps({k:v for k,v in r.items() if k not in ('forecast','outcome')}))
        if r.get('outcome'):print('death probabilities:',r['outcome']['attacker_death_probability'],r['outcome']['defender_death_probability'])

if __name__=='__main__':main()
