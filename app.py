import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
from gtts import gTTS
from io import BytesIO
from datetime import datetime
import pandas as pd
import numpy as np

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Carbon Footprint & Green Energy AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# PREMIUM GLASSMORPHISM + PARTICLE SYSTEM + ADVANCED ANIMATIONS
# ================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        :root {
            --primary-glow: #00ff88;
            --primary-glow-soft: #00ff88aa;
            --secondary-glow: #00d4ff;
            --glass-bg: rgba(255,255,255,0.05);
            --glass-border: rgba(255,255,255,0.1);
            --dark-bg: #0a0a0f;
            --card-bg: rgba(20,20,30,0.6);
        }

        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
            overflow-x: hidden;
        }

        .particles {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 0;
        }

        section[data-testid="stSidebar"] {
            background: rgba(10,10,15,0.95); backdrop-filter: blur(30px);
            border-right: 1px solid var(--glass-border);
            border-radius: 0 24px 24px 0;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        }

        .sidebar-title {
            font-size: 32px; font-weight: 900;
            background: linear-gradient(135deg, var(--primary-glow), var(--secondary-glow));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; text-align: center; margin: 2rem 0;
            letter-spacing: -0.5px; position: relative;
        }
        .sidebar-title::after {
            content: ''; position: absolute; bottom: -8px; left: 50%;
            transform: translateX(-50%); width: 60px; height: 3px;
            background: linear-gradient(90deg, var(--primary-glow), var(--secondary-glow));
            border-radius: 2px;
        }

        .nav-btn {
            width: 100%; padding: 16px 20px; margin: 8px 0; border-radius: 16px;
            font-size: 16px; font-weight: 600; border: 1px solid var(--glass-border);
            background: var(--glass-bg); backdrop-filter: blur(20px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative;
            overflow: hidden;
        }
        .nav-btn:hover { 
            border-color: var(--primary-glow); background: rgba(0,255,136,0.15);
            transform: translateX(8px) scale(1.02); box-shadow: 0 20px 40px rgba(0,255,136,0.3);
        }

        .premium-card {
            background: var(--glass-bg); backdrop-filter: blur(25px);
            border: 1px solid var(--glass-border); border-radius: 24px;
            padding: 2.5rem; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4);
            position: relative; overflow: hidden; transition: all 0.4s ease;
        }
        .premium-card:hover {
            transform: translateY(-8px); box-shadow: 0 35px 70px -15px rgba(0,0,0,0.5);
        }

        .glow-header {
            font-size: 3rem; font-weight: 900;
            background: linear-gradient(135deg, #ffffff, var(--primary-glow));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; margin-bottom: 1.5rem; position: relative;
        }
        .glow-header::after {
            content: ''; position: absolute; bottom: -10px; left: 0;
            width: 80px; height: 4px; background: linear-gradient(90deg, var(--primary-glow), var(--secondary-glow));
            border-radius: 2px;
        }

        .metric-card {
            background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.1));
            backdrop-filter: blur(20px); border: 1px solid rgba(0,255,136,0.3);
            border-radius: 20px; padding: 2rem; text-align: center;
        }
        .metric-value {
            font-size: 2.5rem; font-weight: 900;
            background: linear-gradient(135deg, var(--primary-glow), var(--secondary-glow));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--primary-glow), rgba(0,255,136,0.8));
            border: none; color: #000; font-weight: 700; border-radius: 16px;
            padding: 12px 32px; box-shadow: 0 10px 30px rgba(0,255,136,0.4);
        }

        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
            50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
            100% { transform: translateY(0px) rotate(360deg); opacity: 0.7; }
        }
    </style>
    
    <div class="particles">
        <div style="position: absolute; width: 4px; height: 4px; background: var(--primary-glow); border-radius: 50%; animation: float 20s infinite linear; top: 20%; left: 10%;"></div>
        <div style="position: absolute; width: 3px; height: 3px; background: var(--secondary-glow); border-radius: 50%; animation: float 25s infinite linear reverse; top: 60%; right: 15%;"></div>
        <div style="position: absolute; width: 2px; height: 2px; background: var(--primary-glow); border-radius: 50%; animation: float 18s infinite linear; bottom: 30%; left: 70%;"></div>
    </div>
