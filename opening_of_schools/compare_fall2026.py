"""Compare the Opening of Schools Report 2024-2025 (and its 2022-23 / 2023-24 columns) with
fall 2026 (SY 2026-27) data: the district dashboard (data.district65.net, pulled 10/1/2026) and the
district's FY27 K-5 section list (emailed 10/1/2026).

Like-for-like universe: students at D65's K-8 schools (elementary, middle and magnet schools),
which is what the dashboard covers. The report's K-5 and 6-8 rows already exclude Park, Rice
and SEES; JEH / Family Center is reported separately. Fall 2026 is Oct. 1; the report is Sept. 30.
Writes data/compare/*.csv and images/*.png.
Made with help from Claude (an AI model), which can make mistakes. Please verify.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OOS = os.path.join(HERE, "data", "oos_2024_25")
DASH = os.path.join(ROOT, "data", "dashboard_2026-10-01")
OUT = os.path.join(HERE, "data", "compare"); IMG = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True); os.makedirs(IMG, exist_ok=True)

Y24, Y26 = "2024-25", "2026-27"
NOT_K8 = ["Family Center", "Joseph E Hill Education Center", "Park School", "Rice Childrens Center",
          "Special Education Evaluation / Services"]
SHORT = lambda s: (s.replace("Dr Martin Luther King Jr Literary & Fine Arts School", "King Arts")
                    .replace("Dr Bessie Rhodes School of Global Studies", "Bessie Rhodes")
                    .replace(" Elementary School", "").replace(" Middle School", " (MS)")
                    .replace(" School", ""))

# ── Load ──────────────────────────────────────────────────────────────────────────
t2 = pd.read_csv(f"{OOS}/table_2_enrollment_by_grade.csv")
t1 = pd.read_csv(f"{OOS}/table_1_enrollment_school_grade_race.csv")
t5 = pd.read_csv(f"{OOS}/table_5_iep_by_school.csv")
t6 = pd.read_csv(f"{OOS}/table_6_k5_twi.csv")
ay = pd.read_csv(f"{OOS}/across_years.csv")
eg = pd.read_csv(f"{DASH}/enrollment_by_school_grade.csv")
hd = pd.read_csv(f"{DASH}/students_home_demographics.csv")
cs = pd.read_csv(f"{ROOT}/data/class_size_detail_by_school_v2.csv")

k8_24 = t2[~t2.School.isin(NOT_K8)].copy()
eg = eg[eg.school != "District"].copy()
dist = hd[hd.school == "District"]
dv = lambda chart, cat: float(dist[(dist.chart_id == chart) & (dist.category == cat)].value.sum())

# ── 1. Across years, extended with fall 2026 ─────────────────────────────────────
g = {str(i): f"grade_{i}" for i in range(9)}
k26 = eg["grade_0"].sum(); k5_26 = eg[[f"grade_{i}" for i in range(6)]].sum().sum()
m_26 = eg[[f"grade_{i}" for i in (6, 7, 8)]].sum().sum()
iep24_k8 = t5[~t5.School.isin(NOT_K8)]["Total IEP"].sum()
twi24 = t6[["Monitoring 2 yrs", "TWE", "TWS", "TWX"]].sum().sum()
twi26 = dv("home-twi", "TWE") + dv("home-twi", "TWS") + dv("home-twi", "TWX")
piv = ay.pivot(index="metric", columns="school_year", values="value_text")
order = ["Total Enrollment", "JEH / Family Center", "Kindergarten students (excluding Park, Rice, SEES)",
         "K-5 (excluding Park, Rice, SEES)", "6-8 (excluding Park, Rice, SEES)", "Park students",
         "Rice students", "SEES (Outplaced)", "SEES (Eval / Services Only)", "Low income students",
         "McKinney-Vento students", "K-5 TWI students", "IEP students", "ELL students",
         "School-Age child care", "Immunization compliance", "Transportation"]
piv = piv.reindex(order)[["2022-23", "2023-24", "2024-25"]]
f26 = {
    "Kindergarten students (excluding Park, Rice, SEES)": f"{k26:,.0f}",
    "K-5 (excluding Park, Rice, SEES)": f"{k5_26:,.0f}",
    "6-8 (excluding Park, Rice, SEES)": f"{m_26:,.0f}",
    "K-5 TWI students": f"{twi26:,.0f}†",
}
piv["2026-27 (10/1 dashboard)"] = [f26.get(m, "not on dashboard") for m in piv.index]
piv.loc["K-8 schools total (K-5 + 6-8)"] = [
    f"{int(ay[(ay.school_year == y) & ay.metric.str.startswith(('K-5 (excl', '6-8 (excl'))]['count'].sum()):,}"
    for y in ["2022-23", "2023-24", "2024-25"]] + [f"{k5_26 + m_26:,.0f}"]
piv.loc["IEP students at K-8 schools"] = ["", "", f"{iep24_k8:,} ({iep24_k8 / k8_24['Total Enrollment'].sum() * 100:.0f}%)",
                                          f"{dv('home-iep', 'Has IEP'):,.0f} ({dv('home-iep', 'Has IEP') / 5415 * 100:.0f}%)"]
piv.loc["EL students at K-8 schools"] = ["", "", "not by school in report",
                                         f"{dv('home-lep', 'EL'):,.0f} ({dv('home-lep', 'EL') / 5415 * 100:.0f}%)"]
twi_k5_24 = twi24 / ay[(ay.school_year == "2024-25") & ay.metric.str.startswith("K-5 (excl")]["count"].item() * 100
piv.loc["K-5 TWI as % of K-5 (TWE+TWS+TWX only)"] = ["", "", f"{t6[['TWE', 'TWS', 'TWX']].sum().sum():,} ({t6[['TWE', 'TWS', 'TWX']].sum().sum() / 3728 * 100:.1f}%)",
                                                    f"{twi26:,.0f} ({twi26 / k5_26 * 100:.1f}%)"]
piv.index.name = "metric"
piv.to_csv(f"{OUT}/across_years_with_fall2026.csv")

# ── 2. By school ─────────────────────────────────────────────────────────────────
s24 = k8_24.set_index("School")["Total Enrollment"]
s26 = eg.set_index("school")["total"]
bys = pd.DataFrame({Y24: s24, Y26: s26}).fillna(0).astype(int)
bys["change"] = bys[Y26] - bys[Y24]
bys["pct_change"] = np.where(bys[Y24] > 0, (bys["change"] / bys[Y24] * 100).round(1), np.nan)
bys["note"] = ""
bys.loc["Kingsley Elementary School", "note"] = "closed after 2024-25"
bys.loc["Dr Bessie Rhodes School of Global Studies", "note"] = "closed after 2024-25"
bys.loc["Foster School", "note"] = "opened after 2024-25"
bys.loc["Willard Elementary School", "note"] = "TWI strand moved to Foster"
bys.index.name = "school"
bys = bys.sort_values(Y26, ascending=False)
bys.loc["Total (K-8 schools)"] = [bys[Y24].sum(), bys[Y26].sum(), bys["change"].sum(),
                                  round(bys["change"].sum() / bys[Y24].sum() * 100, 1), ""]
bys.to_csv(f"{OUT}/enrollment_by_school.csv")

# ── 3. By grade, with cohorts ─────────────────────────────────────────────────────
gr24 = k8_24[["K"] + [str(i) for i in range(1, 9)]].sum()
gr26 = eg[[f"grade_{i}" for i in range(9)]].sum().set_axis(gr24.index)
byg = pd.DataFrame({"grade": gr24.index, Y24: gr24.values.astype(int), Y26: gr26.values.astype(int)})
byg["change_same_grade"] = byg[Y26] - byg[Y24]
# cohort: students in grade g in 2026-27 vs. the same students' grade (g-2) in 2024-25
byg["cohort_2024_25_grade"] = ["", ""] + list(gr24.index[:-2])
byg["cohort_2024_25_count"] = [np.nan, np.nan] + list(gr24.values[:-2])
byg["cohort_change"] = byg[Y26] - byg["cohort_2024_25_count"]
byg.to_csv(f"{OUT}/enrollment_by_grade.csv", index=False)

# ── 4. Race / ethnicity at K-8 schools ───────────────────────────────────────────
r24 = t1[~t1.School.isin(NOT_K8) & t1.Grade.between(0, 8)]
race_cols = {"Asian": "Asian", "Black or African American": "Black or African American",
             "Hispanic or Latino": "Hispanic or Latino", "Middle Eastern or North African": "Middle Eastern or North African",
             "Multi-racial": "Multi-racial", "White": "White"}
rr24 = {k: r24[k].sum() for k in race_cols}
rr24["Other (American Indian, Pacific Islander)"] = r24["American Indian or Alaska Native"].sum() + r24["Native Hawaiian / Other Pac Islander"].sum()
rr26 = {k: dv("home-race", k) for k in race_cols}
rr26["Other (American Indian, Pacific Islander)"] = dv("home-race", "Other*")
race = pd.DataFrame({Y24: pd.Series(rr24), Y26: pd.Series(rr26)}).astype(int)
race[f"{Y24}_pct"] = (race[Y24] / race[Y24].sum() * 100).round(1)
race[f"{Y26}_pct"] = (race[Y26] / race[Y26].sum() * 100).round(1)
race["change"] = race[Y26] - race[Y24]
race["pct_pts_change"] = (race[f"{Y26}_pct"] - race[f"{Y24}_pct"]).round(1)
race.index.name = "race_ethnicity"
race.to_csv(f"{OUT}/race_ethnicity_k8.csv")

# ── 5. IEP by school ───────────────────────────────────────────────────────────────
iep26 = hd[(hd.chart_id == "home-iep") & (hd.category == "Has IEP") & (hd.school != "District")].set_index("school").value
i24 = t5[~t5.School.isin(NOT_K8)].set_index("School")["Total IEP"]
iep = pd.DataFrame({f"iep_{Y24}": i24, f"iep_{Y26}": iep26}).fillna(0).astype(int)
iep[f"enrollment_{Y24}"] = s24.reindex(iep.index).fillna(0).astype(int)
iep[f"enrollment_{Y26}"] = s26.reindex(iep.index).fillna(0).astype(int)
for y in (Y24, Y26):
    iep[f"iep_pct_{y}"] = (iep[f"iep_{y}"] / iep[f"enrollment_{y}"].replace(0, np.nan) * 100).round(1)
iep.index.name = "school"
iep.to_csv(f"{OUT}/iep_by_school.csv")

# ── 6. TWI by school ──────────────────────────────────────────────────────────────
tw26 = hd[hd.chart_id == "home-twi"].pivot_table(index="school", columns="category", values="value", aggfunc="sum").drop("District")
tw = pd.DataFrame({f"twi_{Y24}": t6.set_index("School")[["Monitoring 2 yrs", "TWE", "TWS", "TWX"]].sum(axis=1),
                   f"twi_{Y26}": tw26.sum(axis=1)}).fillna(0).astype(int)
tw["change"] = tw[f"twi_{Y26}"] - tw[f"twi_{Y24}"]
for c in ["TWE", "TWS", "TWX"]:
    tw[f"{c}_{Y24}"] = t6.set_index("School")[c].reindex(tw.index).fillna(0).astype(int)
    tw[f"{c}_{Y26}"] = tw26[c].reindex(tw.index).fillna(0).astype(int)
tw.index.name = "school"
tw.loc["Total"] = tw.sum()
tw.to_csv(f"{OUT}/twi_by_school.csv")

# ── 7. Class size: report's K-2 / 3-5 approximations vs. fall 2026 sections ─────────
cs["band"] = np.where(cs.grade <= 2, "K-2", "3-5")
band = cs.groupby("band")[["students", "sections"]].sum()
band["students_per_section_2026_27"] = (band.students / band.sections).round(1)
band["report_2024_25_approx"] = [18, 17]   # 3-5, K-2 (sorted index)
band["report_max_goal"] = [25, 23]
band.index.name = "grades"
band.to_csv(f"{OUT}/class_size_bands.csv")

# ── Charts ────────────────────────────────────────────────────────────────────────
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False})
GRAY, NAVY = "#9aa3b5", "#1f3a8a"

# A. K-8 enrollment, 2022-23 → 2026-27 (no 2025-26 point)
yrs = ["2022-23", "2023-24", "2024-25"]
k5 = [ay[(ay.school_year == y) & ay.metric.str.startswith("K-5 (excl")]["count"].item() for y in yrs] + [k5_26]
m8 = [ay[(ay.school_year == y) & ay.metric.str.startswith("6-8 (excl")]["count"].item() for y in yrs] + [m_26]
xs = [0, 1, 2, 4]; labels = yrs + ["2026-27"]
fig, ax = plt.subplots(figsize=(7.5, 4.3))
ax.bar(xs, k5, color=NAVY, width=.62, label="K-5")
ax.bar(xs, m8, bottom=k5, color=GRAY, width=.62, label="6-8")
for x, a, b in zip(xs, k5, m8):
    ax.text(x, a + b + 60, f"{a + b:,.0f}", ha="center", fontsize=11, fontweight="bold")
    ax.text(x, a / 2, f"{a:,.0f}", ha="center", color="white", fontsize=10)
    ax.text(x, a + b / 2, f"{b:,.0f}", ha="center", color="#1f2430", fontsize=10)
ax.text(3, 2600, "2025-26\nnot in this\ncomparison", ha="center", va="center", fontsize=9, color="#777")
ax.set_xticks(xs, labels); ax.set_ylim(0, 6800); ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.legend(frameon=False, loc="upper right", ncol=2)
ax.set_title("Students at D65's K-8 schools", loc="left", fontsize=14, fontweight="bold", pad=18)
ax.text(0, 1.02, "Sept. 30 counts from the Opening of Schools Report; 2026-27 from the dashboard on Oct. 1, 2026",
        transform=ax.transAxes, fontsize=8.5, color="#555")
plt.tight_layout(); fig.savefig(f"{IMG}/k8_enrollment_trend.png", dpi=200); plt.close(fig)

# B. By school, 2024-25 vs 2026-27
b = bys.drop("Total (K-8 schools)").copy(); b.index = b.index.map(SHORT)
b = b.sort_values([Y26, Y24])
fig, ax = plt.subplots(figsize=(7.5, 6))
y = np.arange(len(b))
ax.barh(y + .2, b[Y24], height=.38, color=GRAY, label=Y24)
ax.barh(y - .2, b[Y26], height=.38, color=NAVY, label=f"{Y26} (10/1)")
for i, (n24, n26, ch) in enumerate(zip(b[Y24], b[Y26], b["change"])):
    if n24 and n26:
        txt = f"{ch:+d}"
    elif n26:
        txt = "new"
    else:
        txt = "closed"
    ax.text(max(n24, n26) + 8, i, txt, va="center", fontsize=9.5, color="#333")
ax.set_yticks(y, b.index); ax.set_xlabel("Students"); ax.grid(axis="x", color="#eee"); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower right")
ax.set_title("Enrollment by school, 2024-25 vs. fall 2026", loc="left", fontsize=14, fontweight="bold")
plt.tight_layout(); fig.savefig(f"{IMG}/enrollment_by_school.png", dpi=200); plt.close(fig)

# C. By grade
fig, ax = plt.subplots(figsize=(7.5, 4))
x = np.arange(9)
ax.bar(x - .2, byg[Y24], width=.38, color=GRAY, label=Y24)
ax.bar(x + .2, byg[Y26], width=.38, color=NAVY, label=f"{Y26} (10/1)")
for i, v in enumerate(byg["change_same_grade"]):
    ax.text(i, max(byg[Y24][i], byg[Y26][i]) + 12, f"{v:+d}", ha="center", fontsize=9)
ax.set_xticks(x, ["K"] + [str(i) for i in range(1, 9)]); ax.set_xlabel("Grade")
ax.set_ylim(0, 800); ax.grid(axis="y", color="#eee"); ax.set_axisbelow(True)
ax.legend(frameon=False, ncol=2, loc="upper left")
ax.set_title("Students per grade at K-8 schools", loc="left", fontsize=14, fontweight="bold")
plt.tight_layout(); fig.savefig(f"{IMG}/enrollment_by_grade.png", dpi=200); plt.close(fig)

# D. Race/ethnicity shares
rp = race.sort_values(f"{Y26}_pct")
fig, ax = plt.subplots(figsize=(7.5, 3.8))
y = np.arange(len(rp))
ax.barh(y + .2, rp[f"{Y24}_pct"], height=.38, color=GRAY, label=Y24)
ax.barh(y - .2, rp[f"{Y26}_pct"], height=.38, color=NAVY, label=f"{Y26} (10/1)")
for i, (a, c) in enumerate(zip(rp[f"{Y24}_pct"], rp[f"{Y26}_pct"])):
    ax.text(max(a, c) + .6, i, f"{c:.1f}% ({c - a:+.1f} pts)", va="center", fontsize=9)
ax.set_yticks(y, [s.replace(" (American Indian, Pacific Islander)", "*") for s in rp.index])
ax.set_xlim(0, 56); ax.set_xlabel("% of students at K-8 schools"); ax.legend(frameon=False, loc="lower right")
fig.text(.01, .01, "*American Indian or Alaska Native, Native Hawaiian or Pacific Islander (the dashboard groups these as Other)", fontsize=7.5, color="#555")
ax.set_title("Race/ethnicity at K-8 schools", loc="left", fontsize=14, fontweight="bold")
plt.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(f"{IMG}/race_ethnicity.png", dpi=200); plt.close(fig)

print(piv.to_string()); print(); print(bys.to_string()); print(); print(byg.to_string()); print()
print(race.to_string()); print(); print(iep.to_string()); print(); print(tw.to_string()); print(); print(band.to_string())
