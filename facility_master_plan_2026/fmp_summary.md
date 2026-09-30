# D65 Facility Master Plan (Mar 2026 draft): summary

Source: [*Evanston/Skokie School District 65 Facility Master Plan*](https://resources.finalsite.net/images/v1774292798/district65net/qe007gerizmoqz8hfewa/District65MFP2026.pdf), Studio GC, draft dated March 20, 2026. It is 2,493 pages. The main report is pp. 1–358 and the rest is appendices: the ISBE decennial safety survey, AHERA asbestos reports, masonry and roof surveys, ComEd carbon-free assessments, the 2024 McKibben demographic study, and the D65 Sustainability Plan.

## Main findings

- **Aging systems.** Nearly every building has HVAC, plumbing and electrical systems at or past the end of their service life. Examples are 1990s-era boilers, galvanized water piping, window A/C units and old unit ventilators. Buildings date from 1901 (Washington) to 2002 (Joseph E. Hill).
- **Safety and code.** The top priorities are items cited in the ISBE Safety Survey: fire alarm panels nearing obsolescence, restrooms and drinking fountains that don't meet ADA, and spaces with too little ventilation. The buildings are generally structurally sound.
- **Enrollment decline.** McKibben (Nov 2024) projects K–8 enrollment falling by about 456 students (−7.3%) from 2024–25 to 2029–30, and about 1% more by 2034–35. The total fertility rate is 1.33. The report calls for "right-sizing" through consolidation and boundary changes, and notes that Bessie Rhodes and Kingsley close at the end of 2025–26.
- **Capital need.** The report puts it at about **$598M for 2027–2075**, in 2025 dollars escalated 4.5% a year (pp. 22–23). The largest totals are Haven ($56.8M), Chute ($50.6M), Joseph E. Hill ($46.1M), Washington ($43.3M), Nichols ($42.7M) and King Arts ($40.8M).
- **Maintenance benchmark.** The 2025 *State of Our Schools* report recommends spending 4% of current replacement value a year. For the district's 1,290,525 gross SF that is about **$20.6M a year**. Actual facility spending in 2021–2025 was between $0 and $3.1M a year.
- **Sustainability.** The report includes conceptual geothermal well-field layouts (24–144 wells per site) and rooftop solar layouts for each school.
- **Next steps.** Handle safety and code items first. Then build a phased, multi-year capital plan tied to enrollment, with continued community engagement.

## Gen-ed classrooms: what the report does and doesn't say

**The report does not give a gen-ed classroom count.** Its room schedules sort rooms only into six broad departments: Staff/Office, Small Group Spaces, Shared Instructional Spaces/Specials, Core Curriculum, Circulation and Building Support. Nothing separates general-education homerooms from special education, ELL or intervention rooms. The report also has no capacity, teaching-station or utilization figures.

The closest proxy is rooms **named "CLASSROOM" in the Core Curriculum department**. That rule leaves out science labs, art and music rooms, and rooms labeled sensory, therapy or special ed. It also leaves out the "CLASSROOM" rooms the report files under Small Group Spaces, which are mostly at Haven (13) and Nichols (17). By this rule there are **389 rooms across 17 buildings**, or **224 in the 10 K–5 schools** (254 including King Arts).

Some rooms named "CLASSROOM" may still be used for special ed or other programs, so treat this as an upper-bound proxy, not a gen-ed count. The comparison below uses this repo's `data/capacity_comparison.csv`:

| School | MFP "Classroom" (Core Curriculum) | Floor-plan classrooms (existing) | Cordogan teaching stations |
|---|---:|---:|---:|
| Dawes | 21 | 20 | 19 |
| Dewey | 26 | 24 | 24 |
| Kingsley* | 22 | 20 | 20 |
| Lincoln | 30 | 28 | 27 |
| Lincolnwood | 18 | 19 | 19 |
| Oakton† | 21 | 25 | 26 |
| Orrington† | 17 | 19 | 20 |
| Walker | 19 | 18 | 18 |
| Washington | 27 | 24 | 24 |
| Willard | 23 | 24 | 24 |
| King Arts | 30 | 27 | 30 |
| Bessie Rhodes* | 18 | — | — |
| Chute (MS) | 27 | — | 35 |
| Haven (MS) | 39 (+13 in Small Group) | — | 47 |
| Nichols (MS) | 19 (+17 in Small Group) | — | 41 |
| Joseph E. Hill (Pre-K) | 19 | — | — |
| Park (special ed) | 13 | — | — |

\* Closing after 2025–26. † The MFP schedule is cut off in the PDF, so these counts are low.

**Median Core Curriculum classroom size** ranges from about 615 SF (Nichols) and 690 SF (Joseph E. Hill) up to about 990 SF (Bessie Rhodes, Walker). Room-level detail is in `fmp_rooms.csv`.

## Plan tag vs. schedule discrepancies

Each room's occupant load comes from a room tag on the life-safety floor plans (Appendix A1.1). The tag is matched to the room schedule by school, room number **and** area (within ±2 SF). Of 2,458 scheduled rooms:

- **1,656** have a plan tag with the same number and area. 1,344 of these carry an occupant load; the rest are restrooms, corridors and stairs, which the plans don't give a load.
- **794** have no plan tag with their room number, so no occupant load.
- **8** have a tag with their room number but a different area. They get no occupant load and are listed in **`fmp_area_discrepancies.csv`**.

In 7 of the 8, the schedule uses the same room number twice. For example, Oakton lists 119 as both STORAGE (31 SF) and an office (319 SF), and the plan tag belongs to the other room. The eighth is Haven's 311 GYM BALCONY, which is 1,610 SF in the schedule and 1,615 SF on the plan. Duplicate room numbers are an error in the district's source drawings worth flagging.

The file's columns are: school, room number, schedule name/department/area, plan-tag names/areas/occupant loads, area difference, how many times the number appears in the schedule, PDF pages for both sources, and likely cause.

## How this was made (process and prompts)

This was built with Claude (Cowork mode; model configured as `claude-opus-5-5`) in one session on Sept 30, 2026, from the PDF above.

**Prompts, in order (verbatim):**

1. "give me a summary of this and pull out all the charts from the schools re: rooms, type, and capacity to build a dataset please" *(with the PDF attached)*
2. "thank you make a folder for this in the d65 data folder"
3. "make a md file" / "is there anything about the total gen-ed classrooms from this report?"
4. "in the md file, add this link: … explain the process and prompt used to generate all this. add in the md a file that identifies the discrepancy between the tables re: area matches schedule"

**Process:**

1. **Map the document.** Extracted text from all 2,493 pages (`pdftotext`). Found the table of contents, the 17 school sections in Section 3.0, and each school's "Existing Building Data" panel and "Room Department Schedule" tables (27 pages). Read the summary, demographics, sustainability, budget and conclusions sections for the summary above. Charts that are images (enrollment history and projections, the cost-by-year table) were read visually from rendered pages.
2. **Extract the room schedules.** Plain text extraction garbles some schedules: the tables are placed as clipped views of one larger drawing, so hidden rows overlap visible ones (Lincoln and Oakton especially). Using PyMuPDF with clip-aware text extraction (`TEXT_CLIP`) returned only the visible text. Rows were rebuilt from word positions: number, name, area, and department columns, with wrapped names joined, and department headers, subtotals and grand totals parsed separately.
3. **Verify.** Room counts and SF were checked against each school's printed "Grand total" (every school that shows one matches; SF differs by ≤6 from rounding) and against each department subtotal. Schools with no grand total or with rows cut off at the page edge were flagged: Oakton, Orrington, Dawes and Dewey. Gross SF across schools adds up to the report's 1,290,525 SF.
4. **Classify.** Departments were standardized (e.g., "CORE CURICULUM" becomes Core Curriculum). A `room_type` was assigned from keyword rules on the room name. This is derived and was not in the report.
5. **Get "capacity."** The schedules give area only. Occupant loads were read from room tags (name / number / area / occupancy) on the 68 life-safety plan sheets, using word geometry to find the number stacked directly under each "### SF" area. Tags with implausible loads (more than 1 person per 5 SF, i.e., a mislabeled nearby number) were dropped. Tags were then joined to the schedule on school + room number + area.
6. **Package.** Built the CSVs and an Excel workbook whose school and department roll-ups are live formulas (checked with a recalculation pass: 0 errors). Capital-need totals per school were transcribed from pp. 22–23.
7. **Gen-ed classrooms.** Searched the full text for gen-ed, homeroom, teaching-station, capacity and utilization language and found none. Built the "CLASSROOM in Core Curriculum" proxy and compared it to this repo's `data/capacity_comparison.csv`.

**Limits:** Only what is printed in this draft was extracted, and nothing was checked against the district's CAD/Revit files. `room_type` and the gen-ed proxy are judgment calls. Occupant load is a building-code figure, not program capacity.

## Files in this folder

See `README.md`.
