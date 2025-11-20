# ✅ Fully Streamlit-Cloud Compatible Premium App (Voice Output Only)
# — No PyAudio, No soundfile, No WebRTC Mic —
# — Retains Premium Dark UI, Achievements, Badges, AI Energy Assistant —

import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
from gtts import gTTS
from io import BytesIO
import base64

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Carbon Footprint & Green Energy AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# DARK PREMIUM UI + MODERN NAVBAR
# -------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp { background-color: #0c0c0c !important; }
        body, label, p, span, div { color: white !important; }
        h1, h2, h3, h4 { color: white !important; font-weight: 700; }

        /* NAVBAR */
        .cool-navbar {
            background: linear-gradient(90deg, #000000, #111111, #000000);
            border-radius: 16px;
            padding: 12px;
            margin-bottom: 30px;
            display: flex;
            justify-content: center;
            gap: 25px;
            box-shadow: 0 0 25px rgba(0,255,140,0.15);
        }
        .nav-button {
            background-color: #1a1a1a;
            padding: 10px 26px;
            border-radius: 12px;
            color: #e8ffe8 !important;
            font-size: 17px;
            font-weight: 600;
            border: 1px solid #00c85333;
            transition: 0.25s;
        }
        .nav-button:hover {
            background-color: #00c85355 !important;
            border-color: #00c853;
            transform: translateY(-3px);
            box-shadow: 0 0 12px #00c853aa;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# GEMINI CONFIG
# -------------------------------------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# -------------------------------------------------------
# ★ FUNCTION: TEXT → SPEECH (WORKS ON STREAMLIT CLOUD) ★
# -------------------------------------------------------
def speak(text):
    tts = gTTS(text)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    st.audio(audio_bytes.read(), format="audio/mp3")

# -------------------------------------------------------
# BADGES + ACHIEVEMENTS
# -------------------------------------------------------
def carbon_badge(score):
    if score < 8:
        return "🟢 **Low Carbon Footprint – Eco Champion!**"
    elif score < 15:
        return "🟡 **Moderate Footprint – Room for Improvement.**"
    else:
        return "🔴 **High Footprint – Needs Action Immediately.**"

def achievements(score):
    ach = []
    if score < 6: ach.append("🌟 Eco-Starter Award")
    if score < 10: ach.append("💚 Green Lifestyle Badge")
    if score < 14: ach.append("🔥 Carbon Reducer Badge")
    if score >= 14: ach.append("⚠️ High Emission Alert Badge")
    return ach

# -------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

st.markdown('<div class="cool-navbar">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
if col1.button("🏠 Home"): st.session_state["page"] = "Home"
if col2.button("🌍 Carbon Calculator"): st.session_state["page"] = "Carbon"
if col3.button("⚡ Green Energy AI"): st.session_state["page"] = "AI"
st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state["page"]

# -------------------------------------------------------
# PAGE: HOME — SUPER PREMIUM UI
# -------------------------------------------------------
if page == "Home":
    st.title("🌱 Carbon Footprint Analyzer & Green Energy Assistant")
    st.subheader("Premium Science Exhibition Model (With AI & TTS)")

    st.markdown(
        """
        ### ✨ Features
        - 🌍 **Full Carbon Footprint Calculator**
        - 🏅 **Eco Badge Rating System**
        - 🏆 **Achievements Based on Your Score**
        - 📊 **Beautiful Pie Chart Emission Visualization**
        - 🤖 **AI Assistant for Green Energy & Sustainability**
        - 🔊 **Text-to-Speech Voice Output (Cloud Compatible)**
        - 🎨 **Premium Dark Mode UI with Glowing Navbar**
        """
    )

# -------------------------------------------------------
# PAGE: CARBON FOOTPRINT CALCULATOR
# -------------------------------------------------------
elif page == "Carbon":
    st.title("🌍 Complete Carbon Footprint Calculator")

    # Transport
    st.header("🚗 Transportation")
    km_daily = st.slider("Daily Distance (km)", 0, 200, 10)
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
    factor = {"Petrol": 0.118, "Diesel": 0.134, "Electric": 0.02}
    transport_em = km_daily * factor[fuel]

    # Electricity
    st.header("💡 Electricity Usage")
    units = st.number_input("Monthly Units (kWh)", 0, 2000, 150)
    electricity_em = units * 0.82 / 30

    # LPG
    st.header("🔥 LPG")
    lpg = st.slider("Cylinders per year", 0, 24, 6)
    lpg_em = (lpg * 42.5) / 365

    # AC
    st.header("❄ Air Conditioner")
    ac_hr = st.slider("Daily AC Hours", 0, 24, 4)
    ac_em = ac_hr * 1.5 * 0.82

    # Geyser
    st.header("🚿 Geyser")
    gey = st.slider("Daily usage (hrs)", 0.0, 5.0, 0.5)
    gey_em = gey * 2 * 0.82

    # Waste
    st.header("🗑 Waste Generation")
    waste = st.slider("Daily waste (kg)", 0.0, 5.0, 0.5)
    waste_em = waste * 0.09

    # Food
    st.header("🍽 Diet")
    food = st.selectbox("Diet Type", ["Vegetarian", "Eggs", "Chicken", "Fish", "Mixed Non-Veg"])
    food_map = {"Vegetarian": 2, "Eggs": 3, "Chicken": 4.5, "Fish": 5.5, "Mixed Non-Veg": 6.5}
    food_em = food_map[food]

    total = sum([transport_em, electricity_em, lpg_em, ac_em, gey_em, waste_em, food_em])

    if st.button("Calculate Footprint"):
        st.success(f"### 🌎 Total Emission: **{total:.2f} kg CO₂/day**")

        st.info(carbon_badge(total))

        st.subheader("🏆 Achievements")
        for a in achievements(total): st.write("- " + a)

        labels = ["Transport", "Electricity", "LPG", "AC", "Geyser", "Waste", "Food"]
        values = [transport_em, electricity_em, lpg_em, ac_em, gey_em, waste_em, food_em]
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Emission Breakdown")
        st.pyplot(fig)

# -------------------------------------------------------
# PAGE: AI — WITH PREMIUM LOOK + TTS
# -------------------------------------------------------
elif page == "AI":
    st.title("⚡ Green Energy AI Assistant")

    if not GEMINI_KEY:
        st.error("Gemini API Key Missing!")
    else:
        question = st.text_area("Ask anything about renewable energy:")

        if st.button("Ask AI"):
            model = genai.GenerativeModel("gemini-2.5-flash")
            res = model.generate_content(question)
            st.write(res.text)

            if st.checkbox("🔊 Hear Answer"):
                speak(res.text)
