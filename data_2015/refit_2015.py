"""Re-estimates the 2015 hitting/pitching lines once each player's games played are known (supplied by the league).
Run from this folder; rewrites ../players.json in place (keeps jerseys, logos, awards, etc.)."""
import json,csv,collections,sys
import numpy as np,pandas as pd
from sklearn.linear_model import LinearRegression
sys.path.insert(0,'.')
from model15 import lg_rate,own_rate
RAW=open('../players.json').read();TAIL=RAW[len(RAW.rstrip('\n')):];d=json.loads(RAW);P=d['players'];T=d['teams']
NICK={'Panthers':'Brookside Panthers','Kraken':'Brookside Kraken','Lavahogs':'Beaver Brook Lavahogs','Aces':'Brentwood Aces','Mustangs':'Brentwood Mustangs','Squirrels':'Brookside Squirrels'}
GP_TXT="""Panthers|Peter Fraioli 36|Victor Cottini 20
Kraken|Parker Gibbons 26|TJ Fuerst 7|Alex Homem 5|Brandon Groothius 2|Michael Sullivan 3|Nima Khodakhah 1|Will DeLuca 3
Lavahogs|Brandon Gibbons 26|Darien Sharpe 5|Evan Wilkins 1|Lucas Snider 3|Mathew Wilkins 1|Nou Matsushita 3|Pat Rucci 1|Tarif Sabur 3
Aces|AJ Cefaloni 31|Ava Cefaloni 3|Austin Corvino 20|James Choi 15|Victor Arcara 3|Christian Cefaloni 2|David Cross 5|Dean Corvino 3|Mark Scocchera 3|Peter Sposato 5|Raff Greco 3|Ryan Becton 3
Mustangs|Griffin Krueger 25|Vinny Spoto 2|James Choi 5|Victor Arcara 5|Peter Sposato 10|Tochi Onwuasoanya 8|Troy Straus 2|Ben Groothius 2|Landon Krueger 2
Squirrels|Joey Cardascia 22|Vinny Spoto 12"""
GP={}
for line in GP_TXT.splitlines():
    parts=line.split('|');tm=NICK[parts[0]]
    for x in parts[1:]:
        nm,g=x.rsplit(' ',1);GP[(nm,tm)]=int(g)
PLAYED={}
for tm in NICK.values():PLAYED[tm]=len([g for g in T[tm]['seasons']['2015']['games'] if g['phase']=='Regular'])
RF={tm:T[tm]['seasons']['2015']['record']['Regular']['RF'] for tm in PLAYED}
for (n,tm),g in GP.items(): assert g<=PLAYED[tm],(n,tm,g,PLAYED[tm])
# sheet totals
F={}
for r in csv.DictReader(open('/Users/parkergibbons/Downloads/2015 BWB Stats - Sheet1.csv')):
    f=lambda k:float(r[k]) if r[k].strip() else 0.0
    nm={'Nima Khodakdah':'Nima Khodakhah'}.get(r['Player'],r['Player'])
    F[nm]=dict(HR=int(f('HR')),RBI=int(f('RBI')),W=int(f('W')),L=int(f('L')),SV=int(f('SV')),ER=int(f('ER')),IPouts=int(round(f('IP')*3)))
for (n,tm) in GP: assert n in F,n
# ---- training (2016-2020 regular season; real fields only) ----
rec=[]
for n,p in P.items():
    for s in p['seasons']:
        if s['type']=='Regular' and not s.get('tot') and not s.get('split') and s.get('team') and 2016<=s['year']<=2020:
            r={k:s.get(k,0) or 0 for k in ['G_bat','AB','H','1B','2B','3B','HR','RBI','BB','K','HBP','R','PA','G_pit','IPouts','ER','pH','pBB','pK','W','L','SV']};r.update(name=n,year=s['year']);rec.append(r)
