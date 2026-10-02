"""Extract every table from District 65's Opening of Schools Report 2024-2025 (January 2025,
data as of Sept. 30, 2024) into tidy CSVs in data/oos_2024_25/.

Source: https://resources.finalsite.net/images/v1738077970/district65net/vw6lsh1di6lqoeyhkv2a/OpeningofSchoolsReportSY24-25-FINAL.pdf
(saved in source/; SHA-256 01216830...ad94). Tables are read with pdfplumber; blank cells are
written as 0 (the report leaves zero cells blank in Tables 2-10). Every table total is checked.
Made with help from Claude (an AI model), which can make mistakes. Please verify.
"""
import os
import re
import pdfplumber
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "source", "OpeningofSchoolsReportSY24-25-FINAL.pdf")
OUT = os.path.join(HERE, "data", "oos_2024_25")
os.makedirs(OUT, exist_ok=True)

clean = lambda s: re.sub(r"\s+", " ", s or "").strip()


def num(s):
    s = clean(s).replace(",", "").replace("*", "")
    if s == "":
        return 0
    try:
        return int(s)
    except ValueError:
        return float(s) if re.fullmatch(r"-?\d+\.\d+", s) else s


pdf = pdfplumber.open(PDF)
tables = {}  # title -> list of row lists (header row first)
for i, page in enumerate(pdf.pages):
    for t in page.extract_tables():
        first = next((clean(c) for c in t[0] if c), "")
        title = first if first.startswith("Table") else None
        if title is None and i == 2:
            title = "Across Years Comparison"
            rows = t
        else:
            rows = t[1:]
        key = title.split(" - ")[0] if title.startswith("Table") else title
        if key in tables:
            tables[key]["rows"] += rows[1:]          # repeated header on continuation pages
            tables[key]["pages"].append(i + 1)
        else:
            tables[key] = {"title": title, "rows": rows, "pages": [i + 1]}


def frame(key):
    t = tables[key]
    hdr = [(clean(h) or "metric").replace("- ", "-") for h in t["rows"][0]]
    df = pd.DataFrame([[clean(c) for c in r] for r in t["rows"][1:]], columns=hdr)
    return df


written = []


def save(df, name):
    df.to_csv(os.path.join(OUT, name), index=False)
    written.append((name, len(df)))


# Across years: keep the text (has % and * flags) and parse counts / pct / flag
ay = frame("Across Years Comparison")
long = ay.melt(id_vars="metric", var_name="school_year", value_name="value_text")
long["from_previous_report"] = long.value_text.str.contains(r"\*")
long["count"] = long.value_text.str.extract(r"^([\d.]+)")[0].astype(float)
long["pct"] = long.value_text.str.extract(r"\((\d+)%\)")[0].astype(float)
long.loc[long.value_text.str.endswith("%") & ~long.value_text.str.contains(r"\("), "pct"] = \
    long.value_text.str.extract(r"^([\d.]+)%")[0].astype(float)
long.loc[long.value_text.str.match(r"^[\d.]+%"), "count"] = None
save(long, "across_years.csv")

# Tables with a school/first column + numeric columns
simple = {
    "Table A": ("table_a_school_enrollment.csv", "Total Enrollment"),
    "Table B": ("table_b_demographic_changes.csv", None),
    "Table C": ("table_c_native_language.csv", None),
    "Table D": ("table_d_accepted_to_magnet.csv", "Total"),
    "Table 2": ("table_2_enrollment_by_grade.csv", None),
    "Table 3A": ("table_3a_kindergarten_by_race.csv", None),
    "Table 3B": ("table_3b_prek_experience_by_race.csv", None),
    "Table 3C": ("table_3c_prek_experience_by_school.csv", None),
    "Table 4": ("table_4_low_income.csv", None),
    "Table 5": ("table_5_iep_by_school.csv", None),
    "Table 6": ("table_6_k5_twi.csv", None),
    "Table 7": ("table_7_not_attending_area_school.csv", None),
    "Table 8A": ("table_8a_bessie_rhodes_by_area.csv", None),
    "Table 8B": ("table_8b_king_arts_by_area.csv", None),
    "Table 9": ("table_9_acc_by_area.csv", None),
    "Table 10": ("table_10_child_care.csv", None),
}
frames = {}
for key, (name, total_label) in simple.items():
    df = frame(key)
    first = df.columns[0]
    for c in df.columns[1:]:
        if c != "Pct":
            df[c] = df[c].map(num)
    df[first] = df[first].str.replace("’", "'")
    frames[key] = df
    save(df, name)

