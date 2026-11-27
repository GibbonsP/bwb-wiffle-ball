"""Adds the 2015 season to players.json.
Known: standings, game scores, and per-player HR/RBI/W/L/ER/IP/SV. Everything else (PA/AB/H/2B/3B/BB/K/HBP/R, hits-walks-strikeouts allowed, games)
is estimated with empirical-Bayes shrinkage models fitted on the 2016-2020 era (same 3-inning game / HBP rules), tied to league totals."""
import json,re,csv,sys,collections,copy
import numpy as np,pandas as pd
from sklearn.linear_model import LinearRegression
sys.path.insert(0,'.')
from model15 import lg_rate,own_rate
RAW=open('../players.json').read();TAIL=RAW[len(RAW.rstrip('\n')):]
d=json.loads(RAW);P=d['players'];T=d['teams']
assert '2015' not in T['Brookside Panthers']['seasons'],'2015 already added'
NICK={'Panthers':'Brookside Panthers','Eagles':'Brookside Kraken','Manatees':'Beaver Brook Lavahogs','Wicked Aces':'Brentwood Aces','Aces':'Brentwood Aces',
      'Mustangs':'Brentwood Mustangs','Flying Squirrels':'Brookside Squirrels','Squirrels':'Brookside Squirrels'}
NAMEFIX={'Nima Khodakdah':'Nima Khodakhah'}
TG=40
_g=json.load(open('games2015.json'))
PLAYED=collections.Counter()
for _x in _g:
    if _x['phase']=='Regular':
        PLAYED[NICK[_x['a'][0]]]+=1;PLAYED[NICK[_x['h'][0]]]+=1   # forfeits (in the standings, not on the game list) carry no stats
# ---------- training frame (2016-2020 regular season, real fields) ----------
rec=[]
for n,p in P.items():
    for s in p['seasons']:
        if s['type']=='Regular' and not s.get('tot') and not s.get('split') and s.get('team') and 2016<=s['year']<=2020:
            r={k:s.get(k,0) or 0 for k in ['G_bat','AB','H','1B','2B','3B','HR','RBI','BB','K','HBP','R','PA','G_pit','IPouts','ER','pH','pBB','pK','W','L','SV']}
            r.update(name=n,year=s['year']);rec.append(r)
tr=pd.DataFrame(rec)
tr_bat=tr[tr.PA>=6];tr_bat17=tr_bat[tr_bat.year!=2016]
tr_pit=tr[tr.IPouts>=6];tr_pit17=tr_pit[tr_pit.year!=2016]
# ---------- 2015 inputs ----------
rows=[]
for r in csv.DictReader(open('/Users/parkergibbons/Downloads/2015 BWB Stats - Sheet1.csv')):
    f=lambda k:float(r[k]) if r[k].strip() else 0.0
    nm=NAMEFIX.get(r['Player'],r['Player'])
    teams=[{'Aces':'Wicked Aces'}.get(t,t) for t in r['Teams'].split('/')]
    rows.append(dict(name=nm,teams=[NICK[t] for t in teams],HR=int(f('HR')),RBI=int(f('RBI')),W=int(f('W')),L=int(f('L')),SV=int(f('SV')),
                     ER=int(f('ER')),IPouts=int(round(f('IP')*3)),ERA=f('ERA')))
