from app.llm_client import call_llm


def route_query(question: str) -> dict:
    try:
        result = call_llm(question)

        tool = result.get("tool", "kpi_tool")
        store_id = int(result.get("store_id", 1))
        horizon = int(result.get("horizon", 6))

        if tool not in ["forecast_tool", "kpi_tool"]:
            tool = "kpi_tool"

        if store_id < 1:
            store_id = 1

        if horizon < 1:
            horizon = 6

        return {
            "tool": tool,
            "store_id": store_id,
            "horizon": horizon
        }
    except Exception:
        return{
            "tool": "kpi_tool",
            "store_id": 1,
            "horizon": 6
        }