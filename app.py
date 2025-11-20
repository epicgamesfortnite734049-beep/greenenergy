# app.py — Full Neon Sci-Fi Premium UI (Style A)
import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os
import soundfile as sf
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from datetime import datetime

# -----------------------------
# Config
# -----------------------------
st.set_page_config(
    page_title="Carbon Footprint & Green Energy AI — Neon",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Gemini API key (keeps existing logic)
# -----------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
if GEMINI_KEY:
    try:
        genai.configure(api_key=GEMINI_KEY)
    except Exception as e:
        # continue — page will show error where applicable
        print("genai configure error:", e)

# -----------------------------
# Session state initialization
# -----------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"
if "achievements" not in st.session_state:
    st.session_state["achievements"] = set()
if "carbon_history" not in st.session_state:
    st.session_state["carbon_history"] = []
if "ai_queries" not in st.session_state:
    st.session_state["ai_queries"] = 0
if "last_transcript" not in st.session_state:
    st.session_state["last_transcript"] = ""

# -----------------------------
# Utility: Audio recorder processor for streamlit-webrtc
# -----------------------------
class RecorderProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv_audio(self, frame):
        """
        frame: av.AudioFrame
        Convert to numpy array and store
        """
        try:
            arr = frame.to_ndarray()
            # Normalize to float32 if needed
            if arr.dtype != np.float32:
                arr = arr.astype(np.float32) / np.iinfo(arr.dtype).max
            self.frames.append(arr)
        except Exception:
            pass
        return frame

def save_webrtc_audio(processor: RecorderProcessor, samplerate=48000):
    """
    Concatenate recorded frames and save to a temporary WAV file.
    Returns filepath or None.
    """
    if not processor or not processor.frames:
        return None
    try:
        pieces = []
        for f in processor.frames:
            # f can be 2D (channels, samples) -> convert to mono
            if f.ndim == 2:
                mono = np.mean(f, axis=0)
            else:
                mono = f
            pieces.append(mono)
        audio = np.concatenate(pieces).astype(np.float32)
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp.name, audio, samplerate)
        return tmp.name
    except Exception as e:
        st.error(f"Error saving audio: {e}")
        return None

def transcribe_wav_with_google(wav_path):
    """
    Use speech_recognition (Google Web Speech) to transcribe a WAV file.
    """
    try:
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return None

def play_text_tts(text):
    """
    Convert text to speech using gTTS and play it in Streamlit.
    """
    try:
        tts = gTTS(text)
        buf = BytesIO()
        tts.write_to_fp(buf)
        audio_bytes = buf.getvalue()
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("TTS failed: " + str(e))

