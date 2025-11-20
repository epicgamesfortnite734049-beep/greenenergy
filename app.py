import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import speech_recognition as sr
from gtts import gTTS
import base64
from io import BytesIO
import os

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Carbon Footprint & Green Energy AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# GEMINI CONFIG (unchanged)
# -----------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# -----------------------------
# DARK THEME + NAVBAR (unchanged)
# -----------------------------
st.markdown("""
    <style>
        :root{
            --neon:#00ff85;
            --neon-2:#00c853;
            --card-bg: rgba(255,255,255,0.03);
        }

        .stApp { background-color: #060709 !important; color: #eafaf1 !important; }
        body, label, p, span, div { color: #eafaf1 !important; }
        h1, h2, h3, h4 { color: #eafaf1 !important; font-weight: 700; }

        /* NEW AESTHETIC NAVBAR */
        .cool-navbar {
            background: linear-gradient(90deg, rgba(0,0,0,0.9), rgba(10,10,10,0.8));
            border-radius: 14px;
            padding: 10px 18px;
            margin-bottom: 22px;
            box-shadow: 0 8px 40px rgba(0,200,120,0.06);
            display: flex;
            justify-content: center;
            gap: 18px;
            align-items: center;
        }

        .nav-button {
            background-color: rgba(255,255,255,0.03);
            padding: 8px 22px;
            border-radius: 12px;
            color: var(--neon) !important;
            font-size: 16px;
            font-weight: 600;
            border: 1px solid rgba(0,200,120,0.08);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            backdrop-filter: blur(4px);
        }

        .nav-button:hover {
            background: linear-gradient(90deg, rgba(0,200,120,0.06), rgba(0,200,120,0.02));
            border-color: rgba(0,200,120,0.35);
            transform: translateY(-4px);
            box-shadow: 0 6px 22px rgba(0,200,120,0.12);
            cursor: pointer;
        }

        .hero {
            background: linear-gradient(180deg, rgba(0,0,0,0.35), rgba(0,0,0,0.25));
            padding: 28px;
            border-radius: 16px;
            border: 1px solid rgba(0,200,120,0.06);
            box-shadow: 0 10px 40px rgba(0,200,120,0.04);
            display:flex;
            gap:20px;
            align-items:center;
        }

        .hero-left {
            flex: 1;
            padding: 10px 18px;
        }

        .hero-right {
            width: 420px;
            min-width: 260px;
            max-width: 460px;
            text-align:center;
        }

        .hero-title {
            font-size: 2.6rem;
            line-height:1.05;
            letter-spacing: 0.6px;
            margin-bottom: 6px;
            color: white;
            text-shadow: 0 6px 30px rgba(0,255,150,0.06), 0 0 18px rgba(0,200,120,0.06);
        }

        .hero-sub {
            color: #bfffe2;
            font-size: 1.05rem;
            margin-bottom: 18px;
        }

        .neon-pill {
            display:inline-block;
            padding:10px 14px;
            background: linear-gradient(90deg, rgba(0,255,150,0.06), rgba(0,200,120,0.02));
            border-radius: 999px;
            color: var(--neon);
            font-weight:700;
            border: 1px solid rgba(0,200,120,0.12);
            margin-bottom: 12px;
            box-shadow: 0 8px 30px rgba(0,200,120,0.04), 0 0 14px rgba(0,200,120,0.02) inset;
        }

        .feature-grid { display:flex; gap:14px; margin-top:18px; }
        .feature-card {
            background: var(--card-bg);
            padding: 14px;
            border-radius: 12px;
            flex:1;
            border: 1px solid rgba(0,200,120,0.04);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 40px rgba(0,200,120,0.06);
        }
        .feature-title { font-weight:700; color: #eafaf1; margin-bottom:6px; }
        .feature-desc { color:#bfeee0; font-size:0.95rem; }

        /* Animated energy wave */
        .energy-wave {
            width:100%;
            height:8px;
            background: linear-gradient(90deg, rgba(0,200,120,0.18), rgba(0,255,150,0.25), rgba(0,200,120,0.18));
            border-radius: 999px;
            margin-top: 18px;
            box-shadow: 0 10px 30px rgba(0,200,120,0.06);
            animation: pulse 3.5s infinite;
            opacity:0.95;
        }
        @keyframes pulse {
            0% { transform: translateX(-6px) scaleX(0.98); }
            50% { transform: translateX(6px) scaleX(1.02); }
            100% { transform: translateX(-6px) scaleX(0.98); }
        }

        /* download link style */
        .download-zip {
            display:inline-block;
            margin-top:12px;
            padding:10px 14px;
            border-radius:10px;
            background:linear-gradient(90deg, rgba(0,255,150,0.06), rgba(0,200,120,0.02));
            color:var(--neon);
            text-decoration:none;
            border:1px solid rgba(0,200,120,0.1);
        }

        /* responsive tweaks */
        @media (max-width: 900px) {
            .hero { flex-direction:column; }
            .hero-right { width:100%; }
            .feature-grid { flex-direction:column; }
        }

    </style>
""", unsafe_allow_html=True)

