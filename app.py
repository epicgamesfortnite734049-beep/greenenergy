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
# DARK PREMIUM THEME + SMOOTH SIDEBAR
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
            padding-top: 20px;
            transition: 0.3s ease;
        }

        /* Sidebar Title */
        .sidebar-title {
            font-size: 28px;
            font-weight: 900;
            color: #00ffae;
            text-align: center;
            margin-bottom: 30px;
            letter-spacing: 1px;
            text-shadow: 0px 0px 12px #00ffaeaa;
        }

        /* Sidebar Buttons (new premium style) */
        .sidebar-btn {
            padding: 12px 20px;
            margin: 10px 8px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 500;
            color: #e3e3e3;
            text-align: center;
            border: 1px solid #00ff8c33;
            background: rgba(20,20,20,0.7);
            backdrop-filter: blur(4px);
            transition: 0.25s ease-in-out;
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
            font-weight: 700;
            box-shadow: 0px 0px 12px #00ff8caa;
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

    st.sidebar.markdown(f"<div class='{selected}'>{label}</div>", unsafe_allow_html=True)


# New Smooth Animated Buttons
sidebar_button("Home", "🏠 Home")
sidebar_button("Carbon", "🌍 Carbon Calculator")
sidebar_button("AI", "⚡ Green Energy AI Assistant")
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
