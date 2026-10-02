import pandas as pd, numpy as np, matplotlib, textwrap
matplotlib.use('Agg'); import matplotlib.pyplot as plt
U='/mnt/user-data/uploads/d65-dashboard-data'
plt.rcParams.update({'font.family':'Carlito','font.size':13,'axes.spines.top':False,'axes.spines.right':False})
INK,MUTED='#1b2a41','#666'
# ---- B: building cost per student, dot range
bc=pd.read_csv(f'{U}/data/building_costs_v2_2026-10-01.csv').set_index('account')
sc=pd.read_csv(f'{U}/projections/v2_2026-10-01/data/scenario_receivers_90pct.csv'); ok=sc[sc.util.round()<=100]
k5=bc.dropna(subset=['per_student_scen_avg']).sort_values('per_student_scen_avg',ascending=False)
def costchart(path, w=9.6, h=4.6, fs=13, labels=True):
    fig,ax=plt.subplots(figsize=(w,h))
    for i,(s,r) in enumerate(k5.iterrows()):
        v=r.total_est/ok[ok.school==s].students
        ax.plot([v.min(),v.max()],[i,i],color='#dde1ea',lw=9,solid_capstyle='round',zorder=1)
        ax.scatter(v,[i]*len(v),s=18,color='#d9a400',edgecolor='#8a6a00',lw=.5,zorder=2)
        ax.scatter([r.per_student_scen_avg],[i],marker='D',s=70,color='#c8662a',zorder=4)
        ax.scatter([r.per_student],[i],s=80,facecolor='white',edgecolor='#c0392b',lw=2.4,zorder=5)
        if labels: ax.text(max(v.max(),r.per_student)+18,i,f"avg ${r.per_student_scen_avg:,.0f}",va='center',fontsize=fs-1,color='#c8662a',fontweight='bold')
    ax.set_yticks(range(len(k5)),k5.index,fontsize=fs); ax.invert_yaxis(); ax.tick_params(axis='y',length=0)
    ax.spines['left'].set_visible(False); ax.grid(axis='x',color='#eee'); ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f"${v:,.0f}")); ax.set_xlim(950,2150)
    ax.set_xlabel('Estimated yearly building cost per student',color='#444',fontsize=fs-1)
    h_=[plt.Line2D([],[],ls='',marker='o',mfc='white',mec='#c0392b',mew=2.2,ms=9,label='Today (Oct 1, 2026)'),
        plt.Line2D([],[],ls='',marker='o',color='#d9a400',ms=6,label='Each closure scenario'),
        plt.Line2D([],[],ls='',marker='D',color='#c8662a',ms=8,label='Scenario average'),
        plt.Line2D([],[],ls='-',color='#dde1ea',lw=8,label='Range')]
    ax.legend(handles=h_,loc='lower left',bbox_to_anchor=(0,1.0),ncol=4,frameon=False,fontsize=fs-1)
    plt.tight_layout(); fig.savefig(path,dpi=220); plt.close(fig)
costchart('img/building_cost.png')
costchart('img/building_cost_small.png',w=6.4,h=3.9,fs=11)
# ---- C: EBF gap by group (11 schools today)
t3=pd.read_csv(f'{U}/EBF/v2_2026-10-01/data/ebf_k5_table3_savings.csv').set_index('Staff group')
t2=pd.read_csv(f'{U}/EBF/v2_2026-10-01/data/ebf_k5_table2_difference.csv').set_index('Staff group')
c3=[c for c in t3.columns if c.startswith('11')][0]; c2=[c for c in t2.columns if c.startswith('11')][0]
names={'Special-ed teachers + SLP, OT/PT':'Special-ed teachers & therapists','Teacher assistants / paras + behavior techs':'Paras & behavior techs',
 'Social workers, psychologists, FACE liaisons':'Social work, psych, FACE','EL / ESL / bilingual teachers':'ESL / bilingual','Specialist teachers (PE, music, art, drama…)':'Specialists (PE, music, art)',
 'Nurses':'Nurses','Educational support staff (MISC)':'Educational support','School office staff + health clerks':'Office & health clerks','Librarians':'Librarians',
 'Guidance counselors':'Counselors','Interventionists (core + low-income)':'Interventionists','Instructional coaches':'Instructional coaches','Core classroom teachers':'Classroom teachers',
 'Principals':'Principals','Assistant principals':'Assistant principals'}
