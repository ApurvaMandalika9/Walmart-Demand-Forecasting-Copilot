import re


def parse_store_id(text: str, default: int = 1) -> int:
    m = re.search(r"store\s*(\d+)", text.lower())
    return int(m.group(1)) if m else default


def parse_horizon_weeks(text: str, default: int = 6) -> int:
    m = re.search(r"next\s*(\d+)\s*weeks?", text.lower())
    return int(m.group(1)) if m else default


def route_query(text: str) -> str:
    t = text.lower()
    # Forecast intents
    if "forecast" in t or "predict" in t:
        return "forecast"

    # KPI intents
    if "kpi" in t or "average" in t or "avg" in t or "mean" in t or "summary" in t:
        return "kpi"

    return "unknown"