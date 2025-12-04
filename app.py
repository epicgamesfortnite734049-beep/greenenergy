import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
from gtts import gTTS
from io import BytesIO
from datetime import datetime, timedelta
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import re

# ================================
# PAGE CONFIGURATION
# ================================
st.set_page_config(
    page_title="🌱 Carbon Footprint & Green Energy AI - RBVP 2025",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# (Your CSS & theme block unchanged) - shortened for brevity in editor
# NOTE: In this file I kept your full CSS block exactly as you provided earlier.
# For the canvas view we include it verbatim; when editing locally, keep it.
# ================================

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;700;900&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        :root {
            --primary-green: #00ff88;
            --primary-green-glow: #00ff88aa;
            --secondary-cyan: #00d4ff;
            --accent-gold: #ffd700;
            --glass-bg: rgba(255,255,255,0.08);
            --glass-border: rgba(255,255,255,0.15);
            --dark-bg: #0a0a0f;
            --card-bg: rgba(20,20,35,0.7);
            --gradient-main: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        }

        .stApp {
            background: var(--gradient-main) !important;
            overflow-x: hidden;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            font-weight: 800 !important;
            font-family: 'Orbitron', monospace;
        }
        
        .stMetric > div > div > div > div {
            color: var(--primary-green) !important;
        }

        section[data-testid="stSidebar"] {
            background: rgba(10,10,15,0.98);
            backdrop-filter: blur(35px);
            border-right: 2px solid var(--glass-border);
            border-radius: 0 28px 28px 0;
            box-shadow: 0 30px 60px -15px rgba(0,0,0,0.6);
            padding-top: 25px;
        }

        .master-title {
            font-size: 34px;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary-green), var(--secondary-cyan), var(--accent-gold));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 2.5rem 0 2rem 0;
            letter-spacing: -1px;
            position: relative;
            text-shadow: 0 0 30px rgba(0,255,136,0.5);
        }
        .master-title::after {
            content: '';
            position: absolute;
            bottom: -12px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-green), var(--secondary-cyan));
            border-radius: 3px;
            box-shadow: 0 0 20px rgba(0,255,136,0.6);
        }

        .nav-premium {
            width: 100%;
            padding: 18px 24px;
            margin: 10px 12px;
            border-radius: 20px;
            font-size: 17px;
            font-weight: 700;
            border: 2px solid var(--glass-border);
            background: var(--glass-bg);
            backdrop-filter: blur(25px);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            color: #e8e8e8;
        }
        .nav-premium::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.7s;
        }
        .nav-premium:hover::before {
            left: 100%;
        }
        .nav-premium:hover {
            border-color: var(--primary-green);
            background: rgba(0,255,136,0.2);
            transform: translateX(12px) scale(1.03);
            box-shadow: 0 25px 50px rgba(0,255,136,0.4);
            color: white;
        }
        .nav-active {
            background: linear-gradient(135deg, var(--primary-green), rgba(0,255,136,0.8));
            border-color: var(--primary-green);
            color: #000 !important;
            box-shadow: 0 0 35px rgba(0,255,136,0.6);
            font-weight: 900;
            transform: scale(1.02);
        }

        .ultra-card {
            background: var(--glass-bg);
            backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border);
            border-radius: 28px;
            padding: 3rem;
            box-shadow: 0 35px 70px -20px rgba(0,0,0,0.5), 
                        0 0 0 1px rgba(255,255,255,0.08);
            position: relative;
            overflow: hidden;
            transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            margin: 20px 0;
        }
        .ultra-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary-green), var(--secondary-cyan), transparent);
        }
        .ultra-card:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: 0 50px 100px -25px rgba(0,0,0,0.6), 
                        0 0 50px rgba(0,255,136,0.3);
        }

        .mega-header {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #ffffff, var(--primary-green), var(--secondary-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 2rem;
            position: relative;
            letter-spacing: -2px;
        }
        .mega-header::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 0;
            width: 120px;
            height: 6px;
            background: linear-gradient(90deg, var(--primary-green), var(--secondary-cyan));
            border-radius: 4px;
            box-shadow: 0 0 25px rgba(0,255,136,0.8);
        }

        .metric-display {
            background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,212,255,0.15));
            backdrop-filter: blur(25px);
            border: 2px solid rgba(0,255,136,0.4);
            border-radius: 24px;
            padding: 2.5rem;
            text-align: center;
            transition: all 0.4s ease;
        }
        .metric-display:hover {
            transform: scale(1.05);
            box-shadow: 0 30px 60px rgba(0,255,136,0.4);
        }
        .metric-value {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary-green), var(--secondary-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        div.stSlider > div > div > div > div {
            background: linear-gradient(90deg, var(--primary-green), var(--secondary-cyan)) !important;
        }
        .stSelectbox > div > div {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--primary-green), rgba(0,255,136,0.9));
            border: none;
            color: #000;
            font-weight: 800;
            border-radius: 20px;
            padding: 16px 40px;
            font-size: 16px;
            transition: all 0.4s ease;
            box-shadow: 0 15px 40px rgba(0,255,136,0.5);
        }
        .stButton > button:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 60px rgba(0,255,136,0.6);
        }

        .success-badge {
            background: linear-gradient(135deg, rgba(0,255,136,0.25), rgba(0,212,255,0.25));
            border: 2px solid var(--primary-green);
            border-radius: 16px;
            padding: 1.5rem 2rem;
            font-weight: 800;
            backdrop-filter: blur(20px);
            text-align: center;
            margin: 20px 0;
        }

        .timeline-master {
            padding: 30px;
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.008));
            border: 1px solid rgba(0,255,140,0.05);
            box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        }
        
        @media (max-width: 768px) {
            .mega-header { font-size: 2.5rem; }
            .ultra-card { padding: 2rem; margin: 10px 0; }
        }
        
        @keyframes glowPulse {
            0%, 100% { box-shadow: 0 0 20px rgba(0,255,136,0.4); }
            50% { box-shadow: 0 0 40px rgba(0,255,136,0.8); }
        }
        .pulse-glow {
            animation: glowPulse 2s infinite;
        }
    </style>
