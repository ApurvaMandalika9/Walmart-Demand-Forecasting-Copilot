from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent import route_query
from app.tools import forecast_tool, kpi_tool

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Walmart Sales Copilot API"}

@app.get("/query")
def query(question: str):
    route = route_query(question)

    tool = route["tool"]
    store_id = route["store_id"]
    horizon = route["horizon"]

    if tool == "forecast_tool":
        result = forecast_tool(store_id=store_id, horizon=horizon)
        return {
            "answer": f"Forecast for store {store_id} for next {horizon} weeks",
            "tool_trace": [f"forecast_tool(store_id={store_id}, horizon={horizon})"],
            "router": "gemini",
            **result
        }

    if tool == "kpi_tool":
        result = kpi_tool(store_id=store_id, horizon=horizon)
        return {
            "answer": f"KPIs for store {store_id} for next {horizon} weeks",
            "tool_trace": [f"kpi_tool(store_id={store_id}, horizon={horizon})"],
            "router": "gemini",
            **result
        }

    return {
        "answer": "I could not determine the correct tool for this query.",
        "router": "gemini"
    }

@app.get("/forecast")
def forecast(store_id: int = 1, horizon: int = 6):
    return forecast_tool(store_id=store_id, horizon=horizon)