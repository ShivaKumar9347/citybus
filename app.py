"""
City Bus Timetable Tuning Team - Interactive Web Application
Built with Streamlit & Multi-Agent Architecture (Plan-Act-Reflect Loop)
"""

import streamlit as st
import json
import os
import copy
import pandas as pd
import matplotlib.pyplot as plt

# Import agents
from agents import (
    demand_analyst,
    service_standards_agent,
    timetable_planner,
    simulation_agent,
    operations_manager
)

# Page configuration
st.set_page_config(
    page_title="City Bus Timetable Tuning Team",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 20px;
    }
    .agent-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0F172A;
        padding: 6px 12px;
        background-color: #F1F5F9;
        border-radius: 6px;
        border-left: 4px solid #2563EB;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .violation-tag {
        color: #DC2626;
        font-weight: 600;
    }
    .ok-tag {
        color: #16A34A;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def load_routes():
    with open("data/ridership_data.json", "r") as f:
        return json.load(f)["routes"]


def load_memory():
    if os.path.exists("memory/timetable_memory.json"):
        with open("memory/timetable_memory.json", "r") as f:
            return json.load(f)
    return []


def main():
    # Header Banner
    st.markdown('<p class="main-title">🚌 City Bus Timetable Tuning Team</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Autonomous Multi-Agent System for Dynamic Bus Frequency Optimization & Reflection | <b>Q16 • CO3 & CO4</b></p>',
        unsafe_allow_html=True
    )

    routes = load_routes()

    # Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Simulation Settings")
        
        # Route Selector
        route_options = {r["route_name"]: r for r in routes}
        selected_route_name = st.selectbox("Select Route:", list(route_options.keys()))
        selected_route = copy.deepcopy(route_options[selected_route_name])

        # Scenario Selector
        scenario = st.radio(
            "Operational Scenario:",
            [
                "Round 1: Normal Operations",
                "Round 2: Peak Surge Bottleneck (+40%)",
                "Festival Day: Severe Demand Surge (+65%)"
            ]
        )

        st.markdown("---")
        st.markdown("**Student Details:**")
        st.write("• **Name:** Myakala Bikshapathi")
        st.write("• **Reg No:** 12323593")
        st.write("• **Section:** K3E2327 (Group K3)")
        st.write("• **Course:** CSE476 (Agentic AI)")
        st.write("• **Supervisor:** Mr. Ravneet Singh")

        st.markdown("---")
        st.markdown("[🔗 GitHub Repository](https://github.com/ShivaKumar9347/citybus)")

    # Apply Scenario Ridership Modifications
    is_festival = False
    round_num = 1
    if "Round 2" in scenario:
        round_num = 2
        selected_route["hourly_ridership"]["08:00-09:00"] = int(selected_route["hourly_ridership"]["08:00-09:00"] * 1.4)
        selected_route["hourly_ridership"]["17:00-18:00"] = int(selected_route["hourly_ridership"]["17:00-18:00"] * 1.4)
        selected_route["route_name"] += " (Round 2 Surge)"
    elif "Festival Day" in scenario:
        is_festival = True
        round_num = 1
        for b in selected_route["hourly_ridership"]:
            selected_route["hourly_ridership"][b] = int(selected_route["hourly_ridership"][b] * 1.65)
        selected_route["route_name"] += " [FESTIVAL DAY]"

    # Top Key Metrics
    total_ridership = sum(selected_route["hourly_ridership"].values())
    peak_demand = max(selected_route["hourly_ridership"].values())
    peak_hour = max(selected_route["hourly_ridership"], key=selected_route["hourly_ridership"].get)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Selected Route", selected_route["route_id"], selected_route_name)
    m2.metric("Fleet Limit", f"{selected_route['fleet_limit']} buses/hr")
    m3.metric("Total Daily Demand", f"{total_ridership:,} pax")
    m4.metric("Peak Demand", f"{peak_demand} pax", f"at {peak_hour}")

    # Tabs for Workflow
    tab_run, tab_memory, tab_standards = st.tabs(["🚀 Multi-Agent Workflow", "🧠 Shared Memory Ledger", "📖 Transit Standards (RAG)"])

    with tab_run:
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            run_clicked = st.button("▶️ Execute Multi-Agent System", type="primary", use_container_width=True)
        with col_info:
            st.caption("Click to trigger the Plan-Act-Reflect multi-agent coordination loop for the selected route and scenario.")

        if run_clicked:
            with st.spinner("🤖 Coordinating Agents (Demand Analyst → Standards RAG → Timetable Planner → Simulator → Operations Manager)..."):
                # Phase 1: Demand Analyst
                demand_data = demand_analyst.run(selected_route)

                # Phase 2: Service Standards Agent (RAG)
                standards_data = service_standards_agent.run(demand_data)

                # Phase 3: Timetable Planner Agent
                planner_data = timetable_planner.run(standards_data)

                # Phase 4: Simulation Agent
                sim_data = simulation_agent.run(planner_data)

                # Phase 5: Operations Manager Agent
                final_data = operations_manager.run(sim_data, is_festival=is_festival)

                st.session_state["last_run"] = {
                    "demand": demand_data,
                    "standards": standards_data,
                    "planner": planner_data,
                    "sim": sim_data,
                    "final": final_data
                }

        if "last_run" in st.session_state:
            data = st.session_state["last_run"]

            # ----------------------------------------------------
            # 1. Demand Analyst Agent
            # ----------------------------------------------------
            st.markdown('<div class="agent-header">1. 📊 Demand Analyst Agent (PLAN Phase)</div>', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns([2, 3])
            with col_d1:
                st.write("**Ridership Distribution by Band Type:**")
                df_demand = pd.DataFrame([
                    {"Time Band": k, "Passengers": v["passengers"], "Type": v["band_type"].capitalize()}
                    for k, v in data["demand"]["demand_summary"].items()
                ])
                st.dataframe(df_demand, height=260, use_container_width=True)
            with col_d2:
                st.write("**Agent Demand Analysis (LLM Synthesis):**")
                st.info(data["demand"]["analyst_summary"])
                
                # Demand Bar Chart
                fig, ax = plt.subplots(figsize=(8, 2.8))
                ax.bar(df_demand["Time Band"], df_demand["Passengers"], color="#2563EB")
                ax.set_ylabel("Hourly Passengers")
                plt.xticks(rotation=45, ha='right', fontsize=8)
                plt.tight_layout()
                st.pyplot(fig)

            # ----------------------------------------------------
            # 2. Service Standards Retrieval Agent (RAG)
            # ----------------------------------------------------
            st.markdown('<div class="agent-header">2. 📜 Service Standards Retrieval Agent (PLAN Phase • Grounded RAG)</div>', unsafe_allow_html=True)
            col_s1, col_s2 = st.columns([1, 1])
            with col_s1:
                st.write("**Retrieved Governing Policies (RAG Chunks):**")
                with st.expander("View Peak Hours Standards Chunk", expanded=False):
                    st.text(data["standards"]["standards_by_type"].get("peak", "N/A"))
                with st.expander("View Off-Peak Hours Standards Chunk", expanded=False):
                    st.text(data["standards"]["standards_by_type"].get("off-peak", "N/A"))
                with st.expander("View Late-Evening Standards Chunk", expanded=False):
                    st.text(data["standards"]["standards_by_type"].get("late-evening", "N/A"))
            with col_s2:
                st.write("**Synthesized Service Rules:**")
                st.success(data["standards"]["rules_summary"])

            # ----------------------------------------------------
            # 3. Timetable Planner Agent
            # ----------------------------------------------------
            st.markdown('<div class="agent-header">3. 📋 Timetable Planner Agent (ACT Phase • Fleet Constrained)</div>', unsafe_allow_html=True)
            col_p1, col_p2 = st.columns([2, 3])
            with col_p1:
                df_plan = pd.DataFrame([
                    {
                        "Time Band": k,
                        "Required": v["required_buses"],
                        "Allocated": v["allocated_buses"],
                        "Status": "⚠️ Overcrowded (Fleet Capped)" if v["is_overcrowded"] else "✅ Feasible"
                    }
                    for k, v in data["planner"]["initial_timetable"].items()
                ])
                st.dataframe(df_plan, height=260, use_container_width=True)
            with col_p2:
                st.write("**Planner Assessment:**")
                st.info(data["planner"]["planner_note"])
                if data["planner"]["overcrowded_bands"]:
                    st.warning(f"🚨 Initial Overcrowded Bottlenecks: {', '.join(data['planner']['overcrowded_bands'])}")
                else:
                    st.success("All time bands satisfied within fleet limit.")

            # ----------------------------------------------------
            # 4. Simulation Agent
            # ----------------------------------------------------
            st.markdown('<div class="agent-header">4. 🧪 Simulation Agent (ACT Phase • Passenger Load Simulator)</div>', unsafe_allow_html=True)
            sim_rows = []
            for k, v in data["sim"]["simulation_results"].items():
                violations = []
                if v["load_violation"]: violations.append("LOAD FAIL")
                if v["wait_violation"]: violations.append("WAIT FAIL")
                status = ", ".join(violations) if violations else "OK"
                sim_rows.append({
                    "Time Band": k,
                    "Buses": v["allocated_buses"],
                    "Pax (Sim)": v["simulated_passengers"],
                    "Load %": f"{v['load_percentage']}%",
                    "Max Load": f"{v['max_load_pct']}%",
                    "Wait (min)": f"{v['waiting_time_minutes']}m",
                    "Max Wait": f"{v['max_wait']}m",
                    "Result": status
                })
            df_sim = pd.DataFrame(sim_rows)
            st.dataframe(df_sim, use_container_width=True)
            st.info(data["sim"]["sim_summary"])

            # ----------------------------------------------------
            # 5. Operations Manager Agent
            # ----------------------------------------------------
            st.markdown('<div class="agent-header">5. 👔 Operations Manager Agent (REFLECT Phase • Revisions & Audit)</div>', unsafe_allow_html=True)
            
            # Before vs After Table
            rev_rows = []
            for k, v in data["final"]["revised_timetable"].items():
                old_buses = data["planner"]["initial_timetable"][k]["allocated_buses"]
                new_buses = v["allocated_buses"]
                delta = f"{old_buses} ➔ {new_buses}" if v["changed"] else f"{old_buses} (Unchanged)"
                rev_rows.append({
                    "Time Band": k,
                    "Allocation": delta,
                    "Status": "↑ REVISED (+1 Bus)" if v["changed"] else "Maintained",
                    "Reason & Citation": v.get("reason", "Standard satisfied")
                })
            df_rev = pd.DataFrame(rev_rows)
            st.dataframe(df_rev, use_container_width=True)

            col_rep, col_chart = st.columns([1, 1])
            with col_rep:
                st.write("**Official Operations Report:**")
                st.success(data["final"]["ops_report"])
            with col_chart:
                st.write("**Frequency Comparison (Initial vs Revised):**")
                fig_comp, ax_comp = plt.subplots(figsize=(7, 3.2))
                bands = list(data["planner"]["initial_timetable"].keys())
                init_vals = [data["planner"]["initial_timetable"][b]["allocated_buses"] for b in bands]
                rev_vals = [data["final"]["revised_timetable"][b]["allocated_buses"] for b in bands]
                
                import numpy as np
                x = np.arange(len(bands))
                w = 0.35
                ax_comp.bar(x - w/2, init_vals, w, label="Initial Timetable", color="#94A3B8")
                ax_comp.bar(x + w/2, rev_vals, w, label="Revised Timetable", color="#2563EB")
                ax_comp.axhline(selected_route["fleet_limit"], color="red", linestyle="--", label=f"Fleet Limit ({selected_route['fleet_limit']})")
                ax_comp.set_ylabel("Buses / Hour")
                ax_comp.set_xticks(x)
                ax_comp.set_xticklabels(bands, rotation=45, ha='right', fontsize=7.5)
                ax_comp.legend(fontsize=8)
                plt.tight_layout()
                st.pyplot(fig_comp)

    # Tab 2: Shared Memory Ledger
    with tab_memory:
        st.subheader("🧠 Persistent Timetable Memory Ledger (`memory/timetable_memory.json`)")
        st.write("All autonomous revisions and operations reports are recorded in this shared memory file across planning rounds:")
        mem = load_memory()
        if mem:
            for idx, entry in enumerate(reversed(mem)):
                with st.expander(f"Session {len(mem) - idx}: Route {entry.get('route_name', '')} (Violations: {entry.get('violations_found', 0)}, Changes: {entry.get('changes_made', 0)})", expanded=(idx==0)):
                    st.json(entry)
        else:
            st.info("No recorded sessions in memory yet. Execute the system to generate entries.")

    # Tab 3: Transit Standards (RAG)
    with tab_standards:
        st.subheader("📖 Municipal Transit Service Standards (`data/service_standards.txt`)")
        st.write("This document is the Ground Truth knowledge source for the Service Standards Retrieval Agent (RAG):")
        with open("data/service_standards.txt", "r") as f:
            st.code(f.read(), language="markdown")


if __name__ == "__main__":
    main()
