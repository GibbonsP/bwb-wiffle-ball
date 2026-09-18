import pandas as pd, numpy as np, json, csv, datetime, re
from collections import Counter, defaultdict

DL = '/Users/parkergibbons/Downloads/'

def _phase(dn):
    dn = str(dn)
    if 'Playoffs' in dn: return 'Playoffs'
    if 'All-Star' in dn: return 'AllStar'
    if 'Spring' in dn: return 'Spring'
    if 'Fall' in dn: return 'Fall'
    return 'Regular'

# --- franchise name timeline: (year, season-name) -> canonical franchise -----
FRAN = {}
with open(DL + '2026 BWB Season 2.0 - Franchise Name Timeline.csv',
          encoding='latin-1', newline='') as fh:
    _fr = list(csv.reader(fh))
_fyears = _fr[0][1:]
NICK_FIX = {'The Process': 'Process'}   # trim historical article

for row in _fr[1:]:
    canon = NICK_FIX.get(row[0].strip(), row[0].strip())
    if not canon:
        continue
    for i, y in enumerate(_fyears):
        nm = row[i + 1].strip()
        if nm:
            FRAN[(int(y), nm)] = canon

# nickname -> "<Location> <Nickname>" display name
PREFIX = {
    'Panthers': 'Brookside', 'Kraken': 'Brookside', 'Gladiators': 'Brentwood',
    'Process': 'Glenwood', 'Kings': 'Harris', 'Shock': 'Shelton',
    'Sox': 'Davenport', 'Lavahogs': 'Beaver Brook', 'Braves': 'Brentwood',
    'Bananas': 'Brentwood', 'Royals': 'Brookside', 'Aces': 'Brentwood',
    'Squirrels': 'Brookside', 'Dragons': 'Purchase', 'Mustangs': 'Brentwood',
    'Angels': 'Downtown', 'Titans': 'Downtown', 'PawSox': 'Purchase',
    'Diablos': 'Gleason', 'Snapping Turtles': 'Silver Lake',
}

LOC_OF = {v + ' ' + k: v for k, v in PREFIX.items()}   # full name -> location

def _prefixed(nick):
    return PREFIX[nick] + ' ' + nick if nick in PREFIX else nick

def canon_team(year, name):
    return _prefixed(FRAN.get((int(year), name), name))

def franchise_loc(full_name):
    return LOC_OF.get(full_name, '')

# --- games.csv: team-name map, and TeamID -> (year, phase, name) --------------
with open(DL + 'games.csv', encoding='latin-1', newline='') as fh:
    GR = list(csv.reader(fh))
GH = {k: i for i, k in enumerate(GR[0])}

def _gcol(r, k): return r[GH[k]]

_tname = {}       # TeamID -> canonical franchise name
TID2CTX = {}      # TeamID -> (year, phase, canonical name)
TID2RAW = {}      # TeamID -> the name used that season
for r in GR[1:]:
    yr = int(_gcol(r, 'Date').split('/')[-1])
    ph = _phase(_gcol(r, 'DivisionName'))
    for side in ('Visiting', 'Home'):
        tid = _gcol(r, side + 'TeamID')
        if tid:
            raw = NICK_FIX.get(_gcol(r, side + 'TeamName'), _gcol(r, side + 'TeamName'))
            cn = canon_team(yr, raw)
            _tname[int(tid)] = cn
            TID2RAW[int(tid)] = raw
            TID2CTX[int(tid)] = (yr, ph, cn)

# --- team_player_lookup.csv: PlayerID -> TeamID / team name ------------------
PID2TEAM, PID2TID = {}, {}
with open(DL + 'team_player_lookup.csv', encoding='latin-1', newline='') as fh:
    _lk = csv.reader(fh)
    next(_lk, None)  # header
    for r in _lk:
        if len(r) < 2 or not r[1].strip().isdigit():
            continue
        tid = r[0].strip()
        if tid and int(tid) in _tname:
            PID2TID[int(r[1].strip())] = int(tid)
            PID2TEAM[int(r[1].strip())] = _tname[int(tid)]

xl = pd.ExcelFile('/Users/parkergibbons/Downloads/BWB League Lineup Export.xlsx')
df = pd.read_excel(xl, 'Player_Stats_with_Game_Info', header=1)
g = pd.read_excel(xl, 'Games', header=0)
dm = g.set_index('GameID')['DivisionName'].to_dict()
df['Division'] = df['GameID'].map(dm)
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

def gtype(d):
    d = str(d)
    if 'Playoffs' in d: return 'Playoffs'
    if 'All-Star' in d: return 'AllStar'
    if 'Spring' in d: return 'Spring'
    if 'Fall' in d: return 'Fall'
    return 'Regular'
df['GameType'] = df['Division'].map(gtype)
df['TeamName'] = df['PlayerID'].map(
    lambda p: (TID2CTX.get(PID2TID.get(int(p), -1)) or (None, None, None))[2])

# --- integrity check: a player's looked-up team (from their PlayerID's own
#     registration) should be one of the two teams that actually played in
#     that game. It won't be if the stat sheet has a stray duplicate row under
#     a second PlayerID for a game the player only really appeared in once
#     (e.g. a guest appearance for another club) — drop those duplicates.
_gid_teams = {}
for _r in GR[1:]:
    _gid = _gcol(_r, 'GameID')
    if not _gid:
        continue
    try:
        _yr = int(_gcol(_r, 'Date').split('/')[-1])
    except ValueError:
        continue
    _vn = canon_team(_yr, NICK_FIX.get(_gcol(_r, 'VisitingTeamName'), _gcol(_r, 'VisitingTeamName')))
    _hn = canon_team(_yr, NICK_FIX.get(_gcol(_r, 'HomeTeamName'), _gcol(_r, 'HomeTeamName')))
    _gid_teams[int(_gid)] = {_vn, _hn}

def _team_played_in_game(row):
    teams = _gid_teams.get(int(row['GameID']))
    return teams is None or pd.isna(row['TeamName']) or row['TeamName'] in teams

_bad_team = ~df.apply(_team_played_in_game, axis=1)
if _bad_team.any():
    print(f'dropping {_bad_team.sum()} row(s) whose team did not actually play in that game:')
    print(df.loc[_bad_team, ['PlayerName', 'PlayerID', 'GameID', 'TeamName']].to_string())
    df = df[~_bad_team].copy()

ALIAS = {
    'AJ':'AJ Cefaloni', 'Bennett':'Bennett Breig', 'Darien':'Darien Sharpe',
    'Evan':'Evan Wilkins', 'Griffin':'Griffin Krueger', 'JB':'JB Breig',
    'Joey':'Joey Cardascia', 'Mathew':'Mathew Wilkins', 'Parker':'Parker Gibbons',
    'Tristan':'Tristan An', 'Victor':'Victor Cottini', 'Vinny':'Vinny Spoto',
    'BOB':'Brandon Gibbons', 'BOB Gibbons':'Brandon Gibbons',
    # 2017 first-name records resolved by the league
    'Alex':'Alex Homem', 'Jake':'Jake Quigley', 'James':'James Choi',
    'Peter':'Peter Fraioli', 'Jaden':'Jaden Helmer', 'Sam':'Sam Estroff',
    'Sean':'Sean Walther',
    # name-spelling merges
    'Dan Brady':'Daniel Brady',
    'A.J. Cefaloni':'AJ Cefaloni', 'T.J. Ciafone':'TJ Ciafone',
    'Evan Wilkens':'Evan Wilkins', 'Tommy Giandomenico':'Tom Giandomenico',
    # early (2017-19) records used "Bob Gibbons"; same person as Brandon Gibbons
    'Bob Gibbons':'Brandon Gibbons',
    # one 2021 Spring Training season used the nickname in place of the surname
    'Trevor "Garfield" Meyler':'Trevor Meyler',
}
df['PlayerName'] = df['PlayerName'].map(lambda n: ALIAS.get(n, n))

# Keep every game type; each is presented as its own section.
df = df[df['GameType'].isin(['Regular','Playoffs','AllStar','Spring','Fall'])].copy()
for c in df.columns:
    if df[c].dtype.kind in 'fi':
        df[c] = df[c].fillna(0)

