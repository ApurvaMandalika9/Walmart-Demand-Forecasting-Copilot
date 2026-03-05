import pandas as pd

def load_data():

    df = pd.read_csv("data/walmart_sales.csv")

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

    df = df.sort_values(["Store","Date"])

    return df

def create_features(df):

    df["week"] = df["Date"].dt.isocalendar().week
    df["month"] = df["Date"].dt.month

    df["lag_1"] = df.groupby("Store")["Weekly_Sales"].shift(1)
    df["lag_2"] = df.groupby("Store")["Weekly_Sales"].shift(2)
    df["lag_4"] = df.groupby("Store")["Weekly_Sales"].shift(4)

    df["rolling_mean_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .shift(1)
        .rolling(4)
        .mean()
    )

    df = df.dropna()

    return df