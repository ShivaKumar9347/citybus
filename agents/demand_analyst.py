"""
Agent 1: Demand Analyst Agent
Reads hourly ridership data and identifies demand patterns.
"""
import json
from utils.groq_client import ask_llm


def load_ridership(filepath: str = "data/ridership_data.json") -> dict:
    """Tool: Load ridership data from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def classify_time_band(hour_start: int) -> str:
    """Classify a time band as peak, off-peak, or late-evening."""
    if hour_start in [7, 8, 16, 17, 18]:
        return "peak"
    elif hour_start == 20:
        return "late-evening"
    else:
        return "off-peak"


def run(route: dict) -> dict:
    """
    Demand Analyst Agent: Analyses ridership for a single route.
    Returns a structured demand summary per time band.
    """
    print(f"\n[Demand Analyst] Analysing route: {route['route_name']}")

    ridership = route["hourly_ridership"]
    demand_summary = {}

    for band, passengers in ridership.items():
        hour_start = int(band.split(":")[0])
        band_type = classify_time_band(hour_start)
        demand_summary[band] = {
            "passengers": passengers,
            "band_type": band_type
        }

    # Ask LLM to summarise the demand pattern
    ridership_text = json.dumps(demand_summary, indent=2)
    prompt = f"""
You are analysing bus ridership for route: {route['route_name']}.
Here is the hourly ridership data:
{ridership_text}

In 3-4 sentences, summarise:
1. Which time bands have the highest demand.
2. The overall demand pattern (morning peak, evening peak, etc.).
3. Any time bands that might need special attention.
"""
    summary = ask_llm(prompt, system="You are a transport demand analyst.")
    print(f"[Demand Analyst] Summary: {summary}")

    return {
        "route_id": route["route_id"],
        "route_name": route["route_name"],
        "fleet_limit": route["fleet_limit"],
        "demand_summary": demand_summary,
        "analyst_summary": summary
    }
