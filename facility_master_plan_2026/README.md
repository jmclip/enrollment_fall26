# D65 Facility Master Plan (2026) — room dataset

Source: [*Evanston/Skokie School District 65 Facility Master Plan*](https://resources.finalsite.net/images/v1774292798/district65net/qe007gerizmoqz8hfewa/District65MFP2026.pdf), Studio GC, draft dated March 20, 2026 (`District65MFP2026.pdf`, 2,493 pages). Page numbers below are PDF pages.

## Files

| File | Contents |
|---|---|
| `fmp_rooms.csv` | One row per room (2,458 rooms, 17 schools) from each school's "Room Department Schedule" (Section 3.0), with occupant load joined from the Life Safety Reference Plans (Appendix A1.1). |
| `fmp_schools.csv` | One row per school: grades, year(s) built, gross SF, room/classroom roll-ups, occupant-load totals, the report's capital need 2027–2075 ($M), and completeness notes. |
| `fmp_plan_occupancy_tags.csv` | Raw room tags read off the life-safety floor plans (number, name, area, occupant load), one row per tag per sheet. |
| `fmp_area_discrepancies.csv` | The 8 rooms whose room number appears on a plan tag with a different area than the schedule, with both areas, tag names/loads, source pages and likely cause. |
| `fmp_summary.md` | Report summary, gen-ed classroom analysis, discrepancy notes, and how this dataset was made (process and prompts). |
| `fmp_room_dataset.xlsx` | Same data as a workbook with live formula roll-ups (Schools, Dept Summary, Rooms, Plan Occupancy Tags). |

## Key columns (`fmp_rooms.csv`)

- `area_sf` — room area from the schedule.
- `department` / `department_std` — the report's category (Staff/Office, Small Group Spaces, Shared Instructional Spaces/Specials, Core Curriculum, Circulation, Building Support), as printed and standardized.
- `room_type` — keyword classification of the room name (Classroom, Office/Admin, Restroom, Storage/Custodial, etc.). Derived, not from the report.
- `occupant_load` — code occupant load from the plan tag (area ÷ load factor; classrooms ≈ SF/20). **Not** a program or student capacity. The plans give no load for restrooms, corridors and stairs, so those are blank.
- `plan_area_sf`, `plan_tag_area_matches` — area on the plan tag and whether it agrees with the schedule (±2 SF). Occupant load is filled only when it matches. It is blank (no tag) for 794 rooms and `False` for 8 rooms, which are listed in `fmp_area_discrepancies.csv`.

## Caveats

- Room counts match the printed "Grand total" for every school that shows one.
- **Oakton** and **Orrington** schedules are cut off in the PDF itself (a few Core Curriculum/Circulation rows are hidden, Building Support is truncated, and there is no grand total). **Dawes** and **Dewey** show no Building Support subtotal or grand total, so they may also be truncated.
- Chute's C111 Courtyard (5,462 SF) has no department in the schedule, so it is coded `(blank in source)`.
- Capital-need figures come from "Overall Summary by Building and Year" (pp. 22–23): 2025 dollars escalated 4.5%/yr. The school figures sum to $598.5M; the report's total is $598.2M (rounding).
- The enrollment history and projection charts in the report are images and were not extracted.
