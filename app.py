import sqlite3
import pandas as pd
import streamlit as st

st.title("Smart City Health Risk Dashboard")

@st.cache_data
def load_data():
    conn = sqlite3.connect("database/final.db")
    df = pd.read_sql("SELECT * FROM derived_data", conn)
    conn.close()
    return df

df = load_data()

st.write(df.head())

st.sidebar.header("Filters")

city = st.sidebar.selectbox(
    "Select City",
    df["city"].unique()
)

date = st.sidebar.selectbox(
    "Select Date",
    df[df["city"] == city]["date"].unique()
)

row = df[
    (df["city"] == city) &
    (df["date"] == date)
].iloc[0]

st.subheader(f"City: {city} | Date: {date}")

st.write("Vehicle Count:", row["vehicle_count"])
st.write("Average Speed:", row["avg_speed"])
st.write("Temperature:", row["temperature"])
st.write("AQI:", row["aqi"])
st.write("Health Risk Score:", row["health_risk_score"])
st.write("Risk Level:", row["risk_level"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("🚗 Vehicles", row["vehicle_count"])
c2.metric("⚡ Avg Speed", f"{row['avg_speed']} km/h")
c3.metric("🌫️ AQI", row["aqi"])
c4.metric("🏥 Respiratory Cases", row["respiratory_cases"])

st.subheader("Overall Health Risk")

if row["risk_level"] == "Low":
    st.success("🟢 LOW RISK")
elif row["risk_level"] == "Medium":
    st.warning("🟡 MEDIUM RISK")
else:
    st.error("🔴 HIGH RISK")

st.write("Risk Score:", row["health_risk_score"])

st.subheader("🚦 Traffic")
st.write("Congestion Level:", row["congestion_level"])

st.subheader("🌦️ Weather")
st.write("Temperature:", row["temperature"])
st.write("Heat Index:", row["heat_index"])
st.write("Humidity:", row["humidity"])
st.write("Rainfall:", row["rainfall"])

st.subheader("🏥 Health")
st.write("Respiratory Cases:", row["respiratory_cases"])
st.write("Heat-related Cases:", row["heat_related_cases"])

city_df = df[df["city"] == city]
st.line_chart(city_df.set_index("date")["health_risk_score"])

city_coords = {
    "Delhi": [28.61, 77.21],
    "Mumbai": [19.07, 72.87],
    "Bangalore": [12.97, 77.59]
}

map_df = pd.DataFrame({
    "lat": [city_coords[city][0]],
    "lon": [city_coords[city][1]]
})

st.subheader("📍 City Location")
st.map(map_df)
