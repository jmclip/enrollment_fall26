# Scraping the D65 Data Dashboard

How the dashboard data in `../data/` was collected, and how to repeat it.

> **AI assistance:** This analysis was built with help from Claude, Anthropic's AI assistant. Claude can make mistakes, including in transcribing data, in calculations and in interpretation. Please verify figures against the original sources before relying on them.

## The source

- **Site:** [data.district65.net](https://data.district65.net), Evanston/Skokie School District 65's public "D65 Dashboard"
- **Pages:** Home, Students (Assessments, Attendance, Discipline) and Sustainability (Utility Usage, Scorecard)
- **Filters on the Students pages:** school, grade, race/ethnicity, IEP, EL and free/reduced lunch
- **What's available:** only the aggregates the charts show (counts, percentages, distributions). No student-level records are exposed. Groups under 10 students are merged into "Other*".
- **Pulled:** 2026-09-23 (fall of SY27)

## How the site works

The dashboard is a [Plotly Dash](https://dash.plotly.com/) app. Everything a chart shows comes from a few endpoints:

| Endpoint | What it returns |
|---|---|
| `GET /_dash-layout` | Page structure, including dropdown options such as the test types |
| `GET /_dash-dependencies` | Every callback: its outputs, inputs and state (the "API map") |
| `POST /_dash-update-component` | Runs one callback and returns its outputs, usually Plotly figures |

**The flow for student data:**

1. **Load.** A startup callback (input `dummy.children`) loads all datasets **on the server** and returns only keys, for example `SERVERSIDE_{"backend_uid": "FileSystemBackend…", "key": "ps_df_current_1790160202"}`. It uses dash-extensions' server-side outputs.
2. **Filter.** The filter callback (outputs `ps-df-current-filter.data`, `bm-df-filter.data`, …) takes those keys plus the filter values and returns keys to the filtered datasets.
3. **Chart.** Chart callbacks take the filtered keys and return Plotly figures:

| Callback (one output from it) | Page | Charts |
|---|---|---|
| `home-grade.figure` | `/` | Enrollment, ADA, IEP, EL, TWI, race/ethnicity, grade, incident levels |
| `att-ada.figure` | `/students/attendance` | ADA, chronic absenteeism, attendance-rate distribution |
| `lvl.figure` | `/students/discipline` | Incidents by level, month, race, grade, school, plus summary counts |
| `ast-graph-1.figure` + `test-type-dropdown.value` | `/students/assessments` | Benchmark categories, percentile and growth distributions for STAR Reading, STAR Early Literacy (and Spanish versions), i-Ready Math |
| `global-use.figure` + `account-dropdown-menu.value` | `/sustainability/utility-usage` | Utility use, carbon, cost, EUI, savings; "All" or one of 18 building accounts |

**Decoding:** Plotly sends number arrays as base64 typed arrays, `{"dtype": "i2", "bdata": "…"}`. Decode them with the given dtype, for example `numpy.frombuffer(base64.b64decode(bdata), dtype)`. Histograms contain one value per student, so the export groups them into 10-point bins.

## ⚠️ The shared-filter problem

The server stores filtered datasets under **one key shared by every visitor**, for example `ps_df_current_filter_<timestamp>`. If someone else filters the dashboard between your filter call and your chart call, you get *their* subset.

Safeguards used:

- Requests run strictly one after another: filter, then charts, then the next school.
- **Consistency check:** each school's IEP pie (Has IEP + No IEP) must add up to its enrollment number, and the school is rerun until it does.
- **Totals check:** school enrollments, IEP counts and incidents must add up to the district totals (5,462 / 953 / 968 on 2026-09-23).

## Option A: run the script

```bash
pip install -r requirements.txt
python3 scraping/d65_scrape.py          # run from the project folder
```

`d65_scrape.py` calls the dashboard the same way the browser does. It pulls the district-wide view, each school, all five assessments and all 19 utility views ("All" plus 18 accounts). It writes these files to `data/`:

- `students_home_demographics.csv`
- `students_attendance.csv`
- `students_discipline.csv`
- `students_assessments.csv`
- `sustainability_utility.csv`
- `school_summary.csv`
- `d65_dashboard_all_long.csv`

It then prints whether the schools add up to the district totals. Rerun the notebook afterward.

> The script's decoding was tested against real responses, but the script hasn't been run end to end against the live site. Expect small fixes on its first run: callback ids change if the district updates the dashboard.

## Option B: reproduce by hand in a browser

This is how the 2026-09-23 pull was actually done.

1. Open [data.district65.net](https://data.district65.net), then open developer tools (Network tab).
2. Filter requests for `_dash-update-component`. Click through the pages and change a filter, and each chart's request and JSON response appears.
3. In the Console, `await fetch('/_dash-dependencies').then(r => r.json())` lists every callback, and repeating a request with `fetch('/_dash-update-component', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: …})` returns the same data.
4. The pull ran the steps above from the browser console for the district and each of the 14 schools, then for each utility account. It flattened the figures into rows, checked sums (and SHA-256 checksums when copying the data out), and decoded them into the CSVs.

## Being a good citizen

- Space out requests (the script pauses about 0.5 s between calls) and pull only what you need. This is a small district server.
- The data is public and aggregate, but it describes students. Keep small-group caveats in mind when publishing.

## Output format

All dashboard CSVs are long/tidy: `school` (or `account`), `chart_id`, `chart_title`, `series`, `category`, `value`. Summary-count tables (for example "Students: 5462") become `category = Students`, `value = 5462`.
