"""
Agent 5: Operations Manager Agent
Reviews simulation results and produces a revised timetable.
Writes changes to timetable memory.
"""
import json
import os
from utils.groq_client import ask_llm
from utils.rag import retrieve

MEMORY_FILE = "memory/timetable_memory.json"
BUS_CAPACITY = 60


def load_memory() -> list:
    """Load timetable revision memory."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_memory(memory: list):
    """Save timetable revision memory."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def get_standard_clause(violation_type: str, standards: dict) -> str:
    """RAG: Retrieve the specific standard clause for a violation type."""
    all_chunks = []
    for text in standards.values():
        all_chunks.extend([c.strip() for c in text.split("\n\n") if c.strip()])

    query = f"{violation_type} maximum load waiting time revision rule"
    return retrieve(query, all_chunks, top_k=2)


def revise_timetable(sim_data: dict) -> dict:
    """
    Revise the timetable based on simulation violations.
    Strategy: for each violating band, increase buses by 1 (if fleet allows).
    """
    revised = {}
    changes = []
    fleet_limit = sim_data["fleet_limit"]

    for band, info in sim_data["simulation_results"].items():
        current_buses = info["allocated_buses"]
        new_buses = current_buses

        reason = None
        clause = None

        if info["load_violation"] or info["wait_violation"]:
            # Try to add one more bus
            if current_buses < fleet_limit:
                new_buses = current_buses + 1

                # Find relevant standard clause
                vtype = "load" if info["load_violation"] else "waiting time"
                clause = get_standard_clause(vtype, sim_data["standards_by_type"])

                reason = []
                if info["load_violation"]:
                    reason.append(
                        f"Load {info['load_percentage']}% exceeded max {info['max_load_pct']}%"
                    )
                if info["wait_violation"]:
                    reason.append(
                        f"Wait {info['waiting_time_minutes']} min exceeded max {info['max_wait']} min"
                    )
                reason = "; ".join(reason)

                changes.append({
                    "band": band,
                    "old_buses": current_buses,
                    "new_buses": new_buses,
                    "reason": reason,
                    "standard_clause": clause
                })
            else:
                reason = f"Cannot add buses - fleet limit ({fleet_limit}) reached"
                changes.append({
                    "band": band,
                    "old_buses": current_buses,
                    "new_buses": new_buses,
                    "reason": reason,
                    "standard_clause": "Section 3.1: Fleet Limit Rule - cannot exceed fleet limit."
                })

        revised[band] = {
            "allocated_buses": new_buses,
            "passengers": info["passengers"],
            "band_type": info["band_type"],
            "changed": new_buses != current_buses,
            "reason": reason,
            "standard_clause": clause
        }

    return revised, changes


def run(sim_data: dict, is_festival: bool = False) -> dict:
    """
    Operations Manager: Reviews simulation and produces revised timetable.
    """
    print(f"\n[Operations Manager] Reviewing route: {sim_data['route_name']}")

    revised_timetable, changes = revise_timetable(sim_data)

    # Build a prompt for LLM to write the final operations report
    changes_text = "\n".join([
        f"  {c['band']}: {c['old_buses']} -> {c['new_buses']} buses | Reason: {c['reason']}"
        for c in changes
    ]) if changes else "  No changes needed."

    festival_note = " (FESTIVAL DAY - demand spike applied)" if is_festival else ""
    prompt = f"""
Route: {sim_data['route_name']}{festival_note}
Fleet limit: {sim_data['fleet_limit']}

Simulation found {len(sim_data['violations'])} violation(s).

Timetable revisions made:
{changes_text}

As Operations Manager, write a brief official revision report (4-6 sentences) covering:
1. What violations were found.
2. What changes were made and why.
3. Whether the fleet limit was a constraint.
4. The standard clause that justifies each change.
"""
    ops_report = ask_llm(prompt, system="You are a city bus Operations Manager writing an official report.")
    print(f"[Operations Manager] Report:\n{ops_report}")

    # Save to memory
    memory = load_memory()
    memory.append({
        "route_id": sim_data["route_id"],
        "route_name": sim_data["route_name"],
        "is_festival": is_festival,
        "violations_found": len(sim_data["violations"]),
        "changes_made": len([c for c in changes if c["old_buses"] != c["new_buses"]]),
        "changes": changes,
        "ops_report": ops_report
    })
    save_memory(memory)
    print(f"[Operations Manager] Revision saved to memory.")

    return {
        "route_id": sim_data["route_id"],
        "route_name": sim_data["route_name"],
        "fleet_limit": sim_data["fleet_limit"],
        "initial_timetable": sim_data["initial_timetable"],
        "simulation_results": sim_data["simulation_results"],
        "revised_timetable": revised_timetable,
        "changes": changes,
        "ops_report": ops_report,
        "is_festival": is_festival
    }
