import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Denver Weather", page_icon="🌤️", layout="wide")

# Disable fade/transition so charts don't blink between reruns
st.markdown("""
 <style>
 [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
 transition: none !important;
 opacity: 1 !important;
 }
 </style>
""", unsafe_allow_html=True)

st.title("🌤️ Live Weather Data Demo (Denver)")
st.caption("Real-time weather data from Open-Meteo API with auto-refresh.")

# Section 2: Config
lat, lon = 39.7392, -104.9903  # Denver
wurl = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"

# Sample fallback data
SAMPLE_WEATHER_DF = pd.DataFrame([{
    "time": pd.to_datetime("2024-01-01 12:00:00"),
    "temperature": 15.0,
    "wind": 10.0
}])

# Section 3: Fetch (Cached)
@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def get_weather():
    """Return (df, error_message). Never raise. Safe for beginners."""
    try:
        r = requests.get(wurl, timeout=10)
        r.raise_for_status()
        j = r.json()["current"]
        df = pd.DataFrame([{
            "time": pd.to_datetime(j["time"]),
            "temperature": j["temperature_2m"],
            "wind": j["wind_speed_10m"]
        }])
        return df, None
    except requests.RequestException as e:
        return None, f"Network/HTTP error: {e}"

# Section 4: Auto Refresh Controls
st.subheader("🔁 Auto Refresh Settings")
refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
auto_refresh = st.toggle("Enable auto-refresh", value=False)
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

# Section 5: Main View
st.subheader("Current Weather")
df, err = get_weather()
if err:
    st.warning(f"{err}\nShowing sample data so the demo continues.")
    df = SAMPLE_WEATHER_DF.copy()

st.dataframe(df, use_container_width=True)

# Use a line chart for temperature over time (more appropriate than bar chart)
fig = px.line(df, x="time", y="temperature", 
              title="Temperature (°C)",
              markers=True)
st.plotly_chart(fig, use_container_width=True)

# Optional: Add wind speed chart
fig2 = px.line(df, x="time", y="wind",
               title="Wind Speed (m/s)",
               markers=True,
               color_discrete_sequence=["green"])
st.plotly_chart(fig2, use_container_width=True)

# If auto-refresh is ON, wait and rerun the app
if auto_refresh:
    time.sleep(refresh_sec)
    get_weather.clear()
    st.rerun()