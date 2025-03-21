import requests
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# API Key (Replace with a secure method)
API_KEY = "7ad0fdea176e0fe925d29c4f40e68151"

# Streamlit App
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-image: url('https://source.unsplash.com/1600x900/?weather,sky');
            background-size: cover;
            color: white;
            text-align: center;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
        }
        .stApp {
            align-items: center;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-title'>🌦️ Weather Forecast Dashboard</div>", unsafe_allow_html=True)

# User Input for City Name
city = st.text_input("Enter City Name:", "New York")

# Fetch Weather Data
def fetch_weather(city):
    URL = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch Data
data = fetch_weather(city)

if data and "list" in data:
    # Extract Relevant Data
    df = pd.DataFrame(data["list"])
    df["date_time"] = pd.to_datetime(df["dt_txt"])
    df["temperature"] = df["main"].apply(lambda x: x["temp"])
    df["humidity"] = df["main"].apply(lambda x: x["humidity"])
    df["wind_speed"] = df["wind"].apply(lambda x: x["speed"])

    # Latest Weather Info
    st.subheader(f"📍 Current Weather in {city}")
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperature", f"{df['temperature'][0]} °C")
    col2.metric("💨 Wind Speed", f"{df['wind_speed'][0]} m/s")
    col3.metric("💧 Humidity", f"{df['humidity'][0]} %")

    # Temperature Line Chart
    st.subheader(f"📈 Temperature Trend in {city}")
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(x=df["date_time"], y=df["temperature"], marker="o", ax=ax)
    ax.set_xticks(df["date_time"][::8])  # Show fewer labels for readability
    ax.set_xticklabels(df["date_time"][::8].dt.strftime('%d %b, %H:%M'), rotation=30)
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title(f"Temperature Trend in {city}")
    st.pyplot(fig)

    # Humidity & Wind Speed Bar Chart
    st.subheader(f"💨 Humidity & Wind Speed in {city}")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(df["date_time"], df["humidity"], color="blue", label="Humidity (%)", width=0.5)
    ax.bar(df["date_time"], df["wind_speed"], color="red", alpha=0.7, label="Wind Speed (m/s)", width=0.5)
    ax.set_xticks(df["date_time"][::8])
    ax.set_xticklabels(df["date_time"][::8].dt.strftime('%d %b, %H:%M'), rotation=30)
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("Values")
    ax.set_title(f"Humidity & Wind Speed in {city}")
    ax.legend()
    st.pyplot(fig)
else:
    st.error("⚠️ City not found! Please enter a valid city name.")
