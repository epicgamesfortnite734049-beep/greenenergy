import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
from gtts import gTTS
from io import BytesIO

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Carbon Footprint & Green Energy AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# DARK PREMIUM THEME + SMOOTH SIDEBAR + TIMELINE ANIMATIONS
# ================================
st.markdown("""
    <style>
        /* App Background */
        .stApp {
            background-color: #0c0c0c !important;
        }
        body, p, label, span, div {
            color: white !important;
        }
        h1, h2, h3, h4 {
            color: white !important;
            font-weight: 700 !important;
        }

        /* Sidebar Base */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f0f, #050505);
            border-right: 1px solid #00ff8c33;
            padding-top: 18px;
            transition: 0.3s ease;
        }

        /* Sidebar Title */
        .sidebar-title {
            font-size: 28px;
            font-weight: 900;
            color: #00ffae;
            text-align: center;
            margin-bottom: 22px;
            letter-spacing: 1px;
            text-shadow: 0px 0px 12px #00ffaeaa;
        }

        /* Sidebar Buttons (premium) */
        .sidebar-btn {
            padding: 12px 18px;
            margin: 8px 10px;
            border-radius: 10px;
            font-size: 17px;
            font-weight: 600;
            color: #e8e8e8;
            text-align: center;
            border: 1px solid #00ff8c33;
            background: rgba(20,20,20,0.7);
            backdrop-filter: blur(4px);
            transition: all 0.22s ease-in-out;
        }

        .sidebar-btn:hover {
            color: black;
            background: #00ff8c;
            border-color: #00ff8c;
            transform: translateX(6px);
            box-shadow: 0px 0px 12px #00ff8c77;
            cursor: pointer;
        }

        /* Selected Button */
        .selected-btn {
            background: #00ff8c;
            color: black !important;
            border: 1px solid #00ff8c;
            font-weight: 800;
            box-shadow: 0px 0px 14px #00ff8caa;
        }

        /* Timeline container */
        .timeline-wrap {
            padding: 22px;
            border-radius: 12px;
            background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.007));
            border: 1px solid rgba(0,255,140,0.02);
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            margin-top: 10px;
        }

        .timeline {
            position: relative;
            margin: 20px 0;
            padding-left: 30px;
        }

        /* Vertical line */
        .timeline::before {
            content: '';
            position: absolute;
            left: 12px;
            top: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, rgba(0,255,140,0.12), rgba(0,200,120,0.08));
            border-radius: 2px;
            box-shadow: 0 8px 30px rgba(0,255,140,0.03);
        }

        .timemarker {
            position: relative;
            margin-bottom: 20px;
            opacity: 0;
            transform: translateY(18px);
            animation: fadeUp 0.55s ease forwards;
        }

        .timemarker:nth-child(1) { animation-delay: 0.05s; }
        .timemarker:nth-child(2) { animation-delay: 0.12s; }
        .timemarker:nth-child(3) { animation-delay: 0.20s; }
        .timemarker:nth-child(4) { animation-delay: 0.28s; }
        .timemarker:nth-child(5) { animation-delay: 0.36s; }
        .timemarker:nth-child(6) { animation-delay: 0.44s; }
        .timemarker:nth-child(7) { animation-delay: 0.52s; }
        .timemarker:nth-child(8) { animation-delay: 0.60s; }
        .timemarker:nth-child(9) { animation-delay: 0.68s; }
        .timemarker:nth-child(10){ animation-delay: 0.76s; }

        @keyframes fadeUp {
            to {
                opacity: 1;
                transform: translateY(0px);
            }
        }

        .time-dot {
            position: absolute;
            left: 0;
            top: 4px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #aaffcc, #00ff8c);
            border: 3px solid #07120a;
            box-shadow: 0 6px 22px rgba(0,255,140,0.12);
        }

        .time-card {
            margin-left: 36px;
            padding: 12px 16px;
            border-radius: 10px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(0,255,140,0.03);
        }

        .time-title {
            color: #e8ffe8;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .time-desc {
            color: #bfeee0;
            margin: 0;
            font-size: 0.98rem;
        }

        .timeline-footer {
            margin-top: 18px;
            padding: 12px;
            border-radius: 10px;
            background: rgba(0,0,0,0.35);
            color: #cfeee0;
            border: 1px solid rgba(0,255,140,0.03);
        }

        /* responsive */
        @media (max-width: 900px) {
            .timeline { padding-left: 10px; }
            .time-card { margin-left: 28px; }
        }
    </style>
""", unsafe_allow_html=True)

