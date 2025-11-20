import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import speech_recognition as sr
from gtts import gTTS
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
# MINIMAL PREMIUM (B1) THEME for Home
# -----------------------------
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0d0f;
            --card: rgba(255,255,255,0.03);
            --glass-border: rgba(255,255,255,0.06);
            --accent: #66e39f;
            --muted: #bcded0;
        }
        html, body, .stApp {
            background: linear-gradient(180deg, #070809 0%, #0b0d0f 100%) !important;
            color: #e9f8f0 !important;
            font-family: 'Inter', sans-serif;
        }

        /* Top navbar */
        .cool-navbar {
            background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border-radius: 12px;
            padding: 8px 14px;
            margin-bottom: 20px;
            display:flex;
            justify-content:center;
            gap:12px;
            align-items:center;
            border: 1px solid rgba(255,255,255,0.02);
            box-shadow: 0 6px 26px rgba(0,0,0,0.6);
        }
        .nav-button {
            background: transparent;
            padding: 8px 18px;
            border-radius: 10px;
            color: var(--muted) !important;
            font-weight:600;
            border: 1px solid transparent;
            transition: all .18s ease;
        }
        .nav-button:hover {
            color: white !important;
            transform: translateY(-3px);
            border: 1px solid rgba(255,255,255,0.04);
            box-shadow: 0 8px 30px rgba(12, 45, 32, 0.08);
            cursor: pointer;
        }

        /* Hero */
        .hero {
            display:flex;
            gap:22px;
            align-items:center;
            padding:22px;
            border-radius:14px;
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border:1px solid var(--glass-border);
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            margin-bottom:18px;
        }
        .hero-left { flex:1; padding:8px 12px; }
        .hero-right { width:420px; min-width:260px; max-width:460px; }

        .hero-title {
            font-size:2.4rem;
            margin-bottom:6px;
            color: #f7fff7;
            letter-spacing:0.2px;
        }
        .hero-sub {
            color: var(--muted);
            font-size:1.02rem;
            margin-bottom:14px;
        }
        .pill {
            display:inline-block;
            padding:8px 12px;
            border-radius:999px;
            background: rgba(102,227,159,0.06);
            color: var(--accent);
            font-weight:700;
            border: 1px solid rgba(102,227,159,0.08);
            margin-bottom:10px;
        }

        .feature-grid { display:flex; gap:12px; margin-top:12px; }
        .feature-card {
            background: var(--card);
            padding:12px;
            border-radius:10px;
            flex:1;
            border:1px solid rgba(255,255,255,0.02);
        }
        .feature-title { color:#f8fff8; font-weight:700; margin-bottom:6px; }
        .feature-desc { color: var(--muted); font-size:0.95rem; }

        /* subtle horizontal accent */
        .accent-line {
            height:8px;
            border-radius:999px;
            background: linear-gradient(90deg, rgba(102,227,159,0.14), rgba(102,227,159,0.08));
            margin-top:14px;
            box-shadow: 0 6px 26px rgba(102,227,159,0.03);
        }

        /* demo panel */
        .demo-panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            padding:14px;
            border-radius:10px;
            border:1px solid rgba(255,255,255,0.02);
            text-align:left;
            color: var(--muted);
        }
        .demo-stat { font-weight:700; color:#f6fff6; }

        /* download link */
        .download-link {
            display:inline-block;
            margin-top:12px;
            padding:10px 14px;
            border-radius:10px;
            background: transparent;
            color: var(--accent);
            text-decoration:none;
            border: 1px solid rgba(102,227,159,0.06);
        }

        /* responsive */
        @media (max-width:900px) {
            .hero { flex-direction:column; }
            .hero-right { width:100%; }
            .feature-grid { flex-direction:column; }
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# NAVIGATION BAR (functional, unchanged)
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
# HOME (Minimal Premium UI B1) — updated only this page
# -----------------------------
if page == "Home":
    # Use the uploaded file path as the download URL (as provided in conversation)
    # Developer note: using the local uploaded path from the history
    project_zip_path = "sandbox:/mnt/data/serpent_bravo-chatbot (1).zip"

    st.markdown(f"""
    <div class="hero">
        <div class="hero-left">
            <div class="pill">Exhibition Mode • Ready</div>
            <div class="hero-title">Carbon Footprint Analyzer & Green Energy AI</div>
            <div class="hero-sub">A compact, presentation-ready tool for demonstrations — accurate calculations, clear visuals, and AI-backed explanations. Designed for school science exhibitions.</div>

            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-title">Precise Calculator</div>
                    <div class="feature-desc">Combine transport, electricity, LPG, AC, geyser, waste, and diet into a single footprint figure.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">Interactive AI</div>
                    <div class="feature-desc">Ask about solar, wind, EVs, and sustainable home tips — powered by Gemini 2.5 Flash.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">Voice Enabled</div>
                    <div class="feature-desc">Speak directly to the app during your live demo (browser or local mode as supported).</div>
                </div>
            </div>

            <div class="accent-line"></div>

            <div style="margin-top:12px;">
                <a class="download-link" href="{project_zip_path}" target="_blank">📦 Download Project Assets</a>
                <span style="color:var(--muted); margin-left:10px;">(README, assets & deploy files)</span>
            </div>
        </div>

        <div class="hero-right">
            <div class="demo-panel">
                <div style="font-size:0.95rem; color:var(--muted); margin-bottom:10px;">Demo quick stats</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <div style="color:var(--muted)">Monthly Electricity</div><div class="demo-stat">350 kWh</div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <div style="color:var(--muted)">Daily Travel</div><div class="demo-stat">20 km</div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <div style="color:var(--muted)">Estimated CO₂</div><div class="demo-stat">9.8 kg/day</div>
                </div>
                <div style="text-align:center; margin-top:8px;">
                    <a class="download-link" href="#Carbon">Open Calculator →</a>
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