# -----------------------------
# NAVIGATION BAR (unchanged functionality)
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

# -----------------------------
# HERO / FRONT PAGE: FUTURISTIC GREEN-TECH (STYLE A)
# Only the Home page UI is upgraded. All functionality below remains unchanged.
# -----------------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
        <div class="hero-left">
            <div class="neon-pill">Live • Science Exhibition Ready</div>
            <div class="hero-title">✨ Live Carbon Footprint Analyzer & Green Energy AI</div>
            <div class="hero-sub">Interactive, voice-enabled, and educational — built for a science exhibition demo. Instant insights, clear visuals, and guided recommendations.</div>

            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-title">🔍 Accurate Calculations</div>
                    <div class="feature-desc">Transport, electricity, LPG, AC, geyser, waste and diet — all combined into a clear footprint.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">🎙️ Voice Interaction</div>
                    <div class="feature-desc">Speak your questions to the app during the demo — modern and hands-on.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">🤖 AI Knowledge Assistant</div>
                    <div class="feature-desc">Gemini-powered explanations for green energy topics — great for judges and visitors.</div>
                </div>
            </div>

            <div class="energy-wave"></div>

            <div style="margin-top:16px;">
                <a class="download-zip" href="sandbox:/mnt/data/serpent_bravo-chatbot (1).zip" target="_blank">📦 Download Project Assets</a>
                <span style="color:#9fffd6; margin-left:12px; font-size:0.95rem;">(Includes README & deployment files)</span>
            </div>
        </div>

        <div class="hero-right">
            <!-- stylized demo panel -->
            <div style="background:linear-gradient(180deg, rgba(0,0,0,0.25), rgba(10,10,10,0.2)); padding:16px; border-radius:12px; border:1px solid rgba(0,200,120,0.06); box-shadow: 0 8px 30px rgba(0,200,120,0.03);">
                <h3 style="margin-bottom:6px; color: #dfffe9;">Quick Demo</h3>
                <div style="color:#bfffe0; font-size:0.95rem; margin-bottom:8px;">Try our one-click demo values for exhibition mode:</div>
                <div style="display:flex; gap:8px; margin-bottom:10px;">
                    <button onclick="" style="padding:8px 12px; border-radius:8px; background:rgba(0,255,150,0.06); border:1px solid rgba(0,200,120,0.08); color:var(--neon); font-weight:700;">Demo 1</button>
                    <button onclick="" style="padding:8px 12px; border-radius:8px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.03); color:#bfffe0;">Demo 2</button>
                </div>
                <div style="background: rgba(0,0,0,0.35); padding:10px; border-radius:8px; color:#cffff0; font-size:0.95rem;">
                    <strong>Live Stats</strong>
                    <div style="margin-top:8px;">
                        <div>Monthly Electricity: <strong>350 kWh</strong></div>
                        <div>Daily Travel: <strong>20 km</strong></div>
                        <div>Estimated Daily CO₂: <strong>9.8 kg</strong></div>
                    </div>
                </div>
                <div style="margin-top:12px; text-align:center;">
                    <a class="download-zip" href="#Carbon">🚀 Open Calculator</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# PAGE 2 : CARBON (unchanged logic)
# -----------------------------
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
        if total < 8:
            st.info("🟢 **Low Carbon Footprint – Eco Friendly!**")
        elif total < 15:
            st.info("🟡 **Moderate Footprint – Can Improve.**")
        else:
            st.info("🔴 **High Footprint – Needs Immediate Action.**")

        # Achievements
        st.subheader("🏆 Your Achievements")
        if total < 6:
            st.write("- 🌟 Eco-Starter Award")
        if total < 10:
            st.write("- 💚 Green Lifestyle Badge")
        if total < 14:
            st.write("- 🔥 Carbon Reducer Badge")
        if total >= 14:
            st.write("- ⚠️ High Emission Alert Badge")

        # Pie Chart
        labels = ["Transport","Electricity","LPG","AC","Geyser","Waste","Food"]
        values = [transport_em, electricity_em, lpg_em, ac_em, gey_em, waste_em, food_em]
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)

# -----------------------------
# PAGE 3 : AI (unchanged logic)
# -----------------------------
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
                # voice_to_text uses microphone; in cloud env this may not work — kept as-is per your logic
                try:
                    recognizer = sr.Recognizer()
                    with sr.Microphone() as source:
                        st.info("🎤 Listening… Speak now.")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                        spoken = recognizer.recognize_google(audio)
                        st.success(f"🟢 You said: {spoken}")
                        text_input = spoken
                except Exception as e:
                    st.error("Voice input failed: " + str(e))

        if st.button("Ask AI"):
            model = genai.GenerativeModel("gemini-2.5-flash")
            res = model.generate_content(text_input)
            st.write(res.text)

            # Optional Voice Output
            if st.checkbox("🔊 Hear AI Response"):
                try:
                    tts = gTTS(res.text)
                    buffer = BytesIO()
                    tts.write_to_fp(buffer)
                    audio_bytes = buffer.getvalue()
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.error("Text-to-speech failed: " + str(e))

# -----------------------------
# END
# -----------------------------
