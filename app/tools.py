import pandas as pd
from app.features import load_data, create_features
from app.forecasting import train_model, make_future_forecast

def forecast_tool(store_id: int, horizon: int = 6):
    df = load_data()
    df = create_features(df)

    # Train model on selected store (fast + simple for MVP)
    model, feature_cols, store_df = train_model(df, store_id=store_id)

    forecast_df = make_future_forecast(model, feature_cols, store_df, horizon=horizon)

    return {
        "store_id": store_id,
        "horizon_weeks": horizon,
        "forecast": forecast_df.to_dict(orient="records"),
    }


def kpi_tool(store_id: int, horizon: int = 6):
    df = load_data()
    df = create_features(df)
    store_df = df[df["Store"] == store_id].sort_values("Date")

    last_n = store_df.tail(horizon)

    if len(last_n) == 0:
        return {"store_id": store_id, "kpis": {}, "warning": "No data found for that store_id."}
    
    avg_sales = float(last_n["Weekly_Sales"].mean())
    max_sales = float(last_n["Weekly_Sales"].max())
    last_week = float(last_n["Weekly_Sales"].iloc[-1])

    return {
        "store_id": store_id,
        "horizon_weeks": horizon,
        "kpis": {
            "avg": avg_sales,
            "max": max_sales,
            "last_week_sales": last_week,
        }
    }