tr=pd.DataFrame(rec);tb=tr[(tr.PA>=6)&(tr.G_bat>0)];tb17=tb[tb.year!=2016];tp=tr[tr.IPouts>=6];tp17=tp[tp.year!=2016]
pam=LinearRegression(fit_intercept=False).fit(tb[['G_bat','RBI']],tb.PA)
pred_tb=pam.predict(tb[['G_bat','RBI']]);tb=tb.assign(pa_pred=pred_tb)
def pa_est(n,G,RBI):
    base=float(pam.predict(pd.DataFrame({'G_bat':[G],'RBI':[RBI]}))[0]);o=tb[tb.name==n]
    if len(o):
        k=80;m=o.RBI.sum();ratio=o.PA.sum()/o.pa_pred.sum();w=m/(m+k);base*=w*ratio+(1-w)
    return base
trn=tb.assign(nh=tb.H-tb.HR,den=tb.PA-tb.HR);trn17=tb17.assign(nh=tb17.H-tb17.HR)
lg_nh=lg_rate(trn,'nh','den');lg_BB=lg_rate(tb,'BB','PA');lg_HBP=lg_rate(tb,'HBP','PA');lg_K=lg_rate(tb17,'K','PA')
lg_2B=lg_rate(trn17,'2B','nh');lg_3B=lg_rate(trn17,'3B','nh');lg_R=lg_rate(tb17,'R','RBI')
pg=LinearRegression(fit_intercept=False).fit(tp[['IPouts']],tp.G_pit)
pit_h=LinearRegression(fit_intercept=False).fit(tp17[['IPouts','ER']],tp17.pH)
lg_pBB=lg_rate(tp17,'pBB','IPouts');lg_pK=lg_rate(tp,'pK','IPouts')
# ---- fixed / league-supplied lines ----
FIXED_RATES={'Parker Gibbons':dict(BB=113/576,K=90/576,HBP=31/576,AVG=.575)}
FIXED_LINE={('Evan Wilkins','Beaver Brook Lavahogs'):dict(G_bat=1,AB=5,H=5,**{'1B':1,'2B':0,'3B':0},BB=2,K=0,HBP=1,PA=8,R=7,TB=17)}
# ---- split each player's sheet totals across his clubs by games played ----
def split_int(v,w):
    w=np.array(w,float);raw=v*w/w.sum();fl=np.floor(raw).astype(int);rem=int(v-fl.sum())
    for i in np.argsort(-(raw-fl))[:rem]:fl[i]+=1
    return list(fl)
teams_of=collections.defaultdict(list)
for (n,tm),g in GP.items():teams_of[n].append((tm,g))
per={}   # (name,team)-> inputs
for n,tl in teams_of.items():
    ws=[g for _,g in tl];sp={k:split_int(F[n][k],ws) for k in F[n]}
    for i,(tm,g) in enumerate(tl):per[(n,tm)]={'G':g,**{k:sp[k][i] for k in sp}}
