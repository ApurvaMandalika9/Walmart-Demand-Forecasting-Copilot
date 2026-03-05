import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

def train_model(df: pd.DataFrame, store_id: int):
    store_df = df[df["Store"] == store_id].copy().sort_values("Date")

    feature_cols = [
        "week",
        "month",
        "lag_1",
        "lag_2",
        "lag_4",
        "rolling_mean_4",
        "Temperature",
        "Fuel_Price",
        "CPI",
        "Unemployment",
        "Holiday_Flag",
    ]

    X = store_df[feature_cols]
    y = store_df["Weekly_Sales"]

    model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )
    model.fit(X, y)

    return model, feature_cols, store_df

def predict(model, X_test):

    preds = model.predict(X_test)

    return preds

def make_future_forecast(model, feature_cols, store_df: pd.DataFrame, horizon: int = 6):
    """
    Iteratively forecast next `horizon` weeks using last known row and rolling lags.
    """
    last = store_df.iloc[-1].copy()
    last_date = pd.to_datetime(last["Date"])

    preds = []
    history_sales = store_df["Weekly_Sales"].tolist()

    # For exogenous variables, keep last values constant (fast MVP)
    temp = float(last["Temperature"])
    fuel = float(last["Fuel_Price"])
    cpi = float(last["CPI"])
    unemp = float(last["Unemployment"])
    holiday = int(last["Holiday_Flag"])

    for i in range(1, horizon + 1):
        future_date = last_date + pd.Timedelta(weeks=i)

        week = int(future_date.isocalendar().week)
        month = int(future_date.month)

        lag_1 = history_sales[-1]
        lag_2 = history_sales[-2]
        lag_4 = history_sales[-4]
        rolling_mean_4 = sum(history_sales[-4:]) / 4.0

        row = {
            "week": week,
            "month": month,
            "lag_1": lag_1,
            "lag_2": lag_2,
            "lag_4": lag_4,
            "rolling_mean_4": rolling_mean_4,
            "Temperature": temp,
            "Fuel_Price": fuel,
            "CPI": cpi,
            "Unemployment": unemp,
            "Holiday_Flag": holiday,
        }

        X_future = pd.DataFrame([row])[feature_cols]
        yhat = float(model.predict(X_future)[0])

        preds.append({"date": future_date.strftime("%Y-%m-%d"), "predicted_sales": yhat})

        history_sales.append(yhat)

    return pd.DataFrame(preds)