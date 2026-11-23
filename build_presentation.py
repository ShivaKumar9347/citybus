import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_ppt():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_NAVY_DARK = RGBColor(15, 23, 42)    # #0F172A
    C_NAVY = RGBColor(30, 41, 59)         # #1E293B
    C_PRIMARY = RGBColor(37, 99, 235)     # #2563EB Royal Blue
    C_ACCENT = RGBColor(234, 88, 12)      # #EA580C Transit Orange
    C_LIGHT_BG = RGBColor(248, 250, 252)  # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255)   # #FFFFFF
    C_BORDER = RGBColor(226, 232, 240)    # #E2E8F0
    C_TEXT_DARK = RGBColor(15, 23, 42)
    C_TEXT_MUTED = RGBColor(100, 116, 139)# #64748B
    C_TEXT_LIGHT = RGBColor(255, 255, 255)
    C_GREEN = RGBColor(22, 163, 74)       # #16A34A

    def set_slide_bg(slide, color=C_LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="CSE476: AGENTIC AI — MULTI-AGENT TRANSIT OPTIMIZATION"):
        # Top banner/category
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_PRIMARY

        # Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

    def add_card(slide, left, top, width, height, title, subtitle, bullets, border_color=C_BORDER, header_color=C_NAVY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = header_color

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(10)
            p_sub.font.italic = True
            p_sub.font.color.rgb = C_TEXT_MUTED
            p_sub.space_after = Pt(6)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(10)
            pb.font.color.rgb = C_TEXT_DARK
            pb.space_after = Pt(3)

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, C_NAVY_DARK)

    # Accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(0.15), Inches(2.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_ACCENT
    bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(0.9), Inches(11.3), Inches(2.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CSE476: AGENTIC AI (PROJECT SEMESTER 2026)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p = tf1.add_paragraph()
    p.text = "City Bus Timetable Tuning Team"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT

    p = tf1.add_paragraph()
    p.text = "An Autonomous Plan-Act-Reflect Multi-Agent System for Dynamic Frequency Optimization"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Bottom Meta Cards
    # Card 1: Project Scope
    meta1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(5.6), Inches(3.2))
    meta1.fill.solid()
    meta1.fill.fore_color.rgb = C_NAVY
    meta1.line.color.rgb = RGBColor(51, 65, 85)
    tf_m1 = meta1.text_frame
    tf_m1.margin_left = tf_m1.margin_top = Inches(0.3)
    p = tf_m1.paragraphs[0]
    p.text = "PROJECT SPECIFICATIONS & TARGETS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT
    bullets_m1 = [
        "Project ID: Q16 (Group 16) — City Bus Timetable Tuning Team",
        "Evaluation Target: CO3 & CO4 Compliance (30 Marks)",
        "Cognitive Taxonomy: Bloom's Taxonomy Levels L4, L5, L6",
        "Core Paradigm: Plan-Act-Reflect Loop Coordination",
        "Key Capabilities: Grounded RAG + Shared Timetable Memory",
        "GitHub: https://github.com/ShivaKumar9347/citybus"
    ]
    for b in bullets_m1:
        pb = tf_m1.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = C_TEXT_LIGHT
        pb.space_after = Pt(4)

    # Card 2: Student & Supervisor
    meta2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.6), Inches(5.7), Inches(3.2))
    meta2.fill.solid()
    meta2.fill.fore_color.rgb = C_NAVY
    meta2.line.color.rgb = RGBColor(51, 65, 85)
    tf_m2 = meta2.text_frame
    tf_m2.margin_left = tf_m2.margin_top = Inches(0.3)
    p = tf_m2.paragraphs[0]
    p.text = "SUBMITTED BY & GUIDANCE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    bullets_m2 = [
        "Student Name: Myakala Bikshapathi",
        "Registration Number: 12323593",
        "Section: K3E2327 (Group K3)",
        "Course Code: CSE476 — Agentic AI",
        "Faculty Supervisor: Mr. Ravneet Singh (UID: 35120)",
        "Discipline: Computer Science and Engineering",
        "Institution: Lovely Professional University, Punjab"
    ]
    for b in bullets_m2:
        pb = tf_m2.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = C_TEXT_LIGHT
        pb.space_after = Pt(4)

    # ==========================================
    # SLIDE 2: Problem Statement
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "Problem Statement: Transit Inefficiencies & Static Schedules")

    cards_s2 = [
        ("Peak Overcrowding Crisis", "Severe Service Degradation", [
            "Fixed schedules fail to respond to commuter demand spikes.",
            "Morning (07:00-09:00) & evening peaks experience >140% passenger capacity.",
            "Excessive load leads to safety hazards and passenger dropouts."
        ]),
        ("Waiting Time Inconsistency", "Long Passenger Headways", [
            "Off-peak intervals frequently stretch past 30 minutes.",
            "Violates municipal transport service quality standards.",
            "Lack of responsive re-allocation causes passenger frustration."
        ]),
        ("Physical Fleet Constraints", "Resource Capping Bottlenecks", [
            "Transit depots operate under strict vehicle availability limits.",
            "Unconstrained scheduling causes depot deficits and unfulfilled trips.",
            "Manual schedulers cannot simultaneously balance load and fleet bounds."
        ]),
        ("Isolated Operations Silos", "Absence of Feedback Loops", [
            "Traditional operations treat planning, simulation, and revisions separately.",
            "Post-day feedback is rarely synthesized into next-day timetable updates.",
            "Autonomous multi-agent collaboration provides dynamic adaptation."
        ])
    ]
    w = Inches(5.6)
    h = Inches(2.6)
    coords = [
        (Inches(0.8), Inches(1.6)), (Inches(6.8), Inches(1.6)),
        (Inches(0.8), Inches(4.5)), (Inches(6.8), Inches(4.5))
    ]
    for i, c in enumerate(cards_s2):
        add_card(s2, coords[i][0], coords[i][1], w, h, c[0], c[1], c[2])

    # ==========================================
    # SLIDE 3: Proposed Solution
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "Proposed Solution: Plan-Act-Reflect Multi-Agent System")

    cards_s3 = [
        ("1. Dynamic Plan Phase", "Demand Sensing & Standards RAG", [
            "Demand Analyst Agent ingests hourly ridership across 15 time bands.",
            "Service Standards Agent performs keyword RAG over regulatory manuals.",
            "Synthesizes load and headway rules (80% peak load, 10-min max wait)."
        ]),
        ("2. Fleet-Constrained Act Phase", "Scheduling & Virtual Simulation", [
            "Timetable Planner sets hourly frequencies capped at route fleet limits.",
            "Passenger-Load Simulator injects stochastic variance (±5%) to stress test.",
            "Calculates actual passenger crowding % and average waiting headway."
        ]),
        ("3. Reflective Optimization", "Operations Review & Memory Ledger", [
            "Operations Manager critiques simulation defects against standards.",
            "Adds targeted frequency increments where fleet headroom permits.",
            "Logs standard clause justifications into persistent timetable memory."
        ]),
        ("4. Special Event Resilience", "Festival Surge Scenario Handling", [
            "Handles sudden 65% demand surges during regional festival days.",
            "Re-optimizes allocations to alleviate bottlenecks while honoring fleet bounds.",
            "Outputs transparent comparison between normal and festival timetables."
        ])
    ]
    for i, c in enumerate(cards_s3):
        add_card(s3, coords[i][0], coords[i][1], w, h, c[0], c[1], c[2])

    # ==========================================
    # SLIDE 4: Multi-Agent Architecture
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "Multi-Agent System: Five Specialized Modular Agents")

    col_w = Inches(2.2)
    col_h = Inches(5.2)
    agents_s4 = [
        ("Demand Analyst", "PLAN PHASE", [
            "Tool: Ridership JSON Parser",
            "Classifies 15 time bands into Peak, Off-Peak, Late-Evening.",
            "Detects morning/evening commuter surge patterns.",
            "Generates natural language demand summary via LLM."
        ], C_PRIMARY),
        ("Standards RAG", "GROUNDING", [
            "Tool: Keyword RAG Retriever",
            "Indexes municipal transport service guidelines.",
            "Retrieves max load factors (80% peak, 90% off-peak).",
            "Fetches max headway rules (10m peak, 15m off-peak)."
        ], C_ACCENT),
        ("Timetable Planner", "ACT PHASE", [
            "Tool: Frequency Optimizer",
            "Calculates required buses: ceil(Demand / Capacity x Load).",
            "Enforces hard route fleet cap (3 to 5 buses/hour).",
            "Flags initial overcrowded bottlenecks."
        ], C_PRIMARY),
        ("Simulation Agent", "ACT PHASE", [
            "Tool: Passenger Load Sim",
            "Simulates real-world ridership with stochastic variance.",
            "Calculates exact load % per bus (Capacity: 60).",
            "Flags LOAD FAIL and WAIT FAIL violations."
        ], C_NAVY),
        ("Operations Manager", "REFLECT PHASE", [
            "Tool: Memory Ledger Writer",
            "Reviews simulation defects across all bands.",
            "Increments frequency where fleet capacity allows.",
            "Cites Section 1.1, 2.1, 3.1 & writes to shared memory."
        ], C_GREEN)
    ]
    for i, ag in enumerate(agents_s4):
        x = Inches(0.8) + i * Inches(2.4)
        add_card(s4, x, Inches(1.6), col_w, col_h, ag[0], ag[1], ag[2], header_color=ag[3])

    # ==========================================
    # SLIDE 5: System Workflow & Lifecycle
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "Plan-Act-Reflect Loop Workflow & Execution Lifecycle")

    steps_s5 = [
        ("Step 1: Ingest Ridership", "Demand Analyst extracts hourly passenger counts from ridership_data.json and tags peak/off-peak windows."),
        ("Step 2: Retrieve Standards", "Service Standards Agent executes RAG over service_standards.txt to extract governing policies for each time band."),
        ("Step 3: Initial Timetable", "Timetable Planner sets bus allocation within hard route fleet limits (R1: 5, R2: 4, R3: 3 buses)."),
        ("Step 4: Synthetic Simulation", "Simulation Agent runs virtual passenger loading, calculating load percentages and headway waiting times."),
        ("Step 5: Operational Reflection", "Operations Manager reviews defects, implements +1 bus revisions within fleet limits, and writes audit report to memory.")
    ]
    for i, st in enumerate(steps_s5):
        y = Inches(1.6) + i * Inches(1.05)
        step_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(0.9))
        step_box.fill.solid()
        step_box.fill.fore_color.rgb = C_CARD_BG
        step_box.line.color.rgb = C_PRIMARY if i % 2 == 0 else C_ACCENT
        step_box.line.width = Pt(1.5)
        
        tf = step_box.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = st[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_DARK
        
        p2 = tf.add_paragraph()
        p2.text = st[1]
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_MUTED

    # ==========================================
    # SLIDE 6: RAG-Based Standards Retrieval
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "Grounded RAG: Transport Service Standards Knowledge Base")

    c6_left = ("RAG Retrieval Mechanism", "Grounding Against Hallucinations", [
        "Knowledge Source: service_standards.txt (Municipal Transit Guidelines).",
        "Document Chunking: Splitting by regulatory sections (Load, Headway, Fleet, Revisions).",
        "Keyword Retrieval Engine: Computes query-to-chunk token overlap without complex vector DBs.",
        "Precision Grounding: Guarantees that agent decisions cite verified transit regulations.",
        "Zero Parametric Hallucination: Bus capacities (60) and thresholds are hard-grounded."
    ])
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), c6_left[0], c6_left[1], c6_left[2])

    c6_right = ("Transit Standards Thresholds", "Core Service Rules Enforced", [
        "Section 1.1 (Load Standard):",
        "  • Peak Hours: Maximum load <= 80% capacity (48 pax/bus).",
        "  • Off-Peak Hours: Maximum load <= 90% capacity (54 pax/bus).",
        "Section 2.1 (Waiting Time Standard):",
        "  • Peak Hours: Max wait <= 10 min (Frequency >= 6/hr).",
        "  • Off-Peak Hours: Max wait <= 15 min (Frequency >= 4/hr).",
        "  • Late Evening: Max wait <= 20 min (Frequency >= 3/hr).",
        "Section 3.1 (Fleet Limit Rule):",
        "  • Total buses dispatched must never exceed route fleet ceiling.",
        "Section 5.1 (Special Event Standard):",
        "  • Governs 40-80% passenger demand spikes during festival operations."
    ])
    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), c6_right[0], c6_right[1], c6_right[2])

    # ==========================================
    # SLIDE 7: Shared Memory & Revision Ledger
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "Shared Timetable Memory & Multi-Round Revision Ledger")

    c7_1 = ("Timetable Memory Ledger", "memory/timetable_memory.json", [
        "Persistent JSON-based shared memory accessible by all agents.",
        "Stores complete historical trajectory of planning rounds.",
        "Tracks route ID, round number, violations detected, and revisions made.",
        "Maintains audit trail with natural language operations justifications."
    ])
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), c7_1[0], c7_1[1], c7_1[2])

    c7_2 = ("Sample Memory Entry Structure", "Structured Reflection Record", [
        "• route_id: 'R1' (City Center - Airport)",
        "• round: 1 | is_festival: false",
        "• violations_found: 10 (Load Failures + Wait Time Failures)",
        "• revisions_made: 5 frequency adjustments",
        "• changes: [",
        "    { band: '06:00-07:00', old: 3, new: 4, reason: 'Wait 20m > max 15m' },",
        "    { band: '10:00-11:00', old: 3, new: 4, reason: 'Wait 20m > max 15m' },",
        "    { band: '08:00-09:00', old: 5, new: 5, reason: 'Fleet limit (5) reached' }",
        "  ]",
        "• ops_report: 'Official Operations Report: Adjusted off-peak headways...'"
    ])
    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), c7_2[0], c7_2[1], c7_2[2])

    # ==========================================
    # SLIDE 8: Technology Stack & Transit Dataset
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "Technology Stack & Empirical Transit Dataset")

    c8_stack = ("Core Technology Stack", "Modular & Lightweight Architecture", [
        "Language & Framework: Python 3.8+ modular multi-agent structure.",
        "LLM Engine: Groq Cloud Inference API (Llama-3 / Qwen-3.8B model).",
        "Execution Speed: Ultra-fast LLM inference (<1.5s per turn).",
        "RAG Architecture: Deterministic TF-IDF keyword overlap chunking.",
        "Simulation Engine: Pure Python discrete-time passenger queue model.",
        "Version Control: Git & GitHub public repository."
    ])
    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), c8_stack[0], c8_stack[1], c8_stack[2])

    c8_data = ("3 Urban Route Evaluation Dataset", "data/ridership_data.json", [
        "Route R1: City Center - Airport",
        "  • Fleet Cap: 5 buses | Peak Demand: 450 pax/hr (08:00-09:00)",
        "  • Profile: Heavy commuter traffic with extreme morning/evening peaks.",
        "Route R2: North Station - South Mall",
        "  • Fleet Cap: 4 buses | Peak Demand: 400 pax/hr (08:00-09:00)",
        "  • Profile: Mixed commercial/retail corridor with steady midday load.",
        "Route R3: University - Tech Park",
        "  • Fleet Cap: 3 buses | Peak Demand: 320 pax/hr (17:00-18:00)",
        "  • Profile: Student/tech corridor with extended evening rush."
    ])
    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), c8_data[0], c8_data[1], c8_data[2])

    # ==========================================
    # SLIDE 9: Testing, Evaluation & Results
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "Experimental Results: 3 Routes × 2 Rounds & Festival Day")

    # Results Table
    table_s9 = s9.shapes.add_table(7, 6, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.2))
    table_s9.table.columns[0].width = Inches(2.5)
    table_s9.table.columns[1].width = Inches(1.5)
    table_s9.table.columns[2].width = Inches(1.8)
    table_s9.table.columns[3].width = Inches(1.8)
    table_s9.table.columns[4].width = Inches(2.2)
    table_s9.table.columns[5].width = Inches(1.9)

    headers_t = ["Route & Test Scenario", "Fleet Limit", "Initial Violations", "Revisions Made", "Bottleneck Alleviation", "Fleet Compliance"]
    for j, h in enumerate(headers_t):
        cell = table_s9.table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_TEXT_LIGHT

    rows_data = [
        ("R1: City Center - Airport (R1)", "5 buses", "10 bands", "5 revisions", "Resolved (off-peak)", "PASS (<= 5 buses)"),
        ("R2: North Station - South Mall (R1)", "4 buses", "13 bands", "8 revisions", "Resolved (headways)", "PASS (<= 4 buses)"),
        ("R3: University - Tech Park (R1)", "3 buses", "15 bands", "2 revisions", "Resolved (boundary)", "PASS (<= 3 buses)"),
        ("R1: Airport (Round 2 Surge)", "5 buses", "10 bands", "5 revisions", "Peak load flagged", "PASS (Fleet Bound)"),
        ("R2: South Mall (Round 2 Surge)", "4 buses", "13 bands", "8 revisions", "Headways improved", "PASS (Fleet Bound)"),
        ("R1: Festival-Day Add-on (+65%)", "5 buses", "12 bands", "5 revisions", "Max Capacity Deployed", "PASS (Emergency Alert)")
    ]
    for i, r in enumerate(rows_data):
        for j, val in enumerate(r):
            cell = table_s9.table.cell(i+1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if i % 2 == 0 else C_CARD_BG
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = C_TEXT_DARK

    # Summary callout
    callout = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8))
    callout.fill.solid()
    callout.fill.fore_color.rgb = RGBColor(239, 246, 255)
    callout.line.color.rgb = C_PRIMARY
    callout.line.width = Pt(1.5)
    tf_co = callout.text_frame
    tf_co.margin_left = tf_co.margin_top = Inches(0.2)
    p = tf_co.paragraphs[0]
    p.text = "KEY EVALUATION FINDINGS & OUTCOMES:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    findings = [
        "1. Overcrowding Mitigation: Operations Manager successfully resolved waiting-time and off-peak load violations across all routes.",
        "2. Strict Fleet Boundary Enforcement: No route ever exceeded its operational depot fleet limit (100% boundary compliance).",
        "3. Festival-Day Responsiveness: System adapted to +65% surges by deploying maximum available fleet and citing Section 5.1 rules."
    ]
    for f in findings:
        pf = tf_co.add_paragraph()
        pf.text = f
        pf.font.size = Pt(9.5)
        pf.font.color.rgb = C_TEXT_DARK

    # ==========================================
    # SLIDE 10: Conclusion & Future Scope
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "Conclusion & Future Research Directions")

    c10_1 = ("Demonstrated Achievements", "CSE476 CO3 & CO4 Fulfilled", [
        "• Full Plan-Act-Reflect Loop implementation coordinating 5 specialized agents.",
        "• Grounded RAG integration preventing hallucinated scheduling decisions.",
        "• Shared Timetable Memory enabling multi-round reflection and auditability.",
        "• 100% fleet limit compliance across normal, round 2, and festival stress tests.",
        "• Production-ready modular architecture deployed on GitHub."
    ])
    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), c10_1[0], c10_1[1], c10_1[2], header_color=C_GREEN)

    c10_2 = ("Future Enhancements", "Expanding Scalability & Real-Time Control", [
        "• Real-Time GPS Tracking: Integrating live vehicle telemetry for dynamic dispatching.",
        "• Inter-Route Fleet Balancing: Borrowing excess buses from quiet routes during spikes.",
        "• Dense Vector RAG: Upgrading to embedding-based retrieval (ChromaDB/FAISS).",
        "• Multi-Depot Operations: Optimizing deadheading and recharging for Electric Bus fleets.",
        "• Predictive Machine Learning: Deep learning passenger flow forecasting using weather/events."
    ])
    add_card(s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), c10_2[0], c10_2[1], c10_2[2], header_color=C_PRIMARY)

    # Save to PPT folder
    out_path1 = r"c:\Users\shiva\OneDrive\Desktop\citybus\PPT\Q16_K3E2327_MyakalaBikshapathi.pptx"
    out_path2 = r"c:\Users\shiva\OneDrive\Desktop\citybus\PPT\Q16_K3_MyakalaBikshapathi.pptx"
    prs.save(out_path1)
    prs.save(out_path2)
    print("PowerPoint presentation generated successfully!")

if __name__ == "__main__":
    build_ppt()
