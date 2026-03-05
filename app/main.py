from fastapi import FastAPI
from app.agent import route_query, parse_store_id, parse_horizon_weeks
from app.tools import forecast_tool, kpi_tool

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Walmart Sales Copilot API"}

@app.get("/query")
def query(question: str):
    route = route_query(question)

    if route == "forecast":
        store_id = parse_store_id(question, default=1)
        horizon = parse_horizon_weeks(question, default=6)
        result = forecast_tool(store_id=store_id, horizon=horizon)
        return {
            "answer": f"Forecast for store {store_id} for next {horizon} weeks",
            "tool_trace": [f"forecast_tool(store_id={store_id}, horizon={horizon})"],
            **result
        }

    if route == "kpi":
        store_id = parse_store_id(question, default=1)
        result = kpi_tool(store_id=store_id)
        return {
            "answer": f"KPIs for store {store_id}",
            "tool_trace": [f"kpi_tool(store_id={store_id})"],
            **result
        }

    return {"answer": "Try: 'forecast next 6 weeks for store 1' or 'kpi for store 1'."}

@app.get("/forecast")
def forecast(store_id: int = 1, horizon: int = 6):
    return forecast_tool(store_id=store_id, horizon=horizon)