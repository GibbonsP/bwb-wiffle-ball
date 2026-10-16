"""Add the 2016 season to players.json (run once; keeps a .bak2016 copy).
Sources: the 2016 BWB statistics CSV, the predicted 2B/3B CSV (2016_predicted_2B_3B.csv),
data_2016.SCORES_2016 (game results) and the official 2016 standings the commissioner supplied.
2016 has no game logs, so season rows are flagged est (estimated doubles/triples and hits/walks allowed)."""
import json, csv, math
from data_2016 import SCORES_2016

DL = '/Users/parkergibbons/Downloads/'
d = json.load(open('players.json'))
P, T = d['players'], d['teams']

FULL = {'Panthers':'Brookside Panthers','Eagles':'Brookside Kraken','Aces':'Brentwood Aces','Wicked Aces':'Brentwood Aces',
        'Dashers':'Brentwood Braves','Bulldogs':'Brentwood Mustangs','Bull Dogs':'Brentwood Mustangs','Hotdoggers':'Beaver Brook Lavahogs'}
RAW16 = {'Brookside Panthers':'Panthers','Brookside Kraken':'Eagles','Brentwood Aces':'Aces','Brentwood Braves':'Dashers',
         'Brentwood Mustangs':'Bulldogs','Beaver Brook Lavahogs':'Hotdoggers'}
OFFICIAL = {'Brookside Panthers':(26,9),'Brookside Kraken':(20,15),'Brentwood Aces':(6,29),
            'Beaver Brook Lavahogs':(24,11),'Brentwood Braves':(18,17),'Brentwood Mustangs':(11,24)}
DIVS = {'North':[['Brookside Panthers','^'],['Brookside Kraken','*'],['Brentwood Aces','']],
        'South':[['Beaver Brook Lavahogs','^'],['Brentwood Braves','*'],['Brentwood Mustangs','']]}

AGG = [k for k in P['Parker Gibbons']['seasons'][0] if k not in ('year','type','team','teamPartial')]
num = lambda v: float(v) if v not in ('', None) else 0.0

# league later-career rates for hits / walks allowed (the CSV has no pitching H/BB)
_pH = _pBB = _o = 0
for p in P.values():
    c = p['careerReg']; _pH += c['pH']; _pBB += c['pBB']; _o += c['IPouts']
RPH, RPBB = _pH/(_o/3), _pBB/(_o/3)

raw = list(csv.DictReader(open(DL + '2016 BWB Statistics - 2016 BWB.csv', encoding='utf-8-sig')))
pred = {(r['Player'], r['Team']): r for r in csv.DictReader(open('2016_predicted_2B_3B.csv'))}
rows = [r for r in raw if '/' not in r['Team']]          # one row per player per team
assert len(rows) == len(pred) == 31

# runs scored were not recorded for 2016: estimate as HR (a home run always scores the hitter) plus a share of
# the hitter's other times on base, using the midpoint of the 2017 and 2018 league rates of that share
def _k(year):
    t = {k: 0 for k in ('R','H','HR','BB','HBP')}
    for p in P.values():
        for s in p['seasons']:
            if s['type']=='Regular' and s['year']==year and not s.get('split') and not s.get('tot') and not s.get('est'):
                for k in t: t[k] += s[k]
    return (t['R'] - t['HR']) / (t['H'] - t['HR'] + t['BB'] + t['HBP'])
K_RUNS = (_k(2017) + _k(2018)) / 2
_exp = {(r['Player'], r['Team']): num(r['HR']) + K_RUNS * (num(r['H']) - num(r['HR']) + num(r['BB']) + num(r['HBP'])) for r in rows}
_fl = {k: int(v) for k, v in _exp.items()}
for k in sorted(_exp, key=lambda k: -(_exp[k] - _fl[k]))[:round(sum(_exp.values())) - sum(_fl.values())]: _fl[k] += 1
R16 = _fl      # (player, team) -> estimated runs, rounded so the league total is preserved

def season_row(r):
    pr = pred[(r['Player'], r['Team'])]
    GP, AB, H, HR = int(num(r['GP'])), int(num(r['AB'])), int(num(r['H'])), int(num(r['HR']))
    b2, b3, b1 = int(pr['2B_pred']), int(pr['3B_pred']), int(pr['1B'])
    assert b1 + b2 + b3 + HR == H
    outs = round(num(r['IP']) * 3); ipn = outs / 3
    c = P.get(r['Player'], {}).get('careerReg')
    php = (c['pH']/(c['IPouts']/3)) if c and c['IPouts'] else RPH
    pbb = (c['pBB']/(c['IPouts']/3)) if c and c['IPouts'] else RPBB
    BB, HBP = int(num(r['BB'])), int(num(r['HBP']))
    row = {k: 0 for k in AGG}
    row.update({'G_bat':GP, 'GS_bat':GP, 'AB':AB, 'R':R16[(r['Player'], r['Team'])], '1B':b1, '2B':b2, '3B':b3, 'HR':HR, 'RBI':int(num(r['RBI'])), 'BB':BB, 'HBP':HBP,
        'H':H, 'TB':b1 + 2*b2 + 3*b3 + 4*HR, 'PA':AB + BB + HBP,
        'G_pit':(min(GP, max(1, math.ceil(outs/9))) if outs else 0), 'IPouts':outs, 'pR':int(num(r['ER'])), 'ER':int(num(r['ER'])),
        'pH':round(ipn*php), 'pBB':round(ipn*pbb), 'pK':int(num(r['SO'])),
        'W':int(num(r['W'])), 'L':int(num(r['L'])), 'SV':int(num(r['SV']))})
    return row

