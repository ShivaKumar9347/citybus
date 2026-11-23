"""
City Bus Timetable Tuning Team
Multi-Agent System - Main Entry Point

Architecture: Plan-Act-Reflect Loop
Agents:
  1. Demand Analyst Agent
  2. Service Standards Retrieval Agent  (RAG)
  3. Timetable Planner Agent
  4. Simulation Agent
  5. Operations Manager Agent

Usage:
  python main.py              -> Normal run (3 routes, 2 planning rounds)
  python main.py --festival   -> Festival day scenario
"""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from agents import demand_analyst, service_standards_agent, timetable_planner, simulation_agent, operations_manager


# ─────────────────────────── helpers ────────────────────────────

def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_timetable(label: str, timetable: dict):
    print(f"\n--- {label} ---")
    print(f"{'Time Band':<20} {'Buses':>6} {'Type':<12} {'Note'}")
    print("-" * 60)
    for band, info in timetable.items():
        buses = info.get("allocated_buses", info.get("frequency_per_hour", "?"))
        band_type = info.get("band_type", "")
        note = ""
        if info.get("is_overcrowded"):
            note = "⚠ OVERCROWDED (fleet limit)"
        elif info.get("changed"):
            note = f"↑ REVISED — {info.get('reason', '')[:40]}"
        print(f"{band:<20} {buses:>6} {band_type:<12} {note}")


def print_simulation(sim_results: dict):
    print("\n--- Simulation Results ---")
    print(f"{'Time Band':<20} {'Buses':>6} {'Load%':>7} {'Wait(min)':>10} {'Status'}")
    print("-" * 65)
    for band, info in sim_results.items():
        status = []
        if info.get("load_violation"):
            status.append("LOAD FAIL")
        if info.get("wait_violation"):
            status.append("WAIT FAIL")
        status_str = ", ".join(status) if status else "OK"
        print(
            f"{band:<20} {info['allocated_buses']:>6} "
            f"{info['load_percentage']:>7.1f} {info['waiting_time_minutes']:>10.1f} "
            f"  {status_str}"
        )


def apply_festival_ridership(route: dict, spike_factor: float = 1.6) -> dict:
    """Multiply ridership by spike_factor to simulate festival demand."""
    import copy
    festival_route = copy.deepcopy(route)
    festival_route["route_name"] += " [FESTIVAL DAY]"
    for band in festival_route["hourly_ridership"]:
        festival_route["hourly_ridership"][band] = int(
            festival_route["hourly_ridership"][band] * spike_factor
        )
    return festival_route


# ─────────────────────────── plan-act-reflect loop ────────────────────────────

def run_planning_round(route: dict, round_num: int, is_festival: bool = False) -> dict:
    """
    Run one full plan-act-reflect cycle for a route.
    Returns the final result dict.
    """
    print_separator(f"ROUND {round_num} | Route: {route['route_name']}")

    # PLAN: Demand analysis
    demand_data = demand_analyst.run(route)

    # PLAN: Retrieve service standards (RAG)
    standards_data = service_standards_agent.run(demand_data)

    # ACT: Create timetable
    planner_data = timetable_planner.run(standards_data)

    # Print initial timetable
    print_timetable("Initial Timetable", planner_data["initial_timetable"])

    # ACT: Simulate
    sim_data = simulation_agent.run(planner_data)

    # Print simulation results
    print_simulation(sim_data["simulation_results"])

    # REFLECT: Operations Manager reviews and revises
    final_data = operations_manager.run(sim_data, is_festival=is_festival)

    # Print revised timetable
    print_timetable("Revised Timetable", final_data["revised_timetable"])

    print(f"\n[Operations Report]\n{final_data['ops_report']}")

    # Print changes with standard clauses
    if final_data["changes"]:
        print("\n--- Changes with Standard Clauses ---")
        for change in final_data["changes"]:
            if change["old_buses"] != change["new_buses"]:
                print(f"\n  Band: {change['band']}")
                print(f"  Change: {change['old_buses']} → {change['new_buses']} buses")
                print(f"  Reason: {change['reason']}")
                if change.get("standard_clause"):
                    print(f"  Standard: {change['standard_clause'][:200]}...")

    return final_data


# ─────────────────────────── main ────────────────────────────

def main():
    is_festival = "--festival" in sys.argv

    # Load routes
    with open("data/ridership_data.json", "r") as f:
        data = json.load(f)
    routes = data["routes"]

    # Reset memory for a clean run
    with open("memory/timetable_memory.json", "w") as f:
        json.dump([], f)

    print_separator("CITY BUS TIMETABLE TUNING TEAM")
    print("Multi-Agent System | Plan-Act-Reflect Architecture")
    if is_festival:
        print("🎉 FESTIVAL DAY MODE ACTIVE")

    all_results = []

    # Evaluation: 3 routes × 2 planning rounds
    for round_num in range(1, 3):   # Round 1 and Round 2
        print(f"\n{'#'*60}")
        print(f"PLANNING ROUND {round_num}")
        print(f"{'#'*60}")

        for route in routes:
            route_to_run = route

            # On Round 2, inject a known overcrowded band to test revision
            if round_num == 2:
                import copy
                route_to_run = copy.deepcopy(route)
                # Spike the morning peak to force overcrowding
                route_to_run["hourly_ridership"]["08:00-09:00"] = int(
                    route["hourly_ridership"]["08:00-09:00"] * 1.4
                )
                route_to_run["hourly_ridership"]["17:00-18:00"] = int(
                    route["hourly_ridership"]["17:00-18:00"] * 1.4
                )
                route_to_run["route_name"] = route["route_name"] + " (Round 2)"

            # Festival mode: spike the first route additionally
            if is_festival and route["route_id"] == "R1":
                route_to_run = apply_festival_ridership(route_to_run, spike_factor=1.65)

            result = run_planning_round(route_to_run, round_num, is_festival=is_festival)
            all_results.append(result)

    # ── Final Summary ──
    print_separator("FINAL SUMMARY")
    for res in all_results:
        changes_made = sum(1 for c in res["changes"] if c["old_buses"] != c["new_buses"])
        overcrowded_removed = sum(
            1 for band, info in res["revised_timetable"].items()
            if info.get("changed") and not info.get("is_overcrowded", False)
        )
        print(f"\nRoute: {res['route_name']}")
        print(f"  Fleet limit: {res['fleet_limit']} buses")
        print(f"  Violations found: {len(res.get('changes', []))}")
        print(f"  Revisions made:   {changes_made}")
        print(f"  Within fleet limit: YES" if changes_made <= res["fleet_limit"] else "  Within fleet limit: CHECK")

    print("\n✅ All planning rounds complete. Revisions saved to memory/timetable_memory.json")


if __name__ == "__main__":
    main()
