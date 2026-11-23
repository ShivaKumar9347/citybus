"""
Agent 3: Timetable Planner Agent
Sets bus frequency for each time band within the fleet limit.
"""
import math
from utils.groq_client import ask_llm

# Constants
BUS_CAPACITY = 60  # passengers per bus
PEAK_MAX_LOAD = 0.80       # 80% of capacity during peak
OFFPEAK_MAX_LOAD = 0.90    # 90% during off-peak
LATE_MAX_LOAD = 0.90       # 90% late evening


def calculate_required_buses(passengers: int, band_type: str) -> int:
    """Calculate how many buses are needed for a given ridership and band type."""
    if band_type == "peak":
        max_load = PEAK_MAX_LOAD
    else:
        max_load = OFFPEAK_MAX_LOAD
    max_passengers_per_bus = BUS_CAPACITY * max_load
    required = math.ceil(passengers / max_passengers_per_bus)
    return max(required, 2)  # minimum 2 buses per band


def run(standards_data: dict) -> dict:
    """
    Timetable Planner Agent: Creates initial timetable for a route.
    Caps buses at fleet_limit.
    """
    print(f"\n[Timetable Planner] Creating timetable for route: {standards_data['route_name']}")

    fleet_limit = standards_data["fleet_limit"]
    timetable = {}
    overcrowded_bands = []

    for band, info in standards_data["demand_summary"].items():
        passengers = info["passengers"]
        band_type = info["band_type"]
        required = calculate_required_buses(passengers, band_type)

        # Cap at fleet limit
        allocated = min(required, fleet_limit)
        is_overcrowded = required > fleet_limit

        timetable[band] = {
            "passengers": passengers,
            "band_type": band_type,
            "required_buses": required,
            "allocated_buses": allocated,
            "is_overcrowded": is_overcrowded,
            "frequency_per_hour": allocated
        }

        if is_overcrowded:
            overcrowded_bands.append(band)

    # Ask LLM to summarise the initial timetable plan
    timetable_text = "\n".join([
        f"  {band}: {v['allocated_buses']} buses "
        f"({'OVERCROWDED' if v['is_overcrowded'] else 'OK'})"
        for band, v in timetable.items()
    ])
    prompt = f"""
Route: {standards_data['route_name']}
Fleet limit: {fleet_limit} buses

Initial timetable allocation:
{timetable_text}

Overcrowded bands: {overcrowded_bands if overcrowded_bands else 'None'}

In 2-3 sentences, describe the initial timetable and flag any overcrowded time bands.
"""
    planner_note = ask_llm(prompt, system="You are a city bus timetable planner.")
    print(f"[Timetable Planner] Note: {planner_note}")

    return {
        "route_id": standards_data["route_id"],
        "route_name": standards_data["route_name"],
        "fleet_limit": fleet_limit,
        "initial_timetable": timetable,
        "overcrowded_bands": overcrowded_bands,
        "planner_note": planner_note,
        "rules_summary": standards_data["rules_summary"],
        "standards_by_type": standards_data["standards_by_type"]
    }
