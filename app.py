import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Weather App", page_icon="🌤️")

st.title("🌤️ Weather Visualization App")

API_KEY = "0a0e189fdf6fb8620117fede7c709339"

city = st.text_input("Enter city name:")

if city:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            st.error("❌ City not found or invalid API key")
            st.write(data)
        else:
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            st.success(f"Weather in {city}")
            st.write(f"🌡️ Temperature: {temp} °C")
            st.write(f"🔥 Feels Like: {feels_like} °C")
            st.write(f"💧 Humidity: {humidity}%")
            st.write(f"🌬️ Wind Speed: {wind_speed} m/s")

            # Bar Chart
            st.subheader("Temperature vs Feels Like")
            fig, ax = plt.subplots()
            ax.bar(["Temperature", "Feels Like"], [temp, feels_like])
            st.pyplot(fig)

            # Pie Chart
            st.subheader("Humidity vs Air")
            air = 100 - humidity
            fig, ax = plt.subplots()
            ax.pie([humidity, air], labels=["Humidity", "Air"], autopct="%1.1f%%")
            st.pyplot(fig)

    except Exception as e:
        st.error("⚠️ App crashed")
        st.write(e)