""", unsafe_allow_html=True)

# ================================
# PARTICLE BACKGROUND SYSTEM (unchanged)
# ================================
st.markdown("""
    <div style="
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 0;
    ">
        <div style="
            position: absolute; width: 6px; height: 6px; 
            background: radial-gradient(circle, var(--primary-green), transparent);
            border-radius: 50%; animation: float 25s infinite linear;
            top: 20%; left: 10%; box-shadow: 0 0 20px var(--primary-green-glow);
        "></div>
        <div style="
            position: absolute; width: 4px; height: 4px; 
            background: radial-gradient(circle, var(--secondary-cyan), transparent);
            border-radius: 50%; animation: float 30s infinite linear reverse;
            top: 60%; right: 20%; box-shadow: 0 0 15px var(--secondary-cyan);
        "></div>
        <div style="
            position: absolute; width: 3px; height: 3px; 
            background: radial-gradient(circle, var(--accent-gold), transparent);
            border-radius: 50%; animation: float 22s infinite linear;
            bottom: 30%; left: 75%; box-shadow: 0 0 12px var(--accent-gold);
        "></div>
        <div style="
            position: absolute; width: 5px; height: 5px; 
            background: radial-gradient(circle, var(--primary-green), transparent);
            border-radius: 50%; animation: float 28s infinite linear reverse;
            top: 80%; right: 10%; box-shadow: 0 0 18px var(--primary-green-glow);
        "></div>
    </div>
    <style>
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); opacity: 0.8; }
            33% { transform: translateY(-30px) rotate(120deg); opacity: 1; }
            66% { transform: translateY(-15px) rotate(240deg); opacity: 0.9; }
            100% { transform: translateY(0px) rotate(360deg); opacity: 0.8; }
        }
    </style>