F=pd.DataFrame(rows)
# CSV sanity: ERA*IP/3 ~ ER
chk=F[(F.IPouts>0)&(F.ERA>0)];print('ERA/ER consistency max abs diff',round(float((chk.ER-chk.ERA*chk.IPouts/9).abs().max()),2))
# ---------- batting model ----------
K=dict(PA=80,H=100,BB=30,K=30,HBP=30,B2=100,B3=100,R=100)
lgPA=lg_rate(tr_bat,'PA','RBI')
trn=tr_bat.assign(nh=tr_bat.H-tr_bat.HR,den=tr_bat.PA-tr_bat.HR);lg_nh=lg_rate(trn,'nh','den')
trn17=tr_bat17.assign(nh=tr_bat17.H-tr_bat17.HR)
lg_BB=lg_rate(tr_bat,'BB','PA');lg_HBP=lg_rate(tr_bat,'HBP','PA');lg_K=lg_rate(tr_bat17,'K','PA')
lg_2B=lg_rate(trn17,'2B','nh');lg_3B=lg_rate(trn17,'3B','nh');lg_R=lg_rate(tr_bat17,'R','RBI')
gm=LinearRegression(fit_intercept=False).fit(tr_bat[['PA']],tr_bat.G_bat)
pg=LinearRegression(fit_intercept=False).fit(tr_pit[['IPouts']],tr_pit.G_pit)
pit_h=LinearRegression(fit_intercept=False).fit(tr_pit17[['IPouts','ER']],tr_pit17.pH)
lg_pBB=lg_rate(tr_pit17,'pBB','IPouts');lg_pK=lg_rate(tr_pit,'pK','IPouts')
bat={};pit={}
for _,r in F.iterrows():
    n=r['name']
    if r.RBI+r.HR>0:
        PA=r.RBI*own_rate(tr_bat,n,'PA','RBI',K['PA'],lgPA);PA=max(PA,r.HR+(1 if r.RBI>0 else 0),1)
        nh=max(PA-r.HR,0)*own_rate(trn,n,'nh','den',K['H'],lg_nh)
        bat[n]=dict(PA=PA,HR=r.HR,RBI=r.RBI,nh=nh,
            BB=PA*own_rate(tr_bat,n,'BB','PA',K['BB'],lg_BB),HBP=PA*own_rate(tr_bat,n,'HBP','PA',K['HBP'],lg_HBP),
            K=PA*own_rate(tr_bat17,n,'K','PA',K['K'],lg_K),
            b2=nh*own_rate(trn17,n,'2B','nh',K['B2'],lg_2B),b3=nh*own_rate(trn17,n,'3B','nh',K['B3'],lg_3B),
            R=max(r.RBI*own_rate(tr_bat17,n,'R','RBI',K['R'],lg_R),r.HR))
    if r.IPouts>0:
        o=tr_pit17[tr_pit17.name==n];base=pit_h.predict(pd.DataFrame({'IPouts':[r.IPouts],'ER':[r.ER]}))[0]
        if len(o):
            bo=pit_h.predict(o[['IPouts','ER']]).sum();w=o.IPouts.sum()/(o.IPouts.sum()+120);base*=(w*(o.pH.sum()/bo)+(1-w)) if bo>0 else 1
        pit[n]=dict(IPouts=r.IPouts,ER=r.ER,pH=base,
                    pBB=r.IPouts*own_rate(tr_pit17,n,'pBB','IPouts',30,lg_pBB),
                    pK=r.IPouts*own_rate(tr_pit,n,'pK','IPouts',30,lg_pK),
                    G=max(1,round(pg.predict(pd.DataFrame({'IPouts':[r.IPouts]}))[0])))
# league ties: hits & walks allowed = hits & walks drawn; strikeouts: batter total = pitcher total = their mean
sH=sum(v['nh']+v['HR'] for v in bat.values());sBB=sum(v['BB'] for v in bat.values())
for k,tot in (('pH',sH),('pBB',sBB)):
    f=tot/sum(v[k] for v in pit.values())
    for v in pit.values():v[k]*=f
sK=(sum(v['K'] for v in bat.values())+sum(v['pK'] for v in pit.values()))/2
for dct,k in ((bat,'K'),(pit,'pK')):
    f=sK/sum(v[k] for v in dct.values())
    for v in dct.values():v[k]*=f
def alloc(vals,total=None):
    total=round(sum(vals)) if total is None else total;fl=[int(np.floor(x)) for x in vals];rem=total-sum(fl)
    for i in sorted(range(len(vals)),key=lambda i:-(vals[i]-fl[i]))[:max(rem,0)]:fl[i]+=1
    return fl
bn=list(bat);pn=list(pit)
for k in ('BB','K','HBP','R'):
    for n,v in zip(bn,alloc([bat[n][k] for n in bn])):bat[n][k+'i']=v
hv=alloc([bat[n]['nh']+bat[n]['HR'] for n in bn])
for n,v in zip(bn,hv):bat[n]['Hi']=v
for k in ('pH','pBB','pK'):
    tot=round(sum(pit[n][k] for n in pn))
    for n,v in zip(pn,alloc([pit[n][k] for n in pn])):pit[n][k+'i']=v
# integer batting lines
B={}
CAP={r['name']:sum(PLAYED[t] for t in r['teams']) for _,r in F.iterrows()}
for n in bn:
    v=bat[n];PA=int(round(v['PA']));H=v['Hi'];HR=v['HR'];BB=v['BBi'];HBP=v['HBPi'];AB=PA-BB-HBP
    if AB<H:AB=H;PA=AB+BB+HBP
    H=max(H,HR)
    b2=int(round(v['b2']));b3=int(round(v['b3']))
    while b2+b3>H-HR:
        if b2>=b3 and b2>0:b2-=1
        elif b3>0:b3-=1
        else:break
    b1=H-HR-b2-b3;PA=AB+BB+HBP
    B[n]=dict(G_bat=int(min(max(round(gm.predict(pd.DataFrame({'PA':[PA]}))[0]),1),CAP[n])),AB=AB,R=max(v['Ri'],HR),**{'1B':b1,'2B':b2,'3B':b3},HR=HR,RBI=v['RBI'],BB=BB,K=min(v['Ki'],max(AB-H,0)),HBP=HBP,H=H,PA=PA,TB=b1+2*b2+3*b3+4*HR)
