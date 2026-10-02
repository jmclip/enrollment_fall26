import pandas as pd
U='/mnt/user-data/uploads/d65-dashboard-data'
bc=pd.read_csv(f'{U}/data/building_costs_v2_2026-10-01.csv').set_index('account')
bc=bc.drop(index='Foster',errors='ignore')
k=lambda v:f"${v/1000:,.0f}K"; d=lambda v:f"${v:,.0f}"
k5=bc.dropna(subset=['per_student_scen_avg']).sort_values('per_student_scen_avg',ascending=False)
oth=bc[bc.per_student_scen_avg.isna()].loc[['King Arts','Haven','Chute','Nichols']]
rows=""
for a,r in k5.iterrows():
    rows+=f"<tr><td>{a}</td><td>{r.students:.0f}</td><td>{r.utilization_now_pct:.0f}% → {r.utilization_scen_avg_pct:.0f}%</td><td>$241K</td><td>{k(r.building_staff_est-240753)}</td><td>{k(r.util_2025)}</td><td><b>{k(r.total_est)}</b></td><td><b>{d(r.per_student)}</b></td><td class=or><b>{d(r.per_student_scen_avg)}</b></td></tr>"
for a,r in oth.iterrows():
    nm=a+(' (MS)' if a in ('Haven','Chute','Nichols') else '')
    rows+=f"<tr><td>{nm}</td><td>{r.students:.0f}</td><td>{r.utilization_now_pct:.0f}%</td><td>$241K</td><td>{k(r.building_staff_est-240753)}</td><td>{k(r.util_2025)}</td><td><b>{k(r.total_est)}</b></td><td><b>{d(r.per_student)}</b></td><td class=or>—</td></tr>"
