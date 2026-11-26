# 🚌 City Bus Timetable Tuning Team

> **Q16 | Group 16 | CO3 & CO4 | Bloom's L4, L5, L6 | 30 Marks**

A multi-agent system that automates city bus timetable planning using a **Plan-Act-Reflect** loop architecture.

---

## 🎯 Objective

Design, build, and demonstrate a working prototype of a multi-agent system that:
- Automates bus frequency planning for city routes
- Applies a defined coordination architecture (Plan-Act-Reflect)
- Uses RAG (Retrieval-Augmented Generation) over service standards
- Revises timetables based on simulated passenger loads

---

## 🏗️ Architecture

```
Plan-Act-Reflect Loop
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  PLAN                                               │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │ Demand Analyst   │──▶│ Service Standards RAG  │  │
│  │ Agent            │   │ Agent                  │  │
│  └──────────────────┘   └────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  ACT                                                │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │ Timetable        │──▶│ Simulation Agent       │  │
│  │ Planner Agent    │   │ (Passenger Load Sim)   │  │
│  └──────────────────┘   └────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  REFLECT                                            │
│  ┌──────────────────────────────────────────────┐   │
│  │ Operations Manager Agent                     │   │
│  │ (Reviews, Revises, Writes to Memory)         │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🤖 Agents

| Agent | Role |
|-------|------|
| **Demand Analyst** | Reads hourly ridership data, classifies bands (peak/off-peak/late), summarises demand patterns |
| **Service Standards** | Runs keyword-based RAG over `service_standards.txt` to retrieve applicable rules |
| **Timetable Planner** | Calculates required buses per time band, caps at fleet limit, creates initial timetable |
| **Simulation Agent** | Simulates passenger load and waiting time, detects standard violations |
| **Operations Manager** | Reviews violations, revises timetable, cites standard clauses, saves to memory |

---

## 📁 Project Structure

```
citybus/
├── app.py                         # Interactive Web Dashboard (Streamlit GUI)
├── main.py                        # Terminal entry point - runs the full multi-agent system
├── requirements.txt               # Python dependencies
├── .env                           # API key (not committed to GitHub)
├── .gitignore
│
├── agents/
│   ├── demand_analyst.py          # Agent 1
│   ├── service_standards_agent.py # Agent 2 (RAG)
│   ├── timetable_planner.py       # Agent 3
│   ├── simulation_agent.py        # Agent 4
│   └── operations_manager.py      # Agent 5
│
├── utils/
│   ├── groq_client.py             # Groq LLM wrapper
│   └── rag.py                     # Keyword-based RAG retrieval
│
├── data/
│   ├── ridership_data.json        # Hourly ridership for 3 routes
│   └── service_standards.txt      # Service standards (RAG source)
│
└── memory/
    └── timetable_memory.json      # Shared memory across agents
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run — Interactive Web Interface (Streamlit GUI)
```bash
streamlit run app.py
```
> This opens a full web dashboard in your browser with interactive charts, route selectors, and real-time multi-agent workflow inspection.

### 4. Run — Terminal mode (3 routes, 2 planning rounds)
```bash
python main.py
```

### 5. Run — Festival day scenario (Terminal)
```bash
python main.py --festival
```

---

## 📊 Expected Output

### Normal Run
- **Initial timetable** per time band per route
- **Simulation results**: load %, waiting time, violations
- **Revised timetable** with reason and standard clause per change
- **Operations report** per route
- **Summary** of all 3 routes across 2 planning rounds

### Festival Run
- Same as above, but Route R1 gets a 65% ridership spike
- System re-plans and shows changes from normal timetable

---

## 📋 Service Standards (RAG Source)

| Rule | Peak | Off-Peak | Late Evening |
|------|------|----------|--------------|
| Max Load | 80% | 90% | 90% |
| Max Wait | 10 min | 15 min | 20 min |
| Min Frequency | 6/hr | 4/hr | 3/hr |

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq API (`llama3-8b-8192`) |
| RAG | Keyword-based retrieval (no vector DB) |
| Memory | JSON file (`timetable_memory.json`) |
| Language | Python 3.8+ |

---

## 📈 Evaluation Targets

- ✅ 3 routes over 2 planning rounds
- ✅ Each round has a known overcrowded time band
- ✅ Revised timetable removes overcrowding without exceeding fleet limit
- ✅ Festival day scenario (Group-of-3 add-on)

---

## 👥 Group Members

| Registration Number | Roll Number | Student Name |
|--------------------|-------------|--------------|
| | | |
| | | |
| | | |
