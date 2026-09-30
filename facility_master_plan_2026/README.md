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

# D65 Facility Master Plan (March 2026 draft): summary and overview

**Source:** [*Evanston/Skokie School District 65 Facility Master Plan*](https://resources.finalsite.net/images/v1774292798/district65net/qe007gerizmoqz8hfewa/District65MFP2026.pdf), Studio GC (architects/engineers, Chicago), draft dated March 20, 2026. It runs 2,493 pages: the main report is pp. 1–358 and the rest is appendices. Page numbers below are PDF pages.

## At a glance

| | |
|---|---|
| Buildings assessed | 17 schools (10 K–5, 2 K–8 magnets, 3 middle schools, Joseph E. Hill early childhood/admin, Park School ages 3–22) |
| Gross building area | **1,290,525 SF** across the 17 schools |
| Build dates | 1901 (Washington) to 2002 (Joseph E. Hill); 12 of 17 buildings were built before 1960 |
| Site visits | October 2025 – January 2026. No complete existing drawings were available, so concealed conditions are assumed. |
| Capital need, 2027–2075 | **$598.2M** (2025 dollars escalated 4.5%/yr) |
| First 5 years (2027–31) | **$182.6M** |
| First 10 years (2027–36) | **$409.7M**, including a **$131.7M spike in 2034** |
| Maintenance benchmark | 4% of replacement value, or **$20.6M a year** |
| Actual facility spending, FY2021–25 | **$5.7M total** ($0 to $3.1M a year) |
| Enrollment (K–8, McKibben) | 7,419 (2019–20) → 5,922 (2024–25) → 5,521 (2029–30) → 5,466 (2034–35) |
| Closures already decided | Bessie Rhodes and Kingsley, at the end of 2025–26 |

## Summary of the report

This is Studio GC's draft Facility Master Plan for District 65, dated March 20, 2026. It runs 2,493 pages, but the main report is only the first ~358. The rest is appendices: the state safety survey, asbestos reports, masonry and roof surveys, ComEd energy assessments, the demographic study and the sustainability plan.

- **Buildings are old and systems are near the end of their life.** Nearly every school's heating/cooling, plumbing and electrical systems are at or past their expected lifespan. Build dates range from 1901 (Washington) to 2002 (Joseph E. Hill). The top priorities are safety and code items: fire alarm panels, restrooms and drinking fountains that don't meet ADA rules, and poor ventilation.
- **Cost:** the estimated capital need for 2027–2075 is about **$598M**, in 2025 dollars inflated 4.5% a year. The biggest totals are Haven ($56.8M), Chute ($50.6M), Joseph E. Hill ($46.1M) and Washington ($43.3M). The report compares this with a benchmark of spending 4% of replacement value a year on maintenance, which works out to about $20.6M a year for the district's 1.29M sq ft. For contrast, the district spent between $0 and $3.1M a year on facilities over 2021–2025.
- **Enrollment:** a November 2024 demographic study projects K–8 enrollment falling by about 456 students (–7.3%) by 2029–30, then another ~1% by 2034–35. The report calls for "right-sizing" through consolidation and boundary changes. It notes that Bessie Rhodes and Kingsley close at the end of 2025–26.
- **Sustainability:** it includes rough site layouts for geothermal systems (24 to 144 wells per site) and rooftop solar at each school.
- **Next steps:** fix safety and code items first, then a phased capital plan tied to enrollment, with community engagement.

## What's in the report

| Section | Pages | Contents |
|---|---|---|
| 1.0 Preface | 6–9 | Purpose and scope, district overview |
| 2.0 Executive Summary | 10–13 | Key findings, recommendations, next steps |
| 3.0 Facility Assessments | 14–329 | District cost summary by building and year (pp. 22–23); 5-year spending history (p. 24); maintenance benchmark (p. 25). Then about 16–20 pages per school: building data and enrollment chart, color-coded floor plans, room schedule, overview and history, architectural assessment (site, envelope, roofs, interiors, ADA), and an MEPFP (mechanical, electrical, plumbing, fire protection) evaluation. |
| 4.0 Demographic Forecasts | 330–333 | Summary of the Kofron (2022) and McKibben (2024) studies |
| 5.0 Sustainability | 334–347 | Geothermal well-field and rooftop solar test fits for each school |
| 6.0 Budget Considerations | 348–351 | Construction cost drivers, Turner/Mortenson cost indices |
| 7.0 Conclusions | 352–356 | Findings, district-wide themes, next steps |
| A1 Decennial Safety Survey | ~358–715 | Life-safety reference plans (room occupant loads), existing conditions, violations and recommendations schedules |
| A2 AHERA asbestos | ~716–1,600 | Three-year reinspections and management plans for each building |
| A3–A4 Masonry and roof surveys | ~1,600–1,900 | 2025 photo reports |
| A5 ComEd Carbon-Free Assessments | ~1,900–2,401 | Energy-efficiency measures, electrification, incentives |
| A6 Demographic Study | 2,403–2,447 | McKibben, Nov 2024: population and enrollment forecasts by attendance area |
| A7 Sustainability Plan | 2,449–2,493 | D65 Sustainability Plan (April 2025) |

## School-by-school overview

*Rooms* and *Classrooms* come from this folder's dataset. Classrooms are rooms named "CLASSROOM" in the Core Curriculum department, a proxy defined below. Capital figures are from pp. 22–23. $/GSF is the total 2027–2075 need divided by gross SF.

| School | Grades | Built (additions) | GSF | Site (acres) | Floors | Rooms | Classrooms | 5-yr need | 10-yr need | Total need | $/GSF |
|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| Chute MS | 6–8 | 1966 (2014) | 149,776 | 8.5 | 3 | 208 | 27 | $19.4M | $42.9M | $50.6M | $338 |
| Haven MS | 6–8 | 1926 (1931, '49, '54, '67, 2013) | 140,835 | 6.8 | 4 | 224 | 39 | $22.0M | $43.9M | $56.8M | $403 |
| Nichols MS | 6–8 | 1928 (2015 ×2) | 97,518 | 2.9 | 4 + bsmt | 256 | 19 | $14.7M | $32.9M | $42.7M | $438 |
| King Arts | K–8 | 1956 (1963) | 103,374 | 4.0 | 2 | 189 | 30 | $7.1M | $18.8M | $40.8M | $395 |
| Bessie Rhodes* | K–8 | 1957 | 51,323 | 3.4 | 2 + bsmt | 78 | 18 | $6.3M | $15.9M | $33.5M | $653 |
| Dawes | K–5 | 1954 (1959) | 58,125 | 9.6 | 1 + bsmt | 95 | 21 | $10.3M | $24.1M | $31.5M | $542 |
| Dewey | K–5 | 1940 (2009, 2011) | 65,605 | 3.5 | 3 + bsmt | 119 | 26 | $8.3M | $21.4M | $26.7M | $407 |
| Kingsley* | K–5 | 1967 | 53,949 | 4.5 | 2 | 119 | 22 | $8.0M | $21.4M | $25.8M | $478 |
| Lincoln | K–5 | 1953 (1968, 1970, 2013) | 67,360 | 1.5 | 2 | 115 | 30 | $7.5M | $19.5M | $34.0M | $505 |
| Lincolnwood | K–5 | 1949 (1952) | 61,023 | 9.4 | 2 + bsmt | 144 | 18 | $10.9M | $25.9M | $31.6M | $518 |
| Oakton† | K–5 | 1914 | 88,300 | 6.5 | 3 + bsmt | 188 | 21 | $10.6M | $27.8M | $36.6M | $415 |
| Orrington† | K–5 | 1911 (1931) | 51,213 | 2.0 | 2 + bsmt | 89 | 17 | $6.0M | $16.0M | $25.2M | $492 |
| Walker | K–5 | 1962 | 52,824 | 7.5 | 2 | 75 | 19 | $10.2M | $20.3M | $29.1M | $551 |
| Washington | K–5 | 1901‡ | 77,751 | 4.7 | 3 | 154 | 27 | $15.3M | $33.5M | $43.3M | $557 |
| Willard | K–5 | 1922 (1932, 1937, 2011) | 60,020 | 5.4 | 2 + bsmt | 103 | 23 | $13.2M | $20.6M | $25.7M | $428 |
| Joseph E. Hill | Pre-K (+ admin) | 2001–02 | 75,900 | 5.1 | 2 | 224 | 19 | $4.4M | $9.1M | $46.1M | $607 |
| Park School | Ages 3–22 | 1959 (1961) | 35,629 | 1.3 | 2 | 78 | 13 | $8.4M | $15.7M | $18.5M | $519 |
| **Total** | | | **1,290,525** | | | **2,458** | **389** | **$182.6M** | **$409.7M** | **$598.2M** | **$463** |

\* Closing after 2025–26. † The room schedule is cut off in the PDF, so room and classroom counts are low. ‡ Washington's "Existing Building Data" panel says 1901, but its "Overview and Building History" page repeats Bessie Rhodes' address (3701 Davis St, Skokie) and 1957 date, an apparent copy-paste error in the draft. The Section 3.0 overview pages also list ground-floor/upper-floor GSF breakdowns for each building.

**Patterns:**

- **Near-term need.** The largest first-5-year needs are the three middle schools (Haven $22.0M, Chute $19.4M, Nichols $14.7M), then Washington ($15.3M) and Willard ($13.2M). Washington has the biggest single-year item in 2027 ($10.3M), and Willard's peaks in 2031 ($8.7M).
- **Joseph E. Hill** is the newest building but has the fourth-highest total need ($46.1M). It is back-loaded: $13.5M in 2037, $11.7M in 2040 and $8.6M in 2055, as its 2001 systems reach end of life.
- **Closing schools.** Bessie Rhodes ($33.5M, the highest $/GSF at $653) and Kingsley ($25.8M) together carry about $59M of projected need.

## Capital need by year

District totals by year (pp. 22–23), in $M, escalated at 4.5%/yr:

| 2027 | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | 2037 | 2040 | 2055 | Other years | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 40.7 | 34.4 | 35.5 | 24.8 | 47.2 | 18.5 | 28.4 | **131.7** | 22.8 | 25.6 | 64.1 | 55.6 | 24.8 | 44.1 | **598.2** |

- **The 2034 spike.** In 2034 every building has a large line ($4.6M–$16.3M each; Chute $16.3M, Haven $13.0M, Washington $11.5M, Lincolnwood $10.5M). This looks like a lifecycle-replacement year for many systems at once, and in practice it would need to be phased.
- **Other peaks.** 2037 ($64.1M, driven by King Arts at $14.2M and Joseph E. Hill at $13.5M) and 2040 ($55.6M).
- **Scale of the gap.** Recommended maintenance is about $20.6M a year (2% periodic renewals, 1% alterations, 1% deferred-maintenance catch-up). Actual district facility spending was $0 (2021), $1.08M (2022), $3.10M (2023), $0.31M (2024) and $1.18M (2025), or about $5.7M over five years. Over the same period the benchmark implies about $100M.

## Enrollment

McKibben Demographics, November 2024 (Appendix A6, pp. 2432–2447). Forecasts are by **attendance area**, not building enrollment, so the magnets, Joseph E. Hill and Park are not broken out.

| | 2019–20 | 2024–25 | 2029–30 | 2034–35 | Change 2024–25 → 2034–35 |
|---|---:|---:|---:|---:|---:|
| K–5 | 4,832 | 3,816 | 3,558 | 3,609 | −5.4% |
| 6–8 | 2,587 | 2,106 | 1,963 | 1,857 | −11.8% |
| **K–8 total** | **7,419** | **5,922** | **5,521** | **5,466** | **−7.7%** |

- **Past decline.** Enrollment fell 20% from 2019–20 to 2024–25. The forecast has K–5 bottoming out around 2029–30 and edging up after that. Grades 6–8 keep falling into the early 2030s as smaller cohorts move up.
- **Discrepancy.** The report's narrative (p. 332) says K–8 falls "approximately 456 students (−7.3%)" from 2024–25 to 2029–30. The McKibben district table in its own appendix shows 5,922 → 5,521, a drop of **401 (−6.8%)**.
- **Drivers cited:** a total fertility rate of 1.33, more empty-nest households, low housing turnover, out-migration of 18–24 year-olds, and downsizing among residents 70+. Birth rates fell more than 30% over a decade, per the 2022 Kofron study.

**By attendance area** (K–5 or 6–8):

| Area / school | 2019–20 | 2024–25 | 2029–30 | 2034–35 |
|---|---:|---:|---:|---:|
| Dawes | 373 | 319 | 300 | 314 |
| Dewey | 524 | 417 | 384 | 377 |
| Kingsley | 217 | 189 | 197 | 203 |
| Lincoln | 588 | 452 | 412 | 414 |
| Lincolnwood | 289 | 181 | 181 | 194 |
| Oakton | 501 | 454 | 421 | 419 |
| Orrington | 363 | 259 | 264 | 254 |
| Walker | 492 | 397 | 358 | 366 |
| Washington | 537 | 424 | 385 | 383 |
| Willard | 419 | 247 | 226 | 242 |
| 5th Ward (new attendance area) | 529 | 477 | 430 | 443 |
| Chute MS | 751 | 670 | 626 | 592 |
| Haven MS | 923 | 714 | 673 | 638 |
| Nichols MS | 913 | 722 | 664 | 627 |

## Building conditions: recurring themes

These come from the per-school architectural assessments (Section 3.0) and the conclusions (Section 7.0).

- **Mechanical, electrical, plumbing and fire protection.** Nearly every building has major systems at or near end of life: boilers from the 1990s or earlier at some sites, galvanized water piping, window A/C units, aging unit ventilators and dated building-automation systems. Most buildings have no central cooling. The report favors 4-pipe hydronic or geothermal systems when equipment is replaced. LED lighting upgrades are largely complete.
- **Accessibility (every school).** Standard ADA items appear everywhere: accessible toilet stalls, hi-lo drinking fountains, counter and fixture heights, signage, lever hardware and door clearances. Some buildings have bigger access gaps:
  - **Elevator needed:** Kingsley, Orrington and Washington
  - **Areas with no ramp or elevator:** Oakton
  - **Entries to be rebuilt:** Dawes and Kingsley
- **Roofs.** Built-up roofs are "near life expectancy" at King Arts, Kingsley, Lincoln, Nichols, Oakton and Walker. Dawes needs budgeting for annex roof replacement. Joseph E. Hill's metal coping is approaching replacement.
- **Envelope and site.**
  - Heavy masonry cracking on King Arts' west wall (outside Classrooms 125–129)
  - Nichols' 1928 windows are near the end of their life cycle
  - Exterior stair railings "extremely rusted" at King Arts, Kingsley and Oakton
  - Dewey's paving is "generally in bad condition"
  - Park and Walker are recommended for drop-off/pick-up traffic studies
  - Every site is recommended for camera inspection of underground storm piping
- **Interiors.** Common items across buildings are water-damaged ceilings, split or peeling VCT/VAT flooring (VAT often contains asbestos; see Appendix A2), peeling wall base, leaking sinks and rusted door bottoms.
- **Safety survey (Appendix A1).** The ISBE decennial survey's violations must be remediated on state timelines, and the report treats them as the first priority.

## Sustainability and cost context

- **Geothermal test fits** (conceptual; no subsurface investigation), in potential number of wells:
  - Chute 80; Oakton 66; Washington 54; Dewey 48; Lincoln 48; Lincolnwood 42; Dawes 40; Willard 40; Walker 36; Orrington 32; Park 24
  - Nichols 70; Haven + Kingsley 144 (shared)
  - King Arts + Joseph E. Hill: 55 and 70 as independent well fields, or a single shared field
- **Rooftop solar test fits** are reviewed for roof structure but not for roof age or replacement timing.
- **Construction costs.** The Turner Building Cost Index rose from 943 (2015) to 1,510 (Q4 2025), up 60%. Studio GC's average school cost is $478/SF in 2025, projected at $500 (2026), $522 (2027) and $546 (2028) at 4.5%/yr. Mortenson reports labor up 4.6% and materials up 6.6% year over year (Q3 2025, structural steel +8.1%).

## Report recommendations and next steps

1. Prioritize urgent health, life-safety and infrastructure needs, especially ISBE Safety Survey citations.
2. Build a phased, multi-year capital roadmap sequenced by need, cost-avoidance opportunities and funding capacity.
3. Align facility decisions with enrollment projections: utilization, consolidation, boundary changes, and "the right number of schools, in the right places, with the right capacity."
4. Deepen community engagement as planning proceeds.
5. Integrate sustainability and equity goals into every major capital project.

## Issues in the draft worth flagging

- **Enrollment numbers disagree.** The narrative's enrollment decline (−456, −7.3%) doesn't match the appendix table (−401, −6.8%).
- **Washington's overview page is copied.** It repeats Bessie Rhodes' address and 1957 construction date.
- **Oakton and Orrington room schedules are cut off** in the PDF, and Dawes and Dewey show no grand totals.
- **Room numbers are reused.** Seven rooms share a number with another room in the same building (see discrepancies below).
- **Enrollment charts are unreadable.** The per-school charts and projection tables in Section 3.0 are embedded at about 72 dpi.
- **No capacity analysis.** Despite the emphasis on right-sizing, the plan gives no utilization, teaching-station or program-capacity figures.

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
5. "ok develop the md file for master facilities to add more summary detail and a better overview pls" / "I want the summary of the report you gave in the md file also"

**Process:**

1. **Map the document.** Extracted text from all 2,493 pages (`pdftotext`). Found the table of contents, the 17 school sections in Section 3.0, and each school's "Existing Building Data" panel and "Room Department Schedule" tables (27 pages). Read the summary, demographics, sustainability, budget and conclusions sections for the summary above. The cost-by-year table is an image and was read from rendered pages. The per-school enrollment charts in Section 3.0 are embedded at too low a resolution to read, so enrollment figures come from the McKibben appendix instead.
2. **Extract the room schedules.** Plain text extraction garbles some schedules: the tables are placed as clipped views of one larger drawing, so hidden rows overlap visible ones (Lincoln and Oakton especially). Using PyMuPDF with clip-aware text extraction (`TEXT_CLIP`) returned only the visible text. Rows were rebuilt from word positions: number, name, area, and department columns, with wrapped names joined, and department headers, subtotals and grand totals parsed separately.
3. **Verify.** Room counts and SF were checked against each school's printed "Grand total" (every school that shows one matches; SF differs by ≤6 from rounding) and against each department subtotal. Schools with no grand total or with rows cut off at the page edge were flagged: Oakton, Orrington, Dawes and Dewey. Gross SF across schools adds up to the report's 1,290,525 SF.
4. **Classify.** Departments were standardized (e.g., "CORE CURICULUM" becomes Core Curriculum). A `room_type` was assigned from keyword rules on the room name. This is derived and was not in the report.
5. **Get "capacity."** The schedules give area only. Occupant loads were read from room tags (name / number / area / occupancy) on the 68 life-safety plan sheets, using word geometry to find the number stacked directly under each "### SF" area. Tags with implausible loads (more than 1 person per 5 SF, i.e., a mislabeled nearby number) were dropped. Tags were then joined to the schedule on school + room number + area.
6. **Package.** Built the CSVs and an Excel workbook whose school and department roll-ups are live formulas (checked with a recalculation pass: 0 errors). Capital-need totals per school were transcribed from pp. 22–23.
7. **Expanded overview (prompt 5).** Pulled each school's "Overview and Building History" page (address, additions, acreage, floors), the "Items to Be Addressed" lists from the architectural assessments, the full year-by-school cost table (pp. 22–23, read from rendered images and checked against the printed yearly and school totals), and the attendance-area enrollment forecasts from the McKibben study (Appendix A6, pp. 2432–2447, which are text tables, unlike the low-resolution images in Section 3.0).
8. **Gen-ed classrooms.** Searched the full text for gen-ed, homeroom, teaching-station, capacity and utilization language and found none. Built the "CLASSROOM in Core Curriculum" proxy and compared it to this repo's `data/capacity_comparison.csv`.

**Limits:** Only what is printed in this draft was extracted, and nothing was checked against the district's CAD/Revit files. `room_type` and the gen-ed proxy are judgment calls. Occupant load is a building-code figure, not program capacity.

