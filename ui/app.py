import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Walmart Sales Copilot", layout="centered")
st.title("Walmart Sales Forecasting Copilot")

st.write("Type a question like: **forecast next 6 weeks for store 1** or **kpi for store 1**")

question = st.text_input("Your question", value="forecast next 6 weeks for store 1")

if st.button("Ask Copilot"):
    with st.spinner("Calling API..."):
        resp = requests.get(f"{API_URL}/query", params={"question": question}, timeout=120)

    if resp.status_code != 200:
        st.error(f"API Error {resp.status_code}: {resp.text}")
    else:
        data = resp.json()

        #st.subheader("Answer")
        #st.write(data.get("answer", ""))

        st.subheader("Tool Trace")
        st.code("\n".join(data.get("tool_trace", [])) or "No tools used")

        #st.subheader("Raw Response")
        #st.json(data)

        # If forecast exists, plot it
        if "forecast" in data and isinstance(data["forecast"], list) and len(data["forecast"]) > 0:
            st.subheader("Forecast Plot")

            df = pd.DataFrame(data["forecast"])
            # expecting columns: date, yhat
            if "date" in df.columns and "predicted_sales" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("date").set_index("date")
                st.line_chart(df["predicted_sales"])
            else:
                st.info("Forecast data returned but missing expected keys: 'date' and 'predicted_sales'.")

        # --- KPI UI ---
        if "kpis" in data and isinstance(data["kpis"], dict) and len(data["kpis"]) > 0:
            st.subheader("KPI Summary")

            kpis = data["kpis"]

            c1, c2, c3 = st.columns(3)
            c1.metric("Avg (last 8 weeks)", f"{kpis.get('avg_last_8_weeks', 0):,.0f}")
            c2.metric("Max (last 8 weeks)", f"{kpis.get('max_last_8_weeks', 0):,.0f}")
            c3.metric("Last week sales", f"{kpis.get('last_week_sales', 0):,.0f}")

            # Optional: bar chart of these KPIs
            #st.subheader("KPI Chart")
            #kpi_df = pd.DataFrame(
            #    {
            #        "metric": ["avg_last_8_weeks", "max_last_8_weeks", "last_week_sales"],
            #        "value": [
            #            kpis.get("avg_last_8_weeks", 0),
            #            kpis.get("max_last_8_weeks", 0),
            #            kpis.get("last_week_sales", 0),
            #       ],
            #    }
            #)
            #st.bar_chart(kpi_df.set_index("metric"))