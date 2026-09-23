#!/usr/bin/env python3
"""
Pull the aggregate numbers behind https://data.district65.net (a Plotly Dash app)
and save them as CSVs.

How it works: the dashboard keeps its raw data on the server. Each chart is built
by a POST to /_dash-update-component. This script makes the same calls the browser
makes, decodes the Plotly figures, and writes tidy CSVs.

Usage:   python3 scraping/d65_scrape.py   (from the project folder; writes/refreshes the dashboard CSVs in data/)
Details: scraping/README.md
Needs:   pip install requests pandas

Note: the site's "filtered" datasets are cached server-side under one shared key,
so if someone else is filtering the dashboard at the same moment, results can
cross. The script re-runs a school until its IEP pie adds up to its enrollment,
and checks that schools sum to the district total at the end.
"""
import base64, datetime, pathlib, re, sys, time
import numpy as np, pandas as pd, requests

BASE = "https://data.district65.net"
TESTS = ["STAR Reading", "STAR Early Literacy", "STAR Reading Spanish",
         "STAR Early Literacy Spanish", "i-Ready Math"]
S = requests.Session()
S.headers["User-Agent"] = "d65-dashboard-export (personal research)"
DEPS = None


def call(output_contains, inputs, state=(), changed=()):
    """POST one Dash callback, the same request the browser makes, and return its response.

    output_contains: any output id of the callback (used to look it up in /_dash-dependencies).
    Retries a few times, because the dashboard server occasionally drops requests.
    """
    global DEPS
    if DEPS is None:
        DEPS = S.get(f"{BASE}/_dash-dependencies", timeout=60).json()
    cb = next(d for d in DEPS if output_contains in d["output"] and not d.get("clientside_function"))
    spec = cb["output"]
    parts = spec[2:-2].split("...") if spec.startswith("..") else [spec]
    outs = [dict(zip(("id", "property"), p.split("@")[0].split("."))) for p in parts]
    outs = outs if spec.startswith("..") else outs[0]
    body = {"output": spec, "outputs": outs, "inputs": list(inputs),
            "state": list(state), "changedPropIds": list(changed)}
    for attempt in range(4):
        r = S.post(f"{BASE}/_dash-update-component", json=body, timeout=120)
        if r.status_code == 204:
            return {}
        if r.ok:
            return r.json()["response"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def dec(v):
    """Decode Plotly's base64 typed arrays."""
    if isinstance(v, dict) and "bdata" in v:
        a = np.frombuffer(base64.b64decode(v["bdata"]), dtype=np.dtype(v["dtype"]))
        if v.get("shape"):
            a = a.reshape([int(x) for x in str(v["shape"]).split(",")])
        return a.tolist()
    return v


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "")


def texts(node):
    """Collect the text strings inside a Dash HTML component (used for the summary-count tables)."""
    out = []
    def walk(x):
        if isinstance(x, (str, int, float)):
            out.append(str(x))
        elif isinstance(x, list):
            for i in x: walk(i)
        elif isinstance(x, dict):
            walk(x.get("children", x.get("props", {}).get("children")))
    walk(node)
    return out


