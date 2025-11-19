import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import speech_recognition as sr
from gtts import gTTS
import base64
from io import BytesIO

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Carbon Footprint & Green Energy AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# DARK THEME + NEW NAVBAR
# -----------------------------
st.markdown("""
    <style>
        .stApp { background-color: #0c0c0c !important; }
        body, label, p, span, div { color: white !important; }
        h1, h2, h3, h4 { color: white !important; font-weight: 700; }

        /* NEW AESTHETIC NAVBAR */
        .cool-navbar {
            background: linear-gradient(90deg, #000000, #111111, #000000);
            border-radius: 16px;
            padding: 10px;
            margin-bottom: 28px;
            box-shadow: 0px 0px 25px rgba(0,255,140,0.15);
            display: flex;
            justify-content: center;
            gap: 25px;
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
            cursor: pointer;
            transform: translateY(-3px);
            box-shadow: 0px 0px 12px #00c853aa;
        }

        .nav-active {
            background-color: #00c853 !important;
            color: black !important;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0px 0px 15px #00ff9d;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# GEMINI CONFIG
# -----------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# -----------------------------
# FUNCTION: VOICE RECOGNITION
# -----------------------------
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening… Speak now.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"🟢 You said: {text}")
            return text
        except:
            st.error("Could not understand audio.")
            return ""

# -----------------------------
# FUNCTION: TEXT → SPEECH
# -----------------------------
def text_to_audio(text):
    tts = gTTS(text)
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    audio_bytes = buffer.getvalue()
    st.audio(audio_bytes, format="audio/mp3")

# -----------------------------
# FUNCTION: BADGE
# -----------------------------
def carbon_badge(score):
    if score < 8:
        return "🟢 **Low Carbon Footprint – Eco Friendly!**"
    elif score < 15:
        return "🟡 **Moderate Footprint – Can Improve.**"
    else:
        return "🔴 **High Footprint – Needs Immediate Action.**"

# -----------------------------
# FUNCTION: ACHIEVEMENTS
# -----------------------------
def achievements(score):
    ach = []
    if score < 6:
        ach.append("🌟 Eco-Starter Award")
    if score < 10:
        ach.append("💚 Green Lifestyle Badge")
    if score < 14:
        ach.append("🔥 Carbon Reducer Badge")
    if score >= 14:
        ach.append("⚠️ High Emission Alert Badge")
    return ach

# -----------------------------
# NAVIGATION
# -----------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

st.markdown('<div class="cool-navbar">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])

if col1.button("🏠 Home"):
    st.session_state["page"] = "Home"
if col2.button("🌍 Carbon Calculator"):
    st.session_state["page"] = "Carbon"
if col3.button("⚡ Green Energy AI"):
    st.session_state["page"] = "AI"

st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state["page"]

# =====================================================================
# PAGE 1 : HOME
# =====================================================================
if page == "Home":
    st.title("🌱 Carbon Footprint Analyzer & Green Energy Assistant")
    st.subheader("A Complete Science Exhibition App")
    st.write("""
    This tool computes your **carbon footprint**, assigns a **carbon rating badge**,  
    gives **achievements**, visualizes emissions with a **pie chart**,  
    and lets you talk using **voice interaction**.
    """)

# =====================================================================
# PAGE 2 : CARBON FOOTPRINT CALCULATOR
# =====================================================================
elif page == "Carbon":
    st.title("🌍 Complete Carbon Footprint Calculator")

    # Transport
    st.header("🚗 Transportation")
    km_daily = st.slider("Daily travel (km)", 0, 200, 10)
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
    emission_map = {"Petrol":0.118, "Diesel":0.134, "Electric":0.02}
    transport_em = km_daily * emission_map[fuel]

    # Electricity
    st.header("💡 Electricity Usage")
    units = st.number_input("Units per month", 0, 2000, 150)
    electricity_em = units * 0.82 / 30

    # LPG
    st.header("🔥 LPG Usage")
    lpg = st.slider("LPG cylinders per year", 0, 24, 6)
    lpg_em = (lpg * 42.5) / 365

    # AC
    st.header("❄ AC Usage")
    ac_hr = st.slider("AC hours per day", 0, 24, 4)
    ac_em = ac_hr * 1.5 * 0.82

    # Geyser
    st.header("🚿 Geyser")
    gey = st.slider("Geyser hours", 0.0, 5.0, 0.5)
    gey_em = gey * 2 * 0.82

    # Waste
    st.header("🗑 Waste")
    waste = st.slider("Daily waste (kg)", 0.0, 5.0, 0.5)
    waste_em = waste * 0.09

    # Food
    st.header("🍽 Diet")
    food = st.selectbox("Diet type", ["Vegetarian","Eggs","Chicken","Fish","Mixed Non-Veg"])
    food_map = {"Vegetarian":2,"Eggs":3,"Chicken":4.5,"Fish":5.5,"Mixed Non-Veg":6.5}
    food_em = food_map[food]

    total = transport_em + electricity_em + lpg_em + ac_em + gey_em + waste_em + food_em

    # Calculate Button
    if st.button("Calculate Footprint"):
        st.success(f"### 🌎 Total Daily Carbon Emission: **{total:.2f} kg CO₂/day**")

        # Badge
        st.info(carbon_badge(total))

        # Achievements
        st.subheader("🏆 Your Achievements")
        for a in achievements(total):
            st.write("- " + a)

        # Pie Chart
        labels = ["Transport","Electricity","LPG","AC","Geyser","Waste","Food"]
        values = [transport_em, electricity_em, lpg_em, ac_em, gey_em, waste_em, food_em]
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)

# =====================================================================
# PAGE 3 : AI
# =====================================================================
elif page == "AI":
    st.title("⚡ Green Energy AI Assistant")

    if not GEMINI_KEY:
        st.error("Gemini API Key Missing!")
    else:
        st.write("Ask anything about renewable energy!")

        colA, colB = st.columns([2,1])

        with colA:
            text_input = st.text_area("Type your question:")

        with colB:
            if st.button("🎤 Speak"):
                spoken = voice_to_text()
                if spoken:
                    text_input = spoken

        if st.button("Ask AI"):
            model = genai.GenerativeModel("gemini-2.5-flash")
            res = model.generate_content(text_input)
            st.write(res.text)

            # Optional Voice Output
            if st.checkbox("🔊 Hear AI Response"):
                text_to_audio(res.text)
