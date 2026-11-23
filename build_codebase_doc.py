import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_codebase_document():
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    C_NAVY = RGBColor(26, 54, 93)
    C_ORANGE = RGBColor(194, 65, 12)

    # Document Header
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_top = p_top.add_run("LOVELY PROFESSIONAL UNIVERSITY\nSCHOOL OF COMPUTER SCIENCE AND ENGINEERING")
    r_top.font.size = Pt(11)
    r_top.font.bold = True
    r_top.font.color.rgb = RGBColor(100, 116, 139)

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = title_p.add_run("CSE476: AGENTIC AI — PROJECT CODEBASE")
    run_t.font.size = Pt(18)
    run_t.font.bold = True
    run_t.font.color.rgb = C_NAVY

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Official Repository Verification & Source Code Document\n")
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True

    # Metadata Table
    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    metadata = [
        ("Project ID & Title", "Q16: CITY BUS TIMETABLE TUNING TEAM"),
        ("Student Name", "Myakala Bikshapathi"),
        ("Registration Number", "12323593"),
        ("Section", "K3E2327 (Group K3)"),
        ("Course & Faculty Supervisor", "CSE476 (Agentic AI) | Mr. Ravneet Singh (UID: 35120)"),
        ("Evaluation Target", "CO3 & CO4 (Bloom's Levels L4, L5, L6) — 30 Marks")
    ]

    for i, (k, v) in enumerate(metadata):
        row = table.rows[i]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.2)
        cell_v.width = Inches(4.3)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_before = Pt(4)
        pk.paragraph_format.space_after = Pt(4)
        rk = pk.add_run(k)
        rk.font.bold = True
        rk.font.size = Pt(10)
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_before = Pt(4)
        pv.paragraph_format.space_after = Pt(4)
        rv = pv.add_run(v)
        rv.font.size = Pt(10)
        
        shd_xml = f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'
        cell_k._tc.get_or_add_tcPr().append(parse_xml(shd_xml))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # GitHub Repository Highlight Box
    h_p = doc.add_paragraph()
    h_p.paragraph_format.space_before = Pt(10)
    h_p.paragraph_format.space_after = Pt(4)
    r_h = h_p.add_run("🔗 OFFICIAL GITHUB REPOSITORY LINK")
    r_h.font.size = Pt(13)
    r_h.font.bold = True
    r_h.font.color.rgb = C_ORANGE

    link_box = doc.add_table(rows=1, cols=1)
    link_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = link_box.rows[0].cells[0]
    c.width = Inches(6.5)
    shd_box = f'<w:shd {nsdecls("w")} w:fill="EFF6FF"/>'
    c._tc.get_or_add_tcPr().append(parse_xml(shd_box))
    
    cp = c.paragraphs[0]
    cp.paragraph_format.space_before = Pt(8)
    cp.paragraph_format.space_after = Pt(8)
    
    c_run = cp.add_run("https://github.com/ShivaKumar9347/citybus\n")
    c_run.font.bold = True
    c_run.font.size = Pt(13)
    c_run.font.color.rgb = RGBColor(37, 99, 235)
    
    info_run = cp.add_run(
        "• Repository Access: Public (Open Source)\n"
        "• Production Branch: master / main\n"
        "• Architecture: Plan-Act-Reflect Multi-Agent Coordination\n"
        "• Core Engine: Python 3.8+ | Groq Llama/Qwen Inference | RAG Knowledge Grounding"
    )
    info_run.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 1. Project Overview & Multi-Agent Architecture
    doc.add_heading("1. Multi-Agent Architecture Overview", level=2)
    doc.add_paragraph(
        "The City Bus Timetable Tuning Team (Q16) is an autonomous multi-agent system engineered to optimize "
        "urban bus transit frequencies. The system operates under a Plan-Act-Reflect loop architecture, executing "
        "collaborative task coordination across five specialized agents:"
    )

    agents_table = doc.add_table(rows=6, cols=3)
    agents_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Agent Name", "Loop Phase", "Core Functional Responsibility"]
    for j, h in enumerate(headers):
        cell = agents_table.rows[0].cells[j]
        p = cell.paragraphs[0]
        p.add_run(h).font.bold = True
        cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="E2E8F0"/>'))

    agent_data = [
        ("Demand Analyst Agent", "PLAN", "Ingests hourly passenger flow data via ridership tools, categorizing operational time bands (peak, off-peak, late-evening)."),
        ("Service Standards Agent", "PLAN (RAG)", "Executes grounded retrieval-augmented generation over transit regulatory standards (load factors, headway thresholds)."),
        ("Timetable Planner Agent", "ACT", "Calculates required bus frequency per time band, enforcing strict vehicle capping within fleet capacity."),
        ("Simulation Agent", "ACT", "Simulates real-world passenger loading, vehicle crowding %, and waiting headway to detect service violations."),
        ("Operations Manager Agent", "REFLECT", "Critiques simulation defects, dynamically re-plans frequencies, cites specific standard clauses, and records to memory.")
    ]

    for i, row_data in enumerate(agent_data):
        row = agents_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].paragraphs[0].add_run(val).font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 2. File and Directory Structure
    doc.add_heading("2. Repository Structure", level=2)
    code_structure = """citybus/
├── main.py                        # Central Orchestrator: Plan-Act-Reflect Loop execution across 3 routes
├── requirements.txt               # Dependencies: groq, python-dotenv, python-docx, python-pptx
├── .env                           # Environment configuration (GROQ_API_KEY)
├── .gitignore                     # Repository exclusions
├── agents/                        # Autonomous Agent Modules
│   ├── demand_analyst.py          # Agent 1: Demand classification and peak identification
│   ├── service_standards_agent.py # Agent 2: RAG retrieval over municipal transit guidelines
│   ├── timetable_planner.py       # Agent 3: Fleet-constrained bus frequency scheduling
│   ├── simulation_agent.py        # Agent 4: Passenger load and waiting-time simulation
│   └── operations_manager.py      # Agent 5: Reflection, revision, and regulatory citation
├── utils/                         # Core Utilities
│   ├── groq_client.py             # LLM Inference client (Llama/Qwen on Groq Cloud)
│   └── rag.py                     # Keyword-based RAG knowledge chunk retriever
├── data/                          # Ground Truth Datasets
│   ├── ridership_data.json        # 3 Urban Routes (R1, R2, R3) across 15 hourly bands
│   └── service_standards.txt      # Regulatory standards document (Load & Headway rules)
└── memory/                        # Cross-Agent Persistence
    └── timetable_memory.json      # Shared timetable revision memory ledger"""

    p_cs = doc.add_paragraph()
    r_cs = p_cs.add_run(code_structure)
    r_cs.font.name = "Consolas"
    r_cs.font.size = Pt(8.5)

    # 3. Setup and Execution
    doc.add_heading("3. Execution & Verification Guide", level=2)
    exec_text = """# Step 1: Clone the repository
git clone https://github.com/ShivaKumar9347/citybus.git
cd citybus

# Step 2: Set up environment and install dependencies
python -m venv venv
.\\venv\\Scripts\\activate
pip install -r requirements.txt

# Step 3: Configure API credentials in .env
GROQ_API_KEY=your_groq_api_key_here

# Step 4: Run Standard Multi-Agent Evaluation (3 Routes x 2 Planning Rounds)
python main.py

# Step 5: Run Group-of-3 Add-on (Festival-Day Demand Surge Scenario)
python main.py --festival"""

    p_ex = doc.add_paragraph()
    r_ex = p_ex.add_run(exec_text)
    r_ex.font.name = "Consolas"
    r_ex.font.size = Pt(8.5)

    paths = [
        r"c:\Users\shiva\OneDrive\Desktop\citybus\CodeBase\Q16_K3E2327_MyakalaBikshapathi.docx",
        r"c:\Users\shiva\OneDrive\Desktop\citybus\CodeBase\Q16_K3_MyakalaBikshapathi.docx"
    ]
    for p in paths:
        doc.save(p)
    print("CodeBase documents generated successfully!")

if __name__ == "__main__":
    create_codebase_document()
