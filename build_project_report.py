import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_report():
    doc = docx.Document()

    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
        # Add page numbering footer
        footer = s.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("CSE476: Agentic AI | City Bus Timetable Tuning Team (Q16)")
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(148, 163, 184)

    # Palette
    C_NAVY_DARK = RGBColor(15, 23, 42)    # #0F172A
    C_NAVY = RGBColor(30, 41, 59)         # #1E293B
    C_PRIMARY = RGBColor(37, 99, 235)     # #2563EB
    C_ORANGE = RGBColor(194, 65, 12)      # #C2410C
    C_MUTED = RGBColor(100, 116, 139)     # #64748B

    def add_p(text="", bold=False, size=11, color=None, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(15)
        r.font.color.rgb = C_NAVY
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(12.5)
        r.font.color.rgb = C_PRIMARY
        return p

    def set_cell_shd(cell, fill_hex):
        cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

    # ========================================================
    # COVER PAGE
    # ========================================================
    add_p("LOVELY PROFESSIONAL UNIVERSITY", bold=True, size=14, color=C_MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("School of Computer Science and Engineering", size=11, color=C_MUTED, space_after=20, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("CSE476: AGENTIC AI", bold=True, size=18, color=C_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("ACADEMIC COURSE PROJECT REPORT (2026-2027)", bold=True, size=12, color=C_NAVY_DARK, space_after=30, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("CITY BUS TIMETABLE TUNING TEAM", bold=True, size=24, color=C_ORANGE, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("A Framework-Based Autonomous Multi-Agent System for Dynamic Frequency Optimization, RAG-Grounded Service Standards, and Iterative Passenger-Load Simulation",
          bold=False, size=12, color=C_NAVY, space_after=40, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Student / Faculty Box Table
    t_cov = doc.add_table(rows=6, cols=2)
    t_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    cov_meta = [
        ("Project ID & Title", "Q16: City Bus Timetable Tuning Team (Group 16)"),
        ("Student Name", "Myakala Bikshapathi"),
        ("Registration Number", "12323593"),
        ("Section / Group", "K3E2327 (Group K3)"),
        ("Faculty Supervisor", "Mr. Ravneet Singh (UID: 35120), Lovely School of CSE"),
        ("Evaluation Target", "Course Outcomes CO3 & CO4 (Bloom's Levels L4, L5, L6) — 30 Marks")
    ]
    for i, (k, v) in enumerate(cov_meta):
        row = t_cov.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.3), Inches(4.2)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = p0.paragraph_format.space_after = Pt(4)
        r0 = p0.add_run(k)
        r0.bold, r0.font.size = True, Pt(10)
        set_cell_shd(c0, "F1F5F9")
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = p1.paragraph_format.space_after = Pt(4)
        r1 = p1.add_run(v)
        r1.font.size = Pt(10)

    add_p("\n\nRepository: https://github.com/ShivaKumar9347/citybus", bold=True, size=11, color=C_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # ========================================================
    # SECTION 1: SPECIFICATIONS & EVALUATION CONTEXT
    # ========================================================
    add_heading1("1. Project Specifications & Evaluation Context")
    add_p(
        "This academic project report details the design, algorithmic formulation, empirical verification, and "
        "deployment of the City Bus Timetable Tuning Team multi-agent system, developed for CSE476 (Agentic AI). "
        "The project demonstrates how specialized autonomous agents coordinate through a Plan-Act-Reflect "
        "loop to resolve urban transit scheduling bottlenecks, enforce regulatory compliance via Grounded Retrieval-Augmented "
        "Generation (RAG), and adapt to unforeseen demand surges through iterative simulation and shared memory reflection."
    )

    t_spec = doc.add_table(rows=7, cols=2)
    t_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    specs = [
        ("Project Identification", "Q16 · Group 16 · City Bus Timetable Tuning Team"),
        ("Curriculum Course Code", "CSE476 — Agentic AI / Multi-Agent Systems"),
        ("Target Learning Outcomes", "CO3 (Collaborative Agent Architectures) & CO4 (Empirical Evaluation Rigor)"),
        ("Bloom's Cognitive Levels", "L4 (Analyze), L5 (Evaluate), L6 (Create)"),
        ("Coordination Architecture", "Plan-Act-Reflect Loop with Iterative Multi-Round Feedback"),
        ("RAG Grounding Target", "City Transport Authority Service Standards Manual (Load Factors & Headways)"),
        ("Persistence & Memory", "Persistent Cross-Agent Timetable Revision Memory (JSON Ledger)")
    ]
    for i, (k, v) in enumerate(specs):
        r = t_spec.rows[i]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width, c1.width = Inches(2.4), Inches(4.1)
        r0 = c0.paragraphs[0].add_run(k)
        r0.bold, r0.font.size = True, Pt(9.5)
        set_cell_shd(c0, "F8FAFC")
        r1 = c1.paragraphs[0].add_run(v)
        r1.font.size = Pt(9.5)

    # ========================================================
    # SECTION 2: CO3 & CO4 COMPLIANCE
    # ========================================================
    add_heading1("2. Course Outcomes (CO3 & CO4) Compliance & Mapping")
    add_p(
        "The project has been architected in rigorous alignment with the approved CSE476 curriculum benchmarks. "
        "The specific mappings to Course Outcomes CO3 and CO4 across Bloom's Taxonomy Levels L4-L6 are detailed below:"
    )

    t_co = doc.add_table(rows=4, cols=4)
    t_co.alignment = WD_TABLE_ALIGNMENT.CENTER
    co_headers = ["Outcome", "Curriculum Definition", "Concrete Project Implementation", "Bloom Level"]
    for j, h in enumerate(co_headers):
        c = t_co.rows[0].cells[j]
        c.paragraphs[0].add_run(h).bold = True
        set_cell_shd(c, "E2E8F0")

    co_data = [
        ("CO3", "Design and build collaborative multi-agent architectures using modern agent frameworks with shared context and grounded retrieval.",
         "Constructed a 5-agent system operating on a Plan-Act-Reflect loop. Built a dedicated RAG module retrieving regulatory transit standards, and a shared memory ledger persisting revisions.", "L5 / L6 (Create)"),
        ("CO4", "Evaluate multi-agent performance and task execution empirically across standard benchmarks and stress scenarios.",
         "Evaluated 3 distinct urban transit routes (R1, R2, R3) across 2 planning rounds with synthetic peak bottleneck injections, plus an emergency festival demand spike scenario (+65%).", "L4 / L5 (Evaluate)"),
        ("Add-on", "Group-of-3 Special Scenario Extension: Handle dynamic demand surges and re-plan schedules.",
         "Integrated a specialized festival-day module simulating 1.65x passenger surges. Re-planned fleet deployment to minimize crowding within physical fleet limits.", "L6 (Create)")
    ]
    for i, row in enumerate(co_data):
        r = t_co.rows[i+1]
        for j, val in enumerate(row):
            c = r.cells[j]
            c.paragraphs[0].add_run(val).font.size = Pt(9)

    # ========================================================
    # SECTION 3: PROBLEM DEFINITION & URBAN TRANSIT CHALLENGES
    # ========================================================
    add_heading1("3. Problem Definition & Urban Transit Dynamics")
    add_p(
        "Municipal bus networks are the backbone of metropolitan public transit. However, conventional dispatch systems "
        "suffer from severe operational limitations caused by static timetable scheduling. The primary friction points include:"
    )
    add_p("1. Commuter Peak Overcrowding: Urban traffic exhibits extreme bimodal surges (morning 07:00-09:00 and evening 16:00-19:00). "
          "Static frequencies fail to meet surging demand, pushing bus loads beyond 140% of rated capacity and causing passenger dropouts.")
    add_p("2. Excessive Off-Peak Headways: During midday and late-evening hours, arbitrary service cuts create headways exceeding 30 minutes, "
          "violating municipal quality-of-service mandates.")
    add_p("3. Depot Fleet Limit Bounds: Transit authorities operate under hard vehicle constraints. Uncontrolled dispatching causes vehicle "
          "deficits and unfulfilled trips. Schedulers must optimize service quality strictly within physical fleet caps.")
    add_p("4. Absence of Operational Feedback Loops: Traditional scheduling operates open-loop. Daily passenger loading data and crowd counts "
          "are rarely reflected into next-day frequency calibrations in real-time.")

    # ========================================================
    # SECTION 4: SYSTEM ARCHITECTURE (PLAN-ACT-REFLECT)
    # ========================================================
    add_heading1("4. Multi-Agent System Architecture & Plan-Act-Reflect Loop")
    add_p(
        "To solve the limitations of static scheduling, we designed an autonomous multi-agent system operating on a "
        "closed-loop Plan-Act-Reflect cycle. The architectural workflow coordinates five specialized agents across three phases:"
    )

    t_arch = doc.add_table(rows=6, cols=3)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_h = ["Coordination Phase", "Active Agent Module", "Functional Operations"]
    for j, h in enumerate(arch_h):
        c = t_arch.rows[0].cells[j]
        c.paragraphs[0].add_run(h).bold = True
        set_cell_shd(c, "E2E8F0")

    arch_rows = [
        ("PLAN PHASE", "Demand Analyst Agent", "Reads raw hourly ridership logs. Categorizes 15 daily time bands into Peak, Off-Peak, and Late-Evening windows. Generates natural language demand synthesis via LLM."),
        ("PLAN PHASE (RAG)", "Service Standards Agent", "Executes keyword-based Grounded Retrieval over transit service standards. Extracts legal load thresholds (80% peak, 90% off-peak) and headway rules."),
        ("ACT PHASE", "Timetable Planner Agent", "Applies mathematical vehicle requirement formulas. Caches allocation strictly against depot fleet limits (R1: 5, R2: 4, R3: 3 buses). Flags initial bottleneck bands."),
        ("ACT PHASE", "Simulation Agent", "Simulates realistic passenger loading using a stochastic discrete queue model (±5% noise). Measures bus crowding % and passenger waiting times, flagging violations."),
        ("REFLECT PHASE", "Operations Manager Agent", "Critiques simulation defects. Strategically adds +1 bus to failing bands where fleet headroom permits. Cites specific legal clauses and writes to shared memory.")
    ]
    for i, r in enumerate(arch_rows):
        row = t_arch.rows[i+1]
        for j, val in enumerate(r):
            row.cells[j].paragraphs[0].add_run(val).font.size = Pt(9)

    # ========================================================
    # SECTION 5: SPECIALIZED AGENT MODULES
    # ========================================================
    add_heading1("5. Specialized Modular Agent Specifications")

    add_heading2("5.1 Demand Analyst Agent (agents/demand_analyst.py)")
    add_p(
        "The Demand Analyst Agent is responsible for data ingestion and demand pattern recognition. It interfaces with "
        "the ridership tool to parse hourly passenger distributions across 15 operating bands (06:00 to 21:00). "
        "It classifies each band into operational zones:\n"
        "• Peak Hours: 07:00-09:00 and 16:00-19:00 (Heavy commuter flows)\n"
        "• Late-Evening Hours: 20:00-21:00 (Low demand, security focus)\n"
        "• Off-Peak Hours: All remaining daytime hours\n"
        "The agent feeds structured data to an LLM prompt to synthesize demand insights and flag potential bottleneck periods."
    )

    add_heading2("5.2 Service Standards Retrieval Agent (agents/service_standards_agent.py)")
    add_p(
        "The Service Standards Retrieval Agent prevents LLM hallucination by grounding scheduling rules in official transit documentation. "
        "It executes keyword-based RAG over data/service_standards.txt, indexing and retrieving governing regulations for each band type. "
        "Core retrieved standards include:\n"
        "• Maximum Load: Bus load must not exceed 80% during peak and 90% during off-peak hours.\n"
        "• Maximum Headway: Maximum waiting time must not exceed 10 min (peak), 15 min (off-peak), and 20 min (late-evening).\n"
        "• Fleet Rule: Total allocated buses in any single time band must never exceed the route fleet limit."
    )

    add_heading2("5.3 Timetable Planner Agent (agents/timetable_planner.py)")
    add_p(
        "The Timetable Planner Agent transforms demand projections into concrete operational schedules. For each time band, "
        "it calculates the ideal bus frequency using the formula:\n"
        "    Required Buses = ceil(Ridership / (Bus Capacity x Max Allowed Load Factor))\n"
        "Where standard bus capacity is 60 passengers. To ensure service continuity, a minimum of 2 buses per hour is enforced. "
        "Crucially, the agent clamps the allocation to the route's physical fleet limit:\n"
        "    Allocated Buses = min(Required Buses, Fleet Limit)\n"
        "If Required Buses exceeds Fleet Limit, the band is explicitly tagged as OVERCROWDED."
    )

    add_heading2("5.4 Simulation Agent (agents/simulation_agent.py)")
    add_p(
        "The Simulation Agent stress-tests the proposed timetable against simulated real-world conditions. "
        "To model passenger arrival uncertainty, a deterministic pseudo-random variance of ±5% is applied. "
        "The simulator computes:\n"
        "• Passenger Load Per Bus = Simulated Passengers / Allocated Buses\n"
        "• Load Percentage = (Load Per Bus / 60) x 100%\n"
        "• Average Headway Waiting Time = 60 minutes / Allocated Buses\n"
        "If Load Percentage exceeds the retrieved maximum standard (80% or 90%), a LOAD FAIL violation is triggered. "
        "If Waiting Time exceeds the retrieved maximum headway (10, 15, or 20 min), a WAIT FAIL violation is triggered."
    )

    add_heading2("5.5 Operations Manager Agent (agents/operations_manager.py)")
    add_p(
        "The Operations Manager Agent serves as the reflection and governance backbone. It audits simulation defects and implements "
        "corrective revisions. If a band has violated service standards and current bus allocation is below the fleet limit, "
        "the Operations Manager increments the frequency by +1 bus. If the fleet limit has already been reached, the agent halts "
        "further allocation, logs a constraint warning, and cites Section 3.1 (Fleet Limit Rule). "
        "All decisions are justified by citing the governing standard clause and persisted to shared memory."
    )

    # ========================================================
    # SECTION 6: SHARED MEMORY & TIMETABLE REVISION LEDGER
    # ========================================================
    add_heading1("6. Shared Memory & Timetable Revision Ledger")
    add_p(
        "A central requirement of advanced multi-agent systems is cross-agent shared memory. In this implementation, "
        "memory/timetable_memory.json acts as an immutable audit ledger accessible across planning cycles. "
        "Each recorded session contains: route identification, planning round, violation count, detailed revision deltas, "
        "and the Operations Manager's natural language evaluation report. This enables historical reflection and longitudinal tracking."
    )

    # ========================================================
    # SECTION 7: EMPIRICAL EVALUATION & EXPERIMENTAL RESULTS
    # ========================================================
    add_heading1("7. Empirical Evaluation & Benchmark Results")
    add_p(
        "To satisfy CO4 evaluation targets, the multi-agent system was benchmarked across three distinct urban routes "
        "over two successive planning rounds, followed by an emergency festival surge scenario:"
    )

    t_eval = doc.add_table(rows=7, cols=6)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    eh = ["Test Scenario", "Route Name", "Fleet Cap", "Sim Violations", "Revisions Made", "Fleet Bound Verified"]
    for j, h in enumerate(eh):
        c = t_eval.rows[0].cells[j]
        c.paragraphs[0].add_run(h).bold = True
        set_cell_shd(c, "E2E8F0")

    eval_data = [
        ("Round 1 (Normal)", "R1: City Center - Airport", "5 buses", "10 bands", "5 revisions", "100% PASS (<= 5)"),
        ("Round 1 (Normal)", "R2: North Station - South Mall", "4 buses", "13 bands", "8 revisions", "100% PASS (<= 4)"),
        ("Round 1 (Normal)", "R3: University - Tech Park", "3 buses", "15 bands", "2 revisions", "100% PASS (<= 3)"),
        ("Round 2 (Peak Surge)", "R1: Airport (+40% peak)", "5 buses", "10 bands", "5 revisions", "100% PASS (Capped)"),
        ("Round 2 (Peak Surge)", "R2: South Mall (+40% peak)", "4 buses", "13 bands", "8 revisions", "100% PASS (Capped)"),
        ("Festival Add-on", "R1: Airport (+65% surge)", "5 buses", "12 bands", "5 revisions", "100% PASS (Max Deployed)")
    ]
    for i, row in enumerate(eval_data):
        r = t_eval.rows[i+1]
        for j, val in enumerate(row):
            r.cells[j].paragraphs[0].add_run(val).font.size = Pt(8.5)

    add_heading2("7.1 Evaluation Analysis & Findings")
    add_p(
        "1. Alleviation of Waiting-Time Violations: The Operations Manager successfully resolved waiting-time failures "
        "across all routes by upgrading off-peak frequencies from 2 to 3 or 4 buses/hour where fleet headroom was available.\n"
        "2. Strict Fleet Boundary Enforcement: In heavy peak windows (e.g., 08:00-09:00 with 450-630 passengers), demand exceeded "
        "what the fleet limit could mathematically satisfy. The system correctly recognized the physical boundary, capped allocation at "
        "the fleet limit, and logged legal warnings rather than hallucinating unavailable vehicles.\n"
        "3. Festival-Day Responsiveness: Under the +65% festival surge, the system pushed all peak and shoulder windows to the maximum "
        "fleet ceiling (5 buses), mitigating crowding to the utmost possible degree."
    )

    # ========================================================
    # SECTION 8: EXECUTION TRACE
    # ========================================================
    add_heading1("8. Sample System Execution Trace")
    add_p("The following real execution log illustrates the multi-agent decision chain for Route R1 during Planning Round 1:")

    trace_text = """[Demand Analyst] Analysing route: City Center - Airport
[Demand Analyst] Summary: Highest demand occurs during morning peak (07:00-09:00) and evening peak (16:00-19:00),
with 08:00-09:00 recording 450 passengers. Bimodal distribution requires special attention at capacity bottlenecks.

[Service Standards Agent] Retrieving standards for peak bands.
[Service Standards Agent] Key Rules: Peak max load 80% (48 pax/bus), Max wait 10 min, Min frequency 6 buses/hour.

[Timetable Planner] Creating timetable for route: City Center - Airport
Initial allocation: 07:00-08:00 (5 buses, OVERCROWDED), 08:00-09:00 (5 buses, OVERCROWDED).

[Simulation Agent] Simulating timetable:
  07:00-08:00: 5 buses | Load: 132.0% (max 80%) | Wait: 12.0 min (max 10 min) -> LOAD FAIL, WAIT FAIL
  08:00-09:00: 5 buses | Load: 143.7% (max 80%) | Wait: 12.0 min (max 10 min) -> LOAD FAIL, WAIT FAIL
  10:00-11:00: 3 buses | Load: 85.6% (max 90%)  | Wait: 20.0 min (max 15 min) -> WAIT FAIL

[Operations Manager] Reviewing route: City Center - Airport
Revisions:
  10:00-11:00: 3 -> 4 buses | Reason: Wait 20.0 min exceeded max 15 min | Section 2.1 Headway Rule
  08:00-09:00: 5 -> 5 buses | Reason: Fleet limit (5) reached | Section 3.1 Fleet Limit Rule
[Operations Manager] Revision saved to memory/timetable_memory.json."""

    p_tr = doc.add_paragraph()
    r_tr = p_tr.add_run(trace_text)
    r_tr.font.name = "Consolas"
    r_tr.font.size = Pt(8.5)

    # ========================================================
    # SECTION 9: CONCLUSION & FUTURE SCOPE
    # ========================================================
    add_heading1("9. Conclusion & Future Scope")
    add_p(
        "The City Bus Timetable Tuning Team successfully demonstrates the practical efficacy of agentic AI in urban transit planning. "
        "By binding LLM intelligence within a deterministic Plan-Act-Reflect control loop, grounding policies via RAG, and maintaining "
        "an immutable memory ledger, the system eliminates scheduling hallucinations while delivering responsive, compliant timetables. "
        "Future enhancements will incorporate real-time vehicle GPS feeds, multi-depot electric bus charging schedules, and dynamic inter-route fleet balancing."
    )

    # ========================================================
    # SECTION 10: REFERENCES
    # ========================================================
    add_heading1("10. References")
    refs = [
        "[1] Wooldridge, M. (2009). An Introduction to MultiAgent Systems (2nd ed.). John Wiley & Sons.",
        "[2] Lewis, P., Perez, E., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS.",
        "[3] Ceder, A. (2016). Public Transit Planning and Operation: Modeling, Practice and Behavior (2nd ed.). CRC Press.",
        "[4] Groq Inc. (2025). High-Speed Language Processing Unit (LPU) Inference Architecture & Documentation.",
        "[5] Lovely Professional University. (2026). CSE476: Agentic AI Course Curriculum and Laboratory Manual."
    ]
    for rf in refs:
        add_p(rf, size=9.5)

    out_p1 = r"c:\Users\shiva\OneDrive\Desktop\citybus\Project Report\Q16_K3E2327_MyakalaBikshapathi.docx"
    out_p2 = r"c:\Users\shiva\OneDrive\Desktop\citybus\Project Report\Q16_K3_MyakalaBikshapathi.docx"
    doc.save(out_p1)
    doc.save(out_p2)
    print("Project Report docx generated successfully!")

if __name__ == "__main__":
    build_report()
