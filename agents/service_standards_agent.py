"""
Agent 2: Service Standards Retrieval Agent
Runs RAG over the transport service standards document.
"""
from utils.rag import load_standards, retrieve
from utils.groq_client import ask_llm


# Load standards once at module level
STANDARDS_CHUNKS = load_standards("data/service_standards.txt")


def get_standards_for_band(band_type: str) -> str:
    """
    Tool: Retrieve relevant service standards for a given band type.
    Uses keyword-based RAG.
    """
    query = f"{band_type} hours maximum load waiting time frequency bus"
    relevant = retrieve(query, STANDARDS_CHUNKS, top_k=4)
    return relevant


def run(demand_data: dict) -> dict:
    """
    Service Standards Agent: For each time band, retrieves the
    applicable service standards using RAG.
    Returns standards context to be used by the Timetable Planner.
    """
    print(f"\n[Service Standards Agent] Retrieving standards for route: {demand_data['route_name']}")

    # Get unique band types in this route
    band_types = set(
        v["band_type"] for v in demand_data["demand_summary"].values()
    )

    standards_by_type = {}
    for band_type in band_types:
        standards_by_type[band_type] = get_standards_for_band(band_type)
        print(f"[Service Standards Agent] Retrieved standards for {band_type} bands.")

    # Ask LLM to summarise the key rules
    all_standards = "\n\n".join(standards_by_type.values())
    prompt = f"""
Based on these service standards:
{all_standards}

List the key rules (max load, waiting time, frequency) that apply to:
- Peak hours
- Off-peak hours
- Late-evening hours
Keep it brief and in bullet points.
"""
    rules_summary = ask_llm(prompt, system="You are a transport service standards expert.")
    print(f"[Service Standards Agent] Key Rules:\n{rules_summary}")

    return {
        "route_id": demand_data["route_id"],
        "route_name": demand_data["route_name"],
        "fleet_limit": demand_data["fleet_limit"],
        "demand_summary": demand_data["demand_summary"],
        "analyst_summary": demand_data["analyst_summary"],
        "standards_by_type": standards_by_type,
        "rules_summary": rules_summary
    }
