"""
Agent 4: Simulation Agent
Runs a passenger-load simulation on the timetable and calculates
actual load and waiting time per time band.
"""
import math
import random
from utils.groq_client import ask_llm

BUS_CAPACITY = 60
MINUTES_IN_HOUR = 60


def simulate_band(passengers: int, buses: int, band_type: str) -> dict:
    """
    Tool: Simulate passenger load and waiting time for one time band.
    """
    # Add slight random variation (±5%) to simulate real-world conditions
    random.seed(passengers)  # Deterministic for reproducibility
    variation = random.uniform(-0.05, 0.05)
    simulated_passengers = int(passengers * (1 + variation))

    # Load per bus
    load_per_bus = simulated_passengers / buses if buses > 0 else simulated_passengers
    load_percentage = (load_per_bus / BUS_CAPACITY) * 100

    # Waiting time = minutes between buses
    waiting_time_minutes = MINUTES_IN_HOUR / buses if buses > 0 else 60

    # Standards thresholds
    if band_type == "peak":
        max_load_pct = 80
        max_wait = 10
    elif band_type == "late-evening":
        max_load_pct = 90
        max_wait = 20
    else:
        max_load_pct = 90
        max_wait = 15

    load_violation = load_percentage > max_load_pct
    wait_violation = waiting_time_minutes > max_wait

    return {
        "simulated_passengers": simulated_passengers,
        "load_per_bus": round(load_per_bus, 1),
        "load_percentage": round(load_percentage, 1),
        "waiting_time_minutes": round(waiting_time_minutes, 1),
        "load_violation": load_violation,
        "wait_violation": wait_violation,
        "max_load_pct": max_load_pct,
        "max_wait": max_wait
    }


def run(planner_data: dict) -> dict:
    """
    Simulation Agent: Simulates the initial timetable and reports results.
    """
    print(f"\n[Simulation Agent] Simulating timetable for route: {planner_data['route_name']}")

    simulation_results = {}
    violations = []

    for band, info in planner_data["initial_timetable"].items():
        result = simulate_band(
            passengers=info["passengers"],
            buses=info["allocated_buses"],
            band_type=info["band_type"]
        )
        simulation_results[band] = {**info, **result}

        if result["load_violation"] or result["wait_violation"]:
            violations.append({
                "band": band,
                "load_violation": result["load_violation"],
                "wait_violation": result["wait_violation"],
                "load_pct": result["load_percentage"],
                "wait_min": result["waiting_time_minutes"]
            })

    # Build a text summary for LLM
    sim_text = "\n".join([
        f"  {band}: {v['allocated_buses']} buses | "
        f"Load: {v['load_percentage']}% (max {v['max_load_pct']}%) | "
        f"Wait: {v['waiting_time_minutes']} min (max {v['max_wait']} min)"
        for band, v in simulation_results.items()
    ])

    prompt = f"""
Route: {planner_data['route_name']}
Simulation results:
{sim_text}

Violations found: {len(violations)} time bands.
Violation details: {violations}

In 3-4 sentences, summarise the simulation results, highlighting which bands 
failed the load or waiting-time standards.
"""
    sim_summary = ask_llm(prompt, system="You are a bus operations simulation analyst.")
    print(f"[Simulation Agent] Summary: {sim_summary}")

    return {
        "route_id": planner_data["route_id"],
        "route_name": planner_data["route_name"],
        "fleet_limit": planner_data["fleet_limit"],
        "initial_timetable": planner_data["initial_timetable"],
        "simulation_results": simulation_results,
        "violations": violations,
        "sim_summary": sim_summary,
        "overcrowded_bands": planner_data["overcrowded_bands"],
        "rules_summary": planner_data["rules_summary"],
        "standards_by_type": planner_data["standards_by_type"]
    }