g=pd.DataFrame({'d':t3[c3],'n':t2[c2]}).drop(index=['Total','Total without special ed & paras']).rename(index=names)
g=g[g.d.abs()>=150000]
sped=['Special-ed teachers & therapists','Paras & behavior techs']
g['grp']=['sped' if i in sped else ('above' if v>0 else 'below') for i,v in zip(g.index,g.d)]
g['o']=g.grp.map({'sped':0,'above':1,'below':2}); g=g.sort_values(['o','d'],ascending=[True,False])
col={'sped':'#7b2d8e','above':'#c8662a','below':'#1f5ea8'}
fig,ax=plt.subplots(figsize=(9.6,5.6))
y=range(len(g))
ax.barh(list(y),g.d/1e6,color=[col[x] for x in g.grp],height=.7)
for i,(nm,r) in enumerate(g.iterrows()):
    lab=f"{'+' if r.d>0 else '−'}${abs(r.d)/1e6:.1f}M · {'+' if r.n>0 else '−'}{abs(r.n):.0f} staff"+('*' if nm=='Classroom teachers' else '')
    if r.d>0: ax.text(r.d/1e6+.15,i,lab,va='center',fontsize=11.5,fontweight='bold' if r.grp=='sped' else 'normal',color=INK)
    elif r.d<-3e6: ax.text(r.d/1e6+.12,i,lab,va='center',ha='left',fontsize=11.5,color='white',fontweight='bold')
    else: ax.text(r.d/1e6-.15,i,lab,va='center',ha='right',fontsize=11.5,color=INK)
ax.set_yticks(list(y),g.index,fontsize=12); ax.invert_yaxis(); ax.tick_params(axis='y',length=0); ax.spines['left'].set_visible(False)
ax.axvline(0,color='#333',lw=1); ax.set_xlim(-7,16.5); ax.grid(axis='x',color='#eee'); ax.set_axisbelow(True)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:('−' if v<0 else '')+f"${abs(v):.0f}M"))
ax.set_xlabel('Yearly cost above (+) or below (−) what EBF funds',color='#444')
h_=[plt.Rectangle((0,0),1,1,color=col[k]) for k in col]
ax.legend(h_,['Special ed (set by IEPs)','Other staff above EBF','Below EBF'],loc='lower right',frameon=False,fontsize=11.5)
plt.tight_layout(); fig.savefig('img/ebf_by_group.png',dpi=220); plt.close(fig)
print(g)
# ---- D: waterfall
tot=t3.loc['Total',c3]; sp=t3.loc['Special-ed teachers + SLP, OT/PT',c3]; pa=t3.loc['Teacher assistants / paras + behavior techs',c3]; ev=tot-sp-pa
fig,ax=plt.subplots(figsize=(4.6,3.9))
vals=[sp,pa,ev,tot]; starts=[0,sp,sp+pa,0]; cols=['#7b2d8e','#7b2d8e','#1f5ea8' if ev<0 else '#c8662a','#1b2a41']
labs=['Special-ed\nteachers &\ntherapists','Paras &\nbehavior\ntechs','Everything\nelse','Net\nabove\nEBF']
for i,(v,s,c) in enumerate(zip(vals,starts,cols)):
    b= s if v>=0 else s+v
    ax.bar(i,abs(v)/1e6,bottom=b/1e6,color=c,width=.62)
    ax.text(i,(max(s,s+v))/1e6+.4,f"{'+' if v>0 and i<3 else ('−' if v<0 else '')}${abs(v)/1e6:.1f}M",ha='center',fontsize=11,fontweight='bold',color=INK)
ax.set_xticks(range(4),labs,fontsize=9.5); ax.set_ylim(0,21); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f"${v:.0f}M"))
ax.grid(axis='y',color='#eee'); ax.set_axisbelow(True); ax.tick_params(axis='x',length=0)
plt.tight_layout(); fig.savefig('img/ebf_waterfall.png',dpi=220); plt.close(fig)
print(sp,pa,ev,tot)
