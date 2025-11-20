# Updated app.py with left-side menu (Streamlit)
# NOTE: This is a template. Replace placeholders with your existing logic.

import streamlit as st
from gtts import gTTS
import os

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Carbon Footprint AI", layout="wide")

# ---- DARK THEME STYLING ----
st.markdown(
    """
    <style>
        body { background-color: #0e1117; }
        .sidebar .sidebar-content {
            background-color: #111827 !important;
            padding-top: 30px;
        }
        .css-1d391kg, .css-1offfwp, .css-1lcbmhc {
            background-color: #111827 !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, span {
            color: #f3f4f6 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- LEFT MENU ----
menu = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "🧮 Carbon Calculator",
    "🎖 Achievements",
    "📊 Your Carbon Badge",
    "🎤 Voice Interaction",
    "ℹ About"
])

# ---- HOME PAGE ----
if menu == "🏠 Home":
    st.title("🌎 Premium Carbon Footprint AI")
    st.subheader("Dark • Modern • Smooth • Premium UI ✨")
    st.write("Welcome to your personalized sustainability dashboard.")

# ---- CARBON CALCULATOR ----
elif menu == "🧮 Carbon Calculator":
    st.title("Carbon Footprint Calculator")
    st.write("Answer questions to estimate your carbon output.")
    
    electricity = st.number_input("Monthly Electricity (kWh)", min_value=0)
    fuel = st.number_input("Monthly Fuel (litres)", min_value=0)
    food = st.selectbox("Diet Type", ["Vegetarian", "Mixed", "Non-Veg"])

    if st.button("Calculate"):
        score = electricity*0.5 + fuel*2
        if food == "Non-Veg": score += 50
        st.success(f"Your estimated carbon score is: {score}")

# ---- ACHIEVEMENTS ----
elif menu == "🎖 Achievements":
    st.title("🏆 Your Sustainability Achievements")
    st.write("Earn badges as you lower your carbon footprint.")

# ---- CARBON BADGE ----
elif menu == "📊 Your Carbon Badge":
    st.title("Your Personalized Carbon Rating Badge")
    st.write("Premium-style badge feature.")

# ---- VOICE INTERACTION ----
elif menu == "🎤 Voice Interaction":
    st.title("🎤 Voice Interaction (TTS Mode)")
    text = st.text_input("Enter text to speak:")
    if st.button("Speak"):
        tts = gTTS(text)
        tts.save("voice.mp3")
        audio_file = open("voice.mp3", "rb")
        st.audio(audio_file.read())

# ---- ABOUT ----
elif menu == "ℹ About":
    st.title("About This App")
    st.write("Created for KV Science Exhibition • Dark Premium UI Version")