by_player = {}
for r in rows:
    by_player.setdefault(r['Player'], []).append((FULL[r['Team']], season_row(r)))

template = P['Tristan An']
new_keys = [k for k in template.keys()]
for name, lst in by_player.items():
    if name not in P:
        z = {k: 0 for k in AGG}
        P[name] = {'name':name, 'career':dict(z), 'careerReg':dict(z), 'careerPO':dict(z), 'seasons':[], 'years':[], 'teamsByYear':{},
                   'gids':[], 'firstDate':'2016-04-05', 'lastDate':'2016-07-27', 'honors':{'rings':[],'awards':[],'asg':[]}}
        for k in new_keys:
            P[name].setdefault(k, None if k=='photo' else [])
    pl = P[name]
    assert not any(s['year']==2016 for s in pl['seasons']), name
    clubs = [c for c,_ in lst]
    if len(lst) == 1:
        c, row = lst[0]
        out = [dict(row, year=2016, type='Regular', team=c, teamPartial=False, est=True)]
        counted = [row]
    else:
        out = [dict(row, year=2016, type='Regular', team=c, teamPartial=False, split=True, est=True) for c,row in lst]
        tot = {k: sum(row[k] for _,row in lst) for k in AGG}
        out.append(dict(tot, year=2016, type='Regular', team=None, teamPartial=False, tot=True, nTeams=len(lst), est=True))
        counted = [tot]
    pl['seasons'].extend(out)
    pl['seasons'].sort(key=lambda s: (s['year'], s['type'], 0 if s.get('split') else (2 if s.get('tot') else 1)))
    pl['years'] = sorted(set(pl['years']) | {2016})
    pl['teamsByYear']['2016'] = {'team': ' / '.join(clubs), 'partial': False}
    for row in counted:
        for k in AGG:
            pl['careerReg'][k] = pl['careerReg'].get(k, 0) + row[k]
            pl['career'][k] = pl['career'].get(k, 0) + row[k]
    pl['firstDate'] = min(pl['firstDate'], '2016-04-05') if pl.get('firstDate') else '2016-04-05'

# ---- teams ----
tg = {c: [] for c in RAW16}; rec = {c: {'RF':0,'RA':0} for c in RAW16}
for dt, a, h, ar, hr in SCORES_2016:
    ac, hc = FULL[a], FULL[h]
    for me, opp, mr, orr, ha in ((ac, hc, ar, hr, 'A'), (hc, ac, hr, ar, 'H')):
        tg[me].append({'date':dt, 'opp':opp, 'ha':ha, 'rf':mr, 'ra':orr, 'res':'W' if mr>orr else 'L' if mr<orr else 'T', 'phase':'Regular'})
        rec[me]['RF'] += mr; rec[me]['RA'] += orr
for club, raw16 in RAW16.items():
    if club not in T:
        loc = club.split(' ')[0] if club.startswith('Brentwood') else club
        T[club] = {'name':club, 'loc':'Brentwood', 'nick':'Aces', 'seasons':{}, 'years':[], 'nameByYear':{}, 'aka':[],
                   'record':{'W':0,'L':0,'T':0,'RF':0,'RA':0}}
    t = T[club]
    if club == 'Brentwood Aces' and 'logo' not in t and isinstance(d['franchiseLogos'].get('Aces'), str):
        t['logo'] = d['franchiseLogos']['Aces']      # the Aces' own wordmark from the league's logo set
    W, L = OFFICIAL[club]
    roster = []
    for name, lst in by_player.items():
        for c, row in lst:
            if c == club and (row['G_bat'] > 0 or row['IPouts'] > 0):
                roster.append({'name':name, 'regular':dict(row, est=True)})
    roster.sort(key=lambda e: -e['regular']['PA'])
    t['seasons']['2016'] = {'roster':roster, 'name':raw16, 'games':sorted(tg[club], key=lambda g:g['date']),
                            'record':{'Regular':{'W':W,'L':L,'T':0,'RF':rec[club]['RF'],'RA':rec[club]['RA']}}}
    t['nameByYear']['2016'] = raw16
    t['years'] = sorted(set(t['years']) | {2016})
    for k, v in (('W',W),('L',L),('T',0),('RF',rec[club]['RF']),('RA',rec[club]['RA'])): t['record'][k] += v
    t['firstYear'], t['lastYear'] = min(t['years']), max(t['years'])
    t['aka'] = sorted(set(t['aka']) | {nm for nm in t['nameByYear'].values() if nm != t['name'] and not t['name'].endswith(' ' + nm)})

d['divisions']['2016'] = DIVS
d['divisions'] = dict(sorted(d['divisions'].items()))
d['seasonRange'] = [2016, d['seasonRange'][1]]
d['nPlayers'] = len(P)
json.dump(d, open('players.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print('players', len(P), 'teams', len(T))
