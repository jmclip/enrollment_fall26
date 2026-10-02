"""Class size v2: actual FY27 (fall 2026) K-5 sections replace the estimated class counts.

Input:  data/k5_sections_fy27.xlsx: the district's FY27 (fall 2026) K-5 section list, one row per section (school, grade,
        program TWI / MonoL / African Centered Curriculum). Received by email from District 65 on October 1, 2026.
        data/dashboard_2026-10-01/enrollment_by_school_grade.csv: students by school and grade, data.district65.net,
        pulled October 1, 2026 (scraping/build_from_long.py).
        data/twi_strands.csv (TWI students by school), data/utilization_1A_website.csv (projected ACC students, Oakton)
        data/utilization_current_vs_predicted.csv (current utilization)
Method: section counts are now actual (v1 estimated them). Students per section are still estimated, because the
        section file has no student counts: each grade's students are spread evenly over all of that grade's sections
        (TWI, ACC and monolingual alike). v1 split TWI/ACC students out using school-wide averages; with real section
        counts that split produced impossible sizes (e.g. a 31.7-student monolingual class at Foster), so v2 doesn't.
Outputs (all *_v2): data/classes_actual_v2.csv, data/class_size_detail_by_school_v2.csv,
        data/table_classes_by_school_grade_v2.csv, data/sections_estimated_vs_actual_v2.csv,
        data/class_size_by_school_overall_v2.csv, data/class_size_vs_utilization_v2.csv,
        images/chart_class_size_heatmap_v2.png, images/chart_class_size_by_school_overall_v2.png,
        images/chart_class_size_vs_utilization_v2.png, images/budget_handout/class_size_by_school_v2.png
Built with help from Claude (AI), which can make mistakes. Please verify.
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from scipy import stats

SHORT = {'Dawes Elementary School': 'Dawes', 'Dewey Elementary School': 'Dewey', 'Foster School': 'Foster',
         'Dr Martin Luther King Jr Literary & Fine Arts School': 'King Arts', 'Lincoln Elementary School': 'Lincoln',
         'Lincolnwood Elementary School': 'Lincolnwood', 'Oakton Elementary School': 'Oakton',
         'Orrington Elementary School': 'Orrington', 'Walker Elementary School': 'Walker',
         'Washington Elementary School': 'Washington', 'Willard Elementary School': 'Willard'}
PROG = {'TWI': 'TWI', 'MonoL': 'Monolingual', 'African Centered Curriculum': 'ACC'}
G = [0, 1, 2, 3, 4, 5]; GL = {0: 'K', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
INK, MUTED = '#1d1d1d', '#666666'

sec = pd.read_excel('data/k5_sections_fy27.xlsx', sheet_name='Sheet1')
sec['school'] = sec['SCHOOL_NAME'].map(SHORT); sec['grade'] = sec['GRADE_LEVEL'].astype(int)
sec['program'] = sec['PROGRAM_NAME'].map(PROG)
assert sec['school'].notna().all() and sec['program'].notna().all()
cnt = sec.pivot_table(index=['school', 'grade'], columns='program', values='SCHOOL_NAME', aggfunc='size', fill_value=0)
cnt = cnt.reindex(columns=['TWI', 'ACC', 'Monolingual'], fill_value=0)

enr = pd.read_csv('data/dashboard_2026-10-01/enrollment_by_school_grade.csv')
enr['school'] = enr['school'].map(SHORT); enr = enr.dropna(subset=['school']).set_index('school')
tw = pd.read_csv('data/twi_strands.csv').set_index('school')
acc_total = pd.read_csv('data/utilization_1A_website.csv').assign(school=lambda d: d['school'].map(SHORT)) \
    .dropna(subset=['school']).set_index('school')['enroll_acc']

rows, classes = [], []
for (school, g), r in cnt.iterrows():
    n = float(enr.loc[school, f'grade_{g}'])
    s_twi, s_acc, s_mono = int(r['TWI']), int(r['ACC']), int(r['Monolingual'])
    tot = s_twi + s_acc + s_mono
    rows.append(dict(school=school, grade=g, grade_label=GL[g], students=n, twi_sections=s_twi, acc_sections=s_acc,
                     mono_sections=s_mono, sections=tot, avg_class_size=round(n / tot, 2)))
    for p, k in [('TWI', s_twi), ('ACC', s_acc), ('Monolingual', s_mono)]:
        classes += [dict(school=school, grade=GL[g], program=p, size=round(n / tot, 1))] * k
detail = pd.DataFrame(rows).sort_values(['school', 'grade'])
detail.to_csv('data/class_size_detail_by_school_v2.csv', index=False)
cl = pd.DataFrame(classes); cl.to_csv('data/classes_actual_v2.csv', index=False)

tbl = detail.pivot_table(index='school', columns='grade_label', values='sections', aggfunc='sum')[list(GL.values())]
tbl['Total'] = tbl.sum(axis=1); tbl.loc['All schools'] = tbl.sum(); tbl.to_csv('data/table_classes_by_school_grade_v2.csv')
old = pd.read_csv('data/table_classes_by_school_grade.csv').set_index('school')
cmp_ = pd.DataFrame({'estimated_k5': old.loc[tbl.index, list(GL.values())].sum(axis=1).astype(int),
                     'actual_k5': tbl['Total'].astype(int)})
cmp_['difference'] = cmp_['actual_k5'] - cmp_['estimated_k5']
gd = (tbl[list(GL.values())] - old.loc[tbl.index, list(GL.values())]).astype(int)
cmp_['grades_that_differ'] = [', '.join(f"{c} ({'+' if v > 0 else ''}{v})" for c, v in gd.loc[s].items() if v) for s in cmp_.index]
cmp_.to_csv('data/sections_estimated_vs_actual_v2.csv')

sa = detail.groupby('school').agg(students=('students', 'sum'), classes=('sections', 'sum'),
                                  avg_of_grade_avgs=('avg_class_size', 'mean'))
sa['weighted_avg'] = sa['students'] / sa['classes']; sa = sa.sort_values('avg_of_grade_avgs')
sa.round(1).to_csv('data/class_size_by_school_overall_v2.csv')

ut = pd.read_csv('data/utilization_current_vs_predicted.csv'); ut['school'] = ut['school'].map(SHORT)
ut = ut.dropna(subset=['school']).set_index('school')
enr_all = enr['total']
ut['dashboard_2026_10_01'] = enr_all.reindex(ut.index)
ut['util_pct_current'] = (100 * ut['dashboard_2026_10_01'] / ut['capacity_used']).round(0)
ut.to_csv('data/utilization_current_2026-10-01.csv')
ut = ut.reset_index()
reg = sa[['avg_of_grade_avgs']].join(ut.dropna(subset=['school']).set_index('school')['util_pct_current']).dropna()
fit = stats.linregress(reg['util_pct_current'], reg['avg_of_grade_avgs'])
reg.round(1).rename(columns={'avg_of_grade_avgs': 'avg_class_size', 'util_pct_current': 'utilization_pct'}) \
   .to_csv('data/class_size_vs_utilization_v2.csv')

# ---- charts --------------------------------------------------------------------------------------------
red_blue = LinearSegmentedColormap.from_list('rpb', ['#e0182d', '#8f3fd1', '#0a3a9e'])
norm = TwoSlopeNorm(vmin=14, vcenter=18, vmax=23)
order = sa.index.tolist()

# heatmap
H = detail.pivot(index='school', columns='grade', values='avg_class_size').loc[order]
S = detail.pivot(index='school', columns='grade', values='sections').loc[order]
H['avg'] = H[G].mean(axis=1); S['avg'] = S[G].sum(axis=1)
fig, ax = plt.subplots(figsize=(10, 7.5))
ax.imshow(H.values.astype(float), cmap=red_blue, norm=norm, aspect='auto')
for i in range(H.shape[0]):
    for j in range(H.shape[1]):
        ax.text(j, i - .12, f'{H.iat[i, j]:.1f}', ha='center', va='center', fontsize=12.5, fontweight='bold', color='white')
        ax.text(j, i + .25, f'{int(S.iat[i, j])} cl.', ha='center', va='center', fontsize=8, color='white')
ax.set_xticks(range(7), ['K', '1', '2', '3', '4', '5', 'School\naverage']); ax.set_yticks(range(len(order)), order)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
ax.set_xticks(np.arange(-.5, 7, 1), minor=True); ax.set_yticks(np.arange(-.5, len(order), 1), minor=True)
ax.grid(which='minor', color='#fcfcfb', linewidth=2); ax.tick_params(which='minor', length=0); ax.axvline(5.5, color='#fcfcfb', lw=7)
ax.set_xlabel('Grade')
ax.set_title('Average class size by school and grade, K–5 (actual fall 2026 sections)', loc='left', fontsize=14, fontweight='bold', color=INK)
fig.text(.01, .01, 'Sections: D65 FY27 K–5 section list (emailed Oct 1, 2026). Students: data.district65.net, pulled Oct 1, 2026. Small number = classes.',
         fontsize=8.5, color=MUTED, style='italic')
plt.tight_layout(rect=(0, .03, 1, 1)); fig.savefig('images/chart_class_size_heatmap_v2.png', dpi=200); plt.close(fig)

# school averages
fig, ax = plt.subplots(figsize=(10, 7))
twi = set(tw.index)
ax.barh(sa.index, sa['avg_of_grade_avgs'], height=.85, color='#3987e5')
for yi, (s, (v, n, k)) in enumerate(zip(sa.index, sa[['avg_of_grade_avgs', 'students', 'classes']].values)):
    ax.text(v + .2, yi, f'{v:.1f}', va='center', fontsize=11, color=INK, fontweight='bold')
    ax.text(.3, yi, f"K–5 students: {n:.0f}   classes: {k:.0f}{'   ·   dual-language (TWI)' if s in twi else ''}",
            va='center', fontsize=10.5, color='white')
ax.axvline(24, color=MUTED, lw=1, ls='--'); ax.set_xlim(0, 26.5); ax.tick_params(axis='y', length=0)
for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
ax.set_xlabel('Average class size (average of K–5 grade averages)')
ax.set_title('Average class size by elementary school (actual fall 2026 sections)', loc='left', fontsize=14, fontweight='bold', color=INK)
plt.tight_layout(); fig.savefig('images/chart_class_size_by_school_overall_v2.png', dpi=200); plt.close(fig)

# regression
fig, ax = plt.subplots(figsize=(10, 7))
xx = np.linspace(reg['util_pct_current'].min() - 3, reg['util_pct_current'].max() + 3, 50)
ax.plot(xx, fit.intercept + fit.slope * xx, color='#e0182d', lw=2)
ax.scatter(reg['util_pct_current'], reg['avg_of_grade_avgs'], s=110, color='#1c5cab', zorder=3)
for s, r in reg.iterrows():
    ax.annotate(s, (r['util_pct_current'], r['avg_of_grade_avgs']), xytext=(8, 4), textcoords='offset points', fontsize=11)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}%'))
for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
ax.grid(color='#e8e7e3'); ax.set_axisbelow(True)
ax.set_xlabel('Current utilization (% of capacity used)'); ax.set_ylabel('Average class size (students)')
ax.set_title("High-utilization buildings don't have bigger classes", loc='left', fontsize=15, fontweight='bold', color=INK, pad=30)
ax.text(0, 1.02, f'r = {fit.rvalue:.2f},  R² = {fit.rvalue**2:.2f},  p = {fit.pvalue:.2f},  n = {len(reg)} schools. '
        'Sections emailed by D65 Oct 1, 2026; enrollment pulled Oct 1, 2026.', transform=ax.transAxes, fontsize=10.5, color=MUTED)
plt.tight_layout(); fig.savefig('images/chart_class_size_vs_utilization_v2.png', dpi=200); plt.close(fig)

# handout dot chart: one dot per grade (the grade's average class size), labeled with the grade
dot_order = order[::-1]
fig, ax = plt.subplots(figsize=(11, 6.4))
ax.axvspan(8, 16, color='#e0182d', alpha=.07); ax.axvspan(21, 28.5, color='#0a3a9e', alpha=.07)
for yi, s_ in enumerate(dot_order):
    d = detail[detail['school'] == s_]
    ax.plot([d['avg_class_size'].min(), d['avg_class_size'].max()], [yi, yi], color='#d9d9d9', lw=1.5, zorder=1)
    d = d.sort_values('avg_class_size'); ys, prev, k = [], None, 0
    for v in d['avg_class_size']:              # grades with (nearly) the same average stack vertically
        k = k + 1 if prev is not None and abs(v - prev) < .35 else 0; prev = v
        ys.append(yi + [0, -.24, .24, -.48][min(k, 3)])
    ax.scatter(d['avg_class_size'], ys, s=150, c=d['avg_class_size'], cmap=red_blue, norm=norm, zorder=2,
               edgecolor='white', linewidth=.8)
    for (_, r), y_ in zip(d.iterrows(), ys):
        ax.text(r['avg_class_size'], y_, r['grade_label'], ha='center', va='center', fontsize=6.5, color='white',
                fontweight='bold', zorder=3)
    ax.text(d['avg_class_size'].max() + .7, yi, f"{int(d['sections'].sum())} classes", va='center', fontsize=9, color=MUTED)
ax.set_yticks(range(len(dot_order)), dot_order); ax.invert_yaxis(); ax.tick_params(axis='y', length=0, labelsize=11)
ax.set_xlim(8, 28.5); ax.set_xticks(range(8, 29, 2)); ax.axvline(24, color=MUTED, lw=1, ls='--')
ax.text(24.1, len(dot_order) - .55, 'cap 24', color=MUTED, fontsize=9)
ax.set_xlabel('Average class size by grade (each dot = one grade, K–5: students ÷ sections)')
for sp in ['top', 'right', 'left']: ax.spines[sp].set_visible(False)
ax.text(8.15, len(dot_order) - .55, 'under 16', color='#e0182d', fontsize=9); ax.text(21.1, -.75, 'over 21', color='#0a3a9e', fontsize=9)
fig.text(.01, .01, 'Sections: District 65 FY27 K–5 section list, received by email Oct 1, 2026. Students: data.district65.net, pulled Oct 1, 2026.',
         fontsize=8, color=MUTED, style='italic')
plt.tight_layout(rect=(0, .03, 1, 1)); fig.savefig('images/budget_handout/class_size_by_school_v2.png', dpi=200); plt.close(fig)

print('grades', len(detail), 'grades<16', int((detail.avg_class_size < 16).sum()), 'grades>21', int((detail.avg_class_size > 21).sum()), 'grades<18', int((detail.avg_class_size < 18).sum()),
      'classes', len(cl), 'under16', int((cl['size'] < 16).sum()), 'over21', int((cl['size'] > 21).sum()),
      'min', cl['size'].min(), 'max', cl['size'].max(), f'r={fit.rvalue:.2f} p={fit.pvalue:.2f}')
print(cmp_.to_string()); print(sa.to_string())
print(detail[detail.grade == 3][['school', 'students', 'sections', 'avg_class_size']].to_string())
print(detail.sort_values('avg_class_size').iloc[[0,1,2,-3,-2,-1]].to_string())
