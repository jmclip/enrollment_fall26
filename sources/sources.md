# Sources

Data behind the files and charts in this project, and how each piece was obtained. CSVs are in `../data/`, charts in `../images/`, screenshots in this folder. Compiled 2026-09-23.

## 1. D65 Data Dashboard — current enrollment, attendance, discipline, assessments, utilities
- **Where:** [data.district65.net](https://data.district65.net) (Evanston/Skokie School District 65 public dashboard)
- **Pulled:** 2026-09-23, fall of school year 2026–27 (SY27)
- **How:** The dashboard is a Plotly Dash app. Its charts come from `POST /_dash-update-component`; the numbers were read from those chart responses, once district-wide and once per school (the school filter). Raw student-level records stay on the district's server and aren't exposed.
- **Files:** `d65_dashboard_all_long.csv`, `students_home_demographics.csv`, `students_attendance.csv`, `students_discipline.csv`, `students_assessments.csv`, `sustainability_utility.csv`, `school_summary.csv`
- **Refresh:** `python3 scraping/d65_scrape.py` (details in `scraping/README.md`)
- **Notes:** Groups under 10 students appear as "Other*". Score and attendance distributions are grouped into 10-point bins. 2026 utility figures cover January–August only. Checks: school enrollments, IEP counts and incidents add up to the district totals (5,462 / 953 / 968).

## 2. District utilization table ("1A_Utilization_website")
- **Where:** Screenshot provided by the user (`source_1A_Utilization_website.png`)
- **What:** Per school: Enroll SY25, area counts, capacity (total, neighborhood, TWI, ACC), **projected** enrollment (total, neighborhood, TWE/TWS/TWX, ACC) and projected utilization %
- **File:** `utilization_1A_website.csv` (transcribed by hand)
- **Checks:** every row's parts add up to its Enroll Total, and every Util % equals Enroll Total ÷ Cap Total
- **Used for:** projected enrollment and capacity for Chute, Haven and Nichols, which the Cordogan table doesn't include

## 3. Capacity table with Cordogan Clark floor-plan counts
- **Where:** Screenshot provided by the user (`source_capacity_cordogan_clark.png`)
- **What:** Per elementary school plus King Arts: Cap Total (baseline), calculated teaching stations, projected Enroll Total, projected utilization, core classroom + SPED square feet, Cordogan Clark teaching stations, capacity and floor-plan classrooms, small group rooms, offices, FAPEL, teachers' lounge, comments
- **File:** `capacity_cordogan_clark.csv` (transcribed by hand)
- **Checks:** Delta = Cordogan capacity − Cap Total on every row, and Util % = Enroll Total ÷ Cap Total
- **Note:** This table's projected enrollment includes Kingsley (167) and differs from table 2 for Lincolnwood (181 vs 280) and Willard (193 vs 261). The elementary-school projections used in the charts come from this table.
- **Verified against source 3b:** classroom square feet, Cordogan teaching stations and Cordogan capacity match the Cordogan Clark report exactly for all 11 schools the report covers. Foster isn't in the report. The floor-plan classroom, small-group room, office, FAPEL and lounge counts are the district's own review and can't be checked against it. The district's counts differ from the report's teaching stations at several schools, for example Dawes 20 vs. 19, and the comments explain why.

## 3b. Cordogan Clark space utilization and capacity report (PDF)
- **Where:** `Cordogan_Clark_D65_Space_Utilization_Capacity_Study_2022-02-14.pdf` in this folder: *Space Guidelines, Building Capacity & Space Utilization Report for Evanston/Skokie School District No. 65*, Cordogan Clark, February 14, 2022 (103 pages; school pages dated December 2021 – February 2022)
- **What:** Space guidelines (pp. 2–5), a district summary (p. 6), and for each building a summary plus room-by-room calculations: core classroom + SPED square feet, teaching stations, capacity, square feet per student, 2021–22 enrollment and utilization, and a capacity goal (85% elementary, 80% middle, 75% Park/Rhodes/King Arts, 90% JEH)
- **File:** `cordogan_clark_2022_report.csv`, one row per building from its summary page (PDF page numbers included). Checked: every school page matches the district summary page, and core + science lab + SPED add up to each total.
- **Used for:** validating source 3 (the notebook checks it on every run), and filling in Chute, Haven and Nichols, which source 3 doesn't include: Cordogan capacity, teaching stations and classroom square feet (with science labs)
- **Differences from the other sources:**
  - Haven: report capacity 937 vs. the 1A table's Cap Total 936. The analysis uses the smaller, so nothing changes.
  - JEH: report capacity 464 vs. the 1A table's 404. JEH isn't part of the analysis.
  - Oakton: the report counts 2 special-education classrooms (13 seats) in 2021–22. The class-size model's one ACC class per grade (6 classes) follows the 1A table's 144 ACC seats instead, which appear to reflect a later program placement.
  - The report's enrollment and utilization columns are for 2021–22 and aren't used.

## 4. Building square footage (derived)
- **Where:** Calculated from source 1 (Sustainability → Utility Usage)
- **How:** square feet = (electric + natural gas MMBtu) × 1,000 ÷ Energy Use Intensity (kBtu/sq ft), using 2025. 2018 gives the same answer within about 20 sq ft. Dividing each building's savings by its savings per square foot agrees within a few percent for nearly all buildings.
- **File:** `building_square_feet.csv`
- **Notes:** Estimates, good to about ±a few hundred sq ft because EUI is rounded. Foster has no utility account on the dashboard. This is the whole building; the square feet in sources 3 and 3b cover only core classrooms plus SPED (and science labs at middle schools).

## Derived files
| File | Built from |
|---|---|
| `enrollment_by_school_grade.csv` | 1 |
| `enrollment_vs_utilization.csv` | 1 + 2 |
| `utilization_current_vs_predicted.csv` | 1 + 2 + 3 + 3b (capacity used = smaller of Cap Total and Cordogan capacity) |
| `capacity_comparison.csv` | 2 + 3 + 3b (middle-school Cordogan stations and capacity) |
| `images/chart_*.png` | produced by `d65_enrollment_by_building.ipynb` |
| `attendance_area_capture.csv` | 1 + 2 |
| `utility_cost_per_student.csv` (includes cost per seat) | 1 + 2 + 3 |
| `twi_strands.csv` | 1 + 2 |
| `class_size_detail_by_school.csv`, `table_students_by_school_grade.csv`, `table_classes_by_school_grade.csv`, `class_size_by_school_overall.csv` | 1 (grade enrollment, TWI counts) + 2 (TWI capacity, projected ACC for Oakton); estimates, see README |
| `classrooms_needed_vs_available.csv` | class-size estimate + 3 (floor-plan classrooms) |
| `building_square_feet.csv` | 1 (derived; see section 4) |

## Definitions used
- **Current enrollment:** dashboard enrollment, fall SY27 (source 1)
- **Projected enrollment:** Enroll Total in sources 2/3 (district projection)
- **Capacity used:** the smaller of Cap Total and Cordogan Clark capacity; Cap Total = 24 × district calculated teaching stations
- **STEP (*):** STEP program use affects total capacity at Lincoln, Lincolnwood and Washington
- **Oakton ACC:** the 1A table's projected ACC enrollment (73) is used for Oakton's ACC classes, because the dashboard doesn't identify ACC students
- **Class counts:** estimated, not reported; see the README's class-size section