def bin10(x):
    """Group a 0-100 value into a 10-point bin label (e.g. 57 -> '50-59'); 100 and above -> '100+'."""
    x = float(x)
    if x >= 100: return "100+"
    b = int(x // 10) * 10
    return f"{b}-{b + 9}"


def flatten(scope, page, resp, test=""):
    """Turn one callback response (a dict of charts) into tidy rows.

    Bars/pies -> one row per category; indicators -> one 'value' row;
    histograms (per-student values) -> counts in 10-point bins; box plots are skipped.
    """
    rows = []
    for cid, v in resp.items():
        base = dict(scope=scope, page=page, test_type=test, chart_id=cid)
        if cid.startswith("students-count"):
            for t in texts(v.get("children")):
                m = re.match(r"^(.*?):\s*([\d.]+)$", t)
                if m:
                    rows.append({**base, "chart_title": "summary counts", "series": "",
                                 "category": m[1], "value": float(m[2])})
            continue
        fig = v.get("figure") if isinstance(v, dict) else None
        if not fig:
            continue
        title = strip_html((fig.get("layout", {}).get("title") or {}).get("text"))
        for t in fig.get("data", []):
            typ, name = t.get("type"), t.get("name") or ""
            if typ == "box":
                continue
            if typ == "indicator":
                rows.append({**base, "chart_title": title or strip_html((t.get("title") or {}).get("text")),
                             "series": "", "category": "value", "value": t.get("value")})
                continue
            if typ == "histogram":  # per-student values -> binned counts
                s = pd.Series(dec(t.get("x")) or []).map(bin10).value_counts()
                for k in sorted(s.index, key=lambda b: 1000 if b == "100+" else int(b.split("-")[0])):
                    rows.append({**base, "chart_title": f"{title} (counts, 10-pt bins)", "series": name,
                                 "category": k, "value": int(s[k])})
                continue
            x = dec(t.get("x", t.get("labels"))) or []
            y = dec(t.get("y", t.get("values"))) or []
            cat, val = (y, x) if t.get("orientation") == "h" else (x, y)
            for c, v2 in zip(cat, val):
                rows.append({**base, "chart_title": title, "series": name, "category": c, "value": v2})
    return rows


def main():
    """Pull district-wide and per-school student pages, then every utility account, and write CSVs to data/."""
    init = call("ps-df-current.data", [{"id": "dummy", "property": "children"}])
    key = lambda k: init[k]["data"]
    schools = [o["label"] if isinstance(o, dict) else o for o in init["school-filter"]["options"]]
    accounts = init["accounts"]["data"]
    stores = ["bm-df", "iready-df", "star-df", "star-el-df", "star-es-df", "star-el-es-df"]

    def filtered(school=None):
        """Apply the dashboard's school filter (or none, for district-wide) and return the filtered dataset keys."""
        r = call("ps-df-current-filter.data",
                 [{"id": "ps-df-current", "property": "data", "value": key("ps-df-current")},
                  {"id": "apply-filters-btn", "property": "n_clicks", "value": 1},
                  {"id": "reset-filters-btn", "property": "n_clicks", "value": None}],
                 [{"id": s, "property": "data", "value": key(s)} for s in stores] + [
                  {"id": "school-filter", "property": "value", "value": [school] if school else None},
                  {"id": "grade-filter", "property": "value", "value": None},
                  {"id": "race-filter", "property": "value", "value": None},
                  {"id": "iep-filter", "property": "value", "value": []},
                  {"id": "el-filter", "property": "value", "value": []},
                  {"id": "lunch-filter", "property": "value", "value": []}],
                 ["apply-filters-btn.n_clicks"])
        return {k.replace("-filter", ""): v["data"] for k, v in r.items() if isinstance(v, dict) and "data" in v}

    def student_pages(label, school):
        """All Students-section charts (home, attendance, discipline, all five assessments) for one school or the district."""
        F = filtered(school)
        d = lambda i, k: {"id": i, "property": "data", "value": F[k]}
        url = lambda p: {"id": "url", "property": "pathname", "value": p}
        rows = flatten(label, "home", call("home-grade.figure",
                       [d("ps-df-current-filter", "ps-df-current"), d("bm-df-filter", "bm-df"), url("/")], changed=["url.pathname"]))
        rows += flatten(label, "attendance", call("att-ada.figure",
                        [d("ps-df-current-filter", "ps-df-current"), url("/students/attendance")], changed=["url.pathname"]))
        rows += flatten(label, "discipline", call("lvl.figure",
                        [d("bm-df-filter", "bm-df"), url("/students/discipline")], changed=["url.pathname"]))
        for tt in TESTS:
            rows += flatten(label, "assessments", call("ast-graph-1.figure",
                [d("iready-df-filter", "iready-df"), d("star-df-filter", "star-df"), d("star-el-df-filter", "star-el-df"),
                 d("star-es-df-filter", "star-es-df"), d("star-el-es-df-filter", "star-el-es-df"),
                 {"id": "test-type-dropdown", "property": "value", "value": tt}, url("/students/assessments")],
                changed=["test-type-dropdown.value"]), tt)
        return rows

    def consistent(rows):
        """Guard against the shared-filter problem: the IEP pie must add up to the enrollment number."""
        iep = sum(r["value"] for r in rows if r["chart_id"] == "home-iep")
        enr = next((r["value"] for r in rows if r["chart_id"] == "home-enrollment"), None)
        return enr and iep == enr

    all_rows = []
    for school in [None] + schools:
        label = school or "District"
        for attempt in range(4):
            rows = student_pages(label, school)
            if consistent(rows):
                break
            print(f"  {label}: inconsistent result, retrying", file=sys.stderr); time.sleep(3)
        else:
            print(f"  WARNING: {label} never came back consistent", file=sys.stderr)
        print(f"students: {label}"); all_rows += [dict(dataset="students", **r) for r in rows]
        time.sleep(0.5)

    per_building = {"global-use-school", "ghg-school", "cost-savings-school"}
    for acct in ["All"] + accounts:
        r = call("global-use.figure",
                 [{"id": "energyCAP-data", "property": "data", "value": key("energyCAP-data")},
                  {"id": "ghg-df", "property": "data", "value": key("ghg-df")},
                  {"id": "account-dropdown-menu", "property": "value", "value": acct},
                  {"id": "url", "property": "pathname", "value": "/sustainability/utility-usage"}],
                 changed=["account-dropdown-menu.value"])
        rows = [x for x in flatten(acct, "utility-usage", r) if acct == "All" or x["chart_id"] not in per_building]
        print(f"energy: {acct}"); all_rows += [dict(dataset="energy", **x) for x in rows]
        time.sleep(0.5)

    df = pd.DataFrame(all_rows)
    out = pathlib.Path(__file__).resolve().parent.parent / "data"   # project data/ folder; overwrites the dashboard CSVs
    out.mkdir(exist_ok=True)
    df.to_csv(out / "d65_dashboard_all_long.csv", index=False)
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

    tot = s.drop("District")[["enrollment", "incidents"]].sum()
    ok = tot.enrollment == s.loc["District", "enrollment"] and tot.incidents == s.loc["District", "incidents"]
    print(f"\nWrote {len(df)} rows to {out}")
    print("Check: schools sum to district totals ->", "OK" if ok else f"MISMATCH {dict(tot)}")


if __name__ == "__main__":
    main()