def agg(frame):
    d = {}
    d['G_bat']  = int(frame['G.1'].sum())
    d['GS_bat'] = int(frame['GS.1'].sum())
    d['AB']  = int(frame['AB'].sum())
    d['R']   = int(frame['R'].sum())
    d['1B']  = int(frame['1B'].sum())
    d['2B']  = int(frame['2B'].sum())
    d['3B']  = int(frame['3B'].sum())
    d['HR']  = int(frame['HR'].sum())
    d['RBI'] = int(frame['RBI'].sum())
    d['BB']  = int(frame['BB'].sum())
    d['K']   = int(frame['K'].sum())
    d['HBP'] = int(frame['HBP'].sum())
    d['SB']  = int(frame['SB'].sum())
    d['CS']  = int(frame['CS'].sum())
    d['SF']  = int(frame['SF'].sum())
    d['SH']  = int(frame['SH'].sum())
    d['H']   = d['1B']+d['2B']+d['3B']+d['HR']
    d['TB']  = d['1B']+2*d['2B']+3*d['3B']+4*d['HR']
    d['PA']  = d['AB']+d['BB']+d['HBP']+d['SF']+d['SH']
    # pitching
    d['G_pit'] = int(frame['G.2'].sum())
    outs = int(frame['IP'].sum())*3 + int(frame['1/3 Innings'].sum())
    d['IPouts'] = outs
    d['pR']  = int(frame['R.1'].sum())
    d['ER']  = int(frame['ER'].sum())
    d['pH']  = int(frame['H'].sum())
    d['pBB'] = int(frame['BB.1'].sum())
    d['pHB'] = int(frame['HB'].sum())
    d['pK']  = int(frame['K.1'].sum())
    d['CG']  = int(frame['CG'].sum())
    d['W']   = int(frame['W'].sum())
    d['L']   = int(frame['L'].sum())
    d['SV']  = int(frame['S'].sum())
    d['BS']  = int(frame['BS'].sum())
    # fielding
    d['G_fld'] = int(frame['G'].sum())
    d['INN'] = float(frame['INN'].sum())
    d['TC']  = int(frame['TC'].sum())
    d['PO']  = int(frame['PO'].sum())
    d['A']   = int(frame['A'].sum())
    d['E']   = int(frame['E'].sum())
    d['DP']  = int(frame['DP'].sum())
    return d

def _played(entry):
    """True if a roster entry shows at least one game in any phase."""
    for ph in ('regular', 'playoffs'):
        v = entry.get(ph)
        if v and (v.get('G_bat', 0) or v.get('G_pit', 0) or v.get('G_fld', 0)):
            return True
    return False

DIVISION_LABELS = {'Brentwood Division','Brookside Division','North Division',
                   'South Division'}

def heuristic_team(frame):
    """Fallback when a PlayerID has no roster entry: the club that shows up in
    (nearly) all of the player's games that slate."""
    c = Counter()
    for _, r in frame.iterrows():
        for t in (r['Visiting Team'], r['Home Team']):
            if isinstance(t, str) and t not in DIVISION_LABELS:
                c[t] += 1
    if not c:
        return None
    return c.most_common(1)[0][0]

def team_for(frame):
    """(team_label, estimated?) for a set of stat rows. Uses the official
    PlayerID->team roster lookup; falls back to the game heuristic."""
    teams, n_auth = [], 0
    for pid in frame['PlayerID']:
        t = PID2TEAM.get(int(pid))
        if t:
            teams.append(t); n_auth += 1
    if teams:
        order = [t for t, _ in Counter(teams).most_common()]
        return ' / '.join(order), False
    return heuristic_team(frame), True

players = {}
for name, pf in df.groupby('PlayerName'):
    seasons = []
    for (yr, gt), sf in pf.groupby(['Year','GameType']):
        clubs = sorted(t for t in sf['TeamName'].dropna().unique())
        if len(clubs) > 1:
            # Baseball-Reference style: one row per club + a season total row
            for c in clubs:
                r = agg(sf[sf['TeamName'] == c])
                r['year'] = int(yr); r['type'] = gt
                r['team'] = c; r['teamPartial'] = False; r['split'] = True
                seasons.append(r)
            tot = agg(sf)
            tot['year'] = int(yr); tot['type'] = gt
            tot['team'] = None; tot['teamPartial'] = False
            tot['tot'] = True; tot['nTeams'] = len(clubs)
            seasons.append(tot)
        else:
            row = agg(sf); row['year'] = int(yr); row['type'] = gt
            tm, est = team_for(sf)
            row['team'] = tm; row['teamPartial'] = bool(est and tm)
            seasons.append(row)
    # one team per calendar year (prefer the regular-season slate)
    teamsByYear = {}
    for yr, yf in pf.groupby('Year'):
        base = yf[yf['GameType'] == 'Regular']
        if len(base) == 0:
            base = yf[yf['GameType'] == 'Playoffs']
        if len(base) == 0:
            base = yf
        tm, est = team_for(base)
        teamsByYear[int(yr)] = {'team': tm, 'partial': bool(est and tm)}
    gids = (pf.sort_values('Date').drop_duplicates('GameID')['GameID']
            .astype(int).tolist())
    players[name] = {
        'name': name,
        'career': agg(pf),
        'careerReg': agg(pf[pf['GameType']=='Regular']),
        'careerPO': agg(pf[pf['GameType']=='Playoffs']),
        'seasons': sorted(seasons, key=lambda r:(r['year'], r['type'],
                                                 0 if r.get('split') else (2 if r.get('tot') else 1))),
        'years': sorted(int(y) for y in pf['Year'].unique()),
        'teamsByYear': teamsByYear,
        'gids': gids,
        'firstDate': pf['Date'].min().strftime('%Y-%m-%d'),
        'lastDate': pf['Date'].max().strftime('%Y-%m-%d'),
    }

# ============================ TEAM / FRANCHISE PAGES ========================
# franchise = team NAME (TeamID is season-scoped). Roster + stat lines come from
# player-stat rows bucketed by PlayerID -> TeamID -> name (df['TeamName'], set above);
# record & game logs come straight from games.csv (VS1/HS1 = runs).

TEAM_PHASES = ['Regular', 'Playoffs', 'Spring', 'Fall']
teams = {}
tdf = df[df['TeamName'].notna() & df['GameType'].isin(TEAM_PHASES)]
for tname, tf in tdf.groupby('TeamName'):
    seasons = {}
    for yr, yf in tf.groupby('Year'):
        roster = []
        for pnm, pf2 in yf.groupby('PlayerName'):
            # drop players who were rostered but never appeared in any game
            if not (int(pf2['G.1'].sum()) or int(pf2['G.2'].sum()) or int(pf2['G'].sum())):
                continue
            e = {'name': pnm}
            for ph in ('Regular', 'Playoffs'):
                sub = pf2[pf2['GameType'] == ph]
                if len(sub):
                    e[ph.lower()] = agg(sub)
            roster.append(e)
        roster.sort(key=lambda e: -(e.get('regular', e.get('playoffs', {})).get('PA', 0)))
        seasons[int(yr)] = {'roster': roster}
    loc = franchise_loc(tname)
    teams[tname] = {'name': tname, 'loc': loc,
                    'nick': tname[len(loc):].strip() if loc else tname,
                    'seasons': seasons,
                    'years': sorted(int(y) for y in tf['Year'].unique())}

