import streamlit as st
import requests
import os
import base64

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="Weather App", layout="wide")
st.snow()

st.markdown(
    """
    <style>
    .stApp {
        background-color: #dedbd2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Global text color */
    html, body, [class*="css"] {
        color: #0a0908 !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0a0908 !important;
    }

    /* Paragraphs, labels, widgets */
    p, span, label, div {
        color: #0a0908 !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #0a0908 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# CSS Styling
# -------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #48cae4, #90e0ef);
}

h1, h2, h3 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #03045e;
}

div.stTextInput > label {
    font-weight: bold;
    color: #0077b6;
    font-size: 18px;
}

div.stTextInput > div > input {
    border-radius: 12px;
    padding: 10px;
    border: 2px solid #0077b6;
}

div.weather-card {
    background: #c2c5aa;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
    margin: 10px;
}

div.weather-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(0,0,0,0.25);
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: #03045e;
}

[data-testid="stMetricLabel"] {
    font-size: 18px;
    color: #0077b6;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Weather background helpers (LOCAL IMAGES)
# -------------------------------------------------
def get_weather_bg(condition):
    condition = condition.lower()
    base_path = "assets/weather"

    if any(word in condition for word in ["sunny", "clear"]):
        return os.path.join(base_path, "sunny.jpg")

    elif any(word in condition for word in ["partly cloudy", "patchy cloud"]):
        return os.path.join(base_path, "partly_cloudy.jpg")

    elif any(word in condition for word in ["cloudy", "overcast"]):
        return os.path.join(base_path, "cloudy.jpg")

    elif any(word in condition for word in ["fog", "mist", "haze"]):
        return os.path.join(base_path, "fog.jpg")

    elif any(word in condition for word in ["drizzle", "light rain", "patchy rain"]):
        return os.path.join(base_path, "drizzle.jpg")

    elif any(word in condition for word in ["rain", "heavy rain", "moderate rain"]):
        return os.path.join(base_path, "rain.jpg")

    elif any(word in condition for word in ["thunder", "storm"]):
        return os.path.join(base_path, "thunder.jpg")

    elif any(word in condition for word in ["snow", "blizzard"]):
        return os.path.join(base_path, "snow.jpg")

    elif any(word in condition for word in ["sleet", "ice", "freezing"]):
        return os.path.join(base_path, "ice.jpg")

    elif any(word in condition for word in ["dust", "smoke", "sand", "tornado", "squall"]):
        return os.path.join(base_path, "dust.jpg")

    else:
        return os.path.join(base_path, "default.jpg")


def set_bg_from_local(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# App title
# -------------------------------------------------
st.markdown("<h1 style='text-align: center;'>🌤️ Weather Saarthi</h1>", unsafe_allow_html=True)

# -------------------------------------------------
# Input city
# -------------------------------------------------
city = st.text_input("Enter a city name:", "Delhi")

if city:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_condition = data['current_condition'][0]

        temp_C = current_condition['temp_C']
        temp_F = current_condition['temp_F']
        weather_desc = current_condition['weatherDesc'][0]['value']
        humidity = current_condition['humidity']
        wind_kmph = current_condition['windspeedKmph']

        # 🔥 Set background dynamically
        bg_image = get_weather_bg(weather_desc)
        set_bg_from_local(bg_image)

        st.markdown(
            f"<h2 style='text-align:center; margin-top:20px;'>Weather in {city}</h2>",
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"<div class='weather-card'><p>Temperature</p><h3>{temp_C}°C / {temp_F}°F</h3></div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div class='weather-card'><p>Condition</p><h3>{weather_desc}</h3></div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='weather-card'><p>Humidity</p><h3>{humidity}%</h3></div>",
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"<div class='weather-card'><p>Wind Speed</p><h3>{wind_kmph} km/h</h3></div>",
                unsafe_allow_html=True
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Could not fetch weather data. Error: {e}")
    except KeyError:
        st.error("Unexpected response format from the weather API.")