# ---- estimate ----
bat={};pit={}
for key,v in per.items():
    n,tm=key
    G,RBI,HR=v['G'],v['RBI'],v['HR']
    if key not in FIXED_LINE:
        PA=max(pa_est(n,G,RBI),HR+(1 if RBI>0 else 0),1);PA=min(PA,G*21.7) if PA>G*21.7 else PA
        PA=max(PA,HR+(1 if RBI>0 else 0))
        nh=max(PA-HR,0)*own_rate(trn,n,'nh','den',100,lg_nh)
        b=dict(G=G,PA=PA,HR=HR,RBI=RBI,nh=nh,BB=PA*own_rate(tb,n,'BB','PA',30,lg_BB),HBP=PA*own_rate(tb,n,'HBP','PA',30,lg_HBP),K=PA*own_rate(tb17,n,'K','PA',30,lg_K),
               b2=nh*own_rate(trn17,n,'2B','nh',100,lg_2B),b3=nh*own_rate(trn17,n,'3B','nh',100,lg_3B),R=max(RBI*own_rate(tb17,n,'R','RBI',100,lg_R),HR))
        if n in FIXED_RATES:
            fr=FIXED_RATES[n];b['BB']=PA*fr['BB'];b['K']=PA*fr['K'];b['HBP']=PA*fr['HBP'];AB=PA-b['BB']-b['HBP'];b['nh']=fr['AVG']*AB-HR;b['fixed']=True
        bat[key]=b
    if v['IPouts']>0:
        base=float(pit_h.predict(pd.DataFrame({'IPouts':[v['IPouts']],'ER':[v['ER']]}))[0]);o=tp17[tp17.name==n]
        if len(o):
            bo=pit_h.predict(o[['IPouts','ER']]).sum();w=o.IPouts.sum()/(o.IPouts.sum()+120);base*=(w*(o.pH.sum()/bo)+(1-w)) if bo>0 else 1
        pit[key]=dict(IPouts=v['IPouts'],ER=v['ER'],pH=base,pBB=v['IPouts']*own_rate(tp17,n,'pBB','IPouts',30,lg_pBB),pK=v['IPouts']*own_rate(tp,n,'pK','IPouts',30,lg_pK),
                      G=min(G,max(1,int(round(float(pg.predict(pd.DataFrame({'IPouts':[v['IPouts']]}))[0]))),v['W']+v['L']+v['SV'])),W=v['W'],L=v['L'],SV=v['SV'])
# runs: each club's hitters score its real runs total
for tm in PLAYED:
    keys=[k for k in bat if k[1]==tm and not bat[k].get('fixed_line')];fixed=sum(FIXED_LINE[k]['R'] for k in FIXED_LINE if k[1]==tm)
    s=sum(bat[k]['R'] for k in keys)
    for k in keys:bat[k]['R']*= (RF[tm]-fixed)/s
# fixed-line players enter the league ties as given
fixedH=sum(v['H'] for v in FIXED_LINE.values());fixedBB=sum(v['BB'] for v in FIXED_LINE.values())
sH=sum(b['nh']+b['HR'] for b in bat.values())+fixedH;sBB=sum(b['BB'] for b in bat.values())+fixedBB
for kk,tot in (('pH',sH),('pBB',sBB)):
    f=tot/sum(p[kk] for p in pit.values())
    for p in pit.values():p[kk]*=f
freeK=[b for b in bat.values() if not b.get('fixed')];fixK=sum(b['K'] for b in bat.values() if b.get('fixed'))+sum(v['K'] for v in FIXED_LINE.values())
sK=(sum(b['K'] for b in bat.values())+sum(v['K'] for v in FIXED_LINE.values())+sum(p['pK'] for p in pit.values()))/2
f=(sK-fixK)/sum(b['K'] for b in freeK)
for b in freeK:b['K']*=f
f=sK/sum(p['pK'] for p in pit.values())
for p in pit.values():p['pK']*=f
def alloc(vals,total=None):
    total=round(sum(vals)) if total is None else total;fl=[int(np.floor(x)) for x in vals];rem=total-sum(fl)
    for i in sorted(range(len(vals)),key=lambda i:-(vals[i]-fl[i]))[:max(rem,0)]:fl[i]+=1
    return fl
bk=list(bat);pk=list(pit)
for k in ('BB','K','HBP','R'):
    for key,v in zip(bk,alloc([bat[x][k] for x in bk])):bat[key][k+'i']=v
for key,v in zip(bk,alloc([bat[x]['nh']+bat[x]['HR'] for x in bk])):bat[key]['Hi']=v
for k in ('pH','pBB','pK'):
    for key,v in zip(pk,alloc([pit[x][k] for x in pk])):pit[key][k+'i']=v