# ================================
# GEMINI API CONFIG
# ================================
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# ================================
# TEXT → SPEECH
# ================================
def text_to_audio(text):
    tts = gTTS(text)
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    audio_data = buffer.getvalue()
    st.audio(audio_data, format="audio/mp3")


# ================================
# BADGE SYSTEM
# ================================
def carbon_badge(score):
    if score < 8:
        return "🟢 *Low Carbon Footprint – Eco Friendly!*"
    elif score < 15:
        return "🟡 *Moderate Footprint – Can Improve.*"
    else:
        return "🔴 *High Footprint – Needs Immediate Action.*"


def achievements(score):
    ach = []
    if score < 6:
        ach.append("🌟 Eco-Starter Award")
    if score < 10:
        ach.append("💚 Green Lifestyle Badge")
    if score < 14:
        ach.append("🔥 Carbon Reducer Badge")
    if score >= 14:
        ach.append("⚠ High Emission Alert Badge")
    return ach


# ================================
# SIDEBAR NAVIGATION (UPGRADED)
# ================================
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

st.sidebar.markdown("<div class='sidebar-title'>🌱 Green Energy AI</div>", unsafe_allow_html=True)

def sidebar_button(name, label):
    selected = "selected-btn" if st.session_state["page"] == name else "sidebar-btn"
    if st.sidebar.button(label, key=name):
        st.session_state["page"] = name
    st.sidebar.markdown(f"<div class='{selected}' style='margin-bottom:6px'>{label}</div>", unsafe_allow_html=True)

# buttons (including Timeline)
sidebar_button("Home", "🏠 Home")
sidebar_button("Carbon", "🌍 Carbon Calculator")
sidebar_button("AI", "⚡ Green Energy AI Assistant")
sidebar_button("Timeline", "📅 Timeline")
sidebar_button("About", "ℹ About This App")

page = st.session_state["page"]

# ================================
# HOME PAGE
# ================================
if page == "Home":
    st.title("🌱 Carbon Footprint Analyzer & Green Energy AI")
    st.subheader("Your Premium Science Exhibition Project")

    st.write("""
        Welcome!  
        This application allows you to:
        - ✔ Calculate your **Carbon Footprint**  
        - ✔ Generate a **Pie Chart Breakdown**  
        - ✔ Earn **Eco Achievements & Carbon Badges**  
        - ✔ Ask questions to an advanced **Green Energy AI**  
        - ✔ Hear AI responses using **Text-to-Speech**  
    """)


# ================================
# CARBON CALCULATOR PAGE
# ================================
elif page == "Carbon":

    st.title("🌍 Full Carbon Footprint Calculator")

    # TRANSPORT
    st.header("🚗 Transportation")
    km = st.slider("Daily Travel (km)", 0, 200, 12)
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
    emission_map = {"Petrol":0.118, "Diesel":0.134, "Electric":0.02}
    transport = km * emission_map[fuel]

    # ELECTRICITY
    st.header("💡 Electricity")
    units = st.number_input("Electricity Units per Month", 0, 2000, 120)
    electricity = units * 0.82 / 30

    # LPG
    st.header("🔥 LPG")
    lpg = st.slider("Cylinders per Year", 0, 24, 6)
    lpg_em = (lpg * 42.5) / 365

    # AC
    st.header("❄ Air Conditioner")
    ac_hr = st.slider("AC Hours Per Day", 0, 24, 3)
    ac_em = ac_hr * 1.5 * 0.82

    # GEYSER
    st.header("🚿 Geyser")
    gey = st.slider("Daily Geyser Use (hours)", 0.0, 5.0, 0.7)
    gey_em = gey * 2 * 0.82

    # WASTE
    st.header("🗑 Waste")
    waste = st.slider("Daily Waste (kg)", 0.0, 5.0, 0.4)
    waste_em = waste * 0.09

    # FOOD
    st.header("🍽 Diet Type")
    diet = st.selectbox("Choose Diet", ["Vegetarian", "Eggs", "Chicken", "Fish", "Mixed Non-Veg"])
    food_map = {"Vegetarian":2, "Eggs":3, "Chicken":4.5, "Fish":5.5, "Mixed Non-Veg":6.5}
    food_em = food_map[diet]

    total = transport + electricity + lpg_em + ac_em + gey_em + waste_em + food_em

    if st.button("Calculate My Carbon Footprint"):
        st.success(f"### 🌎 Total Daily Emission: **{total:.2f} kg CO₂/day**")

        st.info(carbon_badge(total))

        st.subheader("🏆 Achievements Earned")
        for a in achievements(total):
            st.write("- " + a)

        # PIE CHART
        labels = ["Transport", "Electricity", "LPG", "AC", "Geyser", "Waste", "Food"]
        values = [transport, electricity, lpg_em, ac_em, gey_em, waste_em, food_em]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)


