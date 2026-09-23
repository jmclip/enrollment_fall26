# D65 building use analysis

An analysis of how Evanston/Skokie School District 65 buildings are used: enrollment against projections, utilization and capacity, class sizes, dual-language (TWI) strands, attendance-area capture, building space and utility cost.

- **Current data:** the district's public dashboard, https://data.district65.net, pulled 2026-09-23 (fall of school year 2026–27, "SY27").
- **Planning data:** two district utilization/capacity tables, transcribed from screenshots, and Cordogan Clark's February 2022 capacity report (PDF), which verifies the screenshots. See `sources/`.
- **Everything is in one notebook:** `d65_enrollment_by_building.ipynb`. Run it top to bottom to rebuild every table in `data/` and every chart in `images/`.

## Folder layout

```
d65-dashboard-data/
├── README.md                     this file
├── d65_enrollment_by_building.ipynb  analysis notebook (reads data/, writes data/ and images/)
├── d65_scrape.py                 re-pulls the dashboard into data/
├── requirements.txt              Python packages needed
├── data/                         all CSVs: inputs and the tables the notebook writes
├── images/                       all charts (PNG)
└── sources/                      sources.md, the Cordogan Clark report (PDF) and the original screenshots
```

## How to refresh

1. `pip install -r requirements.txt`
2. `python3 d65_scrape.py` pulls the dashboard again and overwrites the dashboard CSVs in `data/` (the first six input files below).
3. Re-run the notebook top to bottom. It needs only four inputs (`students_home_demographics.csv`, `sustainability_utility.csv`, `utilization_1A_website.csv`, `capacity_cordogan_clark.csv`) and rebuilds every other table and chart. The two transcribed tables don't change unless you edit them.

The dashboard stores filtered results in one shared spot on its server, so another visitor filtering at the same moment can mix up numbers. The script re-runs any school whose totals don't add up, and checks that schools sum to the district.

## Data files (`data/`)

### Inputs

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

### Outputs written by the notebook

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
| `class_size_detail_by_school.csv` | **Main class-size file.** Every input and step per school and grade: students, cap, estimated TWI and ACC students and classes, regular students and classes, class sizes |
| `table_students_by_school_grade.csv` | Supporting table 1: students by school and grade (integers, with totals) |
| `table_classes_by_school_grade.csv` | Supporting table 2: estimated classes by school and grade (integers, with totals) |
| `class_size_by_school_overall.csv` | Elementary only (King Arts K–5): average of K–5 grade averages, and the student-weighted average |
| `classrooms_needed_vs_available.csv` | Estimated classes vs. the district's floor-plan classroom count, with spare rooms (upper bound) |
| `table_enrollment_twi_by_school_grade.csv` | Elementary enrollment by grade with TWI (and Oakton ACC) breakouts and strands; estimates are whole students that add up to real totals |

**Programs, neighborhood and cost**

| File | Contents |
|---|---|
| `twi_strands.csv` | Dual-language strands: current TWE/TWS/TWX, capacity, strands, rooms, % full, students per room, Spanish-dominant share, projection |
| `attendance_area_capture.csv` | Students living in each attendance area vs. enrolled, total and neighborhood-only capture % |
| `utility_cost_per_student.csv` | 2025 utility cost per building, enrollment, capacity, empty seats, cost per student, cost per seat, cost matching empty seats |

## Charts (`images/`)

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
| `chart_class_size_heatmap.png` | Estimated class size, every school and grade K–8 |
| `chart_class_size_by_grade.png` | District average class size by grade, K–8 |
| `chart_class_size_by_school.png` | One panel per school: class size by grade, with students ÷ classes |
| `chart_class_size_elementary_by_grade.png` | Elementary schools, one panel each: class size in each K–5 grade, with students ÷ classes and the TWI/ACC/regular class mix written in each bar |
| `chart_class_size_by_school_overall.png` | Elementary schools, one average class size each |
| `table_enrollment_twi_by_school_grade.png` | Table: elementary enrollment by grade with TWI/ACC breakouts and strands |

## Notebook outline

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

## Methods and definitions

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

### Class-size estimate

The dashboard has enrollment by grade, not how many classes each grade has, so classes are **estimated**:

- **Regular classes:** the fewest classes that keep each class at or under the cap, `ceil(students ÷ 24)`. This gives the fewest classrooms and largest average class a grade could have. Real schools may run more, smaller classes.
- **Cap = 24:** the district's capacity standard, not the teacher-contract limit. Change `CAP` in the notebook to use grade-level limits.
- **TWI schools (Dawes, Dewey, Foster, Oakton, Washington), K–5:** one class per strand per grade. TWI students are assumed spread evenly across K–5.
- **Oakton ACC:** one ACC (special-education) class per grade K–5. The dashboard doesn't identify ACC students, so the 1A table's projected 73 are spread evenly (~12 per grade) and taken out of Oakton's regular classes. Change `acc_total` in the notebook if you have the actual count.
- **Middle schools:** sections of up to 24 students, since there are no homerooms. They're excluded from the elementary summaries, and King Arts counts K–5 only there.

## Checks

- School enrollments, IEP counts and incidents add up to district totals (5,462 / 953 / 968).
- Every grade's school enrollments add up to the district total for that grade.
- Transcribed tables: parts add up to Enroll Total, and every Util % and Cordogan Delta recomputes.
- The capacity screenshot's Cordogan figures (square feet, teaching stations, capacity) match Cordogan Clark's February 2022 report for all 11 schools it covers. The notebook asserts this on every run.
- Transcriptions were checked byte for byte (checksums) when moving the dashboard data.

## Known limitations and data to request

- **Class counts are estimates.** Actual sections by school and grade would replace them.
- **TWI by grade:** needed to model the dual-language scenarios room by room.
- **Current ACC enrollment at Oakton:** the model uses the 73 projected.
- **Middle schools:** the Cordogan report gives their teaching stations, capacity and classroom square feet, but there's no floor-plan classroom count, so they're left out of the classrooms-needed comparison.
- **Foster:** has no utility account on the dashboard, so there's no square footage or cost for it.
- **Classroom counts** may include art, music or library rooms, so spare-room figures are upper bounds.
- **The dashboard's shared filter** can cross results between visitors; see How to refresh.
- **`d65_scrape.py` hasn't been run end to end against the live site.** The first pull went through a browser, and the script's chart-decoding code was tested against real responses. Expect small fixes on its first run.

See `sources/sources.md` for where each number comes from.
