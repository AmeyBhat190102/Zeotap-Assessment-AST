import streamlit as st
from frontend.utils import get_city_weather_summary, get_alerts, set_thresholds

st.title("Real-Time Weather Monitoring System")

selected_city = st.sidebar.selectbox("Select a city", ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"])

threshold_temp = st.sidebar.slider("Set Temperature Alert Threshold (°C)", 0, 50, 35)

if st.sidebar.button("Set Alert Threshold"):
    set_thresholds(threshold_temp)
    st.sidebar.write(f"Threshold set at {threshold_temp}°C")

st.header(f"Weather Summary for {selected_city}")
summary = get_city_weather_summary(selected_city)

if summary:
    st.subheader(f"Temperature Data for {selected_city}")
    st.write(f"Average Temperature: {summary['avg_temp']:.2f} °C")
    st.write(f"Maximum Temperature: {summary['max_temp']:.2f} °C")
    st.write(f"Minimum Temperature: {summary['min_temp']:.2f} °C")
    st.write(f"Dominant Weather Condition: {summary['dominant_weather']}")

    st.subheader("Temperature Trends")
    st.line_chart([summary['avg_temp'], summary['max_temp'], summary['min_temp']])

    st.subheader("Alerts")
    alerts = get_alerts(selected_city)
    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.write("No alerts at the moment.")
else:
    st.write("No data available for the selected city.")
