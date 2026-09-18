import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import streamlit as st
import pandas as pd

from load.database import Database
from dashboard.queries import get_risk_data


# 1. PAGE CONFIGURATION

st.set_page_config(
    page_title="MeteoRisk",
    layout="wide"
)


# 2. DATABASE CONNECTION

database = Database()

data = get_risk_data(database.engine)

data["forecast_date"] = pd.to_datetime(
    data["forecast_date"]
)


# 3. HEADER

st.title(" MétéoRisk")

st.write(
    "Anticiper les perturbations logistiques liées "
    "aux conditions météorologiques au Maroc."
)

st.divider()


# 4. SIDEBAR FILTERS

st.sidebar.header("-- Filters")


# City filter

cities = ["All"] + sorted(
    data["city"].dropna().unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "City",
    cities
)


# Period filter

min_date = data["forecast_date"].min().date()
max_date = data["forecast_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Risk level filter

risk_levels = ["All"] + sorted(
    data["risk_level"].dropna().unique().tolist()
)

selected_risk = st.sidebar.selectbox(
    "Risk level",
    risk_levels
)


# 5. APPLY FILTERS

filtered_data = data.copy()


# City

if selected_city != "All":

    filtered_data = filtered_data[
        filtered_data["city"] == selected_city
    ]


# Period

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = pd.Timestamp(
        selected_dates[1]
    )

    filtered_data = filtered_data[
        (filtered_data["forecast_date"] >= start_date)
        &
        (filtered_data["forecast_date"] <= end_date)
    ]


# Risk level

if selected_risk != "All":

    filtered_data = filtered_data[
        filtered_data["risk_level"] == selected_risk
    ]


# 6. EMPTY DATA CHECK

if filtered_data.empty:

    st.warning(
        "No data matches the selected filters."
    )

    st.stop()


# 7. KPI SECTION

st.header("-- Overview")


col1, col2, col3, col4 = st.columns(4)


# Number of forecasts

with col1:

    st.metric(
        "Forecasts",
        len(filtered_data)
    )


# Average risk

with col2:

    average_risk = filtered_data["risk_score"].mean()

    st.metric(
        "Average Risk",
        f"{average_risk:.2f}"
    )


# Maximum risk

with col3:

    maximum_risk = filtered_data["risk_score"].max()

    st.metric(
        "Maximum Risk",
        f"{maximum_risk:.2f}"
    )


# High-risk periods

with col4:

    high_risk_count = (
        filtered_data["risk_level"]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
    )

    st.metric(
        "High Risk Periods",
        high_risk_count
    )


st.divider()




# 12. FORECAST DETAILS

st.header("-- Forecast Details")


display_data = filtered_data.copy()

display_data["forecast_date"] = (
    display_data["forecast_date"]
    .dt.date
)


# Select useful columns

display_data = display_data[
    [
        "city",
        "forecast_date",
        "temperature_max",
        "temperature_min",
        "precipitation_sum",
        "wind_speed_max",
        "temperature_category",
        "precipitation_category",
        "wind_category",
        "risk_score",
        "risk_level"
    ]
]


st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# 8. AVERAGE RISK BY CITY

st.header("-- Average Risk by City")

city_risk = (
    filtered_data
    .groupby("city")["risk_score"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

st.bar_chart(
    city_risk,
    x_label="City",
    y_label="Average Risk Score"
)




# 9. RISK EVOLUTION

st.header("-- Risk Evolution Over Time")

risk_by_date = (
    filtered_data
    .groupby("forecast_date")["risk_score"]
    .mean()
    .round(2)
)

st.line_chart(
    risk_by_date,
    x_label="Date",
    y_label="Average Risk Score"
)



# 10. RISK LEVEL DISTRIBUTION
st.header("-- Risk Level Distribution")

low_count = (
    filtered_data["risk_level"]
    .astype(str)
    .str.lower()
    .eq("low")
    .sum()
)

medium_count = (
    filtered_data["risk_level"]
    .astype(str)
    .str.lower()
    .eq("medium")
    .sum()
)

high_count = (
    filtered_data["risk_level"]
    .astype(str)
    .str.lower()
    .eq("high")
    .sum()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        " Low Risk",
        low_count
    )

with col2:
    st.metric(
        " Medium Risk",
        medium_count
    )

with col3:
    st.metric(
        " High Risk",
        high_count
    )


# 11. WEATHER FACTORS

st.header("-- Weather Factors")


# ------------------------------------------------------------
# Temperature
# ------------------------------------------------------------

st.subheader("🌡️ Temperature Evolution")

temperature_data = (
    filtered_data
    .groupby("forecast_date")[
        [
            "temperature_max",
            "temperature_min"
        ]
    ]
    .mean()
    .round(2)
)

st.line_chart(
    temperature_data,
    x_label="Date",
    y_label="Temperature (°C)"
)



# ------------------------------------------------------------
# Precipitation
# ------------------------------------------------------------

st.subheader("-- Precipitation")

precipitation_data = (
    filtered_data
    .groupby("forecast_date")[
        "precipitation_sum"
    ]
    .mean()
    .round(2)
)

st.bar_chart(
    precipitation_data,
    x_label="Date",
    y_label="Precipitation (mm)"
)




# ------------------------------------------------------------
# Wind
# ------------------------------------------------------------

st.subheader("-- Maximum Wind Speed")

wind_data = (
    filtered_data
    .groupby("forecast_date")[
        "wind_speed_max"
    ]
    .mean()
    .round(2)
)

st.line_chart(
    wind_data,
    x_label="Date",
    y_label="Wind Speed (km/h)"
)




st.divider()