Pt={}
for n in pn:
    v=pit[n];r=F[F.name==n].iloc[0]
    Pt[n]=dict(G_pit=min(max(v['G'],int(r.W+r.L+r.SV)),CAP[n]),IPouts=v['IPouts'],pR=int(v['ER']),ER=int(v['ER']),pH=v['pHi'],pBB=v['pBBi'],pK=v['pKi'],W=int(r.W),L=int(r.L),SV=int(r.SV))
ZERO=['SB','CS','SF','SH','pHB','CG','BS','G_fld','INN','TC','PO','A','E','DP','GS_pit']
# ---------- games / teams ----------
games=json.load(open('games2015.json'));GM={}
nextgid=20150001
for g in games:
    (a,ar),(h,hr)=g['a'],g['h'];ta,th=NICK[a],NICK[h]
    gid=nextgid;nextgid+=1
    GM[str(gid)]={'gid':gid,'date':g['date'],'dt':g['date']+'T12:00:00','div':'2015 BWB Season','phase':g['phase'],'loc':'TBA','innings':3,
        'away':{'team':ta,'line':[],'R':ar,'H':0,'E':0,'bat':[],'pit':[]},'home':{'team':th,'line':[],'R':hr,'H':0,'E':0,'bat':[],'pit':[]},'noBox':True}
OFFICIAL={'Brookside Panthers':(24,16),'Brookside Kraken':(30,10),'Brentwood Aces':(21,19),'Brookside Squirrels':(20,20),'Beaver Brook Lavahogs':(15,25),'Brentwood Mustangs':(7,33)}
NB={'Brookside Panthers':'Panthers','Brookside Kraken':'Eagles','Brentwood Aces':'Wicked Aces','Brookside Squirrels':'Squirrels','Beaver Brook Lavahogs':'Manatees','Brentwood Mustangs':'Mustangs'}
tgames=collections.defaultdict(list)
for gid,g in GM.items():
    for me,opp,mr,orr,ha in ((g['away']['team'],g['home']['team'],g['away']['R'],g['home']['R'],'A'),(g['home']['team'],g['away']['team'],g['home']['R'],g['away']['R'],'H')):
        tgames[me].append({'date':g['date'],'opp':opp,'ha':ha,'rf':mr,'ra':orr,'res':'W' if mr>orr else 'L','phase':g['phase']})
def prec(tm,ph):
    gs=[x for x in tgames[tm] if x['phase']==ph];w=sum(x['res']=='W' for x in gs);l=len(gs)-w
    return w,l,sum(x['rf'] for x in gs),sum(x['ra'] for x in gs),len(gs)
if 'Brookside Squirrels' not in T:
    T['Brookside Squirrels']={'name':'Brookside Squirrels','loc':'Brookside','nick':'Squirrels','seasons':{},'years':[],'nameByYear':{},'record':{'W':0,'L':0,'T':0,'RF':0,'RA':0},'firstYear':2015,'lastYear':2015,'aka':[],'logo':None,'logoHistory':[],'banners':[]}