# ================================
# AI ASSISTANT PAGE
# ================================
elif page == "AI":
    st.title("⚡ Green Energy AI Assistant")

    if not GEMINI_KEY:
        st.error("Gemini API Key Missing!")
    else:
        user_input = st.text_area("Ask a Green Energy Question")

        if st.button("Ask AI"):
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.write(response.text)

            if st.checkbox("🔊 Hear this as Audio"):
                text_to_audio(response.text)


# ================================
# TIMELINE PAGE (NEW)
# ================================
elif page == "Timeline":
    st.title("📅 Timeline of Building This App")

    st.markdown('<div class="timeline-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    timeline_items = [
        ("Day 1", "Concept idea & planning"),
        ("Day 2", "Created base UI structure"),
        ("Day 3", "Added carbon calculator formulas"),
        ("Day 4", "Added pie chart visualization"),
        ("Day 5", "Added badge & achievement system"),
        ("Day 6", "Integrated Gemini AI"),
        ("Day 7", "Added Dark Premium Theme"),
        ("Day 8", "Created Sidebar Navigation"),
        ("Day 9", "Added About section"),
        ("Day 10", "Final polishing for exhibition"),
    ]

    for title, desc in timeline_items:
        st.markdown(f"""
            <div class="timemarker">
                <div class="time-dot"></div>
                <div class="time-card">
                    <div class="time-title">{title}</div>
                    <div class="time-desc">{desc}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # footer statement (as requested)
    st.markdown("""
        <div class="timeline-footer">
            <strong>Note:</strong> This is only the base version of the timeline. Further updates will be added from time to time in a polished way.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ================================
# ABOUT PAGE
# ================================
elif page == "About":
    st.title("ℹ About This App")

    st.markdown("""
        ### 🎯 **Purpose of This App**
        This project helps users:
        - Measure their **daily carbon footprint**
        - Learn how lifestyle affects the planet
        - Understand **renewable energy, sustainability, & eco habits**
        - Use an intelligent **Green Energy AI Assistant**
        - Visualize environmental impact using **charts & badges**
        - Explore climate science in a fun and interactive way

        Built using:
        - **Python + Streamlit**
        - **Gemini AI**
        - **Premium Dark UI**
    """)

    st.markdown("---")

    st.markdown("""
        ### 👤 **Creator**
        ## ⭐ Arsh Kumar Gupta  
        **Class XI–A**

        Kendriya Vidyalaya  
        Rashtriya Bal Vigyanik Utsav
    """)

    st.markdown("---")

    st.markdown("""
        ### 🌟 Vision
        To inspire students to:
        - Think sustainably  
        - Build real solutions for climate change  
        - Create a greener future for India and the world  
    """)
    # ================================
# SIDEBAR NAVIGATION (UPDATED)
# ================================
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

with st.sidebar:
    # Title ABOVE buttons
    st.markdown("<div class='sidebar-title'>🌱 Green Energy AI</div>", unsafe_allow_html=True)

    # Divider line (optional)
    st.markdown("<hr style='border: 1px solid #00ff8c33;'>", unsafe_allow_html=True)

    # Sidebar Buttons
    def sidebar_button(name, label):
        selected_class = "selected-btn" if st.session_state["page"] == name else "sidebar-btn"
        if st.button(label, key=name):
            st.session_state["page"] = name
        st.markdown(f"<div class='{selected_class}'>{label}</div>", unsafe_allow_html=True)

    sidebar_button("Home", "🏠 Home")
    sidebar_button("Carbon", "🌍 Carbon Calculator")
    sidebar_button("AI", "⚡ Green Energy AI Assistant")
    sidebar_button("About", "ℹ About This App")


