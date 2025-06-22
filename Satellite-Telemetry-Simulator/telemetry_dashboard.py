import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Timestamp", "Battery_Level", "Temperature",
                                                   "Signal_Strength", "Altitude", "Solar_Output"])
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

# Sidebar - Configuration
st.sidebar.title("⚙️ Simulation Controls")
refresh_rate = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 2)
max_rows = st.sidebar.slider("Max rows to display", 10, 100, 50)

# Generate telemetry data
def generate_data():
    timestamp = datetime.now().strftime("%H:%M:%S")
    battery = np.clip(100 - len(st.session_state.data) * 0.1 + np.random.uniform(-1, 1), 0, 100)
    temp = np.random.uniform(25, 75)
    signal = np.random.randint(1, 6)
    altitude = np.random.uniform(300, 1000)
    solar = np.random.uniform(100, 900)
    return {
        "Timestamp": timestamp,
        "Battery_Level": battery,
        "Temperature": temp,
        "Signal_Strength": signal,
        "Altitude": altitude,
        "Solar_Output": solar
    }

# Add new telemetry row
new_row = generate_data()
st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
if len(st.session_state.data) > max_rows:
    st.session_state.data = st.session_state.data.iloc[-max_rows:]

# Layout
st.title("🛰️ Satellite Telemetry Dashboard")

# 🔁 Fullscreen toggle
if st.session_state.fullscreen:
    if st.button("🔙 Back to Dashboard"):
        st.session_state.fullscreen = False

    st.subheader("📈 Fullscreen Charts")
    st.line_chart(st.session_state.data.set_index("Timestamp")[[
        "Battery_Level", "Temperature", "Signal_Strength", "Altitude", "Solar_Output"
    ]])

else:
    if st.button("🖥️ View Fullscreen Charts"):
        st.session_state.fullscreen = True

    # Dashboard layout
    st.markdown("Real-time simulation of telemetry metrics.")

    # Metrics
    st.subheader("📊 Live Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("🔋 Battery (%)", f"{new_row['Battery_Level']:.2f}")
    col2.metric("🌡️ Temp (°C)", f"{new_row['Temperature']:.2f}")
    col3.metric("📡 Signal (bars)", int(new_row["Signal_Strength"]))

    col4, col5 = st.columns(2)
    col4.metric("🛰️ Altitude (km)", f"{new_row['Altitude']:.2f}")
    col5.metric("🔆 Solar Output (W)", f"{new_row['Solar_Output']:.2f}")

    # Alerts
    st.subheader("⚠️ Alerts")
    if new_row["Battery_Level"] < 20:
        st.error(f"Low Battery Warning: {new_row['Battery_Level']:.2f}%")
    if new_row["Temperature"] > 70:
        st.warning(f"High Temperature Alert: {new_row['Temperature']:.2f}°C")
    if new_row["Signal_Strength"] <= 1:
        st.info("Signal Strength is critically low")

    # Charts
    st.subheader("📈 Telemetry Charts")
    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.line_chart(st.session_state.data.set_index("Timestamp")[["Battery_Level", "Temperature"]])
    with chart_cols[1]:
        st.line_chart(st.session_state.data.set_index("Timestamp")[["Solar_Output", "Signal_Strength", "Altitude"]])

# Auto-refresh pause
time.sleep(refresh_rate)

# Data Export Section
st.subheader("📁 Export Telemetry Data")
csv = st.session_state.data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download as CSV",
    data=csv,
    file_name="telemetry_data.csv",
    mime="text/csv"
)