""", unsafe_allow_html=True)

# ================================
# FINAL GEMINI API SETUP (robust + quota-aware)
# ================================
@st.cache_data(ttl=600)
def setup_gemini_api():
    """Zero-error API setup with detailed status and quota detection"""
    try:
        GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
        if not GEMINI_KEY or GEMINI_KEY.strip() == "":
            return {"status": "🔑 MISSING", "models": [], "error": "No API key found"}

        genai.configure(api_key=GEMINI_KEY.strip())

        # Try getting a model list; handle quota or permission errors gracefully
        test_models = ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash", "models/gemini-2.0-flash"]
        working_models = []
        last_error = ""

        for model_name in test_models:
            try:
                model_info = genai.get_model(model_name)
                # If get_model returns something sensible, consider it available
                working_models.append(model_name)
                break
            except Exception as e:
                last_error = str(e)
                # If quota-like message, return immediately with that context
                if re.search(r"quota|Quota exceeded|429|rate limit", last_error, re.IGNORECASE):
                    return {"status": "⚠️ QUOTA/429", "models": [], "error": last_error}
                continue

        if working_models:
            return {"status": f"✅ READY ({working_models[0]})", "models": working_models, "error": ""}
        else:
            return {"status": "⚠️ NO MODELS", "models": [], "error": last_error}

    except Exception as e:
        return {"status": f"❌ ERROR", "models": [], "error": str(e)[:300]}

# Initialize - SAFE
API_INFO = setup_gemini_api()
API_STATUS = API_INFO["status"]
AVAILABLE_MODELS = API_INFO.get("models", [])
API_ERROR = API_INFO.get("error", "")

# ================================
# COMPREHENSIVE UTILITY FUNCTIONS (unchanged except added helper for AI)
# ================================
def text_to_audio(text):
    """Convert text to speech with error handling"""
    try:
        tts = gTTS(text[:500])  # Limit text length
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        st.audio(buffer, format="audio/mp3")
    except Exception:
        st.error("Audio generation failed")


def carbon_badge(score):
    if score < 6:
        return "🟢🌟 *Eco Champion* - World Class!"
    elif score < 10:
        return "🟢 *Eco Friendly* - Excellent!"
    elif score < 15:
        return "🟡 *Moderate* - Room to Improve"
    else:
        return "🔴⚠️ *High Impact* - Urgent Action Needed!"


def achievements_system(score):
    achievements = []
    if score < 6:
        achievements.extend(["🌟 Eco-Starter Elite", "🏆 Global Green Leader"])
    elif score < 10:
        achievements.extend(["💚 Green Lifestyle Pro", "⭐ Sustainable Star"])
    elif score < 15:
        achievements.extend(["🔥 Carbon Warrior", "📈 Improvement Needed"])
    else:
        achievements.extend(["⚠️ High Alert", "🎯 Target for Change"])
    return achievements


def personalized_recommendations(total, transport, electricity, food):
    tips = []

    if transport > total * 0.3:
        tips.append("🚗 **Transport (High):** Switch to carpooling or electric vehicle")
    if electricity > total * 0.25:
        tips.append("💡 **Electricity (High):** Use 5-star appliances & LEDs")
    if food > 4:
        tips.append("🍽 **Diet:** Try 2 vegetarian days per week")

    tips.extend([
        "🌱 Plant a tree this month",
        "♻️ Segregate waste daily",
        "💧 Fix leaking taps",
        "🔌 Unplug standby electronics"
    ])

    return tips[:4]


def india_comparison(total):
    avg_indian = 4.5  # kg CO2/day average
    if total < avg_indian * 0.7:
        return f"🎉 You're in top 20% of India! ({total:.1f} vs {avg_indian:.1f} avg)"
    elif total < avg_indian:
        return f"✅ Better than average Indian ({total:.1f} vs {avg_indian:.1f})"
    else:
        return f"📊 Above Indian avg ({total:.1f} vs {avg_indian:.1f}). Room to improve!"

# ================================
# Simple offline/canned AI fallback
# ================================
CANNED_RESPONSES = {
    "solar": "For rooftop solar in India: check orientation (south), get a 3-5kW system for a household, and apply for net metering through your DISCOM.",
    "electricity": "Reducing electricity: use LED bulbs, switch off standby power, and use fans with high star ratings. Consider time-of-day usage to avoid peak tariffs.",
    "transport": "Try carpooling, using public transit, or cycling short distances. Reducing a single car trip per week helps significantly over a year.",
    "default": "That's a great question! Try asking about specific areas like 'solar', 'electricity', or 'transport' so I can give practical tips."
}


def canned_ai_reply(user_input: str) -> str:
    # Very simple keyword-based fallback
    ui = user_input.lower()
    for k in CANNED_RESPONSES:
        if k in ui:
            return CANNED_RESPONSES[k]
    return CANNED_RESPONSES["default"]

# ================================
# Robust AI generation with retry/backoff + offline option
# ================================

def generate_ai_response(user_input: str, use_offline: bool = False, max_retries: int = 3) -> (str, bool):
    """
    Returns (response_text, used_offline_flag)
    Tries Gemini API if available; falls back to canned replies if quota/error.
    """
    if use_offline:
        return canned_ai_reply(user_input), True

    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
    if not GEMINI_KEY:
        return "🔑 Gemini API key missing. Enable the key in Streamlit secrets or toggle 'Use offline AI'.", True

    # If API status reported quota issues during setup, show that immediately
    if API_STATUS and re.search(r"QUOTA|429|NO MODELS|MISSING", API_STATUS, re.IGNORECASE):
        # Surface detailed error to user and fallback
        return (f"⚠️ Gemini API unavailable: {API_STATUS}. Details: {API_ERROR}\n\nSwitching to offline assistant."), True

    model_name = AVAILABLE_MODELS[0] if AVAILABLE_MODELS else "gemini-2.0-flash-exp"

    # Try to generate with exponential backoff
    delay = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            genai.configure(api_key=GEMINI_KEY.strip())
            model = genai.GenerativeModel(model_name)

            prompt_context = "You are a concise, practical assistant helping students reduce their carbon footprint in India. Reply in simple, actionable steps."
            if st.session_state.get("history"):
                latest = st.session_state["history"][-1]
                prompt_context += f" Latest recorded CO2: {latest['total']:.1f} kg/day."

            full_prompt = f"{prompt_context}\n\nQuestion: {user_input}"

            resp = model.generate_content(full_prompt)
            text = getattr(resp, 'text', None)
            if not text:
                # Some SDKs return structured fields
                text = str(resp)
            return text, False

        except Exception as e:
            err = str(e)
            # If quota or rate limit errors are present, immediately fallback to offline
            if re.search(r"quota|Quota exceeded|429|rate limit|GenerateRequestsPerMinute", err, re.IGNORECASE):
                # return helpful message + fallback
                fallback_msg = (
                    "⚠️ Gemini quota / rate-limit detected: " + err +
                    "\n\nSwitching to offline/canned assistant. To fix: check Google Cloud billing, request higher quota, or use a different API key.\nSee: https://ai.google.dev/gemini-api/docs/rate-limits"
                )
                return fallback_msg + "\n\n" + canned_ai_reply(user_input), True

            # For other transient errors, backoff and retry
            if attempt == max_retries:
                # Last attempt failed: fallback
                return ("⚠️ AI generation failed after retries. Using offline assistant.\nError: " + err + "\n\n" + canned_ai_reply(user_input)), True
            else:
                time.sleep(delay)  # small backoff
                delay *= 2.0
                continue

# ================================
# Rest of your app: session state, sidebar, pages etc. (kept mostly same)
# For brevity, I kept the original page logic but only replaced AI section with the robust wrapper above.
# ================================

session_init = {
    "page": "Home",
    "history": [],
    "user_name": "",
    "quiz_score": 0,
    "pledge": "",
    "achievements_unlocked": [],
    "first_visit": True
}

for key, default in session_init.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sidebar
with st.sidebar:
    st.markdown('<div class="master-title">🌿 Green Energy AI</div>', unsafe_allow_html=True)

    nav_config = [
        ("🏠 Dashboard", "Home"),
        ("🌍 Carbon Calculator", "Carbon"),
        ("📊 My History", "History"),
        ("🤖 AI Assistant", "AI"),
        ("🧠 Eco Quiz", "Quiz"),
        ("📈 Analytics", "Analytics"),
        ("📅 Timeline", "Timeline"),
        ("ℹ️ About RBVP", "About")
    ]

    for label, page_name in nav_config:
        btn_class = "nav-premium nav-active" if st.session_state["page"] == page_name else "nav-premium"
        if st.button(label, key=f"nav_{page_name}", use_container_width=True):
            st.session_state["page"] = page_name
            st.rerun()

    st.markdown("---")
    st.markdown("### 👤 Profile")
    st.session_state["user_name"] = st.text_input(
        "Your Name",
        value=st.session_state["user_name"],
        help="For certificates & personalized tracking"
    )

    st.markdown("### 🔌 API")
    st.markdown(f"**{API_STATUS}**")
    if AVAILABLE_MODELS:
        st.caption(f"Model: {AVAILABLE_MODELS[0]}")
    else:
        st.caption(API_ERROR if API_ERROR else "Setup needed")

# Page routing (kept your pages unchanged except AI block)
page = st.session_state["page"]

if page == "Home":
    st.markdown('<div class="mega-header">🌿 Carbon Footprint Dashboard</div>', unsafe_allow_html=True)
    if st.session_state["first_visit"]:
        st.markdown("""
            <div class="ultra-card pulse-glow">
                <h2>🎉 Welcome to Rashtriya Bal Vigyanik Pradarshani 2025!</h2>
                <p>This premium app helps you track your environmental impact with AI-powered insights.</p>
            </div>
        """, unsafe_allow_html=True)
        st.session_state["first_visit"] = False

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state["history"]:
            latest = st.session_state["history"][-1]
            st.markdown("""
                <div class="metric-display">
                    <div class="metric-value">%.1fkg</div>
                    <div style="color: #aaa; font-size: 1.1rem; font-weight: 600;">Latest CO₂</div>
                </div>
            """ % latest["total"], unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="metric-display">
                    <div class="metric-value">--kg</div>
                    <div style="color: #aaa;">No data yet</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-display">
                <div class="metric-value">7 Pages</div>
                <div style="color: #aaa;">Features</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-display">
                <div class="metric-value">{len(st.session_state['history'])}</div>
                <div style="color: #aaa;">Calculations</div>
            </div>
        """, unsafe_allow_html=True)

