# D65 building use analysis

## Summary: savings need to work with the district we have

District 65 faces a financial crisis that is both immediate and far-reaching: the district is looking to cut about 10% of its budget, roughly $20 million. A solution needs to account for the long time horizon while also producing savings in the short term.

- **School closures are being treated as the primary lever, but each one saves less than it appears.** After added busing, closing one school nets roughly $0.2–0.7M a year, about 1–3.5% of the $20 million target. Closing two schools would still come to only about 2–7% of the target. Busing takes back 20–35% of the building savings ([details](#closing-schools-transportation-is-an-important-factor-in-savings)). That's before moving and renovation costs, which come first.
- **Closing too many schools can raise costs in both the short and long term,** through added transportation and moving costs. (See [Closing schools: transportation is an important factor in savings](#closing-schools-transportation-is-an-important-factor-in-savings).)
- **Staff time and labor are not being counted.** Much of the budget challenge comes from staffing. Closures focus administrators on problems whose gains are mostly long-term, and pull attention away from the larger short-term savings available through staffing.

Closing buildings may be one way to address the budget gap, but **solving for high utilization is not the answer.** Across 11 elementary schools, utilization explains about 1% of the difference in class size (r = −0.11), and that holds when any one school is left out (finding 1 below). Any plan has to work with the buildings we have, not an idealized version of an imagined district.

- **Some of the lowest utilization is in larger buildings.** Lincoln, for example, is at 61% of a 576-seat capacity. Instead of focusing only on the utilization rate, the district could look at other good uses for the space, such as partnering with a local preschool.
- **The smallest classes are at the schools with dual-language (TWI) programs** (finding 3 below). Paradoxically, TWI programs are hard to get into, yet have smaller classes in the upper grades, through attrition and the design of the program. The district could allow more strands in K–2 and then consider consolidating strands in grades 4–5, as Oakton appears to have done in 5th grade this year.

**Additional or alternative strategies that could be pursued at the same time.** Closures alone won't reach the $20 million target, so these could run alongside them:

- **Creative building use:** lease or share underused space, for example with a preschool or community partner, instead of judging buildings on utilization alone.
- **Voluntary retirement incentives, negotiated with the teachers' union:** encouraging eligible staff to retire, based on years of service, can reduce costs through attrition instead of layoffs, and help the district keep a stable, high-quality teaching staff going forward.
- **Opening TWI to nearby communities for tuition, if possible:** filling open dual-language seats with tuition-paying students from outside the district would bring in revenue and fill small upper-grade classes.

The district may or may not need to close buildings, but its plan for savings has to account for the unique nature of our district and its buildings. Otherwise the short- and medium-term savings, the ones we need most, can evaporate.

**What any savings plan should include:**

1. **Itemized savings from the Kingsley and Bessie Rhodes closures:** what was actually saved, by category, net of the costs of opening Foster.
2. **The full cost of closing and relocating a school:** direct costs (moving, packing, IT, closing the building), plus the staff and community time the process takes.
3. **Expected renovation costs at receiving schools** to house the programs that move there, such as TWI, STEP and special education.
4. **The specific position categories to be cut and the savings from each:** for example, administration, building staff, classroom teachers, specialists and support staff.
5. **The impact on class size:** how many classes each affected grade would run before and after, and the resulting class sizes, not just building utilization.
6. **A forward-looking case:** how the plan puts the district on sound financial footing for the long term, and how it will improve educational outcomes for all students, not just how it closes this year's gap.

We need to work with the buildings and the district we have: chasing an artificially high utilization rate can lead to ballooning, persistent cost increases. We are excited by the direction things are heading, and we look forward to hearing the vision for D65's future.

An analysis of how Evanston/Skokie School District 65 buildings are used: enrollment against projections, utilization and capacity, class sizes, dual-language (TWI) strands, attendance-area capture, building space and utility cost.

- **Current data:** the district's public dashboard, [data.district65.net](https://data.district65.net), pulled 2026-09-23 (fall of school year 2026–27, "SY27").
  - **HELP WITH ACCURACY** [crowdsourcing-file here](https://docs.google.com/forms/d/e/1FAIpQLSepZPKRXOA8HTbEoWf8sUmXK_UlhWkK4_6y4cl9NQLNEYL1Bw/viewform?usp=dialog) Complete this form if you have data on schools and class sizes
- **Planning data:** two district utilization/capacity tables, transcribed from screenshots, and Cordogan Clark's February 2022 capacity report (PDF), which verifies the screenshots. See `sources/`.
- **Everything is in one notebook:** `d65_enrollment_by_building.ipynb`. Run it top to bottom to rebuild every table in `data/` and every chart in `images/`.
> **AI assistance:** This analysis was built with help from Claude, Anthropic's AI assistant. Claude can make mistakes, including in transcribing data, in calculations and in interpretation. Please verify figures against the original sources in `sources/` before relying on them.

## Key findings

### 1. High-utilization buildings don't have bigger classes: utilization and class size are unrelated

![Class size vs. utilization, elementary schools](images/chart_class_size_vs_utilization.png)

Each dot is an elementary school: current utilization against estimated average class size. The red line is a least-squares fit.

- **The line is flat.** Class size changes by about 0.02 students per point of utilization (r = −0.11, R² = 0.01, p = 0.75, 11 schools). Utilization explains about 1% of the difference in class size between schools.
- **The two extremes point opposite ways.** Oakton has the highest utilization (79%) and the smallest classes (16.2). Willard has the lowest utilization (51%) and the largest classes (21.3).
- **What drives class size instead:** how each grade divides into classes, and programs (TWI, ACC) that add classes. A building with low utilization can still have full classrooms, and a building with high utilization can have small ones.
- **The result doesn't depend on any one school.** Leaving out each school in turn, the correlation stays between −0.33 and +0.20, and no version is statistically significant (every p ≥ 0.35).

<details>
<summary><b>Show the leave-one-out check</b>: the correlation recomputed 11 times, each time without one school</summary>

| School left out | Its utilization | Its class size | r | R² | Slope | p |
|---|---:|---:|---:|---:|---:|---:|
| *None (all 11)* | | | **−0.11** | 0.01 | −0.022 | 0.75 |
| Dawes | 67% | 18.4 | −0.11 | 0.01 | −0.022 | 0.77 |
| Dewey | 59% | 17.5 | −0.19 | 0.04 | −0.040 | 0.59 |
| Foster | 63% | 17.1 | −0.16 | 0.03 | −0.032 | 0.66 |
| King Arts | 68% | 19.8 | −0.12 | 0.01 | −0.025 | 0.74 |
| Lincoln | 61% | 19.6 | −0.08 | 0.01 | −0.017 | 0.82 |
| Lincolnwood | 77% | 21.1 | −0.33 | 0.11 | −0.068 | 0.35 |
| Oakton | 79% | 16.2 | +0.18 | 0.03 | +0.036 | 0.63 |
| Orrington | 58% | 17.9 | −0.17 | 0.03 | −0.038 | 0.63 |
| Walker | 73% | 21.2 | −0.25 | 0.06 | −0.048 | 0.49 |
| Washington | 73% | 17.8 | −0.06 | 0.00 | −0.013 | 0.87 |
| Willard | 51% | 21.3 | +0.20 | 0.04 | +0.045 | 0.58 |

*Slope = change in average class size per percentage point of utilization. Only dropping Oakton or Willard flips the sign, and only to about +0.2. A rank-based (Spearman) correlation gives the same picture: −0.28 to +0.14.*

</details>

### 2. Utilization runs from 51% to 83%

![Current building utilization by school](images/chart_utilization_current.png)

Utilization = fall SY27 enrollment ÷ capacity (the smaller of the district's Cap Total and Cordogan Clark's capacity).

- **STEP (\*)** program use reduces usable capacity at Lincoln, Lincolnwood and Washington.

### 3. The smallest classes are at the dual-language schools

![Estimated average class size by elementary school](images/chart_class_size_by_school_overall.png)

Estimated average class size per school (average of its K–5 grades; King Arts K–5 only).

- **Five of the six smallest averages are TWI schools:** Oakton 16.2, Foster 17.0, Dewey 17.5, Washington 17.8 and Dawes 18.4. The sixth is Orrington, at 17.9.
- **TWI schools average 17.2 students per class; the other schools average 20.0.** Each strand adds its own class at every grade, whether or not it's full.
- **The largest classes are at schools with no programs:** Willard (21.3), Walker (21.2) and Lincolnwood (21.1).

*Class counts are estimated, because the dashboard reports enrollment by grade, not by class: the fewest monolingual/mainstream classes that keep each class at 24 or fewer, plus one class per TWI strand and one ACC class per grade at Oakton. Washington and Oakton's 5th grade use reported class counts. The full math is in the table below.*

### 4. A third of elementary grades average under 18 students per class

![Estimated class size by school and grade, K–5](images/chart_class_size_heatmap.png)

Red is small classes, purple is about 18, and blue is large (up to the 24 cap). The last column is each school's average.

- **23 of the 66 school-grades are under 18.** They are concentrated at Oakton (5 of 6 grades), Dewey (4), and Dawes, Foster, Orrington and Washington (3 each).
- **Small grades split awkwardly.** Orrington's 4th grade has 27 students in 2 classes (13.5 each). A 25th student forces a second class.
- **Walker, Willard and Lincolnwood are blue almost everywhere.**

## Class-size math by school

<details>
<summary><b>Show the class-size math</b>: students ÷ classes for every school and grade, the Oakton note, and the parent-report check</summary>

Students in the grade ÷ estimated classes = average class size (fall SY27, elementary, King Arts K–5 only).

| School | K | 1 | 2 | 3 | 4 | 5 | Avg | Program classes per grade |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Willard | 40 ÷ 2 = **20.0** | 43 ÷ 2 = **21.5** | 44 ÷ 2 = **22.0** | 53 ÷ 3 = **17.7** | 46 ÷ 2 = **23.0** | 47 ÷ 2 = **23.5** | **21.3** | – |
| Walker | 45 ÷ 2 = **22.5** | 57 ÷ 3 = **19.0** | 42 ÷ 2 = **21.0** | 63 ÷ 3 = **21.0** | 66 ÷ 3 = **22.0** | 44 ÷ 2 = **22.0** | **21.2** | – |
| Lincolnwood | 48 ÷ 2 = **24.0** | 60 ÷ 3 = **20.0** | 54 ÷ 3 = **18.0** | 42 ÷ 2 = **21.0** | 48 ÷ 2 = **24.0** | 79 ÷ 4 = **19.8** | **21.1** | – |
| King Arts | 41 ÷ 2 = **20.5** | 40 ÷ 2 = **20.0** | 37 ÷ 2 = **18.5** | 56 ÷ 3 = **18.7** | 54 ÷ 3 = **18.0** | 46 ÷ 2 = **23.0** | **19.8** | – |
| Lincoln | 57 ÷ 3 = **19.0** | 73 ÷ 4 = **18.2** | 53 ÷ 3 = **17.7** | 43 ÷ 2 = **21.5** | 68 ÷ 3 = **22.7** | 56 ÷ 3 = **18.7** | **19.6** | – |
| Dawes | 43 ÷ 2 = **21.5** | 45 ÷ 3 = **15.0** | 42 ÷ 2 = **21.0** | 48 ÷ 3 = **16.0** | 59 ÷ 3 = **19.7** | 51 ÷ 3 = **17.0** | **18.4** | 1 TWI |
| Orrington | 40 ÷ 2 = **20.0** | 35 ÷ 2 = **17.5** | 42 ÷ 2 = **21.0** | 52 ÷ 3 = **17.3** | 27 ÷ 2 = **13.5** | 55 ÷ 3 = **18.3** | **17.9** | – |
| Washington | 58 ÷ 4 = **14.5** | 59 ÷ 3 = **19.7** | 63 ÷ 3 = **21.0** | 64 ÷ 4 = **16.0** | 62 ÷ 4 = **15.5** | 81 ÷ 4 = **20.2** | **17.8** | 2 TWI (class counts reported) |
| Dewey | 48 ÷ 3 = **16.0** | 55 ÷ 3 = **18.3** | 45 ÷ 3 = **15.0** | 52 ÷ 3 = **17.3** | 64 ÷ 3 = **21.3** | 51 ÷ 3 = **17.0** | **17.5** | 1 TWI |
| Foster | 46 ÷ 3 = **15.3** | 42 ÷ 3 = **14.0** | 65 ÷ 4 = **16.2** | 79 ÷ 4 = **19.8** | 57 ÷ 3 = **19.0** | 72 ÷ 4 = **18.0** | **17.0** | 2 TWI |
| Oakton | 68 ÷ 4 = **17.0** | 55 ÷ 4 = **13.8** | 58 ÷ 4 = **14.5** | 54 ÷ 4 = **13.5** | 69 ÷ 4 = **17.2** | 63 ÷ 3 = **21.0** | **16.2** | 1 TWI + 1 ACC (5th: 3 classes, reported) |

*Each cell shows students in that grade ÷ estimated classes = average class size. "Avg" is the average of the six grade averages. "Program classes per grade" lists the dual-language (TWI) and ACC classes included in each grade's count. The rest are monolingual/mainstream classes. For example, Foster kindergarten = 2 TWI + 1 monolingual/mainstream = 3 classes. Monolingual/mainstream classes are the fewest that keep each class at 24 or fewer students. TWI and ACC students are assumed evenly spread across K–5, and Oakton ACC uses the 73 projected students. These are estimates, not reported class counts. Full detail: `data/class_size_detail_by_school.csv`.*

**Note on Oakton.** Oakton's TWI class sizes use the school's total TWI enrollment from the dashboard (75 students), averaged evenly across K–5 (about 12–13 per grade). The dashboard has no ACC enrollment data, so ACC is handled the same way: the 1A table's projected 73 ACC students, averaged across K–5 (about 12 per grade). Unless combined ACC + TWI enrollment in a grade is substantially larger than 25, the results hold: Oakton still needs one TWI class and one ACC class per grade, and the class counts and averages above don't change. We contacted the district on 2026-09-25 about Oakton's strands per grade and will update this when they respond.

**Checked against parent reports (as of 2026-09-24).** Parents reported 11 actual classes through the [crowdsourcing form](https://docs.google.com/forms/d/e/1FAIpQLSepZPKRXOA8HTbEoWf8sUmXK_UlhWkK4_6y4cl9NQLNEYL1Bw/viewform?usp=dialog). Ten were reported with confidence 4–5 out of 5 and a named source (the teacher, a conference, a class email list, the PTA or a child in the class). These are still second-hand reports, not district data. Notebook section 12 compares each report with the estimate above.

| School | Grades reported | Classes reported | Result |
|---|---|---:|---|
| Willard | K, 1, 2, 3, 4, 5 | 8 | **All 8 match the estimate within 2 students.** In grades 1 and 2 every class was reported: 1st grade 22 + 21 = 43, the same as the dashboard's 43. 2nd grade 22 + 21 = 43, against 44 on the dashboard (one parent gave a grade total of 42). |
| Washington | 2, 5 | 3 | **2nd grade matches; 5th grade is 3 above.** 2nd grade: a monolingual/mainstream class of 23 and a TWI class of 19, against an estimate of 21.0 (63 students in 3 classes). The notebook now uses Washington's reported class counts: 4 per grade, 3 in 1st and 2nd. 5th grade (81 students, 4 classes) is departmental, with reported classes of 23 against our 20.2. |

**Still unverified:** every other school's class counts, and class sizes at Washington outside 2nd and 5th grade. Washington's class counts per grade are reported, but its class sizes are still enrollment ÷ classes. **Foster** also has two TWI strands and stays on the estimate until parents report. Files: `data/parent_reported_class_sizes.csv` (every form response), `data/class_size_parent_check.csv` (one row per class, compared with the estimate) and `data/class_size_parent_check_by_grade.csv` (reported classes against dashboard enrollment by grade).

</details>

## Closing schools: transportation is an important factor in savings

Closing a school saves building costs, but some of its students then need a bus. **For a typical closure, added busing takes back roughly a fifth to a third of the building savings.** Any closure estimate should net it out.

This estimate uses the district's transportation data from the Structural Deficit Reduction Plan (SDRP) closure scenarios. Those tables count students at every school by how they get there (bus, hazard route, program placement or walk), both today and under each closure scenario. Because we don't have current busing data, the estimate may count more bused students than there are in SY 2026-27.

| One school closed (typical) | Low | High |
|---|---:|---:|
| Building savings | $0.47M | $0.82M |
| Added busing | −$0.27M | −$0.15M |
| **Net savings** | **$0.20M** | **$0.67M** |

*Yearly. Net low = low savings minus high busing cost; net high = the reverse.*

- **A typical closure adds about 120 general-education bus riders** (roughly 85 to 155, depending on the school), or one or two new bus routes.
- **Most new riders are hazard riders**: students whose new walk crosses an unsafe route, not students who live more than 1.5 miles away. They cluster at one or two receiving schools, which keeps the number of new routes low.
- **Building savings:**
  - the principal ($181K with benefits, FY26 salary disclosure)
  - one office position ($60K, **assumed**)
  - about 2.5 custodians ($65K each, **assumed**)
  - utilities (about $67K a year for a typical building, 2025)
  - The high end adds a librarian ($133K), an assistant principal ($160K) and a health clerk, only if those positions are cut. No savings from combining classes are included.
- **Added busing:**
  - The low end counts new double routes at about $90K each, each carrying about 110 riders over two runs.
  - The high end uses the district's average cost per general-education rider, about $2,200 ($2.4M in general-ed routes ÷ 1,104 riders today; Transportation Memo to the Board, Feb 9, 2026).
  - Special-education busing doesn't change.
- **Not included:**
  - one-time costs: moving, and renovating receiving schools
  - avoided capital and maintenance at closed buildings
  - families who leave the district
  - changes in state funding
  - crossing guards or route changes that could remove a hazard designation
- **Files:** the district's SDRP transportation tables are in `projections/data/`. The calculation is [`build_building_use_sy27.py`](https://github.com/d65-legionofnerds/d65-legionofnerds.github.io/blob/main/dataanalysis/build_building_use_sy27.py) on the Legion of Data Nerds site, with inputs in `dataanalysis/data/sy27_fall/`.

## Replication and technical details

<details>
<summary><b>Show replication and technical details</b>: how the data was collected, folder layout, how to refresh, data and chart files, notebook outline, methods and definitions, checks, and known limitations</summary>

### How the data was collected

- **Current data** comes from the district's public dashboard, [data.district65.net](https://data.district65.net), a Plotly Dash app. Its charts come from requests to `/_dash-update-component`.
- **The pull (2026-09-23):** those same requests were made for the district as a whole and for each of the 14 schools (Home, Attendance, Discipline, and all five assessments), plus every building's utility data. The chart data was decoded into the tidy CSVs in `data/`.
- **Checks:** every school had to add up to the district totals. The dashboard's filter is shared between visitors, so each school was also checked for internal consistency.
- **Planning data** comes from two district tables (typed in from screenshots) and Cordogan Clark's February 2022 capacity report (PDF). See `sources/sources.md`.

Full replication details, the endpoints and the scraper are in **[`scraping/README.md`](scraping/README.md)**.

### Folder layout

```
d65-dashboard-data/
├── README.md                     this file
├── d65_enrollment_by_building.ipynb  analysis notebook (reads data/, writes data/ and images/)
├── scraping/                     d65_scrape.py (re-pulls the dashboard into data/) and replication notes
├── requirements.txt              Python packages needed
├── data/                         all CSVs: inputs and the tables the notebook writes
├── images/                       all charts (PNG)
└── sources/                      sources.md, the Cordogan Clark report (PDF) and the original screenshots
```

### How to refresh

1. `pip install -r requirements.txt`
2. `python3 scraping/d65_scrape.py` pulls the dashboard again and overwrites the dashboard CSVs in `data/` (the first seven input files below). See `scraping/README.md`.
3. Re-run the notebook top to bottom. It needs only four inputs (`students_home_demographics.csv`, `sustainability_utility.csv`, `utilization_1A_website.csv`, `capacity_cordogan_clark.csv`) and rebuilds every other table and chart. The two transcribed tables don't change unless you edit them.

The dashboard stores filtered results in one shared spot on its server, so another visitor filtering at the same moment can mix up numbers. The script re-runs any school whose totals don't add up, and checks that schools sum to the district.

### Data files (`data/`)

#### Inputs

| File | Source | Contents |
|---|---|---|
| `students_home_demographics.csv` | Dashboard | Home page by school: enrollment, grade, IEP, EL, TWI (TWE/TWS/TWX), race/ethnicity, incident levels |
| `students_attendance.csv` | Dashboard | Average daily attendance, chronic absenteeism, attendance-rate distribution (10-pt bins) by school |
| `students_discipline.csv` | Dashboard | Incidents by level, month, race/ethnicity, grade and school |
| `students_assessments.csv` | Dashboard | STAR Reading and Early Literacy (English and Spanish), i-Ready Math: benchmark categories, percentile and growth distributions (10-pt bins), by school |
| `sustainability_utility.csv` | Dashboard | Utility use (electric, gas), carbon, cost, energy use per sq ft (EUI) and savings, 2018–2026, district ("All") and 18 buildings |
| `d65_dashboard_all_long.csv` | Dashboard | All of the above in one long table |
| `school_summary.csv` | Dashboard | One row per school plus District: enrollment, attendance, chronic absenteeism, IEP/EL counts and %, incidents |
| `utilization_1A_website.csv` | Screenshot, district "1A_Utilization_website" | Per school: SY25 enrollment, area counts, capacity (total, neighborhood, TWI, ACC), **projected** enrollment by program, projected utilization |
| `cordogan_clark_2022_report.csv` | Cordogan Clark report (PDF, Feb 2022) | Every building's summary page: core classroom + SPED sq ft (and science labs), teaching stations, capacity, sq ft per student, 2021–22 enrollment and utilization, capacity goal, PDF page |
| `capacity_cordogan_clark.csv` | Screenshot, capacity table with Cordogan Clark counts | Elementary schools + King Arts: Cap Total, teaching stations, projected enrollment, classroom square feet, Cordogan Clark capacity, floor-plan classrooms, offices, other rooms, comments |

Dashboard files are long/tidy: `school` (or `account`), `chart_id`, `chart_title`, `series`, `category`, `value`.

#### Outputs written by the notebook

**Enrollment**

| File | Contents |
|---|---|
| `enrollment_by_school_grade.csv` | Current enrollment by school and grade (K = grade_0) with totals |
| `enrollment_vs_utilization.csv` | Current vs. projected enrollment (1A table) and SY25, with differences |

**Capacity and utilization**

| File | Contents |
|---|---|
| `utilization_current_vs_predicted.csv` | Predicted vs. current utilization, the capacity used and its source |
| `capacity_comparison.csv` | Every capacity figure per school: district and Cordogan teaching stations, floor-plan classrooms, Cap Total, Cordogan capacity, 24 × classrooms, capacity used and source |
| `building_square_feet.csv` | Estimated square feet per building (derived from energy data; see Methods) |

**Class size (estimated)**

| File | Contents |
|---|---|
| `class_size_detail_by_school.csv` | **Main class-size file.** Every input and step per school and grade: students, cap, estimated TWI and ACC students and classes, monolingual/mainstream students and classes, class sizes |
| `table_students_by_school_grade.csv` | Supporting table 1: students by school and grade (integers, with totals) |
| `table_classes_by_school_grade.csv` | Supporting table 2: estimated classes by school and grade (integers, with totals) |
| `class_size_by_school_overall.csv` | Elementary only (King Arts K–5): average of K–5 grade averages, and the student-weighted average |
| `class_size_vs_utilization.csv` | Per elementary school: estimated average class size and current utilization (the data behind the regression chart) |
| `parent_reported_class_sizes.csv` | Class sizes reported by parents through the crowdsourcing form, one row per response (timestamp, school, grade, program, teacher, class size, grade total if given, confidence 1–5, source) |
| `class_size_parent_check.csv` | One row per reported class (duplicate reports combined), with our estimate for the same school, grade and program, the difference, and Consistent (within 2) or Differs |
| `class_size_parent_check_by_grade.csv` | By school and grade: classes reported, sum of reported sizes, dashboard enrollment, estimated classes |
| `classrooms_needed_vs_available.csv` | Estimated classes vs. the district's floor-plan classroom count, with spare rooms (upper bound) |
| `table_enrollment_twi_by_school_grade.csv` | Elementary enrollment by grade with TWI (and Oakton ACC) breakouts and strands; estimates are whole students that add up to real totals |

**Programs, neighborhood and cost**

| File | Contents |
|---|---|
| `twi_strands.csv` | Dual-language strands: current TWE/TWS/TWX, capacity, strands, rooms, % full, students per room, Spanish-dominant share, projection |
| `attendance_area_capture.csv` | Students living in each attendance area vs. enrolled, total and neighborhood-only capture % |
| `utility_cost_per_student.csv` | 2025 utility cost per building, enrollment, capacity, empty seats, cost per student, cost per seat, cost matching empty seats |

### Charts (`images/`)

| Chart | Shows |
|---|---|
| `chart_projected_vs_current_enrollment.png` | Projected vs. current enrollment by school, with totals and gaps |
| `chart_enrollment_difference.png` | Current minus projected, largest gap first |
| `chart_utilization_predicted_vs_current.png` | Predicted vs. current utilization, gap in points |
| `chart_utilization_current.png` | Current utilization, with capacity and classrooms in each bar |
| `chart_learning_space_share.png` | Classroom square feet as a share of the building |
| `chart_attendance_area_capture.png` | Students living in each area vs. enrolled |
| `chart_utility_cost_per_student.png` | 2025 utility cost per enrolled student |
| `chart_utility_cost_per_seat.png` | 2025 utility cost per seat of capacity |
| `chart_class_size_heatmap.png` | Estimated class size, every elementary school and grade K–5 (King Arts K–5 only) |
| `chart_class_size_vs_utilization.png` | Scatter with regression line: estimated average class size vs. current utilization, elementary schools |
| `chart_class_size_by_grade.png` | District average class size by grade, K–8 |
| `chart_class_size_by_school.png` | One panel per school: class size by grade, with students ÷ classes |
| `chart_class_size_elementary_by_grade.png` | Elementary schools, one panel each: class size in each K–5 grade, with students ÷ classes and the TWI/ACC/monolingual-mainstream class mix written in each bar |
| `chart_class_size_by_school_overall.png` | Elementary schools, one average class size each |
| `table_enrollment_twi_by_school_grade.png` | Table: elementary enrollment by grade with TWI/ACC breakouts and strands |

### Notebook outline

0. Setup (libraries, chart style, helpers)
1. Enrollment by school and grade, checked against district totals
2. Projected vs. current enrollment (1A utilization table)
3. Validation of the screenshot against the Cordogan Clark report, then current utilization with Cordogan Clark capacity
4. Enrollment and utilization charts
5. Capacity comparison
6. Building square footage and learning space
7. Attendance-area capture
8. Utility cost per student and per seat
9. Dual-language (TWI) strands
10. Estimated classes and class size: by grade, by school, supporting tables, elementary summaries
11. Enrollment table with TWI breakouts
12. Parent-reported class sizes compared with the estimates

### Methods and definitions

| Term | Definition |
|---|---|
| **Current enrollment** | Dashboard enrollment, fall SY27 |
| **Projected enrollment** | "Enroll Total" in the district tables, a district projection. The elementary projections come from the Cordogan table; Chute, Haven and Nichols from the 1A table |
| **Cap Total** | District baseline capacity = 24 × calculated teaching stations |
| **Capacity used** | The smaller of Cap Total and Cordogan Clark capacity. Middle schools' Cordogan capacity comes from the report (PDF); their Cap Total and projections come from the 1A table |
| **Capacity goal** | Cordogan Clark's target utilization: 85% elementary, 80% middle, 75% Park/Rhodes/King Arts, 90% JEH (in `cordogan_clark_2022_report.csv`) |
| **Utilization** | Enrollment ÷ capacity used. Predicted utilization = projected enrollment ÷ Cap Total, as the district computed it |
| **STEP (\*)** | STEP program use affects total capacity at Lincoln, Lincolnwood and Washington |
| **Classrooms** | The district's floor-plan classroom count (capacity screenshot). Foster uses its teaching-station count because its floor-plan figure is blank. Middle schools have no floor-plan count; charts show their Cordogan teaching stations |
| **Building square feet** | (Electric + gas MMBtu) × 1,000 ÷ EUI (kBtu per sq ft), using 2025. 2018 gives the same result within about 25 sq ft. Accurate to roughly ± a few hundred sq ft |
| **Learning space** | Cordogan "Total SF Core Classrooms + SPED" (plus science labs at middle schools) ÷ building square feet |
| **Area capture** | Current enrollment ÷ students living in the attendance area ("Area Counts"). The neighborhood version subtracts TWI students, so it undercounts at TWI schools, since some TWI students live nearby |
| **Utility cost** | Electric, gas and water, calendar 2025, the last full year. Cost per student uses fall SY27 enrollment |
| **TWI strand** | One dual-language class per grade K–5 (6 rooms, 144 seats). TWE/TWS = English/Spanish-dominant; TWX as labeled by the district (meaning not confirmed) |

#### Class-size estimate

The dashboard has enrollment by grade, not how many classes each grade has, so classes are **estimated**:

- **Monolingual/mainstream classes:** the fewest classes that keep each class at or under the cap, `ceil(students ÷ 24)`. This gives the fewest classrooms and largest average class a grade could have. Real schools may run more, smaller classes.
- **Cap = 24:** the district's capacity standard, not the teacher-contract limit. Change `CAP` in the notebook to use grade-level limits.
- **TWI schools (Dawes, Dewey, Foster, Oakton, Washington), K–5:** one class per strand per grade. TWI students are assumed spread evenly across K–5.
- **Washington (reported class counts):** 4 classes per grade (2 TWI + 2 monolingual/mainstream), except 1st and 2nd grade with 3 (2 TWI + 1). Students are spread evenly across a grade's classes. Set in `KNOWN_CLASSES` in the notebook.
- **Oakton 5th grade (reported class count):** 3 classes instead of 4, assumed to be 1 TWI + 1 ACC + 1 monolingual/mainstream, with students spread evenly. Also set in `KNOWN_CLASSES`.
- **Oakton ACC:** one ACC (African-Centered Curriculum) class per grade K–5. The dashboard doesn't identify ACC students, so the 1A table's projected 73 are spread evenly (~12 per grade) and taken out of Oakton's monolingual/mainstream classes. Change `acc_total` in the notebook if you have the actual count.
- **Middle schools:** sections of up to 24 students, since there are no homerooms. They're excluded from the elementary summaries, and King Arts counts K–5 only there.

### Checks

- School enrollments, IEP counts and incidents add up to district totals (5,462 / 953 / 968).
- Every grade's school enrollments add up to the district total for that grade.
- Transcribed tables: parts add up to Enroll Total, and every Util % and Cordogan Delta recomputes.
- The capacity screenshot's Cordogan figures (square feet, teaching stations, capacity) match Cordogan Clark's February 2022 report for all 11 schools it covers. The notebook asserts this on every run.
- Transcriptions were checked byte for byte (checksums) when moving the dashboard data.

### Known limitations and data to request

- **Class counts are estimates.** Actual sections by school and grade would replace them.
- **TWI by grade:** needed to model the dual-language scenarios room by room.
- **Current ACC enrollment at Oakton:** the model uses the 73 projected.
- **Middle schools:** the Cordogan report gives their teaching stations, capacity and classroom square feet, but there's no floor-plan classroom count, so they're left out of the classrooms-needed comparison.
- **Foster:** has no utility account on the dashboard, so there's no square footage or cost for it.
- **Classroom counts** may include art, music or library rooms, so spare-room figures are upper bounds.
- **The dashboard's shared filter** can cross results between visitors; see How to refresh.
- **`scraping/d65_scrape.py` hasn't been run end to end against the live site.** The first pull went through a browser, and the script's chart-decoding code was tested against real responses. Expect small fixes on its first run.

See `sources/sources.md` for where each number comes from.

</details>
