"""Add the four 2016 playoff games (scores only) to players.json: GAMES, team game logs/records and the bracket's series scores.
Run once, after add_2016.py and add_2016_games.py. The World Series Game 1 date wasn't given; it follows the 9/7 block it was listed under."""
import json
d = json.load(open('players.json'))
FULL = {'Eagles':'Brookside Kraken','Panthers':'Brookside Panthers','Dashers':'Brentwood Braves','Hotdoggers':'Beaver Brook Lavahogs'}
GAMES = [  # (date, away, home, away_runs, home_runs)
    ('2016-08-04', 'Eagles', 'Panthers', 9, 10),          # Brookside Wild Card Game
    ('2016-09-07', 'Dashers', 'Hotdoggers', 7, 8),        # Brentwood Wild Card Game
    ('2016-09-07', 'Hotdoggers', 'Panthers', 11, 17),     # World Series Game 1
    ('2016-09-28', 'Panthers', 'Hotdoggers', 13, 9),      # World Series Game 2
]
assert not any(g['phase']=='Playoffs' and g['date'].startswith('2016') for g in d['games'].values())
rec = {}
for i, (dt, a, h, ar, hr) in enumerate(GAMES):
    gid = 20160090 + i
    d['games'][str(gid)] = {'gid':gid, 'date':dt, 'dt':f'{dt}T{18+i}:00:00', 'div':'2016 BWB Playoffs', 'phase':'Playoffs', 'loc':'TBA', 'innings':3,
        'away':{'team':FULL[a], 'line':[], 'R':ar, 'H':0, 'E':0, 'bat':[], 'pit':[]}, 'home':{'team':FULL[h], 'line':[], 'R':hr, 'H':0, 'E':0, 'bat':[], 'pit':[]}, 'noBox':True}
    for me, opp, mr, orr, ha in ((FULL[a], FULL[h], ar, hr, 'A'), (FULL[h], FULL[a], hr, ar, 'H')):
        res = 'W' if mr > orr else 'L'
        s = d['teams'][me]['seasons']['2016']
        s['games'].append({'date':dt, 'opp':opp, 'ha':ha, 'rf':mr, 'ra':orr, 'res':res, 'phase':'Playoffs'})
        r = s['record'].setdefault('Playoffs', {'W':0, 'L':0, 'T':0, 'RF':0, 'RA':0})
        r[res] += 1; r['RF'] += mr; r['RA'] += orr
for t in FULL.values():
    s = d['teams'][t]['seasons']['2016']; s['games'].sort(key=lambda g: (g['date'], g['phase']=='Playoffs'))
p = d['playoffs']['2016']
p['brookside']['series'] = [[10, 9]]          # Panthers 10, Eagles 9
p['brentwood']['series'] = [[8, 7]]           # Hotdoggers 8, Dashers 7
p['finalSeries'] = [[17, 11], [13, 9]]        # Panthers over Hotdoggers, 2-0
json.dump(d, open('players.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print('games now', len(d['games']))
