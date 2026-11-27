import pandas as pd,numpy as np
from sklearn.linear_model import LinearRegression
BAT=['H','BB','K','HBP','2B','3B','R']
def lg_rate(tr,num,den):return tr[num].sum()/max(tr[den].sum(),1e-9)
def own_rate(tr,name,num,den,k,lg):
    o=tr[tr.name==name];n=o[den].sum()
    return (o[num].sum()+k*lg)/(n+k) if n>0 else lg
def predict(target,tr,K):
    """target: rows with name,HR,RBI,IPouts,ER,W,L,SV,TG ; tr: training seasons (other years). K: dict of prior strengths."""
    out=target[['name']].copy()
    # PA from RBI with own-ratio shrinkage
    lg=lg_rate(tr,'PA','RBI')
    out['PA']=[r.RBI*own_rate(tr,r['name'],'PA','RBI',K['PA'],lg) for _,r in target.iterrows()]
    out['HR']=target.HR.values;out['RBI']=target.RBI.values
    PA=out.PA.values;HR=target.HR.values
    # non-HR hits per (PA-HR)
    trn=tr.assign(nh=tr.H-tr.HR,den=tr.PA-tr.HR)
    lg_h=lg_rate(trn,'nh','den')
    out['nHR_hits']=[ max(PA[i]-HR[i],0)*own_rate(trn,r['name'],'nh','den',K['H'],lg_h) for i,(_,r) in enumerate(target.iterrows())]
    for s in ['BB','K','HBP']:
        l=lg_rate(tr,s,'PA');out[s]=[PA[i]*own_rate(tr,r['name'],s,'PA',K[s],l) for i,(_,r) in enumerate(target.iterrows())]
    out['H']=out.nHR_hits+HR
    trh=tr.assign(nh=tr.H-tr.HR)
    for s in ['2B','3B']:
        l=lg_rate(trh,s,'nh');out[s]=[out.nHR_hits.values[i]*own_rate(trh,r['name'],s,'nh',K[s],l) for i,(_,r) in enumerate(target.iterrows())]
    l=lg_rate(tr,'R','RBI');out['R']=[r.RBI*own_rate(tr,r['name'],'R','RBI',K['R'],l) for _,r in target.iterrows()]
    return out