""", unsafe_allow_html=True)

# ================================
# SESSION STATE & CONFIG
# ================================
if "page" not in st.session_state: st.session_state["page"] = "Home"
if "history" not in st.session_state: st.session_state["history"] = []
if "user_name" not in st.session_state: st.session_state["user_name"] = ""
if "quiz_score" not in st.session_state: st.session_state["quiz_score"] = 0
if "pledge" not in st.session_state: st.session_state["pledge"] = ""

GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
if GEMINI_KEY: genai.configure(api_key=GEMINI_KEY)

# ================================
# UTILITY FUNCTIONS
# ================================
def text_to_audio(text):
    tts = gTTS(text); buffer = BytesIO()
    tts.write_to_fp(buffer); st.audio(buffer.getvalue(), format="audio/mp3")

def carbon_badge(score):
    if score < 8: return "🟢 *Eco Champion*"
    elif score < 15: return "🟡 *Green Progress*"
    return "🔴 *Action Needed*"

def achievements(score):
    ach = []
    if score < 6: ach.append("🌟 Eco-Starter")
    if score < 10: ach.append("💚 Green Badge") 
    if score < 14: ach.append("🔥 Reducer")
    else: ach.append("⚠️ Alert")
    return ach

# ================================
# PREMIUM SIDEBAR
# ================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌱 Green Energy AI</div>', unsafe_allow_html=True)
    
    nav_items = [
        ("🏠 Home", "Home"), ("🌍 Carbon Calculator", "Carbon"), 
        ("📈 History", "History"), ("⚡ AI Assistant", "AI"),
        ("🧠 Quiz", "Quiz"), ("📅 Timeline", "Timeline"), ("ℹ About", "About")
    ]
    
    for label, page_name in nav_items:
        if st.button(label, key=f"nav_{page_name}", use_container_width=True):
            st.session_state["page"] = page_name
    
    st.markdown("---")
    st.session_state["user_name"] = st.text_input("👤 Name", value=st.session_state["user_name"])

page = st.session_state["page"]

# ================================
# FULLY FUNCTIONAL PAGES
# ================================
if page == "Home":
    st.markdown('<div class="glow-header">🌱 Carbon Footprint Analyzer</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
        with st.container():
            st.markdown("""
                <div class="premium-card">
                    <h3 style="color: #00ff88;">✨ Premium Features</h3>
                    <ul style="line-height: 2;">
                        <li>📊 Real-time tracking</li>
                        <li>🎯 Personalized tips</li>
                        <li>🤖 AI Assistant</li>
                        <li>📈 Progress charts</li>
                        <li>🏆 Badges & Quiz</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    with col2:
        if st.session_state["history"]:
            latest = st.session_state["history"][-1]
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{latest['total']:.1f}kg</div>
                    <div style="color: #aaa;">CO₂ Today</div>
                </div>
            """, unsafe_allow_html=True)

elif page == "Carbon":
    st.markdown('<div class="glow-header">🌍 Carbon Calculator</div>', unsafe_allow_html=True)
    
    with st.form("carbon_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.header("🚗 Transport")
            km = st.slider("Daily km", 0, 100, 15)
            fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "Electric"])
        with col2:
            st.header("💡 Electricity")
            units = st.slider("Monthly units", 0, 1000, 150)
            diet = st.selectbox("Diet", ["Veg", "Non-Veg"])
        submitted = st.form_submit_button("🚀 Calculate", use_container_width=True)
    
    if 'submitted' in locals() and submitted:
        total = km * 0.12 + units * 0.8/30 + (6 if diet == "Non-Veg" else 3)
        st.markdown(f"""
            <div class="premium-card" style="text-align: center;">
                <div style="font-size: 4rem; font-weight: 900; color: #00ff88;">{total:.1f}kg</div>
                <div style="color: #aaa; font-size: 1.2rem;">CO₂ per day</div>
                <div style="background: rgba(0,255,136,0.2); padding: 1rem; border-radius: 12px; font-weight: 700;">{carbon_badge(total)}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.session_state["history"].append({"time": datetime.now(), "total": total})
        
        fig, ax = plt.subplots(figsize=(8,6))
        ax.pie([30,25,20,15,10], labels=["Transport","Electricity","Food","Waste","Other"], 
               autopct='%1.1f%%', colors=['#00ff88','#00d4ff','#ffaa00','#ff6b6b','#aaa'])
        st.pyplot(fig)