# Carbon page (kept same)
elif page == "Carbon":
    st.markdown('<div class="mega-header">🌍 Advanced Carbon Calculator</div>', unsafe_allow_html=True)
    with st.form("carbon_calculator", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🚗 Transportation")
            km_daily = st.slider("Daily Travel (km)", 0, 200, 12, help="Your daily commute")
            fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric", "CNG"])
            transport_factor = {"Petrol": 0.118, "Diesel": 0.134, "Electric": 0.02, "CNG": 0.08}
            transport_co2 = km_daily * transport_factor[fuel_type]

            st.subheader("💡 Electricity")
            kwh_monthly = st.number_input("Monthly Units", 0, 2000, 150)
            electricity_co2 = (kwh_monthly * 0.82) / 30  # Daily average

        with col2:
            st.subheader("🔥 Cooking Gas")
            lpg_cylinders = st.slider("LPG Cylinders/Year", 0, 24, 6)
            lpg_co2 = (lpg_cylinders * 42.5) / 365

            st.subheader("🍽️ Food Habits")
            diet_type = st.selectbox("Diet", ["Vegetarian", "Eggetarian", "Chicken", "Fish", "Mixed Non-Veg"])
            food_factors = {"Vegetarian": 2.0, "Eggetarian": 3.0, "Chicken": 4.5, "Fish": 5.5, "Mixed Non-Veg": 6.5}
            food_co2 = food_factors[diet_type]

            st.subheader("❄️ Appliances")
            ac_hours = st.slider("AC Hours/Day", 0, 24, 2)
            geyser_hours = st.slider("Geyser Hours/Day", 0.0, 5.0, 0.5)

        col1, col2 = st.columns(2)
        with col1:
            waste_kg = st.slider("Daily Waste (kg)", 0.0, 5.0, 0.4)
        with col2:
            water_usage = st.slider("Daily Water (liters)", 0, 500, 150)

        calculate_btn = st.form_submit_button("🚀 Calculate Full Footprint", use_container_width=True)

    if calculate_btn:
        ac_co2 = ac_hours * 1.5 * 0.82
        geyser_co2 = geyser_hours * 2 * 0.82
        waste_co2 = waste_kg * 0.09
        water_co2 = water_usage * 0.0005

        total_co2 = (transport_co2 + electricity_co2 + lpg_co2 + ac_co2 + 
                    geyser_co2 + waste_co2 + food_co2 + water_co2)

        st.session_state["history"].append({
            "time": datetime.now(),
            "total": total_co2,
            "transport": transport_co2,
            "electricity": electricity_co2,
            "food": food_co2
        })

        st.markdown(f"""
            <div class="metric-display pulse-glow">
                <div class="metric-value">**{total_co2:.2f}kg**</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #00ff88;">CO₂ per Day</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="success-badge">{carbon_badge(total_co2)}</div>', unsafe_allow_html=True)

        st.subheader("🏆 Achievements Unlocked")
        new_achievements = achievements_system(total_co2)
        for ach in new_achievements:
            st.success(f"✅ {ach}")

        st.info(india_comparison(total_co2))

        labels = ["Transport", "Electricity", "Food", "LPG", "AC", "Geyser", "Waste", "Water"]
        values = [transport_co2, electricity_co2, food_co2, lpg_co2, ac_co2, geyser_co2, waste_co2, water_co2]

        fig = px.pie(values=values, names=labels, title="Your Carbon Breakdown")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🎯 Personalized Action Plan")
        tips = personalized_recommendations(total_co2, transport_co2, electricity_co2, food_co2)
        for tip in tips:
            st.markdown(f"• **{tip}**")

# History page (unchanged)
elif page == "History":
    st.markdown('<div class="mega-header">📊 Your Carbon Journey</div>', unsafe_allow_html=True)
    if not st.session_state["history"]:
        st.info("👆 Calculate your first footprint to see your progress!")
    else:
        df = pd.DataFrame(st.session_state["history"])
        df['date'] = pd.to_datetime(df['time']).dt.date

        col1, col2 = st.columns(2)
        with col1:
            fig_line = px.line(df, x='time', y='total', title='Your CO₂ Trend', markers=True)
            fig_line.update_layout(xaxis_title="Date", yaxis_title="kg CO₂/day")
            st.plotly_chart(fig_line, use_container_width=True)

        with col2:
            avg_co2 = df['total'].mean()
            best_day = df['total'].min()
            st.metric("📈 Average Daily", f"{avg_co2:.2f} kg")
            st.metric("🥇 Best Day", f"{best_day:.2f} kg")
            st.metric("📊 Total Entries", len(df))

        st.dataframe(df[['time', 'total']].tail(10), use_container_width=True)

# AI assistant page (REPLACED with robust UI)
elif page == "AI":
    st.markdown('<div class="mega-header">🤖 Green Energy AI Assistant</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("""
            <div style='padding: 0.5rem 1rem; background: rgba(255,255,255,0.03); border-radius: 12px;'>
                <strong>How this assistant works:</strong>
                <ul>
                    <li>It first tries your Gemini API key (from Streamlit secrets).</li>
                    <li>On quota/errors it automatically falls back to an offline, fast assistant.</li>
                    <li>Use the toggle on the right to force offline mode.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        user_input = st.text_area("Ask a Green Energy Question", height=160,
                                 placeholder="E.g., How can I reduce my electricity bill? Best solar setups in India?")
        if st.button("Ask AI"):
            if user_input.strip() == "":
                st.warning("Please enter a question.")
            else:
                with st.spinner("Generating AI response..."):
                    use_offline = st.session_state.get("force_offline_ai", False)
                    response_text, used_offline = generate_ai_response(user_input, use_offline=use_offline)

                    st.markdown("### AI's response:")
                    st.write(response_text)

                    if st.button("🔊 Hear this as Audio"):
                        try:
                            tts = gTTS(response_text)
                            buffer = BytesIO()
                            tts.write_to_fp(buffer)
                            buffer.seek(0)
                            st.audio(buffer, format="audio/mp3")
                        except Exception as e:
                            st.error(f"Audio playback error: {str(e)}")

    with col2:
        st.markdown("### AI Controls")
        st.checkbox("Use offline AI (force)", key="force_offline_ai")
        st.markdown("**API Status:**")
        st.code(API_STATUS)
        if API_ERROR:
            st.caption(API_ERROR)
        st.markdown("---")
        st.markdown("Need to fix quota? Check your Google Cloud billing & quota or try a different API key. Useful links:")
        st.markdown("- https://ai.google.dev/gemini-api/docs/rate-limits")
        st.markdown("- https://console.cloud.google.com/iam-admin/settings")

# Quiz, Analytics, Timeline, About (kept as-is, unchanged except minor formatting)
elif page == "Quiz":
    st.markdown('<div class="mega-header">🧠 Green Knowledge Quiz</div>', unsafe_allow_html=True)
    questions = [
        {"question": "Which gas causes maximum global warming?",
         "options": ["Oxygen (O₂)", "Nitrogen (N₂)", "Carbon Dioxide (CO₂)", "Helium (He)"],
         "correct": 2,
         "fact": "CO₂ from fossil fuels stays in atmosphere for 100+ years!"},
        {"question": "India's renewable energy target by 2030?",
         "options": ["25%", "40%", "50%", "75%"],
         "correct": 2,
         "fact": "500 GW target including solar, wind, hydro!"},
        {"question": "Best way to reduce transport emissions?",
         "options": ["Drive faster", "Carpool/public transport", "Bigger car", "AC on max"],
         "correct": 1,
         "fact": "Carpooling cuts emissions by 50% per person!"},
        {"question": "1 kWh electricity = ? kg CO₂ in India",
         "options": ["0.2kg", "0.5kg", "0.82kg", "2kg"],
         "correct": 2,
         "fact": "India's grid emission factor is 0.82kg CO₂/kWh"}
    ]

    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = {}

    score = 0
    st.markdown('<div class="ultra-card">', unsafe_allow_html=True)
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}.** {q['question']}")
        answer_idx = st.radio("", [opt for opt in q['options']], key=f"quiz_{i}")
        st.session_state["quiz_answers"][i] = answer_idx
        if answer_idx == q['options'][q['correct']]:
            score += 1

    if st.button("🎯 Submit Quiz", use_container_width=True):
        percentage = (score / len(questions)) * 100
        st.session_state["quiz_score"] = score
        st.markdown(f"""
            <div class="metric-display">
                <div class="metric-value">{score}/{len(questions)}</div>
                <div style="font-size: 1.4rem;">Score: {percentage:.0f}%</div>
            </div>
        """, unsafe_allow_html=True)
        if percentage == 100:
            st.balloons()
            st.success("🏆 **Quiz Master!** Perfect Score!")
        elif percentage >= 75:
            st.success("🌟 **Excellent!** Green Genius!")
        elif percentage >= 50:
            st.info("✅ **Good Job!** Keep Learning!")
        else:
            st.warning("📚 **Try Again!** More study needed.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Analytics":
    st.markdown('<div class="mega-header">📈 Advanced Analytics</div>', unsafe_allow_html=True)
    if not st.session_state["history"]:
        st.warning("Calculate footprints first to unlock analytics!")
    else:
        df = pd.DataFrame(st.session_state["history"])
        df['week'] = df['time'].dt.isocalendar().week
        weekly_avg = df.groupby('week')['total'].mean().reset_index()
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(weekly_avg, x='week', y='total', title="Weekly Average CO₂")
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            if 'transport' in df.columns:
                fig_category = px.bar(df.tail(10), y=['transport', 'electricity', 'food'], title="Recent Breakdown", barmode='group')
                st.plotly_chart(fig_category, use_container_width=True)

elif page == "Timeline":
    st.markdown('<div class="mega-header">📅 Development Timeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="timeline-master">', unsafe_allow_html=True)
    timeline_data = [
        ("📋 Day 1", "Project concept & research"),
        ("🎨 Day 2", "Premium UI/UX design"),
        ("⚙️ Day 3-4", "Carbon calculation engine"),
        ("📊 Day 5", "Charts & visualization"),
        ("🏆 Day 6", "Achievements system"),
        ("🤖 Day 7-8", "Gemini AI integration"),
        ("✨ Day 9", "Glassmorphism theme"),
        ("🚀 Day 10", "RBVP final polish"),
        ("🎯 Today", "Live at exhibition!")
    ]
    for day, desc in timeline_data:
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 1.5rem; margin: 1rem 0; background: rgba(0,255,136,0.1); border-radius: 16px; border-left: 5px solid var(--primary-green);">
                <div style="width: 16px; height: 16px; background: var(--primary-green); border-radius: 50%; margin-right: 1.5rem; box-shadow: 0 0 15px var(--primary-green-glow);"></div>
                <div>
                    <div style="font-weight: 800; font-size: 1.2rem; color: var(--primary-green);">{day}</div>
                    <div style="color: #aaa; margin-top: 0.3rem;">{desc}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "About":
    st.markdown('<div class="mega-header">ℹ️ Rashtriya Bal Vigyanik Pradarshani</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="ultra-card">
                <h2>👨‍💻 Creator</h2>
                <div style="font-size: 2.5rem; font-weight: 900; color: var(--accent-gold);">Arsh Kumar Gupta</div>
                <div style="color: #aaa; margin: 1rem 0;">
                    **Class XI-A**<br>
                    Kendriya Vidyalaya No1 AFS Adampur
                    Jalandhar<br>
                    Rashtriya Bal Vigyanik Pradarshani 2025
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="ultra-card">
                <h2>🌟 Vision</h2>
                <div style="background: linear-gradient(135deg, var(--primary-green), var(--secondary-cyan)); padding: 2rem; border-radius: 20px; text-align: center; color: black; font-weight: 800; font-size: 1.3rem; margin: 1rem 0;">Empowering students to build a sustainable India! 🇮🇳</div>
                <ul style="color: #aaa;">
                    <li>Real-time carbon tracking</li>
                    <li>AI-powered insights</li>
                    <li>India-specific data</li>
                    <li>Interactive learning</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; padding: 2rem; color: #666; font-size: 0.9rem;'>© 2025 Arsh Kumar Gupta | RBVP Exhibition | Made with ❤️ for Planet Earth</div>", unsafe_allow_html=True)