# split players' stat lines across teams
def split_even(val,n):
    base=[val//n]*n
    for i in range(val-sum(base)):base[i]+=1
    return base
teamroster=collections.defaultdict(list);newplayers=0
allnames=set(bat)|set(pit)|set(F.name)
for n in F.name:
    r=F[F.name==n].iloc[0];teams=r.teams;nt=len(teams)
    line={}
    if n in B:line.update(B[n])
    if n in Pt:line.update(Pt[n])
    full={k:0 for k in P[next(iter(P))]['careerReg']}   # all stat keys
    full.update(line)
    if n not in P:
        newplayers+=1
        z={k:0 for k in full}
        P[n]={'name':n,'career':dict(z),'careerReg':dict(z),'careerPO':dict(z),'seasons':[],'years':[],'teamsByYear':{},'gids':[],'firstDate':'2015-03-27','lastDate':'2015-09-22','honors':{'rings':[],'awards':[],'asg':[]}}
    p=P[n]
    first=min(x['date'] for tm in teams for x in tgames[tm]);last=max(x['date'] for tm in teams for x in tgames[tm])
    if n in P and p['seasons'] and any(s['year']>2015 for s in p['seasons']):
        p['firstDate']=min(p.get('firstDate') or first,first)
    else:p['firstDate'],p['lastDate']=first,last
    if nt==1:
        row=dict(full);row.update(year=2015,type='Regular',team=teams[0],teamPartial=False)
        p['seasons'].append(row);teamroster[teams[0]].append({'name':n,'regular':{k:v for k,v in full.items()}})
    else:
        rows_=[]
        for i,tm in enumerate(teams):
            sp={}
            for k,v in full.items():
                sp[k]=split_even(int(v),nt)[i] if isinstance(v,(int,np.integer)) else v
            sp.update(year=2015,type='Regular',team=tm,teamPartial=False,split=True);rows_.append(sp)
            teamroster[tm].append({'name':n,'regular':{k:v for k,v in sp.items() if k not in('year','type','team','teamPartial','split')}})
        # fix 1B/TB/PA consistency after the even split
        for sp in rows_:
            sp['1B']=max(sp['H']-sp['2B']-sp['3B']-sp['HR'],0);sp['TB']=sp['1B']+2*sp['2B']+3*sp['3B']+4*sp['HR'];sp['PA']=sp['AB']+sp['BB']+sp['HBP']
        for rr in teamroster:pass
        tot=dict(full);tot.update(year=2015,type='Regular',team=None,teamPartial=False,tot=True,nTeams=nt)
        p['seasons'].extend(rows_+[tot])
    p['seasons'].sort(key=lambda r:(r['year'],r['type'],0 if r.get('split') else (2 if r.get('tot') else 1)))
    p['years']=sorted(set(p['years'])|{2015});p['teamsByYear']['2015']={'team':' / '.join(teams),'partial':False} if False else None
    p['teamsByYear'].pop('2015',None);p['teamsByYear'][2015 if False else '2015']={'team':' / '.join(teams) if nt>1 else teams[0],'partial':False}
    for k,v in full.items():
        if k in p['careerReg']:
            p['careerReg'][k]=p['careerReg'].get(k,0)+v;p['career'][k]=p['career'].get(k,0)+v
# NOTE roster stat rows on split players must equal split rows (done above); recompute 1B etc already.
for tm,nick in NB.items():
    w,l,rf,ra,gn=prec(tm,'Regular');W,L=OFFICIAL[tm]
    RF,RA=rf,ra   # forfeits have no runs, so team runs are just the recorded games
    pw,pl,prf,pra,pg_=prec(tm,'Playoffs')
    ts=T[tm];ts['seasons']['2015']={'roster':teamroster.get(tm,[]),'name':nick,'games':tgames[tm],
        'record':{'Regular':{'W':W,'L':L,'T':0,'RF':RF,'RA':RA},**({'Playoffs':{'W':pw,'L':pl,'T':0,'RF':prf,'RA':pra}} if pg_ else {})}}
    ts['years']=sorted(set(ts['years'])|{2015});ts['firstYear']=min(ts['firstYear'],2015);ts['nameByYear']['2015']=nick
    ts['record']={'W':ts['record']['W']+W,'L':ts['record']['L']+l*0+L,'T':ts['record'].get('T',0),'RF':ts['record']['RF']+RF,'RA':ts['record']['RA']+RA}
    if tm=='Brookside Squirrels':ts['lastYear']=2015
d['games'].update(GM)
d['divisions']['2015']={'North':[['Brookside Panthers','^'],['Brentwood Aces','*'],['Beaver Brook Lavahogs','']],'South':[['Brookside Kraken','^'],['Brookside Squirrels','*'],['Brentwood Mustangs','']]}
d['playoffs']['2015']['brookside']['series']=[[10,9]];d['playoffs']['2015']['brentwood']['series']=[[9,7]];d['playoffs']['2015']['finalSeries']=[[6,0],[7,4]]
d['seasonRange']=[2015,d['seasonRange'][1]];d['nPlayers']=d['nPlayers']+newplayers
open('players.json.new','w').write(json.dumps(d,ensure_ascii=False,separators=(',',':'))+TAIL)
# ---------- report ----------
print('new players',newplayers,'bat rows',len(B),'pit rows',len(Pt))
print('league H',sum(v['H'] for v in B.values()),'pH',sum(v['pH'] for v in Pt.values()),'BB',sum(v['BB'] for v in B.values()),'pBB',sum(v['pBB'] for v in Pt.values()),'K',sum(v['K'] for v in B.values()),'pK',sum(v['pK'] for v in Pt.values()))
print('PA',sum(v['PA'] for v in B.values()),'AB',sum(v['AB'] for v in B.values()),'R',sum(v['R'] for v in B.values()),'RBI',sum(v['RBI'] for v in B.values()),'IP',sum(v['IPouts'] for v in Pt.values())/3)
for n in ['Parker Gibbons','Peter Fraioli','Victor Cottini','AJ Cefaloni','Griffin Krueger','Joey Cardascia']:
    if n in B:b=B[n];print(n.ljust(16),'G',b['G_bat'],'AB',b['AB'],'H',b['H'],'avg',round(b['H']/b['AB'],3),'HR',b['HR'],'RBI',b['RBI'],'R',b['R'],'BB',b['BB'],'K',b['K'],'HBP',b['HBP'],'2B',b['2B'],'|',Pt.get(n))