# records + game logs from games.csv  (team names mapped to canonical franchise)
def _iso(s):
    try:
        return datetime.datetime.strptime(s, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return s

for r in GR[1:]:
    if _gcol(r, 'Status') != '1':
        continue
    ph = _phase(_gcol(r, 'DivisionName'))
    if ph == 'AllStar':
        continue
    yr = int(_gcol(r, 'Date').split('/')[-1])
    d = _iso(_gcol(r, 'Date'))
    gid = int(_gcol(r, 'GameID'))
    vraw = NICK_FIX.get(_gcol(r, 'VisitingTeamName'), _gcol(r, 'VisitingTeamName'))
    hraw = NICK_FIX.get(_gcol(r, 'HomeTeamName'), _gcol(r, 'HomeTeamName'))
    vn, hn = canon_team(yr, vraw), canon_team(yr, hraw)
    try:
        vr, hr = int(_gcol(r, 'VS1') or 0), int(_gcol(r, 'HS1') or 0)
    except ValueError:
        continue
    for me, raw, opp, mr, oppr, ha in ((vn, vraw, hn, vr, hr, 'A'),
                                       (hn, hraw, vn, hr, vr, 'H')):
        t = teams.get(me)
        if t is None:
            continue
        s = t['seasons'].setdefault(yr, {'roster': []})
        s.setdefault('name', raw)
        if yr not in t['years']:
            t['years'].append(yr)
        res = 'W' if mr > oppr else 'L' if mr < oppr else 'T'
        s.setdefault('games', []).append(
            {'gid': gid, 'date': d, 'opp': opp, 'ha': ha, 'rf': mr, 'ra': oppr,
             'res': res, 'phase': ph})

for t in teams.values():
    t['years'] = sorted(set(t['years']))
    fr = {'W': 0, 'L': 0, 'T': 0, 'RF': 0, 'RA': 0}
    t['nameByYear'] = {}
    for y, s in t['seasons'].items():
        if s.get('name'):
            t['nameByYear'][y] = s['name']
        s['games'] = sorted(s.get('games', []), key=lambda g: g['date'])
        rec = {}
        for g in s['games']:
            rr = rec.setdefault(g['phase'], {'W': 0, 'L': 0, 'T': 0, 'RF': 0, 'RA': 0})
            rr[g['res']] += 1; rr['RF'] += g['rf']; rr['RA'] += g['ra']
            if g['phase'] == 'Regular':
                fr[g['res']] += 1; fr['RF'] += g['rf']; fr['RA'] += g['ra']
        s['record'] = rec
    t['record'] = fr
    t['firstYear'], t['lastYear'] = t['years'][0], t['years'][-1]
    t['aka'] = sorted({nm for nm in t['nameByYear'].values()
                       if nm != t['name'] and not t['name'].endswith(' ' + nm)})

# ============================ BOX SCORES ===================================
with open(DL + 'BWB League Lineup Export - Games.csv', encoding='latin-1', newline='') as fh:
    BX = list(csv.reader(fh))
BHc = {k: i for i, k in enumerate(BX[0])}
INN_COLS = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']

def _bi(r, k):
    v = r[BHc[k]]
    return int(v) if str(v).strip().lstrip('-').isdigit() else 0

def box_bat(row):
    h1, h2, h3, hrn = int(row['1B']), int(row['2B']), int(row['3B']), int(row['HR'])
    return {'n': row['PlayerName'], 'o': int(row['BatOrder']),
            'ab': int(row['AB']), 'r': int(row['R']), 'h': h1 + h2 + h3 + hrn,
            '2b': h2, '3b': h3, 'hr': hrn, 'rbi': int(row['RBI']),
            'bb': int(row['BB']), 'k': int(row['K']), 'hbp': int(row['HBP']),
            'sb': int(row['SB'])}

def box_pit(row):
    return {'n': row['PlayerName'], 'o': int(row['PitchOrder']),
            'ip': int(row['IP']) * 3 + int(row['1/3 Innings']),
            'h': int(row['H']), 'r': int(row['R.1']), 'er': int(row['ER']),
            'bb': int(row['BB.1']), 'k': int(row['K.1']),
            'w': int(row['W']), 'l': int(row['L']), 'sv': int(row['S'])}

games = {}
for r in BX[1:]:
    if r[BHc['Status']] != '1':
        continue
    ph = _phase(r[BHc['DivisionName']])
    gid = int(r[BHc['GameID']])
    yr = int(r[BHc['Date']].split('/')[-1])
    inn = int(r[BHc['Innings Played']] or 3)

    def line(side):
        vals = [_bi(r, '%s - %s' % (c, side)) for c in INN_COLS]
        last = max([i + 1 for i, v in enumerate(vals) if v] + [inn])
        return vals[:last]

    games[gid] = {
        'gid': gid, 'date': _iso(r[BHc['Date']]), 'div': r[BHc['DivisionName']],
        'phase': ph, 'loc': r[BHc['LocationName']], 'innings': inn,
        'away': {'team': canon_team(yr, r[BHc['VisitingTeamName']]), 'line': line('Away'),
                 'R': _bi(r, 'Runs - Away'), 'H': _bi(r, 'Hits - Away'),
                 'E': _bi(r, 'Errors - Away'), 'bat': [], 'pit': []},
        'home': {'team': canon_team(yr, r[BHc['HomeTeamName']]), 'line': line('Home'),
                 'R': _bi(r, 'Runs - Home'), 'H': _bi(r, 'Hits - Home'),
                 'E': _bi(r, 'Errors - Home'), 'bat': [], 'pit': []},
    }

for gid, gf in df.groupby('GameID'):
    G = games.get(int(gid))
    if G is None:
        continue
    for sk in ('away', 'home'):
        sf = gf[gf['TeamName'] == G[sk]['team']]
        b = [box_bat(row) for _, row in sf.iterrows()
             if int(row['BatOrder']) > 0 or row['AB'] or row['BB'] or row['HBP']]
        p = [box_pit(row) for _, row in sf.iterrows()
             if int(row['PitchOrder']) > 0
             or int(row['IP']) * 3 + int(row['1/3 Innings']) > 0]
        b.sort(key=lambda x: x['o'] if x['o'] else 99)
        p.sort(key=lambda x: x['o'] if x['o'] else 99)
        G[sk]['bat'], G[sk]['pit'] = b, p

# ============================ 2016 SUPPLEMENT ============================
# 2016 has only cumulative leader-list stats + game scores (no game logs).
# 2B/3B and hits/walks allowed are extrapolated from each player's later rates.
INCLUDE_2016 = False    # flip on once the 2016 player->team mapping is complete
from data_2016 import STATS_2016, MAP_2016, SCORES_2016
if not INCLUDE_2016:
    STATS_2016, MAP_2016, SCORES_2016 = {}, {}, []

AGG_KEYS = list(agg(df.iloc[0:0]).keys())
_LH = _L2 = _L3 = _LpH = _LpBB = _LpO = 0
for _p in players.values():
    c = _p['careerReg']
    _LH += c['H']; _L2 += c['2B']; _L3 += c['3B']
    _LpH += c['pH']; _LpBB += c['pBB']; _LpO += c['IPouts']
R2B = _L2 / _LH; R3B = _L3 / _LH
RPH = _LpH / (_LpO / 3); RPBB = _LpBB / (_LpO / 3)

NICK16 = {canon_team(2016, nick): nick for (_f, nick) in MAP_2016.values()}

for listed, (full, nick) in MAP_2016.items():
    s = STATS_2016.get(listed, {})
    club = canon_team(2016, nick)
    pl = players.get(full)
    if pl is None:
        z = {k: 0 for k in AGG_KEYS}
        pl = players[full] = {
            'name': full, 'career': dict(z), 'careerReg': dict(z), 'careerPO': dict(z),
            'seasons': [], 'years': [], 'teamsByYear': {}, 'gids': [],
            'firstDate': '2016-04-05', 'lastDate': '2016-07-27'}
    cr = pl['careerReg']
    AB, H, HR = s.get('AB', 0), s.get('H', 0), s.get('HR', 0)
    r2 = (cr['2B'] / cr['H']) if cr.get('H') else R2B
    r3 = (cr['3B'] / cr['H']) if cr.get('H') else R3B
    d2 = max(round(H * r2), 0); d3 = max(round(H * r3), 0)
    while d2 + d3 > max(H - HR, 0):
        if d2 >= d3: d2 -= 1
        else: d3 -= 1
    b1 = max(H - HR - d2 - d3, 0)
    outs = round(s.get('IP', 0) * 3)
    ipn = outs / 3 if outs else 0
    php = (cr['pH'] / (cr['IPouts'] / 3)) if cr.get('IPouts') else RPH
    pbb = (cr['pBB'] / (cr['IPouts'] / 3)) if cr.get('IPouts') else RPBB
    row = {k: 0 for k in AGG_KEYS}
    row.update({
        'year': 2016, 'type': 'Regular', 'team': club, 'teamPartial': False, 'est': True,
        'G_bat': s.get('GP', 0), 'GS_bat': s.get('GP', 0),
        'AB': AB, 'R': 0, '1B': b1, '2B': d2, '3B': d3, 'HR': HR, 'RBI': s.get('RBI', 0),
        'BB': s.get('BB', 0), 'K': 0, 'HBP': s.get('HBP', 0),
        'H': H, 'TB': b1 + 2 * d2 + 3 * d3 + 4 * HR,
        'PA': AB + s.get('BB', 0) + s.get('HBP', 0),
        'G_pit': s.get('GP', 0) if outs else 0, 'IPouts': outs,
        'pR': s.get('ER', 0), 'ER': s.get('ER', 0),
        'pH': round(ipn * php), 'pBB': round(ipn * pbb), 'pK': s.get('K', 0),
        'W': s.get('W', 0), 'L': s.get('L', 0), 'SV': s.get('SV', 0),
    })
    pl['seasons'].append(row)
    pl['seasons'].sort(key=lambda r: (r['year'], r['type'],
                                      0 if r.get('split') else (2 if r.get('tot') else 1)))
    pl['years'] = sorted(set(pl['years']) | {2016})
    pl['teamsByYear'][2016] = {'team': club, 'partial': False}
    for k in AGG_KEYS:
        pl['careerReg'][k] = pl['careerReg'].get(k, 0) + row[k]
        pl['career'][k] = pl['career'].get(k, 0) + row[k]

# --- 2016 team records from the game scores ---
t16 = defaultdict(lambda: {'W': 0, 'L': 0, 'T': 0, 'RF': 0, 'RA': 0})
tg16 = defaultdict(list)
for dt, a, h, ar, hr in SCORES_2016:
    ac, hc = canon_team(2016, a), canon_team(2016, h)
    ra = 'W' if ar > hr else 'L' if ar < hr else 'T'
    rh = 'W' if hr > ar else 'L' if hr < ar else 'T'
    for me, opp, mr, orr, ha, res in ((ac, hc, ar, hr, 'A', ra), (hc, ac, hr, ar, 'H', rh)):
        t16[me][res] += 1; t16[me]['RF'] += mr; t16[me]['RA'] += orr
        tg16[me].append({'date': dt, 'opp': opp, 'ha': ha, 'rf': mr, 'ra': orr,
                         'res': res, 'phase': 'Regular'})

for club, rec in t16.items():
    if club not in teams:
        loc = franchise_loc(club)
        teams[club] = {'name': club, 'loc': loc,
                       'nick': club[len(loc):].strip() if loc else club,
                       'seasons': {}, 'years': [], 'nameByYear': {}, 'aka': [],
                       'record': {'W': 0, 'L': 0, 'T': 0, 'RF': 0, 'RA': 0}}
    t = teams[club]
    raw16 = NICK16.get(club, club)
    roster = []
    for lst, (full, nick) in MAP_2016.items():
        if canon_team(2016, nick) == club and full in players:
            r16 = next((x for x in players[full]['seasons']
                        if x['year'] == 2016 and x['type'] == 'Regular'), None)
            if r16:
                e16 = {'name': full, 'regular': {k: r16[k] for k in AGG_KEYS}}
                if _played(e16):
                    roster.append(e16)
    roster.sort(key=lambda e: -e['regular'].get('PA', 0))
    t['seasons'][2016] = {'roster': roster, 'name': raw16,
                          'games': sorted(tg16[club], key=lambda g: g['date']),
                          'record': {'Regular': dict(rec)}}
    t['nameByYear'][2016] = raw16
    t['years'] = sorted(set(t['years']) | {2016})
    for k in ('W', 'L', 'T', 'RF', 'RA'):
        t['record'][k] += rec[k]
    t['firstYear'], t['lastYear'] = min(t['years']), max(t['years'])
    t['aka'] = sorted({nm for nm in t['nameByYear'].values()
                       if nm != t['name'] and not t['name'].endswith(' ' + nm)})

# ============================ 2026 (prowiffleball.com API) ===============
INCLUDE_2026 = True

def _pwipouts(ip):
    ip = str(ip)
    if '.' in ip:
        whole, frac = ip.split('.'); return int(whole) * 3 + int(frac)
    return int(ip) * 3

if INCLUDE_2026:
    _pwt = {t['shortname']: t['name'] for t in json.load(open(DL + 'pw_teams.json'))}
    _pwt.update({t['name']: t['name'] for t in json.load(open(DL + 'pw_teams.json'))})
    B26 = json.load(open(DL + 'pw_batting-stats.json'))['statistics']
    P26 = json.load(open(DL + 'pw_pitching-stats.json'))['statistics']
    BPO = json.load(open(DL + 'pw_batting-po.json'))['statistics']
    PPO = json.load(open(DL + 'pw_pitching-po.json'))['statistics']
    GM26 = [x for x in json.load(open(DL + 'pw_games.json'))['items'] if x['status'] == 'SUBMITTED']
    GDT = {x['id']: x['dateTime'] for x in GM26}   # LOCAL datetimes (games list, not /scores UTC)
    PW_ALIAS = {'A.J. Cefaloni': 'AJ Cefaloni', 'T.J. Ciafone': 'TJ Ciafone',
                'Dan Brady': 'Daniel Brady'}

    def pw_key(nm):
        nm = PW_ALIAS.get(nm, nm)
        for cand in (nm, nm.replace('.', ''), ALIAS.get(nm)):
            if cand and cand in players:
                return cand
        return nm  # new player -> create under this name

    AGG_KEYS26 = list(agg(df.iloc[0:0]).keys())

    def blank_player(nm):
        z = {k: 0 for k in AGG_KEYS26}
        players[nm] = {'name': nm, 'career': dict(z), 'careerReg': dict(z), 'careerPO': dict(z),
                       'seasons': [], 'years': [], 'teamsByYear': {}, 'gids': [],
                       'firstDate': '2026-01-01', 'lastDate': '2026-12-31'}
        return players[nm]

    def bat_row(s):
        r = {k: 0 for k in AGG_KEYS26}
        r.update({'G_bat': s['games'], 'GS_bat': s['games'], 'AB': s['atBats'], 'R': s['runs'],
                  '1B': s['singles'], '2B': s['doubles'], '3B': s['triples'], 'HR': s['homeruns'],
                  'RBI': s['rbi'], 'BB': s['walks'], 'K': s['strikeouts'], 'HBP': 0,
                  'SF': s['sacFlies'], 'H': s['hits'], 'TB': s['totalBases'],
                  'PA': s['plateAppearances']})
        return r

    def pit_add(r, s):
        outs = _pwipouts(s['inningsPitched'])
        er = round(s['era'] * outs / 9) if outs else 0
        r.update({'G_pit': s['games'], 'IPouts': outs, 'pR': s['runs'], 'ER': er,
                  'pH': s['hits'], 'pBB': s['walks'], 'pHB': 0, 'pK': s['strikeouts'],
                  'W': s['wins'], 'L': s['losses'], 'SV': s['saves']})
        return r

    # --- season W/L/SV per pitcher name (only per-game bits missing from lineups)
    PWL = {}
    for s in P26 + PPO:
        PWL.setdefault(pw_key(s['playerName']), {'W': 0, 'L': 0, 'SV': 0})
    for s in P26:
        d = PWL[pw_key(s['playerName'])]; d['W'] += s['wins']; d['L'] += s['losses']; d['SV'] += s['saves']
    PWLPO = {}
    for s in PPO:
        d = PWLPO.setdefault(pw_key(s['playerName']), {'W': 0, 'L': 0, 'SV': 0})
        d['W'] += s['wins']; d['L'] += s['losses']; d['SV'] += s['saves']

    # --- parse a game's play-by-play into per-batter lines
    def parse_bat(plays, roster_names):
        rn = sorted(roster_names, key=len, reverse=True)
        out = {n: {k: 0 for k in ('ab', 'h', '1b', '2b', '3b', 'hr', 'bb', 'k', 'sf', 'r')} for n in roster_names}
        for inn in plays or {}:
            for e in (plays[inn] or []):
                desc = e['description'] or ''
                bat = next((n for n in rn if desc.startswith(n + ' ')), None)
                if bat is None:
                    continue
                v = desc[len(bat) + 1:]
                o = out[bat]
                if v.startswith('walked'): o['bb'] += 1
                elif v.startswith('struck out'): o['k'] += 1; o['ab'] += 1
                elif v.startswith('singled'): o['h'] += 1; o['1b'] += 1; o['ab'] += 1
                elif v.startswith('doubled'): o['h'] += 1; o['2b'] += 1; o['ab'] += 1
                elif v.startswith('tripled'): o['h'] += 1; o['3b'] += 1; o['ab'] += 1
                elif v.startswith('homered') or v.startswith('hit a grand slam'): o['h'] += 1; o['hr'] += 1; o['ab'] += 1
                elif v.startswith('hit a sacrifice fly'): o['sf'] += 1
                elif ('grounded out' in v[:16] or 'flied out' in v[:12] or 'popped out' in v[:12]
                      or 'lined out' in v[:12] or 'grounded into a double play' in v
                      or "reached on a fielder's choice" in v or 'reached on an error' in v):
                    o['ab'] += 1
                # runs: any "<name> scored" anywhere in the play
                for n in roster_names:
                    if (n + ' scored') in desc:
                        out[n]['r'] += 1
        return out

    s26 = {}  # (pkey, phase) -> agg dict
    disc = []

    def acc(pk, phase, club, gid, bat=None, pit=None):
        key = (pk, phase)
        r = s26.get(key)
        if r is None:
            r = s26[key] = {kk: 0 for kk in AGG_KEYS26}
            r['_team'] = club; r['_gb'] = set(); r['_gp'] = set()
        if bat is not None:
            r['_gb'].add(gid)
            for a, b in (('AB', 'ab'), ('R', 'r'), ('H', 'h'), ('1B', '1b'), ('2B', '2b'),
                         ('3B', '3b'), ('HR', 'hr'), ('BB', 'bb'), ('K', 'k'), ('SF', 'sf'), ('RBI', 'rbi')):
                r[a] += bat.get(b, 0)
        if pit is not None:
            r['_gp'].add(gid)
            for a, b in (('IPouts', 'ip'), ('pH', 'h'), ('pR', 'r'), ('ER', 'er'),
                         ('pBB', 'bb'), ('pK', 'k')):
                r[a] += pit.get(b, 0)

    # --- 2026 box scores + season lines, both from play-by-play + lineups ---
    BOX26 = json.load(open(DL + 'pw_boxes.json'))
    p26gids = defaultdict(list)
    for gid, gd in BOX26.items():
        meta, box, lu = gd.get('meta'), gd.get('box'), gd.get('lineups')
        if not (meta and box and lu):
            continue
        gid = int(gid)
        dt = GDT.get(gid) or meta['dateTime']   # local time from the games list (meta is UTC)
        d = dt[:10]
        ph = 'Playoffs' if d >= '2026-08-22' else 'Regular'
        rpi = box.get('runsPerInning') or {}
        aline = [rpi[str(k)] for k in sorted(int(k) for k in rpi if int(k) > 0)] or [0]
        hline = [rpi[str(k)] for k in sorted((int(k) for k in rpi if int(k) < 0), key=abs)] or [0]
        rn_all = [('%s %s' % (b['firstName'], b['lastName'])).strip()
                  for sd in ('away', 'home') for b in lu[sd].get('batting', [])]
        parsed = parse_bat(gd.get('plays'), rn_all)

        def side(luside, bx, line):
            club = _pwt.get(luside['name'], luside['name'])
            bat = []
            for i, b in enumerate(luside.get('batting', [])):
                raw = ('%s %s' % (b['firstName'], b['lastName'])).strip()
                nm = pw_key(raw); pp = parsed.get(raw, {})
                e = {'n': nm, 'o': i + 1, 'ab': pp.get('ab', b['atBats']), 'r': b['runs'],
                     'h': pp.get('h', b['hits']), '2b': pp.get('2b', 0), '3b': pp.get('3b', 0),
                     'hr': b['homeruns'], 'rbi': b['runsBattedIn'], 'bb': pp.get('bb', 0),
                     'k': pp.get('k', 0), 'hbp': 0, 'sb': 0}
                bat.append(e); p26gids[nm].append((dt, gid))
                acc(nm, ph, club, gid, bat={**pp, 'ab': e['ab'], 'r': b['runs'], 'h': e['h'],
                                            'hr': b['homeruns'], 'rbi': b['runsBattedIn']})
                if b['hits'] != e['h'] or b['atBats'] != e['ab']:
                    disc.append('G%s %s: lineups H%s/AB%s vs plays H%s/AB%s' %
                                (gid, raw, b['hits'], b['atBats'], e['h'], e['ab']))
            pit = []
            for i, p in enumerate(luside.get('pitching', [])):
                raw = ('%s %s' % (p['firstName'], p['lastName'])).strip()
                nm = pw_key(raw); outs = _pwipouts(p['inningsPitched'])
                er = round(float(p.get('era') or 0) * outs / 9) if outs else 0
                pd = {'ip': outs, 'h': p['hits'], 'r': p['runs'], 'er': er,
                      'bb': p['walks'], 'k': p['strikeouts']}
                pit.append({'n': nm, 'o': i + 1, **pd, 'w': 0, 'l': 0, 'sv': 0})
                p26gids[nm].append((dt, gid))
                acc(nm, ph, club, gid, pit=pd)
            return {'team': club, 'line': line, 'R': bx['score'], 'H': bx['hits'],
                    'E': bx['errors'], 'bat': bat, 'pit': pit}

        games[gid] = {
            'gid': gid, 'date': d, 'dt': dt,
            'div': '2026 BWB Playoffs' if ph == 'Playoffs' else '2026 BWB Season',
            'phase': ph, 'loc': meta.get('fieldName') or '',
            'innings': meta.get('scheduledInnings') or 3,
            'away': side(lu['away'], box['away'], aline),
            'home': side(lu['home'], box['home'], hline),
        }

    # --- authoritative season totals from prowiffleball /stats endpoints,
    #     keyed by resolved player name. Play-by-play still feeds the box
    #     scores; these numbers are what the register's season rows show, so
    #     they match the site's player profiles and stat leaders exactly.
    #     ER isn't published, so derive it from ERA (per 3 IP: ER = ERA*IP/3).
    BST26   = {pw_key(s['playerName']): s for s in B26}
    PST26   = {pw_key(s['playerName']): s for s in P26}
    BST26PO = {pw_key(s['playerName']): s for s in BPO}
    PST26PO = {pw_key(s['playerName']): s for s in PPO}

    def reconcile(r, phase, pk):
        b = (BST26PO if phase == 'Playoffs' else BST26).get(pk)
        p = (PST26PO if phase == 'Playoffs' else PST26).get(pk)
        if b:
            r['G_bat'] = r['GS_bat'] = b['games']
            r['AB'], r['R'], r['H'] = b['atBats'], b['runs'], b['hits']
            r['1B'], r['2B'], r['3B'] = b['singles'], b['doubles'], b['triples']
            r['HR'], r['RBI'] = b['homeruns'], b['rbi']
            r['BB'], r['K'], r['SF'] = b['walks'], b['strikeouts'], b['sacFlies']
            r['TB'], r['PA'] = b['totalBases'], b['plateAppearances']
        if p:
            outs = _pwipouts(p['inningsPitched'])
            r['G_pit'], r['IPouts'] = p['games'], outs
            r['pH'], r['pR'] = p['hits'], p['runs']
            r['ER'] = round(float(p['era']) * outs / 9) if outs else 0
            r['pBB'], r['pK'] = p['walks'], p['strikeouts']
            r['W'], r['L'], r['SV'] = p['wins'], p['losses'], p['saves']

    # --- turn accumulated 2026 lines into season rows ---
    for (pk, phase), r in s26.items():
        club = r.pop('_team')
        r['G_bat'] = r['GS_bat'] = len(r.pop('_gb'))
        r['G_pit'] = len(r.pop('_gp'))
        r['1B'] = r['H'] - r['2B'] - r['3B'] - r['HR']
        r['TB'] = r['1B'] + 2 * r['2B'] + 3 * r['3B'] + 4 * r['HR']
        r['PA'] = r['AB'] + r['BB'] + r['SF']
        wl = (PWLPO if phase == 'Playoffs' else PWL).get(pk, {})
        r['W'], r['L'], r['SV'] = wl.get('W', 0), wl.get('L', 0), wl.get('SV', 0)
        reconcile(r, phase, pk)
        pl = players.get(pk) or blank_player(pk)
        r.update({'year': 2026, 'type': phase, 'team': club, 'teamPartial': False})
        pl['seasons'].append(r)
        pl['years'] = sorted(set(pl['years']) | {2026})
        if phase == 'Regular':
            pl['teamsByYear'][2026] = {'team': club, 'partial': False}
        tgt = pl['careerReg'] if phase == 'Regular' else pl['careerPO']
        for kk in AGG_KEYS26:
            tgt[kk] = tgt.get(kk, 0) + r.get(kk, 0)
            pl['career'][kk] = pl['career'].get(kk, 0) + r.get(kk, 0)

    for pl in players.values():
        pl['seasons'].sort(key=lambda r: (r['year'], r['type'],
                                          0 if r.get('split') else (2 if r.get('tot') else 1)))

    # --- reconcile 2026 box-score pitching to the player profiles ----------
    # The per-game lineup feed gives reliable IP/H/BB/K but its runs figure
    # and game ERA don't tie out to the official season pitching line (runs
    # charged differ; earned runs aren't published per game). Spread each
    # pitcher's profile R and ER across his games in proportion to the
    # lineup's per-game runs so every box column now sums to his profile.
    def _distribute(total, weights):
        n = len(weights)
        if n == 0:
            return []
        if total <= 0:
            return [0] * n
        sw = sum(weights)
        raw = [total * w / sw for w in weights] if sw else [total / n] * n
        out = [int(x) for x in raw]
        order = sorted(range(n), key=lambda i: raw[i] - out[i], reverse=True)
        for i in range(total - sum(out)):
            out[order[i]] += 1
        return out

    pit_target, pit_lines = {}, defaultdict(list)
    for pk, pl in players.items():
        for s in pl['seasons']:
            if s['year'] == 2026 and s.get('IPouts'):
                pit_target[(pk, s['type'])] = (s['ER'], s['pR'])
    for gid, G in games.items():
        if not str(G.get('date', '')).startswith('2026'):
            continue
        for sk in ('away', 'home'):
            for ln in G[sk]['pit']:
                pit_lines[(ln['n'], G['phase'])].append(ln)
    for key, lns in pit_lines.items():
        tgt = pit_target.get(key)
        if tgt is None:
            for ln in lns:
                ln['er'] = ln['r']
            continue
        tER, tR = tgt
        new_r = _distribute(tR, [ln['r'] for ln in lns])
        new_er = _distribute(tER, new_r if sum(new_r) else [1] * len(lns))
        for ln, rr, ee in zip(lns, new_r, new_er):
            ln['r'], ln['er'] = rr, ee

    # cross-check parsed season totals vs prowiffleball /stats
    for s in B26:
        pk = pw_key(s['playerName']); g = s26.get((pk, 'Regular'), {})
        for a, b in (('H', 'hits'), ('HR', 'homeruns'), ('BB', 'walks'),
                     ('K', 'strikeouts'), ('2B', 'doubles')):
            if g.get(a, 0) != s[b]:
                disc.append('SEASON %s %s: site %s vs logs %s' % (s['playerName'], a, s[b], g.get(a, 0)))
    print('2026 discrepancies:', len(disc))
    for x in disc[:25]:
        print('  ', x)

    # 2026 team records from the game list (>= 8/22 = playoffs)
    rec26 = defaultdict(lambda: {'Regular': {'W': 0, 'L': 0, 'T': 0, 'RF': 0, 'RA': 0},
                                 'Playoffs': {'W': 0, 'L': 0, 'T': 0, 'RF': 0, 'RA': 0}})
    gm26 = defaultdict(list)
    for x in GM26:
        dtl = x['dateTime']; d = dtl[:10]
        ph = 'Playoffs' if d >= '2026-08-22' else 'Regular'
        ac, hc = _pwt.get(x['awayName'], x['awayName']), _pwt.get(x['homeName'], x['homeName'])
        ar, hr = x['awayScore'], x['homeScore']
        rA = 'W' if ar > hr else 'L' if ar < hr else 'T'
        rH = 'W' if hr > ar else 'L' if hr < ar else 'T'
        for me, opp, mr, orr, ha, res in ((ac, hc, ar, hr, 'A', rA), (hc, ac, hr, ar, 'H', rH)):
            r = rec26[me][ph]
            r[res] += 1; r['RF'] += mr; r['RA'] += orr
            gm26[me].append({'gid': x['id'], 'date': d, 'dt': dtl, 'opp': opp, 'ha': ha, 'rf': mr,
                             'ra': orr, 'res': res, 'phase': ph})
    for nm, lst in p26gids.items():
        if nm in players:
            new = [g for _, g in sorted(set(lst))]          # 2026 gids, chronological
            players[nm]['gids'] = players[nm]['gids'] + [g for g in new
                                                         if g not in players[nm]['gids']]

    for club, rr in rec26.items():
        t = teams.get(club)
        if t is None:
            continue
        roster = []
        for k, pl in players.items():
            r16 = next((x for x in pl['seasons'] if x['year'] == 2026 and x['type'] == 'Regular'
                        and x['team'] == club), None)
            rpo = next((x for x in pl['seasons'] if x['year'] == 2026 and x['type'] == 'Playoffs'
                        and x['team'] == club), None)
            if r16 or rpo:
                e = {'name': k}
                if r16: e['regular'] = {kk: r16[kk] for kk in AGG_KEYS26}
                if rpo: e['playoffs'] = {kk: rpo[kk] for kk in AGG_KEYS26}
                if _played(e):
                    roster.append(e)
        roster.sort(key=lambda e: -(e.get('regular', e.get('playoffs', {})).get('PA', 0)))
        t['seasons'][2026] = {'roster': roster, 'name': t['nick'],
                              'games': sorted(gm26[club], key=lambda g: g.get('dt') or g['date']),
                              'record': {k: dict(v) for k, v in rr.items() if v['W'] + v['L'] + v['T']}}
        t['nameByYear'][2026] = t['nick']
        t['years'] = sorted(set(t['years']) | {2026})
        for k in ('W', 'L', 'T', 'RF', 'RA'):
            t['record'][k] += rr['Regular'][k]
        t['firstYear'], t['lastYear'] = min(t['years']), max(t['years'])

# ============================ AWARDS ======================================
awards = {}   # year -> [ {award, winner, team, note, finalists, div} ]
with open(DL + 'Career_All-Time Franchise & League Individual Stats - '
          'All-Time Awards By Year 2012-.csv', encoding='latin-1', newline='') as fh:
    AR = list(csv.reader(fh))
cur_y, cur_div = None, None
for r in AR:                      # AR[0] is itself a "Awards,…,<year>,…" header
    a = (r[0] or '').strip()
    if a == 'Awards':
        cur_y = int(r[2].strip()); cur_div = None
        awards.setdefault(cur_y, [])
        continue
    if a in ('North', 'South') and len(r) > 1 and r[1].strip() == a:
        cur_div = a
        continue
    if not a or a.startswith('-'):
        continue
    if cur_y is None:
        continue
    awards[cur_y].append({
        'award': a, 'winner': (r[1] or '').strip(), 'team': (r[3] or '').strip(),
        'note': (r[4] or '').strip() if len(r) > 4 else '',
        'finalists': (r[5] or '').strip() if len(r) > 5 else '',
        'div': cur_div,
    })

# ============================ ALL-STAR GAMES ==============================
asg = {}
with open(DL + '2026 BWB Season 2.0 - ASG History.csv',
          encoding='latin-1', newline='') as fh:
    SR = list(csv.reader(fh))

def _split_label(s):
    parts = s.strip().split()
    return ' '.join(parts[:-1]), int(parts[-1])   # ("North", 2017)

for c in range(1, len(SR[0])):
    lab = SR[0][c].strip()
    if not lab:
        continue
    s1, yr = _split_label(lab)
    s2, _ = _split_label(SR[9][c])
    p1 = [SR[r][c].strip() for r in range(1, 8) if r < len(SR) and SR[r][c].strip()]
    p2 = [SR[r][c].strip() for r in range(10, 17) if r < len(SR) and SR[r][c].strip()]
    def _cell(r):
        return SR[r][c].strip() if r < len(SR) and c < len(SR[r]) else ''
    asg[yr] = {
        'squads': [{'name': s1, 'players': p1}, {'name': s2, 'players': p2}],
        'winner': _cell(18), 'mvp': _cell(20), 'hrd': _cell(22), 'series': _cell(24),
    }

nick2full = {t['nick']: t['name'] for t in teams.values()}

# ============================ CHAMPIONS & PER-PLAYER HONORS =================
CHAMPS = [
    (2026, 'Shelton Shock',        'Shelton Shock',       '14-5',  ['Victor Cottini','James Duffelmeyer','Marco Angarano','TJ Ciafone','Chris Canno']),
    (2025, 'Brookside Panthers',   'Brookside Panthers',  '11-10', ['Peter Fraioli','Trevor Meyler','Daniel Cochrane','Peter Sposato','Joey Santarelli','James Duffelmeyer']),
    (2024, 'Brookside Kraken',     'Brookside Kraken',    '15-3',  ['Parker Gibbons','Evan Wilkins','Theo Canning','Kyle Moretzky','Dom Miano']),
    (2023, 'Brentwood Gladiators', 'Brentwood Gladiators','14-5',  ['Austin Corvino','AJ Cefaloni','Brandon Gibbons','Tommy Peck','Daniel Brady','Nima Khodakhah']),
    (2022, 'Brentwood Gladiators', 'Brentwood Gladiators','12-6',  ['Austin Corvino','AJ Cefaloni','Brandon Gibbons','Tommy Peck','Daniel Brady','Nima Khodakhah','Dustin Lee']),
    (2021, 'Brookside Panthers',   'Brookside Panthers',  '13-5',  ['Peter Fraioli','Vinny Spoto','Daniel Cochrane','Trevor Meyler','Peter Sposato','Yuichiro Ochi']),
    (2020, 'Harris Kings',         "Harris Special K's",  '6-12',  ['Jake Quigley','Jason Hegedus','Ben Galluzzo']),
    (2019, 'Glenwood Process',     'Brentwood Process',   '23-4',  ['Evan Wilkins']),
    (2018, 'Harris Kings',         "Harris Special K's",  '18-9',  ['Jake Quigley','Alex Homem','Matt Maida']),
    (2017, 'Brookside Panthers',   'Brookside Panthers',  '25-2',  ['Peter Fraioli','Jake Quigley','Tristan An','Sam Estroff']),
    (2016, 'Brookside Panthers',   'Brookside Panthers',  '29-9',  ['Peter Fraioli','Joey Cardascia']),
    (2015, 'Brookside Kraken',     'Brookside Eagles',    '33-10', ['Parker Gibbons','Alex Homem','TJ Fuerst','Michael Sullivan','Brandon Groothius','Will Deluca']),
    (2014, 'Brookside Panthers',   'Brookside Panthers',  '32-10', ['Peter Fraioli']),
    (2013, 'Brookside Kraken',     'Brookside Eagles',    '42-0',  ['Parker Gibbons','Davis Kim']),
    (2012, None,                   'Davenport Sox',       '14-3',  ['Kento Kamezaki','AJ Cefaloni']),
]
champs = [{'y': y, 'tm': tm, 'full': full, 'score': sc.replace('-', '–'), 'pl': pl}
          for (y, tm, full, sc, pl) in CHAMPS]

# ============================ PLAYOFF BRACKETS ============================
# Four-team bracket per year: two division semifinals (Brookside / Brentwood
# sides), then the final. Names are the nickname the club used that year; each
# semifinal's winner is whichever of its two seeds reached the final.
# (bk_seeds, bw_seeds, (finalist_a, finalist_b), champion)
PLAYOFFS_RAW = {
    2012: (('Sox', 'Tornados'),        ('Capitals', 'Jackals'),           ('Sox', 'Capitals'),            'Sox'),
    2013: (('Wiffles', 'Aces'),        ('Islanders', 'Ducks'),            ('Wiffles', 'Islanders'),       'Islanders'),
    2014: (('Wiffles', 'Warriors'),    ('Wolfpack', 'Kings'),             ('Wiffles', 'Kings'),           'Wiffles'),
    2015: (('Panthers', 'Aces'),       ('Eagles', 'Squirrels'),           ('Panthers', 'Eagles'),         'Eagles'),
    2016: (('Panthers', 'Eagles'),     ('Hotdoggers', 'Dashers'),         ('Panthers', 'Hotdoggers'),     'Panthers'),
    2017: (('Panthers', 'Wildcats'),   ('Dashers', 'Mustangs'),           ('Panthers', 'Dashers'),        'Panthers'),
    2018: (('Panthers', 'Kraken'),     ('The Process', "Special K's"),    ('Kraken', "Special K's"),      "Special K's"),
    2019: (('Lavahogs', 'Panthers'),   ('The Process', 'Kraken'),         ('Lavahogs', 'The Process'),    'The Process'),
    2020: (('Panthers', "Special K's"),('Kraken', 'The Process'),         ("Special K's", 'The Process'), "Special K's"),
    2021: (('Panthers', 'Gladiators'), ('Kraken', 'The Process'),         ('Kraken', 'Panthers'),         'Panthers'),
    2022: (('Shock', 'Panthers'),      ('Kraken', 'Gladiators'),          ('Shock', 'Gladiators'),        'Gladiators'),
    2023: (('Bananas', 'Dragons'),     ('Gladiators', 'Kraken'),          ('Bananas', 'Gladiators'),      'Gladiators'),
    2024: (('Panthers', 'Braves'),     ('Kraken', 'Shock'),               ('Braves', 'Kraken'),           'Kraken'),
    2025: (('Panthers', 'Braves'),     ('Kraken', 'Gladiators'),          ('Panthers', 'Kraken'),         'Panthers'),
    2026: (('Panthers', 'Gladiators'), ('Kraken', 'Shock'),               ('Panthers', 'Shock'),          'Shock'),
}

def _pk_team(y, nick):
    full = canon_team(y, nick)
    return {'nick': nick, 'full': full if full in teams else None}

def _pk_series(a, b, y, winner_nick):
    """Playoff game scores between two seeds that year, winner's score first."""
    if not (a['full'] and b['full']):
        return []
    log = (teams.get(a['full'], {}).get('seasons', {}).get(y, {}) or {}).get('games', [])
    out = [(g['rf'], g['ra']) for g in log
           if g.get('phase') == 'Playoffs' and g.get('opp') == b['full']]
    if winner_nick == a['nick']:
        return [[rf, ra] for rf, ra in out]
    return [[ra, rf] for rf, ra in out]

playoffs = {}
for _y, (_bk, _bw, _fin, _ch) in PLAYOFFS_RAW.items():
    _finset = set(_fin)
    bk = [_pk_team(_y, n) for n in _bk]
    bw = [_pk_team(_y, n) for n in _bw]
    bk_win = next((t['nick'] for t in bk if t['nick'] in _finset), None)
    bw_win = next((t['nick'] for t in bw if t['nick'] in _finset), None)
    bk_w = next((t for t in bk if t['nick'] == bk_win), bk[0])
    bw_w = next((t for t in bw if t['nick'] == bw_win), bw[0])
    playoffs[str(_y)] = {
        'brookside': {'seeds': bk, 'winner': bk_win,
                      'series': _pk_series(bk[0], bk[1], _y, bk_win)},
        'brentwood': {'seeds': bw, 'winner': bw_win,
                      'series': _pk_series(bw[0], bw[1], _y, bw_win)},
        'finalSeries': _pk_series(bk_w, bw_w, _y, _ch),
        'champion': _ch, 'championFull': _pk_team(_y, _ch)['full'],
    }

def _names(s):
    out = []
    for chunk in str(s).split('/'):
        for x in chunk.split(','):
            x = re.sub(r'\(c\)', '', x, flags=re.I).strip()
            if x:
                out.append(x)
    return out

def pkey(n):
    for cand in (n, n.replace('.', ''), ALIAS.get(n), ALIAS.get(n.replace('.', ''))):
        if cand and cand in players:
            return cand
    return None

for p in players.values():
    p['honors'] = {'rings': [], 'awards': [], 'asg': []}

for yr, rows in awards.items():
    for r in rows:
        for nm in _names(r['winner']):
            k = pkey(nm)
            if k:
                players[k]['honors']['awards'].append(
                    {'year': int(yr), 'award': r['award'], 'note': r['note'], 'div': r['div']})

for yr, a in asg.items():
    for sq in a['squads']:
        for raw in sq['players']:
            k = pkey(re.sub(r'\(c\)', '', raw, flags=re.I).strip())
            if k:
                players[k]['honors']['asg'].append(
                    {'year': int(yr), 'squad': sq['name'], 'cap': bool(re.search(r'\(c\)', raw, re.I))})

for c in champs:
    notable = {pkey(x) for x in c['pl']}
    for name, p in players.items():
        won = name in notable
        if not won and c['tm']:
            ty = p['teamsByYear'].get(c['y']) or {}
            won = ty.get('team') == c['tm']
        if won:
            p['honors']['rings'].append({'year': c['y'], 'team': c['tm'] or c['full']})

for p in players.values():
    for key in ('rings', 'awards', 'asg'):
        p['honors'][key].sort(key=lambda r: (-r['year'], r.get('award', '')))

# ---- division alignment per season (team = canonical franchise; ^ = division
#      winner / #1 seed, * = also made playoffs) ----
_D = {
 2026: {'Brookside': [('Brookside Panthers', '^'), ('Brentwood Gladiators', '*'),
                      ('Silver Lake Snapping Turtles', '')],
        'Brentwood': [('Brookside Kraken', '^'), ('Shelton Shock', '*'), ('Harris Kings', '')]},
 2025: {'Brookside': [('Brookside Panthers', '^'), ('Brentwood Braves', '*'),
                      ('Silver Lake Snapping Turtles', '')],
        'Brentwood': [('Brookside Kraken', '^'), ('Brentwood Gladiators', '*'),
                      ('Downtown Titans', '')]},
 2024: {'Brookside': [('Brookside Panthers', '^'), ('Brentwood Braves', '*'),
                      ('Brentwood Bananas', '')],
        'Brentwood': [('Brookside Kraken', '^'), ('Shelton Shock', '*'),
                      ('Brentwood Gladiators', '')]},
 2023: {'Brookside': [('Brentwood Bananas', '^'), ('Purchase Dragons', '*'),
                      ('Shelton Shock', '')],
        'Brentwood': [('Brentwood Gladiators', '^'), ('Brookside Kraken', '*'),
                      ('Brookside Panthers', '')]},
 2022: {'Brookside': [('Shelton Shock', '^'), ('Brookside Panthers', '*'),
                      ('Brentwood Bananas', '')],
        'Brentwood': [('Brookside Kraken', '^'), ('Brentwood Gladiators', '*'),
                      ('Purchase Dragons', '')]},
 2021: {'Brookside': [('Brookside Panthers', '^'), ('Brentwood Gladiators', '*'),
                      ('Harris Kings', '')],
        'Brentwood': [('Brookside Kraken', '^'), ('Glenwood Process', '*'),
                      ('Purchase Dragons', '')]},
 2020: {'North': [('Brookside Panthers', '^'), ('Harris Kings', '*'),
                  ('Beaver Brook Lavahogs', '')],
        'South': [('Glenwood Process', '^'), ('Brookside Kraken', '*'),
                  ('Purchase PawSox', '')]},
 2019: {'North': [('Beaver Brook Lavahogs', '^'), ('Brookside Panthers', '*'),
                  ('Harris Kings', '')],
        'South': [('Glenwood Process', '^'), ('Brookside Kraken', '*'),
                  ('Purchase PawSox', '')]},
 2018: {'North': [('Brookside Panthers', '^'), ('Brookside Kraken', '*'),
                  ('Beaver Brook Lavahogs', '')],
        'South': [('Glenwood Process', '^'), ('Harris Kings', '*'),
                  ('Brentwood Mustangs', '')]},
 2017: {'North': [('Brookside Panthers', '^'), ('Glenwood Process', '*'),
                  ('Brentwood Mustangs', '')],
        'South': [('Brentwood Braves', '^'), ('Brookside Kraken', '*'),
                  ('Beaver Brook Lavahogs', '')]},
}
divisions = {str(y): d for y, d in _D.items()}

# ============================ BROOKSIDE BEAVERS (national team) ==========
# Standalone from BWB league play: GameChanger data for the club's national-
# team tournament appearances. Each tournament is its own `beavers_YYYY.py`
# module; `_BV_TOURNAMENTS` lists them in chronological order and `beavers`
# (a list, one dict per tournament) is what generate.py renders. Names that
# also exist in the register link out to those player pages.
from beavers_2026 import BEAVERS_2026 as _BV_2026

_BV_TOURNAMENTS = [_BV_2026]

_BV_BAT_COLS = ('n', 'ab', 'r', 'h', 'rbi', 'bb', 'k', '2b', '3b', 'hr')
_BV_PIT_COLS = ('n', 'ip', 'h', 'r', 'er', 'bb', 'k', 'w', 'l', 'sv')
_AGGZ = list(agg(df.iloc[0:0]).keys())

beavers = []
for _BV in _BV_TOURNAMENTS:
    def _bvname(n, _BV=_BV):
        return _BV.get('alias', {}).get(n, n)

    _bvbat, _bvpit, _bvgames = {}, {}, []
    for _g in _BV['games']:
        gr = {k: _g[k] for k in ('g', 'phase', 'opp', 'ha', 'res', 'rf', 'ra', 'gid', 'time',
                                 'innings', 'line_bea', 'line_opp', 'he_bea', 'he_opp')}
        gr['date'] = _BV['meta']['date']
        gr['opp_note'] = _g.get('opp_note', '')
        gr['bat'], gr['pit'] = [], []
        gr['opp_bat'] = [dict(zip(_BV_BAT_COLS, tuple(r))) for r in _g.get('opp_bat', [])]
        gr['opp_pit'] = [dict(zip(_BV_PIT_COLS, tuple(r))) for r in _g.get('opp_pit', [])]
        for r in _g['bat']:
            nm = _bvname(r[0])
            e = dict(zip(('n', 'ab', 'r', 'h', 'rbi', 'bb', 'k', '2b', '3b', 'hr'),
                         (nm,) + tuple(r[1:])))
            gr['bat'].append(e)
            d = _bvbat.setdefault(nm, dict.fromkeys(
                ('G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'K'), 0))
            d['G'] += 1
            for a, b in (('AB', 'ab'), ('R', 'r'), ('H', 'h'), ('2B', '2b'), ('3B', '3b'),
                         ('HR', 'hr'), ('RBI', 'rbi'), ('BB', 'bb'), ('K', 'k')):
                d[a] += e[b]
        for r in _g['pit']:
            nm = _bvname(r[0])
            e = dict(zip(('n', 'ip', 'h', 'r', 'er', 'bb', 'k', 'w', 'l', 'sv'),
                         (nm,) + tuple(r[1:])))
            gr['pit'].append(e)
            d = _bvpit.setdefault(nm, dict.fromkeys(
                ('G', 'IPouts', 'pH', 'pR', 'ER', 'pBB', 'pK', 'W', 'L', 'SV'), 0))
            d['G'] += 1
            for a, b in (('IPouts', 'ip'), ('pH', 'h'), ('pR', 'r'), ('ER', 'er'),
                         ('pBB', 'bb'), ('pK', 'k'), ('W', 'w'), ('L', 'l'), ('SV', 'sv')):
                d[a] += e[b]
        _bvgames.append(gr)

    for nm, d in _bvbat.items():
        s1 = d['H'] - d['2B'] - d['3B'] - d['HR']
        d['TB'] = s1 + 2 * d['2B'] + 3 * d['3B'] + 4 * d['HR']
        d['PA'] = d['AB'] + d['BB']

    beavers.append({
        'team': _BV['team'], 'meta': _BV['meta'], 'games': _bvgames,
        'batting': [dict(v, name=k) for k, v in _bvbat.items()],
        'pitching': [dict(v, name=k) for k, v in _bvpit.items()],
        'inRegister': sorted(n for n in set(_bvbat) | set(_bvpit) if n in players),
    })

    # --- also drop this tournament's line onto each player's profile as an
    #     "NWLA" phase (kept fully separate from league regular/postseason).
    for _nm in set(_bvbat) | set(_bvpit):
        _pl = players.get(_nm)
        if _pl is None:
            continue
        _row = {k: 0 for k in _AGGZ}
        _b = _bvbat.get(_nm)
        if _b:
            _row.update({
                'G_bat': _b['G'], 'GS_bat': _b['G'], 'PA': _b['PA'], 'AB': _b['AB'],
                'R': _b['R'], 'H': _b['H'], '2B': _b['2B'], '3B': _b['3B'], 'HR': _b['HR'],
                '1B': _b['H'] - _b['2B'] - _b['3B'] - _b['HR'], 'RBI': _b['RBI'],
                'BB': _b['BB'], 'K': _b['K'], 'TB': _b['TB'],
            })
        _p = _bvpit.get(_nm)
        if _p:
            _row.update({
                'G_pit': _p['G'], 'IPouts': _p['IPouts'], 'pH': _p['pH'], 'pR': _p['pR'],
                'ER': _p['ER'], 'pBB': _p['pBB'], 'pK': _p['pK'],
                'W': _p['W'], 'L': _p['L'], 'SV': _p['SV'],
            })
        _row.update({'year': int(_BV['meta']['date'][:4]), 'type': 'NWLA',
                     'team': _BV['team'], 'teamPartial': False})
        _pl['seasons'].append(_row)
        _pl['seasons'].sort(key=lambda r: (r['year'], r['type'],
                                           0 if r.get('split') else (2 if r.get('tot') else 1)))

# ============================ NO-HITTERS / PERFECT GAMES =================
# Official league-kept list (curated by hand, not derived from box scores) —
# supersedes any box-score heuristic. Rows stop at the first blank line; the
# hand-tallied summary table below that is stale (missing 2026 entries) and
# is ignored in favor of tallying the detail rows ourselves.
_NH_MONTHS = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
              'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11,
              'December': 12}

def _nh_date(s):
    s = s.strip()
    post = s.endswith('*')
    if post:
        s = s[:-1].strip()
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{2})$', s)
    if m:
        mo, d, yy = int(m.group(1)), int(m.group(2)), int(m.group(3))
        yr = 2000 + yy
        return f'{yr:04d}-{mo:02d}-{d:02d}', yr, post
    m2 = re.match(r'^([A-Za-z]+)\s+(\d{4})$', s)
    if m2:
        yr = int(m2.group(2))
        mo = _NH_MONTHS.get(m2.group(1), 0)
        return (f'{yr:04d}-{mo:02d}' if mo else str(yr)), yr, post
    return s, None, post

def _nh_team(yr, name):
    name = NICK_FIX.get(name, name)
    return canon_team(yr, name) if yr else _prefixed(name)

noHitters = []
with open(DL + 'Career_All-Time Franchise & League Individual Stats - '
          'No Hitters_Perfect Games.csv', encoding='latin-1', newline='') as fh:
    _NHR = list(csv.reader(fh))
_NHH = {k: i for i, k in enumerate(_NHR[0])}
for r in _NHR[1:]:
    player_raw = r[_NHH['Player']].strip()
    if not player_raw:
        break  # blank separator row -> stop before the stale summary table
    date_iso, yr, post = _nh_date(r[_NHH['Date']])
    pk = pkey(player_raw)
    team = _nh_team(yr, r[_NHH['Team']].strip())
    opp = _nh_team(yr, r[_NHH['Opponent']].strip())
    ip = float(r[_NHH['IP']] or 0)
    # link to a box score when one exists for this date/matchup (mostly 2020+)
    gid = None
    if date_iso and len(date_iso) == 10:
        for gg in games.values():
            if gg['date'] == date_iso and {gg['away']['team'], gg['home']['team']} == {team, opp}:
                gid = gg['gid']
                break
    noHitters.append({
        'player': pk or player_raw, 'team': team, 'opp': opp,
        'field': r[_NHH['Field']].strip(), 'date': date_iso,
        'dateDisplay': r[_NHH['Date']].strip().rstrip('*'),
        'ip': round(ip * 3), 'bb': int(r[_NHH['BB']] or 0), 'k': int(r[_NHH['K']] or 0),
        'score': r[_NHH['Score']].strip(),
        'perfect': r[_NHH['Result']].strip() == 'Perfect Game',
        'postseason': post, 'notes': r[_NHH['Notes']].strip(), 'gid': gid,
    })
noHitters.sort(key=lambda x: (x['date'] or '', x['player']))

out = {'players': players, 'teams': teams, 'games': games, 'champs': champs,
       'divisions': divisions, 'beavers': beavers, 'playoffs': playoffs,
       'awards': awards, 'asg': asg, 'noHitters': noHitters,
       'nick2full': nick2full, 'ambiguous2017': [],
       'generated': pd.Timestamp.now().strftime('%Y-%m-%d'),
       'seasonRange': [2016 if INCLUDE_2016 else int(df['Year'].min()),
                       2026 if INCLUDE_2026 else int(df['Year'].max())],
       'nPlayers': len(players)}
json.dump(out, open('players.json','w'), separators=(',',':'))
print('players:', len(players), 'json bytes:', len(open('players.json').read()))
# quick check
pg = players['Parker Gibbons']['career']
print('Parker career H/AB', pg['H'], pg['AB'], round(pg['H']/pg['AB'],3), 'HR', pg['HR'], 'IPouts', pg['IPouts'], 'ERA', round(9*pg['ER']/(pg['IPouts']/3),2))