NEW={}
for key in bk:
    v=bat[key];PA=int(round(v['PA']));H=v['Hi'];HR=v['HR'];BB=v['BBi'];HBP=v['HBPi'];AB=PA-BB-HBP
    if AB<H:AB=H;PA=AB+BB+HBP
    H=max(H,HR);b2=int(round(v['b2']));b3=int(round(v['b3']))
    while b2+b3>H-HR:
        if b2>=b3 and b2>0:b2-=1
        elif b3>0:b3-=1
        else:break
    b1=H-HR-b2-b3;PA=AB+BB+HBP
    NEW[key]=dict(G_bat=v['G'],AB=AB,R=max(v['Ri'],HR),**{'1B':b1,'2B':b2,'3B':b3},HR=HR,RBI=v['RBI'],BB=BB,K=min(v['Ki'],max(AB-H,0)),HBP=HBP,H=H,PA=PA,TB=b1+2*b2+3*b3+4*HR)
for key,line in FIXED_LINE.items():NEW[key]=dict(line,HR=per[key]['HR'],RBI=per[key]['RBI'])
for key in pk:
    p=pit[key];NEW.setdefault(key,{}).update(G_pit=p['G'],IPouts=p['IPouts'],pR=p['ER'],ER=p['ER'],pH=p['pHi'],pBB=p['pBBi'],pK=p['pKi'],W=p['W'],L=p['L'],SV=p['SV'])
# players with no pitching/hitting line: zero the other side
BATK=['G_bat','AB','R','1B','2B','3B','HR','RBI','BB','K','HBP','H','PA','TB'];PITK=['G_pit','IPouts','pR','ER','pH','pBB','pK','W','L','SV']
for key in per:
    NEW.setdefault(key,{})
    for k in BATK:NEW[key].setdefault(k,0)
    for k in PITK:NEW[key].setdefault(k,0)
# ---- write back ----
def roster_entry(tm,n):
    return [e for e in T[tm]['seasons']['2015']['roster'] if e['name']==n][0]
for (n,tm),vals in NEW.items():
    p=P[n];rows=[s for s in p['seasons'] if s['year']==2015 and s['type']=='Regular' and not s.get('tot') and s.get('team')==tm];assert len(rows)==1,(n,tm)
    row=rows[0]
    for k,v in vals.items():
        old=row.get(k,0)
        if v!=old:
            row[k]=v;p['careerReg'][k]=p['careerReg'].get(k,0)+(v-old);p['career'][k]=p['career'].get(k,0)+(v-old)
        roster_entry(tm,n)['regular'][k]=v
for n,p in P.items():
    sp=[s for s in p['seasons'] if s['year']==2015 and s['type']=='Regular' and s.get('split')];tot=[s for s in p['seasons'] if s['year']==2015 and s.get('tot')]
    if sp and tot:
        for k in BATK+PITK:tot[0][k]=sum(s.get(k,0) for s in sp)
out=json.dumps(d,ensure_ascii=False,separators=(',',':'),default=lambda o:int(o))+TAIL
bad=0
for n,p in P.items():
    for k in BATK+PITK:
        if sum(s.get(k,0) for s in p['seasons'] if s['type']=='Regular' and not s.get('tot') and s.get('team'))!=p['careerReg'].get(k,0):bad+=1;print('mismatch',n,k)
print('career mismatches',bad)
rows15=[s for p in P.values() for s in p['seasons'] if s['year']==2015 and s['type']=='Regular' and not s.get('tot') and s.get('team')]
print('H',sum(s['H'] for s in rows15),'pH',sum(s['pH'] for s in rows15),'BB',sum(s['BB'] for s in rows15),'pBB',sum(s['pBB'] for s in rows15),'K',sum(s['K'] for s in rows15),'pK',sum(s['pK'] for s in rows15))
for tm in PLAYED:
    r=[s for s in rows15 if s['team']==tm];print(tm.ljust(24),'G',PLAYED[tm],'R',sum(s['R'] for s in r),'RF',RF[tm],'PA',sum(s['PA'] for s in r),'RBI',sum(s['RBI'] for s in r))
if bad==0:
    open('../players.json','w').write(out);print('written')
