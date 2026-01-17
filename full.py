import streamlit as st
import requests
import base64
import os

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="Weather App", layout="wide")
st.snow()

# -------------------------------------------------
# THEME & CSS
# -------------------------------------------------
st.markdown("""
<style>
.stApp { background-color: #dedbd2; }
html, body, [class*="css"] { color: #0a0908 !important; }
.weather-card {
    background: #c2c5aa;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}
.weather-card:hover { transform: translateY(-5px); }
.weather-icon { width: 90px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# WEATHER IMAGE MAPPING (SAME FOLDER)
# -------------------------------------------------
WEATHER_IMAGES = {
    "sunny": "sunny.jpg",
    "clear": "sunny.jpg",
    "partly cloudy": "partly_cloudy.jpg",
    "patchy cloud": "partly_cloudy.jpg",
    "cloudy": "cloudy.jpg",
    "overcast": "cloudy.jpg",
    "fog": "fog.jpg",
    "mist": "fog.jpg",
    "haze": "fog.jpg",
    "drizzle": "drizzle.jpg",
    "light rain": "drizzle.jpg",
    "patchy rain": "drizzle.jpg",
    "rain": "rain.jpg",
    "moderate rain": "rain.jpg",
    "heavy rain": "rain.jpg",
    "thunder": "thunder.jpg",
    "storm": "thunder.jpg",
    "snow": "snow.jpg",
    "blizzard": "snow.jpg",
    "ice": "ice.jpg",
    "freezing": "ice.jpg",
    "dust": "dust.jpg",
    "smoke": "dust.jpg",
    "sand": "dust.jpg"
}

def get_weather_image(condition):
    condition = condition.lower()
    for key, img in WEATHER_IMAGES.items():
        if key in condition:
            return img  # just filename, same folder
    return "default.jpg"

# -------------------------------------------------
# BACKGROUND IMAGE HELPER
# -------------------------------------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# APP TITLE
# -------------------------------------------------
st.markdown("<h1 style='text-align:center;'>🌤️ Weather Saarthi</h1>", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT CITY
# -------------------------------------------------
city = st.text_input("Enter a city name:", "Delhi")

if city:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url).json()
        current = data["current_condition"][0]

        temp_C = current["temp_C"]
        temp_F = current["temp_F"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]

        # Get weather image
        weather_img = get_weather_image(desc)
        set_bg(weather_img)

        st.markdown(f"<h2 style='text-align:center;'>Weather in {city}</h2>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="weather-card">
                <p>🌡 Temperature</p>
                <h3>{temp_C}°C / {temp_F}°F</h3>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="weather-card">
                <img src="data:image/jpg;base64,{base64.b64encode(open(weather_img,'rb').read()).decode()}"
                     class="weather-icon">
                <h3>{desc}</h3>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="weather-card">
                <p>💧 Humidity</p>
                <h3>{humidity}%</h3>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="weather-card">
                <p>🌬 Wind</p>
                <h3>{wind} km/h</h3>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to fetch weather data. {e}")





