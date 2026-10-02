#!/usr/bin/env python3
"""Build the tidy dashboard CSVs from a d65_dashboard_all_long.csv (same post-processing as d65_scrape.py).

Usage: python3 scraping/build_from_long.py data/dashboard_2026-10-01
Used for the 2026-10-01 pull, which was run in a browser (the dashboard isn't reachable from the
scripting environment's network) with the same calls as d65_scrape.py, then saved as d65_dashboard_all_long.csv.
Also writes enrollment_by_school_grade.csv (students by school and grade, from the Home "Grade Level" chart).
Built with help from Claude (AI), which can make mistakes. Please verify.
"""
import pathlib, sys
import pandas as pd

out = pathlib.Path(sys.argv[1])
df = pd.read_csv(out / "d65_dashboard_all_long.csv", dtype={"category": str})
df["value"] = pd.to_numeric(df["value"], errors="coerce")
st = df[df.dataset == "students"].drop(columns="dataset").rename(columns={"scope": "school"})
for page, fn in [("home", "students_home_demographics"), ("attendance", "students_attendance"),
                 ("discipline", "students_discipline"), ("assessments", "students_assessments")]:
    sub = st[st.page == page].drop(columns=["page"] + (["test_type"] if page != "assessments" else []))
    sub.to_csv(out / f"{fn}.csv", index=False)
df[df.dataset == "energy"].drop(columns=["dataset", "page", "test_type"]).rename(
    columns={"scope": "account"}).to_csv(out / "sustainability_utility.csv", index=False)

pick = lambda c, cat=None: st[(st.chart_id == c) & ((st.category == cat) if cat else True)].groupby("school")["value"].sum()
s = pd.DataFrame({"enrollment": pick("home-enrollment"), "ada_pct": pick("home-ada"),
                  "chronic_absenteeism_pct": pick("att-cron-abs"),
                  "iep_students": pick("home-iep", "Has IEP"), "el_students": pick("home-lep", "EL"),
                  "incidents": pick("students-count-discipline", "Incidents"),
                  "students_with_incidents": pick("students-count-discipline", "Students"),
                  "minor_incidents": pick("students-count-discipline", "Minor Incidents"),
                  "major_incidents": pick("students-count-discipline", "Major Incidents")})
s["iep_pct"] = (100 * s.iep_students / s.enrollment).round(1)
s["el_pct"] = (100 * s.el_students / s.enrollment).round(1)
s["incidents_per_100_students"] = (100 * s.incidents / s.enrollment).round(1)
s = s.reindex(["District"] + sorted(i for i in s.index if i != "District")).fillna(0)
s.index.name = "school"
s.to_csv(out / "school_summary.csv")

g = st[st.chart_id == "home-grade"].copy()
g["grade"] = g["category"].astype(float).astype(int)
e = g.pivot_table(index="school", columns="grade", values="value", aggfunc="sum").fillna(0).astype(int)
e = e.reindex(columns=range(9), fill_value=0)
e.columns = [f"grade_{c}" for c in e.columns]
e["total"] = e.sum(axis=1)
e.drop(index="District", errors="ignore").to_csv(out / "enrollment_by_school_grade.csv")

tot = s.drop("District")[["enrollment", "incidents"]].sum()
print(s[["enrollment", "iep_students", "incidents"]].to_string())
print("Schools sum to district:", tot.enrollment == s.loc["District", "enrollment"], tot.incidents == s.loc["District", "incidents"])
print("Grade chart totals match enrollment:", (e.drop(index="District", errors="ignore")["total"] == s.drop("District")["enrollment"]).all())
