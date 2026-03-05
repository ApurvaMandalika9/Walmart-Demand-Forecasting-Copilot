import pandas as pd

df = pd.read_csv("data/walmart_sales.csv")

print(df.head())
print(df.columns)
print(df.describe())