elif page == "History":
    st.markdown('<div class="glow-header">📈 Your Progress</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        if st.session_state["history"]:
            df = pd.DataFrame(st.session_state["history"])
            st.line_chart(df.set_index('time')['total'])
            st.dataframe(df.tail(5))
        else:
            st.info("👆 Calculate your first footprint!")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "AI":
    st.markdown('<div class="glow-header">⚡ AI Assistant</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        if not GEMINI_KEY:
            st.error("🔑 Add GEMINI_API_KEY in Streamlit Secrets")
        else:
            user_input = st.text_area("Ask about green energy...")
            if st.button("Ask AI", use_container_width=True):
                model = genai.GenerativeModel("gemini-1.5-flash")
                context = f"User carbon footprint: {st.session_state['history'][-1]['total']:.1f}kg/day" if st.session_state["history"] else ""
                response = model.generate_content(context + "\n\n" + user_input)
                st.success(response.text)
                if st.button("🔊 Audio"): text_to_audio(response.text)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Quiz":
    st.markdown('<div class="glow-header">🧠 Green Quiz</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        questions = [
            {"q": "Main global warming gas?", "options": ["O₂", "N₂", "CO₂", "He"], "ans": "CO₂"},
            {"q": "Renewable energy?", "options": ["Coal", "Solar", "Petrol", "Diesel"], "ans": "Solar"}
        ]
        
        score = 0
        for i, q in enumerate(questions):
            st.write(f"**Q{i+1}.** {q['q']}")
            ans = st.radio("", q['options'], key=f"q{i}")
            if ans == q['ans']: score += 1
        
        if st.button("Check Score"):
            st.session_state["quiz_score"] = score
            st.success(f"🎉 {score}/{len(questions)} - {'🏆 Champion!' if score == 2 else '💚 Good!'}")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Timeline":
    st.markdown('<div class="glow-header">📅 Development Timeline</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-card">
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div style="display: flex; align-items: center; padding: 1rem; background: rgba(0,255,136,0.1); border-radius: 12px;">
                    <div style="width: 12px; height: 12px; background: #00ff88; border-radius: 50%; margin-right: 1rem;"></div>
                    <span><strong>Day 1:</strong> Concept & Planning</span>
                </div>
                <div style="display: flex; align-items: center; padding: 1rem; background: rgba(0,212,255,0.1); border-radius: 12px;">
                    <div style="width: 12px; height: 12px; background: #00d4ff; border-radius: 50%; margin-right: 1rem;"></div>
                    <span><strong>Day 10:</strong> Premium Glassmorphism UI</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif page == "About":
    st.markdown('<div class="glow-header">ℹ About</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-card">
            <h3>👤 Arsh Kumar Gupta</h3>
            <p><strong>Class XI-A</strong><br>Kendriya Vidyalaya<br>Rashtriya Bal Vigyanik Pradarshani</p>
            <div style="background: linear-gradient(135deg, #00ff88, #00d4ff); padding: 1rem; border-radius: 12px; text-align: center; color: black; font-weight: 700;">
                🌍 Building a Greener Future
            </div>
        </div>
    """, unsafe_allow_html=True)