# Table 1: school x grade x race (grade: -5..-1 = birth-PK ages, 0 = K)
t1 = frame("Table 1")
for c in t1.columns[1:]:
    t1[c] = t1[c].map(num)
t1["School"] = t1["School"].str.replace("’", "'")
frames["Table 1"] = t1
save(t1, "table_1_enrollment_school_grade_race.csv")
pd.DataFrame([{"table": v["title"], "pages": ",".join(map(str, v["pages"])), "rows": len(v["rows"]) - 1}
              for v in tables.values()]).to_csv(os.path.join(OUT, "_tables_index.csv"), index=False)

# ── Checks ──────────────────────────────────────────────────────────────────────
problems = []
def check(label, got, want):
    if got != want:
        problems.append(f"{label}: got {got}, expected {want}")

A = frames["Table A"]; tot = A.loc[A.School == "Total Enrollment", "Students"].item()
check("Table A sums to total", A.loc[A.School != "Total Enrollment", "Students"].sum(), tot)
check("Table A total = 6,241", tot, 6241)
check("Table 1 total = 6,241", t1["Total Enrollment"].sum(), 6241)
race_cols = [c for c in t1.columns if c not in ("School", "Grade", "Total Enrollment")]
check("Table 1 rows add across", int((t1[race_cols].sum(axis=1) != t1["Total Enrollment"]).sum()), 0)
g2 = frames["Table 2"]; gcols = [c for c in g2.columns if c not in ("School", "Total Enrollment")]
check("Table 2 rows add across", int((g2[gcols].sum(axis=1) != g2["Total Enrollment"]).sum()), 0)
check("Table 2 total", g2["Total Enrollment"].sum(), 6241)
by_school = t1.groupby("School")["Total Enrollment"].sum()
a_map = A.set_index("School")["Students"]
for s, v in by_school.items():
    if s in a_map.index: check(f"Table 1 vs A: {s}", v, a_map[s])
check("Table 3A total K = 534 + Park/SEES", frames["Table 3A"]["Total Enrollment"].sum(), 540)
check("Table 4 total = 2,483", frames["Table 4"]["Low Income"].sum(), 2483)
check("Table 5 total = 1,213", frames["Table 5"]["Total IEP"].sum(), 1213)
t6 = frames["Table 6"]; check("Table 6 TWI (excl. WVD) = 775",
      t6[["Monitoring 2 yrs", "TWE", "TWS", "TWX"]].sum().sum(), 775)
check("Table 7 total = 477", frames["Table 7"]["Total Enrollment"].sum(), 477)
check("Table D total", frames["Table D"].query("`Attendance Area School` != 'Total'")["Enrollment"].sum(), 140)
check("Table 9 total = 77", frames["Table 9"]["Total Enrollment"].sum(), 77)
check("Table 10 total", frames["Table 10"].query("School != 'Total'")["Total Enrollment"].sum(), 464)
for k in ["Table 3A", "Table 5", "Table 7", "Table 8A", "Table 8B", "Table 9", "Table 10", "Table 3C"]:
    df = frames[k]; tc = [c for c in df.columns if c.startswith("Total")][0]
    parts = [c for c in df.columns[1:] if c not in (tc, "Pct")]
    bad = df[df[parts].sum(axis=1) != df[tc]]
    if len(bad): problems.append(f"{k}: {len(bad)} rows don't add across: {bad.iloc[:, 0].tolist()}")

for n, r in written: print(f"  {n}: {r} rows")
print("CHECKS:", "all pass" if not problems else "\n  " + "\n  ".join(problems))
