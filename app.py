import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0ea5e9, #2563eb, #1e3a8a);
    color: white;
}
.card {
    background: rgba(255,255,255,0.2);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
h1, h2, h3, p {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌤️ Weather App")
st.write("Enter a city name to view current weather and visualizations 📊")

city = st.text_input("Enter city name:")
API_KEY = "0a0e189fdf6fb8620117fede7c709339"  
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

if city:
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("❌ City not found or API key issue!")
        st.write(data)
    else:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        condition = data["weather"][0]["description"].title()
        icon = data["weather"][0]["icon"]

        # --- Current Weather Card ---
        st.markdown(f"""
        <div class="card">
            <img src="https://openweathermap.org/img/wn/{icon}@2x.png" width="90">
            <h2>{city}</h2>
            <h1>{temp} °C</h1>
            <p>{condition}</p>
            <p>🔥 Feels Like: {feels_like} °C</p>
            <p>💧 Humidity: {humidity}%</p>
            <p>🌬️ Wind Speed: {wind_speed} m/s</p>
        </div>
        """, unsafe_allow_html=True)

        # --- Bar Chart: Temp vs Feels Like ---
        st.subheader("📊 Temperature vs Feels Like")
        fig, ax = plt.subplots()
        ax.bar(["Temperature", "Feels Like"], [temp, feels_like], color=["#fde047","#f97316"])
        ax.set_ylabel("°C")
        st.pyplot(fig)

        # --- Pie / Donut Chart: Humidity vs Remaining Air ---
        st.subheader("💧 Humidity vs Air Percentage")
        air = 100 - humidity
        fig, ax = plt.subplots()
        ax.pie([humidity, air], labels=["Humidity","Remaining Air"], autopct="%1.1f%%", startangle=90)
        centre_circle = plt.Circle((0,0),0.6,fc='white')
        fig.gca().add_artist(centre_circle)
        st.pyplot(fig)

        # --- Wind Speed Comparison ---
        st.subheader("🌬️ Wind Speed Comparison")
        avg_wind = 10  # Example average wind for comparison
        fig, ax = plt.subplots()
        ax.bar(["Current Wind", "Average Wind"], [wind_speed, avg_wind], color=["#22c55e","#38bdf8"])
        ax.set_ylabel("m/s")
        st.pyplot(fig)

        # --- Forecast: Next Hours Line Chart ---
        st.subheader("📈 Temperature Trend (Next Hours)")
        forecast = get_forecast(city)
        temps = []
        times = []
        for item in forecast["list"][:8]:  # Next 24 hours (3-hour intervals)
            temps.append(item["main"]["temp"])
            times.append(item["dt_txt"][11:16])
        fig, ax = plt.subplots()
        ax.plot(times, temps, marker='o', color="#fde047")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        st.pyplot(fig)

        # --- 5-Day Forecast Graph ---
        st.subheader("📅 5-Day Temperature Forecast")
        daily_temps = []
        days = []
        for i in range(0, 40, 8):  # Every 24 hours
            daily_temps.append(forecast["list"][i]["main"]["temp"])
            days.append(forecast["list"][i]["dt_txt"][:10])
        fig, ax = plt.subplots()
        ax.plot(days, daily_temps, marker='o', color="#f97316")
        ax.set_xlabel("Day")
        ax.set_ylabel("Temperature (°C)")
        st.pyplot(fig)
