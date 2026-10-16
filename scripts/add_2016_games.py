"""Add the 2016 regular-season game results to players.json['games'] (scores only, flagged noBox).
Run once, after scripts/add_2016.py. The results come from data_2016.SCORES_2016."""
import json, sys
sys.path.insert(0, '.')
from data_2016 import SCORES_2016
FULL = {'Panthers':'Brookside Panthers','Eagles':'Brookside Kraken','Wicked Aces':'Brentwood Aces','Dashers':'Brentwood Braves',
        'Bulldogs':'Brentwood Mustangs','Hotdoggers':'Beaver Brook Lavahogs'}
d = json.load(open('players.json'))
assert not any(g['date'].startswith('2016') for g in d['games'].values())
perday = {}
for i, (dt, a, h, ar, hr) in enumerate(SCORES_2016):
    k = perday[dt] = perday.get(dt, 0) + 1
    gid = 20160000 + i + 1
    side = lambda nm, r: {'team':FULL[nm], 'line':[], 'R':r, 'H':0, 'E':0, 'bat':[], 'pit':[]}
    d['games'][str(gid)] = {'gid':gid, 'date':dt, 'dt':f'{dt}T{11+k:02d}:00:00', 'div':'2016 BWB Season', 'phase':'Regular',
                            'loc':'TBA', 'innings':3, 'away':side(a, ar), 'home':side(h, hr), 'noBox':True}
json.dump(d, open('players.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print('added', len(SCORES_2016), 'games; total', len(d['games']))
