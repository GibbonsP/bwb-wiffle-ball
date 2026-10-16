"""Add the 2016 All-Star Game (South 3, North 2, 6/23/16) to players.json['games'] as a score-only game."""
import json
d = json.load(open('players.json'))
assert not any(g['phase']=='AllStar' and g['date'].startswith('2016') for g in d['games'].values())
side = lambda team, r: {'team':team, 'line':[], 'R':r, 'H':0, 'E':0, 'bat':[], 'pit':[]}
gid = 20160094
d['games'][str(gid)] = {'gid':gid, 'date':'2016-06-23', 'dt':'2016-06-23T19:00:00', 'div':'2016 All-Star Game', 'phase':'AllStar',
                        'loc':'TBA', 'innings':3, 'away':side('South Division', 3), 'home':side('North Division', 2), 'noBox':True}
json.dump(d, open('players.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print('games now', len(d['games']))
