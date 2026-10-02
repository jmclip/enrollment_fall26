import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from scipy import stats
U='/mnt/user-data/uploads/d65-dashboard-data'
d=pd.read_csv(f'{U}/data/class_size_detail_by_school_v2.csv'); sa=d.groupby('school').avg_class_size.mean()
u=pd.read_csv(f'{U}/legion_site/dataanalysis/data/sy27_fall_v2/utilization_current_vs_predicted.csv')
sh=lambda n:n.replace("Dr Martin Luther King Jr Literary & Fine Arts School","King Arts").replace(" Elementary School","").replace(" School","")
u['s']=u.school.map(sh); u=u.dropna(subset=['util_pct_current']).set_index('s')
r=pd.DataFrame({'cs':sa}).join(u['util_pct_current']).dropna()
f=stats.linregress(r.util_pct_current,r.cs); print(f.rvalue,f.pvalue,len(r)); print(r)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
cm=LinearSegmentedColormap.from_list('rpb',['#e0182d','#8f3fd1','#0a3a9e']); nm=TwoSlopeNorm(vmin=14,vcenter=18,vmax=23)
fig,ax=plt.subplots(figsize=(7,4.6))
x=np.linspace(48,82,50); ax.plot(x,f.intercept+f.slope*x,ls='--',color='#777',lw=1.3)
ax.scatter(r.util_pct_current,r.cs,s=110,c=r.cs,cmap=cm,norm=nm,zorder=3,edgecolor='white')
off={'Willard':(8,-3),'Walker':(-48,-3),'Lincolnwood':(8,-10),'Lincoln':(-14,-15),'King Arts':(8,-3),'Dawes':(8,-6),'Orrington':(-58,4),'Dewey':(-45,-12),'Foster':(-46,-4),'Washington':(8,-4),'Oakton':(-50,-4)}
for s,row in r.iterrows(): ax.annotate(s,(row.util_pct_current,row.cs),xytext=off.get(s,(8,2)),textcoords='offset points',fontsize=11)
ax.set_xlabel('Building utilization (% of capacity used)'); ax.set_ylabel('Average class size, K–5')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f'{v:.0f}%')); ax.set_xlim(47,83); ax.set_ylim(15.5,21.8)
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(color='#eee'); ax.set_axisbelow(True)
ax.set_title("Utilization doesn't predict class size",fontsize=15,fontweight='bold',loc='left',pad=22)
ax.text(0,1.02,f"r = {f.rvalue:.2f}, p = {f.pvalue:.2f}, {len(r)} schools · dot color = class size",transform=ax.transAxes,fontsize=9.5,color='#555',va='bottom')
plt.tight_layout(); fig.savefig('img/scatter.png',dpi=220)