# -----------------------------
# UI CSS — Neon Sci-Fi Premium (A)
# -----------------------------
st.markdown(
    """
    <style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    :root{
        --bg1: #040405;
        --bg2: #071015;
        --neon: #00ff85;
        --neon-2: #00c853;
        --muted: #9fead1;
        --card: rgba(255,255,255,0.02);
        --glass-border: rgba(0,255,140,0.06);
    }

    html, body, .stApp {
        background: radial-gradient(circle at 10% 10%, #03100a 0%, #040405 45%, #071015 100%) !important;
        color: #e8fff6 !important;
        font-family: 'Inter', sans-serif;
    }

    .neon-navbar {
        background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 14px;
        padding: 8px 12px;
        margin-bottom: 18px;
        display:flex;
        justify-content:center;
        gap:12px;
        align-items:center;
        border:1px solid rgba(255,255,255,0.02);
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }

    .nav-btn {
        padding: 8px 16px;
        border-radius: 10px;
        background: transparent;
        color: var(--muted) !important;
        font-weight:600;
        border: 1px solid transparent;
        transition: all .18s ease;
    }
    .nav-btn:hover {
        color: white !important;
        transform: translateY(-4px);
        border: 1px solid rgba(0,255,140,0.06);
        box-shadow: 0 8px 26px rgba(0,255,140,0.06);
        cursor:pointer;
    }
    .nav-active {
        background: linear-gradient(90deg, rgba(0,255,140,0.06), rgba(0,200,120,0.02));
        color: black !important;
        border-radius: 10px;
        padding: 8px 18px;
        font-weight:700;
        box-shadow: 0 10px 40px rgba(0,255,140,0.06);
    }

    /* Hero */
    .hero-wrap {
        padding: 28px;
        border-radius: 16px;
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.007));
        border: 1px solid rgba(0,255,140,0.03);
        box-shadow: 0 12px 60px rgba(0,255,140,0.02);
        display:flex;
        gap:24px;
        align-items:center;
    }
    .hero-left { flex:1; padding:10px 12px; }
    .hero-right { width:420px; min-width:240px; max-width:480px; }

    .hero-title {
        font-size: 34px;
        font-weight:800;
        margin-bottom:6px;
        color: #f6fff9;
        letter-spacing:0.2px;
        text-shadow: 0 8px 40px rgba(0,255,140,0.03);
    }
    .hero-sub {
        color: var(--muted);
        font-size: 1.02rem;
        margin-bottom:14px;
    }
    .neon-pill {
        display:inline-block;
        padding:8px 12px;
        border-radius:999px;
        background: linear-gradient(90deg, rgba(0,255,140,0.06), rgba(0,200,120,0.02));
        color: var(--neon);
        font-weight:700;
        border: 1px solid rgba(0,255,140,0.06);
        margin-bottom:10px;
    }

    .feature-grid { display:flex; gap:12px; margin-top:12px; }
    .feature-card {
        background: var(--card);
        padding:14px;
        border-radius:12px;
        flex:1;
        border: 1px solid rgba(0,255,140,0.02);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(0,255,140,0.04);
        border-color: rgba(0,255,140,0.08);
    }
    .feature-title { font-weight:700; color:#f8fff8; margin-bottom:6px; }
    .feature-desc { color: var(--muted); font-size:0.95rem; }

    /* accent line */
    .accent-line {
        height:6px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(0,255,140,0.18), rgba(0,200,120,0.14));
        margin-top:14px;
        box-shadow: 0 10px 30px rgba(0,255,140,0.02);
    }

    /* glass panels for pages */
    .panel {
        padding:16px;
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.007));
        border:1px solid rgba(0,255,140,0.02);
    }

    /* Carbon page layout improvements */
    .section-row { display:flex; gap:18px; align-items:flex-start; }
    .left-col { flex:1; min-width:280px; }
    .right-col { width:420px; min-width:240px; }

    /* AI chat box */
    .chat-box {
        background: rgba(255,255,255,0.015);
        padding:12px;
        border-radius:10px;
        border:1px solid rgba(255,255,255,0.02);
        max-height: 360px;
        overflow-y: auto;
    }
    .user-bubble { background: linear-gradient(90deg, rgba(0,255,140,0.06), rgba(0,200,120,0.02)); color:black; padding:10px 12px; border-radius:12px; display:inline-block; margin-bottom:8px; }
    .ai-bubble { background: rgba(255,255,255,0.02); color:var(--muted); padding:10px 12px; border-radius:12px; display:inline-block; margin-bottom:8px; }

    /* responsive */
    @media (max-width: 900px) {
        .hero-wrap { flex-direction: column; }
        .section-row { flex-direction: column; }
        .right-col { width:100%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Top Nav (upgraded look)
# -----------------------------
st.markdown('<div class="neon-navbar">', unsafe_allow_html=True)
nav_c1, nav_c2, nav_c3, nav_c4 = st.columns([1,1,1,0.6])
if nav_c1.button("🏠 Home"):
    st.session_state["page"] = "Home"
if nav_c2.button("🌍 Carbon Calculator"):
    st.session_state["page"] = "Carbon"
if nav_c3.button("⚡ Green Energy AI"):
    st.session_state["page"] = "AI"
if nav_c4.button("👤 Profile"):
    st.session_state["page"] = "Profile"
st.markdown('</div>', unsafe_allow_html=True)

# small helper: mark active nav visually (can't alter Streamlit buttons directly easily)
# We'll just rely on page content.

page = st.session_state["page"]

# -----------------------------
# HOME Page — Neon Sci-Fi Premium
# -----------------------------
if page == "Home":
    project_zip_path = "sandbox:/mnt/data/serpent_bravo-chatbot (1).zip"
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-left">
                <div class="neon-pill">LIVE — Exhibition Mode</div>
                <div class="hero-title">Neon Carbon Footprint Analyzer & Green Energy AI</div>
                <div class="hero-sub">Fast, voice-enabled, and presentation-ready. Use during your science exhibition to demo carbon science & renewable solutions.</div>

                <div class="feature-grid">
                    <div class="feature-card">
                        <div class="feature-title">Accurate Carbon Metrics</div>
                        <div class="feature-desc">Combine transport, electricity, LPG, AC, geyser, waste and diet into a single score.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-title">AI Knowledge Assistant</div>
                        <div class="feature-desc">Gemini-powered explanations and suggestions about green energy and sustainability.</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-title">Interactive Voice</div>
                        <div class="feature-desc">Speak to the app using the built-in browser recorder — hands-free demos on stage.</div>
                    </div>
                </div>

                <div class="accent-line"></div>

                <div style="margin-top:12px;">
                    <a class="neon-pill" href="{project_zip_path}" target="_blank" style="text-decoration:none;">📦 Download Project Files</a>
                    <span style="color:var(--muted); margin-left:12px;">(README, assets & deployment)</span>
                </div>
            </div>

            <div class="hero-right">
                <div class="panel">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="color:var(--muted); font-size:0.95rem;">Quick demo profile</div>
                        <div style="font-size:0.85rem; color:var(--muted);">{datetime.now().strftime('%b %d, %Y')}</div>
                    </div>
                    <hr style="border:none; height:1px; background:rgba(255,255,255,0.02); margin:8px 0 12px 0;" />
                    <div style="display:flex; flex-direction:column; gap:10px;">
                        <div style="display:flex; justify-content:space-between;"><div style="color:var(--muted)">Electricity</div><div style="font-weight:700">350 kWh</div></div>
                        <div style="display:flex; justify-content:space-between;"><div style="color:var(--muted)">Daily Travel</div><div style="font-weight:700">20 km</div></div>
                        <div style="display:flex; justify-content:space-between;"><div style="color:var(--muted)">Est. CO₂/day</div><div style="font-weight:700">9.8 kg</div></div>
                    </div>
                    <div style="text-align:center; margin-top:12px;">
                        <a href="#Carbon" class="neon-pill" style="text-decoration:none;">Open Calculator</a>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # How it works section (three steps)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="panel" style="text-align:center;">
                <h3 style="margin-bottom:6px;">1. Input</h3>
                <div style="color:var(--muted)">Answer simple questions about travel, energy and diet.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="panel" style="text-align:center;">
                <h3 style="margin-bottom:6px;">2. Calculate</h3>
                <div style="color:var(--muted)">Get instant footprint results with visualizations.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="panel" style="text-align:center;">
                <h3 style="margin-bottom:6px;">3. Act</h3>
                <div style="color:var(--muted)">AI-backed suggestions & tips to reduce footprint.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# CARBON page — upgraded premium layout but same logic
# -----------------------------
elif page == "Carbon":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.header("🌍 Complete Carbon Footprint Calculator")

    st.markdown('<div class="section-row">', unsafe_allow_html=True)
    # left: inputs, right: summary + achievements
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("📥 Tell us about your daily habits")

        # Transport
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.write("### 🚗 Transportation")
        km_daily = st.slider("Daily travel (km)", 0, 200, 10)
        fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
        emission_map = {"Petrol": 0.118, "Diesel": 0.134, "Electric": 0.02}
        transport_em = km_daily * emission_map[fuel]
        st.markdown("</div>", unsafe_allow_html=True)

        # Electricity
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.write("### 💡 Electricity Usage")
        units = st.number_input("Units per month (kWh)", 0, 2000, 150)
        electricity_em = units * 0.82 / 30
        st.markdown("</div>", unsafe_allow_html=True)

        # LPG
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.write("### 🔥 LPG Usage")
        lpg = st.slider("LPG cylinders per year", 0, 24, 6)
        lpg_em = (lpg * 42.5) / 365
        st.markdown("</div>", unsafe_allow_html=True)

        # AC
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.write("### ❄ AC Usage")
        ac_hr = st.slider("AC hours per day", 0, 24, 4)
        ac_em = ac_hr * 1.5 * 0.82
        st.markdown("</div>", unsafe_allow_html=True)

        # Geyser
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.write("### 🚿 Geyser / Water Heater")
        gey = st.slider("Geyser hours (daily)", 0.0, 5.0, 0.5)
        gey_em = gey * 2 * 0.82
        st.markdown("</div>", unsafe_allow_html=True)

        # Waste & Food
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.write("### 🗑 Waste & 🍽 Food")
        waste = st.slider("Daily waste (kg)", 0.0, 5.0, 0.5)
        waste_em = waste * 0.09
        food = st.selectbox("Diet type", ["Vegetarian", "Eggs", "Chicken", "Fish", "Mixed Non-Veg"])
        food_map = {"Vegetarian": 2, "Eggs": 3, "Chicken": 4.5, "Fish": 5.5, "Mixed Non-Veg": 6.5}
        food_em = food_map[food]
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.subheader("🏁 Summary & Insights")
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        total = transport_em + electricity_em + lpg_em + ac_em + gey_em + waste_em + food_em
        st.metric("Estimated daily CO₂ (kg)", f"{total:.2f} kg")

        # Rating badge (styled text)
        if total < 8:
            st.markdown("<div style='padding:10px; border-radius:8px; background: rgba(0,255,140,0.06); color:black; font-weight:700'>🟢 Low Carbon Footprint — Eco Friendly</div>", unsafe_allow_html=True)
        elif total < 15:
            st.markdown("<div style='padding:10px; border-radius:8px; background: rgba(255,200,0,0.06); color:black; font-weight:700'>🟡 Moderate Footprint — Can Improve</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding:10px; border-radius:8px; background: rgba(255,80,80,0.06); color:black; font-weight:700'>🔴 High Footprint — Needs Action</div>", unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # Achievements (simple logic)
        st.subheader("🏆 Achievements")
        ach_list = []
        if total < 6:
            ach_list.append("🌟 Eco-Starter Award")
        if total < 10:
            ach_list.append("💚 Green Lifestyle Badge")
        if total < 14:
            ach_list.append("🔥 Carbon Reducer Badge")
        if total >= 14:
            ach_list.append("⚠️ High Emission Alert Badge")
        if ach_list:
            for a in ach_list:
                st.write(f"- {a}")
        else:
            st.write("No achievements yet — reduce your footprint to earn badges!")

        # Quick recommendations
        st.markdown("<hr style='border:none; height:1px; background:rgba(255,255,255,0.02); margin:12px 0;'/>", unsafe_allow_html=True)
        st.write("Quick recommendation:")
        if transport_em > 0.3 * total:
            st.write("- 🚴 Consider public transport or carpooling to cut transport emissions.")
        else:
            st.write("- ✅ Transport not the main emission source here.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Calculate button + Pie chart at bottom
    if st.button("Calculate Footprint & Visualize"):
        st.success(f"Total Daily Carbon Emission: **{total:.2f} kg CO₂/day**")

        # store history
        st.session_state["carbon_history"].append(total)

        # Pie chart
        labels = ["Transport", "Electricity", "LPG", "AC", "Geyser", "Waste", "Food"]
        values = [transport_em, electricity_em, lpg_em, ac_em, gey_em, waste_em, food_em]
        fig, ax = plt.subplots(figsize=(6,4))
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        st.pyplot(fig)

# -----------------------------
# AI page — upgraded chat UI + browser voice recorder
# -----------------------------
elif page == "AI":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.header("⚡ Green Energy AI Assistant")

    if not GEMINI_KEY:
        st.error("Gemini API Key Missing — add GEMINI_API_KEY to Streamlit Secrets.")
    else:
        # layout: left chat & input, right voice recorder + presets
        left, right = st.columns([2,1])
        with left:
            st.subheader("Ask the AI about green energy")
            # Chat box (show last ai response and transcripts if exist)
            st.markdown('<div class="chat-box" id="chatbox">', unsafe_allow_html=True)

            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []

            # display chat history
            for item in st.session_state["chat_history"]:
                role = item.get("role")
                text = item.get("text")
                if role == "user":
                    st.markdown(f'<div class="user-bubble">{text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-bubble">{text}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # input area
            user_question = st.text_area("Type your question", value="", height=90)

            col_send, col_clear = st.columns([1,1])
            with col_send:
                if st.button("Ask AI"):
                    query = user_question.strip() or st.session_state.get("last_transcript", "").strip()
                    if not query:
                        st.warning("Enter a question or use voice input.")
                    else:
                        # record user message
                        st.session_state["chat_history"].append({"role":"user","text":query})
                        st.session_state["ai_queries"] = st.session_state.get("ai_queries",0) + 1
                        # call Gemini
                        try:
                            model = genai.GenerativeModel("gemini-2.5-flash")
                            resp = model.generate_content(query)
                            answer = resp.text
                        except Exception as e:
                            answer = f"AI error: {e}"
                        st.session_state["chat_history"].append({"role":"ai","text":answer})
                        st.experimental_rerun()
            with col_clear:
                if st.button("Clear Chat"):
                    st.session_state["chat_history"] = []
                    st.experimental_rerun()

            # optional TTS playback of last AI response
            if st.checkbox("🔊 Play last AI response (TTS)"):
                if st.session_state.get("chat_history"):
                    last_ai = next((m for m in reversed(st.session_state["chat_history"]) if m["role"]=="ai"), None)
                    if last_ai:
                        play_text_tts(last_ai["text"])

        with right:
            st.subheader("🎤 Voice Recorder (Browser)")
            st.write("Use the recorder to speak your question. Click Start → Speak → Stop → Transcribe")

            webrtc_ctx = webrtc_streamer(
                key="ai-voice",
                mode=WebRtcMode.SENDONLY,
                audio_receiver_size=1024,
                media_stream_constraints={"audio": True, "video": False},
                async_processing=False,
                audio_processor_factory=RecorderProcessor,
            )

            if webrtc_ctx and webrtc_ctx.audio_processor:
                proc = webrtc_ctx.audio_processor
                if st.button("Transcribe Voice"):
                    wav = save_webrtc_audio(proc)
                    if wav:
                        st.success("Saved audio, transcribing...")
                        text = transcribe_wav_with_google(wav)
                        if text:
                            st.success("You said: " + text)
                            st.session_state["last_transcript"] = text
                            # prefill input area by reloading page and showing transcript
                            st.experimental_rerun()
                        else:
                            st.error("Transcription failed.")
                        try:
                            os.remove(wav)
                        except:
                            pass
                    else:
                        st.warning("No audio captured yet. Start recorder and speak.")

            st.markdown("<hr/>", unsafe_allow_html=True)
            st.write("Quick topics:")
            if st.button("Solar Basics"):
                st.session_state["chat_history"].append({"role":"user","text":"Explain how solar panels generate electricity in simple terms."})
                st.experimental_rerun()
            if st.button("EV Benefits"):
                st.session_state["chat_history"].append({"role":"user","text":"How do electric vehicles reduce carbon emissions compared to petrol cars?"})
                st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Profile page — history & achievements (added as part of overhaul)
# -----------------------------
elif page == "Profile":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.header("👤 Profile & Achievements")

    history = st.session_state.get("carbon_history", [])
    if history:
        st.subheader("Carbon History (most recent first)")
        st.write(list(reversed(history)))
        fig2, ax2 = plt.subplots()
        ax2.plot(history, marker="o")
        ax2.set_title("Carbon History (daily kg CO₂)")
        st.pyplot(fig2)
    else:
        st.info("No carbon history yet. Run a calculation on the Carbon page.")

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("Achievements")
    ach = st.session_state.get("achievements", set())
    if ach:
        for a in ach:
            st.write(f"- {a}")
    else:
        st.write("No achievements yet — reduce your footprint or ask the AI to earn badges!")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# End
# -----------------------------