ws=bc.per_student.idxmax(); lo=k5.per_student.idxmin()
print(ws, bc.per_student.max(), lo, k5.per_student.min())
FOOT=lambda n:f'<div class="foot"><span>Legion of Data Nerds · D65 budget choices · Fall 2026 · data as of Oct 1, 2026</span><span>{n}</span></div>'
def head(num,kick,title): return f'<div class="sechead"><div class="num">{num}</div><div><div class="kick">{kick}</div><h2>{title}</h2></div></div>'
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>D65 budget choices</title><style>
@page {{ size: letter; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Carlito, Lato, sans-serif; color:#1b2a41; font-size:10.5pt; line-height:1.38; }}
.page {{ width:8.5in; height:11in; padding:0.45in 0.55in 0.5in; position:relative; page-break-after:always; overflow:hidden; }}
.page:last-child {{ page-break-after:auto; }}
.hero {{ background:#16243f; color:#fff; margin:-0.45in -0.55in 0.16in; padding:0.32in 0.55in 0.22in; }}
.eyebrow {{ font-family:Poppins; font-weight:700; letter-spacing:.14em; font-size:7.6pt; color:#e08a4a; text-transform:uppercase; }}
.hero h1 {{ font-family:Lora; font-weight:700; font-size:25pt; line-height:1.1; margin:.08in 0 .1in; }}
.hero p {{ margin:0; font-size:10.5pt; color:#dfe5ef; }}
h2 {{ font-family:Lora; font-weight:700; font-size:18.5pt; line-height:1.15; margin:0; }}
h3 {{ font-family:Lora; font-weight:700; font-size:16pt; margin:.04in 0 .06in; }}
.label {{ font-family:Poppins; font-weight:700; letter-spacing:.14em; font-size:7.2pt; text-transform:uppercase; color:#1b2a41; margin:.12in 0 .06in; }}
.label.or {{ color:#c8662a; }}
.sechead {{ display:flex; gap:.14in; align-items:flex-start; border-bottom:1.5px solid #1b2a41; padding-bottom:.06in; margin-bottom:.1in; }}
.num {{ font-family:Lora; font-weight:700; font-size:30pt; color:#c8662a; line-height:.95; }}
.kick {{ font-family:Poppins; font-weight:700; letter-spacing:.16em; font-size:7.4pt; color:#c8662a; text-transform:uppercase; }}
.lede {{ font-family:Lora; font-size:10.5pt; line-height:1.45; margin:.04in 0 .08in; }}
.cols {{ display:grid; gap:.22in; }} .c2 {{ grid-template-columns:1fr 1fr; }} .c3 {{ grid-template-columns:1fr 1fr 1fr; }}
.guide li {{ margin-bottom:.06in; }} .guide {{ list-style:none; padding:0; margin:0; counter-reset:g; }}
.guide li {{ counter-increment:g; display:flex; gap:.1in; }} .guide li:before {{ content:counter(g); font-family:Lora; font-weight:700; color:#c8662a; font-size:20pt; line-height:1; min-width:.24in; }}
.guide b {{ font-family:Lora; font-size:11pt; }}
.risk {{ display:flex; gap:.08in; margin-bottom:.05in; font-size:9pt; line-height:1.25; }}
.tag {{ font-family:Poppins; font-weight:700; font-size:6.2pt; color:#fff; padding:.03in .06in; border-radius:2px; height:fit-content; min-width:.55in; text-align:center; letter-spacing:.06em; }}
.tag.h {{ background:#c0392b; }} .tag.m {{ background:#c8662a; }}
img {{ max-width:100%; display:block; }}
table {{ width:100%; border-collapse:collapse; font-size:8.6pt; }}
th {{ font-family:Poppins; font-weight:700; font-size:6.4pt; letter-spacing:.1em; text-transform:uppercase; text-align:right; border-bottom:1.5px solid #1b2a41; padding:.04in .05in; color:#1b2a41; vertical-align:bottom; }}
th:first-child, td:first-child {{ text-align:left; }}
td {{ text-align:right; padding:.035in .05in; border-bottom:1px solid #e3e6ec; }}
td.or {{ color:#c8662a; }} tr.sp td {{ background:#f3eef7; color:#5d2270; font-weight:700; }} tr.bold td {{ font-weight:700; }}
.note {{ font-size:7.6pt; color:#555; line-height:1.3; margin-top:.08in; }}
.card {{ border-top:3px solid #1b2a41; background:#f7f7f5; padding:.08in .1in; font-size:9pt; }}
.card.p {{ border-color:#7b2d8e; }} .card.o {{ border-color:#c8662a; }} .card.b {{ border-color:#1f5ea8; }} .card.g {{ border-color:#1f7a4d; }}
.big {{ font-family:Lora; font-weight:700; font-size:21pt; line-height:1.05; }}
.card.p .big {{ color:#7b2d8e; }} .card.o .big {{ color:#c8662a; }} .card.b .big {{ color:#1f5ea8; }}
.card ul {{ padding-left:.16in; margin:.04in 0; }} .card li {{ margin-bottom:.03in; }}
.quote {{ border-left:3px solid #c8662a; background:#f7f5f1; font-family:Lora; font-style:italic; padding:.06in .12in; margin:.06in 0; font-size:10pt; }}
.foot {{ position:absolute; bottom:.28in; left:.55in; right:.55in; border-top:1px solid #ccc; padding-top:.05in; font-size:7pt; color:#777; display:flex; justify-content:space-between; }}
.tiles {{ display:grid; grid-template-columns:repeat(4,1fr); gap:.14in; }}
.tile {{ border-top:3px solid #1b2a41; padding-top:.04in; font-size:8.6pt; line-height:1.25; }}
.tile .big {{ font-size:22pt; }}
.tile.o .big {{ color:#c8662a; }} .tile.p .big {{ color:#7b2d8e; }} .tile.b .big {{ color:#1f5ea8; }}
.ask {{ background:#fdf6ef; border-top:3px solid #c8662a; padding:.08in .12in; font-size:8.8pt; }}
.ask ol, .take ol {{ margin:.03in 0; padding-left:.18in; }} .ask li, .take li {{ margin-bottom:.04in; }}
.take {{ font-size:8.8pt; }}
.small {{ font-size:8.6pt; }}
</style></head><body>

<!-- PAGE 1 -->
<div class="page">
<div class="hero"><div class="eyebrow">Legion of Data Nerds · Budget brief · Fall 2026 · Updated with Oct 1, 2026 data</div>
<h1>Closing a $20 million gap:<br>where the savings actually are</h1>
<p>District 65 needs to cut about 10% of its budget. We looked at class sizes, the options on the table, our staffing against the State's funding model, building costs and the closure scenarios.</p></div>
<div class="cols c2" style="grid-template-columns:1fr 1.15fr">
<div><div class="label">What should guide the plan</div>
<ol class="guide">
<li><div><b>Decide by outcomes, not dollars.</b> Orient decisions and accountability toward what students learn, and judge every cut by its effect on the classroom.</div></li>
<li><div><b>Build a learning organization.</b> Use data to improve, and be willing to say when something didn't work and change course.</div></li>
<li><div><b>Engaged families are an asset.</b> Community groups like ours are part of a healthy district. When parents check out, the system has already failed.</div></li>
</ol></div>
<div><div class="label">Risk assessment: a building-first plan</div>
<div class="risk"><span class="tag h">HIGH</span><div><b>Enrollment numbers are off</b><br>May projection: <b>604</b> kindergartners; Oct 1: <b>530</b> (−12%). About <b>210</b> students attend by permissive transfer.</div></div>
<div class="risk"><span class="tag h">HIGH</span><div><b>Receiving schools overfill</b><br><b>7 of 19 scenarios</b> push a school past capacity.</div></div>
<div class="risk"><span class="tag h">HIGH</span><div><b>Low-enrollment programs</b><br>Closing TWI, ACC or STEP buildings means <b>moving whole programs</b>.</div></div>
<div class="risk"><span class="tag h">HIGH</span><div><b>One-time costs and special ed</b><br>Costs <b>come before savings</b>; IEP services must continue <b>uninterrupted</b>.</div></div>
<div class="risk"><span class="tag h">HIGH</span><div><b>A two-tier system</b><br>Families who can afford it <b>opt for private school</b>, leaving D65 with fewer resources and less engaged support.</div></div>
<div class="risk"><span class="tag m">MEDIUM</span><div><b>Transportation costs</b><br><b>$150–270K a year per closure</b>, 20–35% of building savings.</div></div>
<div class="risk"><span class="tag m">MEDIUM</span><div><b>Equity</b><br>Closures land on <b>specific neighborhoods</b> and TWI access.</div></div>
<div class="risk"><span class="tag m">MEDIUM</span><div><b>Attention is finite</b><br>Closure planning takes time that <b>staffing decisions</b> need.</div></div>
</div></div>
<div class="label or">Class size and the student experience</div>
<h3 style="margin-top:0">A child's class size depends on their school and grade</h3>
<img src="img/class_size.png" style="height:2.75in;margin:0 auto">
<div class="cols c3 small" style="margin-top:.06in">
<div><b>Grade averages run from 13 to 26 students per class.</b> Of the 66 K–5 school-grades (188 sections), <b>12 average under 16</b> and <b>16 average over 21</b>.</div>
<div><b>Same grade, different school:</b> a 3rd grader at Dawes or Washington is in a class of about 16; at Orrington, 26 (52 students in 2 sections, over the 24 cap).</div>
<div><b>Fuller buildings don't have bigger classes</b> (r = −0.14). The spread comes from <b>how grades divide into classes</b> and from TWI and ACC strands.</div>
</div>
<div class="note">Class size = students in the grade ÷ sections. Sections: District 65's FY27 K–5 section list, a spreadsheet received by email from the district on October 1, 2026. Students: data.district65.net, pulled October 1, 2026.</div>
{FOOT(1)}</div>

<!-- PAGE 2 -->
<div class="page">
{head('01','Building costs','Which buildings cost the most to run?')}
<p class="lede">Every building carries a principal, an office and custodians whatever its size, so <b>emptier buildings cost more per student</b>. At the average closure-scenario enrollment, <b>Oakton, Dawes and Lincolnwood</b> cost the most per student; <b>Dewey and Orrington</b> the least.</p>
<div class="label">Building cost per student: today, each closure scenario, and the average</div>
<img src="img/building_cost.png" style="height:3.1in;margin:0 auto">
<table style="margin-top:.08in"><tr><th>Building</th><th>Students<br>Oct 1</th><th>Utilization<br>now → avg*</th><th>Principal<br>+ office</th><th>Custodians</th><th>Utilities</th><th>Total<br>a year</th><th>Per student<br>now</th><th>Per student<br>scenario avg*</th></tr>
{rows}</table>
<div class="cols c2 small" style="margin-top:.1in">
<div><div class="label" style="margin-top:0">What stands out</div><b>Adding students lowers cost per student</b> only at receiving buildings; the district saves just the closed building's costs. <b>Utilities are a small share:</b> $1.33M district-wide.</div>
<div><div class="label" style="margin-top:0">Data we still need</div><b>Maintenance and capital needs by building</b> (10-year Health/Life Safety survey, facility assessment), likely larger than utilities; <b>actual building staff by school</b>; <b>site-level spending per student</b> (ISBE report card); <b>full-year 2026 utilities</b>.</div></div>
<div class="note">*Scenario average = today's cost ÷ the building's average 2027–28 enrollment across the closure scenarios on page 3 where it stays open and at or under capacity (90% of displaced students stay). Foster has no utility account. <b>Sources:</b> enrollment from data.district65.net, pulled Oct 1, 2026. Utilities and energy use (2025) are from the Sept 23, 2026 pull: the Oct 1 dashboard showed incomplete 2025 utility data for some buildings (for example, Chute and King Arts). Square feet derived from energy use ÷ EUI; capacity = smaller of the district's Cap Total and Cordogan Clark (2022); principal pay, FY26 PA 96-0434 salary report ($180,753 average); 64 custodians from the district's employee-category table, allocated by square feet. <b>Assumed:</b> custodian pay $65K and office staff $60K per building. Built with help from Claude (AI); please verify.</div>
{FOOT(2)}</div>

<!-- PAGE 3 -->
<div class="page">
{head('02','Closure scenarios','What closures would do to the receiving schools')}
<p class="lede">Each closed school's projected 2027–28 students go to its receiving schools, with 90% staying in D65. Pairs close one south school (<b>Dewey, Washington, Oakton or Dawes</b>) and one north school (<b>Willard, Lincolnwood or Orrington</b>). "Kept together" sends a school to one building; "split" divides it by open seats.</p>
<img src="img/closure_grid.png" style="height:4.55in;margin:0 auto">
<div class="cols c2 small" style="margin-top:.08in">
<div><div class="label" style="margin-top:0">One closure</div>
<p style="margin:.02in 0"><b>Dewey</b>, split three ways, leaves every receiver at 73–76%, but its TWI strand needs a new home. <b>Orrington</b> kept together fills Willard to 89% and all 24 of its classrooms.</p>
<p style="margin:.02in 0"><b>Lincolnwood</b> kept together doesn't fit: Orrington would reach 117%, with 23 classes for 19 classrooms. Sent whole to Willard instead, it lands right at the limit (100%, 25 classes for 24 classrooms). Splitting it between Orrington and Willard fits (81% and 79%), but every grade is divided between two schools. STEP moves either way.</p>
<p style="margin:.02in 0"><b>Oakton</b>, the fullest building today, splits three ways into Dawes, Washington and Dewey at 83–87%. Oakton's TWI strand and ACC program both need new hosts.</p>
<p style="margin:.02in 0"><b>Dawes</b> splits three ways into Oakton, Washington and Dewey at 79–90%, with classrooms to spare at each. It displaces the fewest students of any south closure. Its TWI strand would move to Dewey or Oakton.</p></div>
<div><div class="label" style="margin-top:0">Two closures</div>
<p style="margin:.02in 0"><b>Six pairs keep every receiver under capacity:</b> Washington, Oakton or Dawes, paired with Willard or Orrington. Even these reach 89–93% somewhere, and each moves at least one TWI strand.</p>
<p style="margin:.02in 0"><b>Every pair with Dewey or Lincolnwood overfills Orrington or Willard</b>, up to 136%. TWI at Dewey, Washington, Oakton and Dawes, ACC at Oakton and STEP at Lincolnwood make relocation costly.</p>
<p style="margin:.02in 0">Each pair could lose <b>25–101 students</b> from the district.</p></div></div>
<div class="note">Projection: Oct 1, 2026 enrollment; grades roll forward one year; incoming K = this year's K. Capacity = smaller of the district's Cap Total and Cordogan Clark. Washington's receivers follow the district's SDRP 3D table; Willard's, Oakton's and Dawes's are assumed from geography. Full tables at 85%, 90% and 95% retention are in projections/v2_2026-10-01/closure_scenarios.md. Estimates built with help from Claude (AI); please verify.</div>
{FOOT(3)}</div>

<!-- PAGE 4 -->
<div class="page">
{head('03','State funding model (EBF)','How K–5 staffing compares with Evidence-Based Funding')}
<p class="lede">Illinois's Evidence-Based Funding formula sets out how many staff the State pays for. On paper, D65 has about 267 more K–5 staff than EBF funds, worth $17.5M a year. Special education explains all of that difference.</p>
<img src="img/ebf_by_group.png" style="height:3.6in;margin:0 auto">
<div class="cols c3" style="margin-top:.1in">
<div class="card p"><div class="big">+$18.7M</div>Special-ed teachers, therapists and paras above EBF's ratio of 1 teacher and 1 aide per 141 students. Staffing follows IEPs and federal law, so this can't simply be cut to match.</div>
<div class="card o"><div class="big">+$6.5M</div>Other groups above EBF: social workers and psychologists ($2.2M), ESL teachers ($1.8M), specialists ($1.7M), nurses ($0.5M).</div>
<div class="card b"><div class="big">−$7.6M</div>Where we're below EBF: classroom teachers, instructional coaches (6 vs. 17), interventionists and counselors.</div></div>
<table style="margin-top:.12in"><tr><th>K–5 staffing</th><th>1 school</th><th>9 schools</th><th>10 schools</th><th>11 (today)</th></tr>
<tr><td>Staff EBF funds</td><td>416</td><td>451</td><td>466</td><td>478</td></tr>
<tr><td>Staff we have (est.)</td><td>745</td><td>745</td><td>745</td><td>745</td></tr>
<tr class="bold"><td>Yearly cost above EBF</td><td>$24.7M</td><td>$20.7M</td><td>$19.0M</td><td>$17.5M</td></tr>
<tr class="sp"><td>Special ed and paras</td><td>$18.7M</td><td>$18.7M</td><td>$18.7M</td><td>$18.7M</td></tr>
<tr><td>Everything else</td><td>$6.0M</td><td>$2.0M</td><td>$0.3M</td><td>−$1.1M</td></tr></table>
<div class="note">EBF is a funding model, not a staffing rule. *The classroom-teacher figure is an upper bound: split evenly over 11 buildings, every grade rounds up to 3 classes. Staff other than classroom teachers are estimated for K–5 at 64% of the district count. Some non-teaching pay is assumed. Ratios from 105 ILCS 5/18-8.15. K–5 enrollment (3,484) and English learners from data.district65.net, pulled Oct 1, 2026.</div>
{FOOT(4)}</div>

<!-- PAGE 5 -->
<div class="page">
{head('04','The options','What each option saves, and what it costs students')}
<div class="cols" style="grid-template-columns:1.45fr 1fr;align-items:start">
<img src="img/options.png">
<div class="small"><p class="lede" style="font-size:10.5pt">Plotting savings against harm puts the choices side by side. Options under the dashed line save more for less disruption to students and families.</p>
<div class="label">Where the money is</div>Consolidating small classes, bringing specialist and support staffing closer to EBF levels, and central-office cuts each save $1–2.6M a year. One closure saves $0.2–0.7M.
<div class="label">Small but low-harm</div>Leasing empty space, TWI tuition seats, shared City services and sponsorships each bring in $0.1–0.6M, with little effect on classrooms.
<div class="label">About the scores</div>The cost-to-students scores are a first draft for discussion. The savings ranges are rough; items marked "estimate" below are illustrative.</div></div>
<table style="margin-top:.12in"><tr><th>Option</th><th>Yearly savings</th><th style="text-align:left">How we estimated it</th></tr>
<tr><td>Close 1 school</td><td>$0.2–0.7M</td><td style="text-align:left">Building-use analysis: building savings minus added busing (net per closure)</td></tr>
<tr><td>Close 2 schools</td><td>$0.4–1.4M</td><td style="text-align:left">Two times the per-closure net; relocation and renovation costs not included</td></tr>
<tr><td>Lease or share empty space</td><td>$0.1–0.4M</td><td style="text-align:left">Estimate: preschool or community partner leases in underused wings</td></tr>
<tr><td>Consolidate small classes</td><td>$1.1–2.2M</td><td style="text-align:left">10–20 fewer sections × ~$111K average teacher pay (EBF analysis)</td></tr>
<tr><td>Consolidate TWI strands in grades 4–5</td><td>$0.2–0.4M</td><td style="text-align:left">2–4 fewer upper-grade TWI sections × ~$111K</td></tr>
<tr><td>Specialist teachers to EBF level</td><td>$1.7–2.6M</td><td style="text-align:left">15–22 FTE above EBF × ~$115K (EBF Table 3)</td></tr>
<tr><td>Pupil support to EBF level</td><td>$1.1–2.2M</td><td style="text-align:left">Half to all of the 21 social work/psych/FACE FTE above EBF × ~$103K</td></tr>
<tr><td>Voluntary retirement incentive</td><td>$0.5–1.5M</td><td style="text-align:left">Estimate: 25–40 retirements replaced at lower step pay net of incentive</td></tr>
<tr><td>Central office admin cuts</td><td>$0.9–1.8M</td><td style="text-align:left">Estimate: 5–10 central office positions × ~$180K total comp</td></tr>
<tr><td>Share admin services with City</td><td>$0.1–0.5M</td><td style="text-align:left">Estimate: shared office space and personnel (creative ideas menu)</td></tr>
<tr><td>TWI tuition seats</td><td>$0.3–0.6M</td><td style="text-align:left">Estimate: 20–40 tuition students × ~$15K</td></tr>
<tr><td>City shared services</td><td>$0.2–0.6M</td><td style="text-align:left">Estimate: crossing guards, maintenance, purchasing (creative ideas menu)</td></tr>
<tr><td>Cell tower, solar and sponsorship revenue</td><td>$0.1–0.4M</td><td style="text-align:left">Estimate: cell tower, solar panel and facility sponsorship revenue (creative ideas menu)</td></tr></table>
{FOOT(5)}</div>

<!-- PAGE 6 -->
<div class="page">
{head('05','Communicating the plan',"What families should hear: priorities, what they get, and how we'll know")}
<p class="lede">Families will judge any plan by what happens in their child's classroom. The plan should say plainly what it protects, what changes, and how the district will show it's working.</p>
<div class="cols c3 small">
<div class="card"><div class="label" style="margin-top:0">Our priorities</div><h3 style="font-size:13pt">What comes first</h3><ul>
<li><b>Class sizes in a set range</b> for every grade at every school</li><li><b>Children stay with their classmates and teachers</b> wherever possible</li><li><b>Programs families chose stay whole:</b> TWI, ACC, STEP</li><li><b>Every IEP is fully served</b>, through any change</li><li><b>Savings reinvested</b> where EBF says we're short: coaching and intervention</li></ul></div>
<div class="card g"><div class="label" style="margin-top:0;color:#1f7a4d">What families get</div><h3 style="font-size:13pt">What changes for them</h3><ul>
<li><b>Predictable class sizes</b>, published for each school and grade</li><li><b>A clear plan for any building move:</b> the timeline, the receiving school, busing, and how classmates stay together</li><li><b>More reading and math intervention</b> as savings are reinvested</li><li><b>A clear budget:</b> what was cut, what it saved, where it went</li></ul></div>
<div class="card b"><div class="label" style="margin-top:0;color:#1f5ea8">Educational outcomes</div><h3 style="font-size:13pt">How we'll know it's working</h3><ul>
<li><b>Class size by school and grade</b>, every fall</li><li><b>Reading and math growth</b> by school and student group</li><li><b>Attendance and chronic absence</b></li><li><b>Special-ed service minutes delivered</b> vs. IEPs</li><li><b>Families staying in D65:</b> transfers in, out and to private schools</li></ul></div></div>
<div class="label">Values to emphasize</div>
<p class="small" style="margin:.02in 0 .08in">Families and staff will need both words and action: tell them what to expect, then follow through.</p>
<div class="cols c3 small">
<div class="card o"><div class="big" style="font-size:16pt">Empathy</div>Listen to families and staff before deciding. Acknowledge what a change means for a school community, and show it in what the plan does, not only in what it says.</div>
<div class="card p"><div class="big" style="font-size:16pt">Accountability</div>Tie every decision to what students learn. Do what the plan promises, report the results, and say so when something isn't working and change course.</div>
<div class="card b"><div class="big" style="font-size:16pt">Transparency</div>Tell families and staff what to expect and when: what's being considered, the timeline, what changes for each child and each job, and what each choice saves.</div></div>
<div class="label">Key messages</div>
<div class="quote">"We're protecting what happens in the classroom first: class sizes, programs, and every child's services."</div>
<div class="quote">"We'll make the biggest savings where they do the least harm, and we'll show our work."</div>
<div class="note">The class-size range is for the district and community to set.</div>
{FOOT(6)}</div>

<!-- PAGE 7 -->
<div class="page">
<div class="sechead"><div class="num">✓</div><div><div class="kick">Recap</div><h2>The whole brief on one page</h2></div></div>
<div class="tiles">
<div class="tile o"><div class="big">1–3.5%</div>of the $20M target from one closure, after busing ($0.2–0.7M a year)</div>
<div class="tile p"><div class="big">$18.7M</div>special-ed staffing above EBF's ratio: the whole gap, set by IEPs</div>
<div class="tile"><div class="big">7 of 19</div>closure scenarios push a receiving school over capacity</div>
<div class="tile b"><div class="big">23 of 66</div>K–5 grades average under 18 students per class (Oct 1, 2026)</div></div>
<div class="cols" style="grid-template-columns:1.1fr 1fr;margin-top:.12in">
<div class="take"><div class="label" style="margin-top:0">Takeaways</div><ol>
<li><b>Class size depends on school and grade:</b> grade averages run from 13 to 26 students and don't track how full a building is (r = −0.14). p. 1</li>
<li><b>Emptier buildings cost more per student:</b> {d(round(k5.per_student.min(),-1))}–{d(round(bc.per_student.max(),-1))} today. Receivers get cheaper per student, but the district saves only the closed building's costs. p. 2</li>
<li><b>Where students go decides if a closure fits.</b> Every scenario that overfills sends students into Orrington or Willard; TWI, STEP and ACC moves are costly. Closing Dawes fits, split among Oakton, Washington and Dewey. p. 3</li>
<li><b>Special ed explains the whole EBF gap.</b> Without it we're $1.1M below the model, and short on coaches and interventionists. p. 4</li>
<li><b>Staffing and class structure save more:</b> $1–2.6M each, against $0.2–0.7M per closure. p. 5</li>
<li><b>Tell families what's protected, what they get, and how the district will know it's working.</b> p. 6</li></ol></div>
<div class="ask"><div class="label or" style="margin-top:0">What we're asking</div><h3 style="font-size:13pt;margin-top:0">What to convey in the plan</h3><ol>
<li>Itemized savings from the Kingsley and Bessie Rhodes closures, net of opening Foster.</li>
<li>The full cost of closing and relocating a school, including TWI, STEP and ACC moves.</li>
<li>Which positions would be cut, by category, and what each saves.</li>
<li>Class counts and class sizes by grade, before and after, not just utilization.</li>
<li>How the plan improves outcomes for students, not only this year's budget.</li></ol>
<p style="font-family:Lora;font-style:italic;margin:.06in 0 0">Decide by outcomes, learn from the data, and treat engaged families as an asset. We need to work with the buildings and the district we have.</p></div></div>
<div class="cols" style="grid-template-columns:1.6fr 1fr;margin-top:.08in">
<div><div class="label" style="margin-top:0">Building cost per student</div><img src="img/building_cost.png" style="height:1.95in"></div>
<div><div class="label" style="margin-top:0">Staffing above EBF</div><img src="img/ebf_waterfall.png" style="height:1.95in"></div></div>
<div class="label">Utilization in every closure scenario, 2027–28</div>
<img src="img/closure_grid.png" style="height:2.2in;margin:0 auto">
{FOOT(7)}</div>
</body></html>'''
open('d65_budget_choices_handout_v3_10_01.html','w').write(html)
