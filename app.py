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
# DARK MODE THEME
# ================================
st.markdown("""
    <style>
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
        .css-1d391kg, .css-1lcbmhc {
            background-color: #111 !important;
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #0f0f0f !important;
            border-right: 1px solid #00ff8c33;
        }
        .sidebar-title {
            font-size: 26px;
            font-weight: 800;
            color: #00ffae;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Sidebar Buttons */
        .sidebar-btn {
            padding: 12px;
            margin-top: 8px;
            font-size: 18px;
            border-radius: 8px;
            text-align: center;
            background-color: #1a1a1a;
            color: white;
            border: 1px solid #00ff8c55;
            transition: 0.25s;
        }
        .sidebar-btn:hover {
            background-color: #00ff8c55;
            cursor: pointer;
        }
        .selected-btn {
            background-color: #00ff8c !important;
            color: black !important;
            border: 1px solid #00ff8c;
            font-weight: 700;
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
# SIDEBAR NAVIGATION
# ================================
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

st.sidebar.markdown("<div class='sidebar-title'>🌱 Green Energy AI</div>", unsafe_allow_html=True)

def sidebar_button(name, label):
    selected = "selected-btn" if st.session_state["page"] == name else "sidebar-btn"
    if st.sidebar.button(label, key=name):
        st.session_state["page"] = name
    st.sidebar.markdown(f"<div class='{selected}'>{label}</div>", unsafe_allow_html=True)


sidebar_button("Home", "🏠 Home")
sidebar_button("Carbon", "🌍 Carbon Calculator")
sidebar_button("AI", "⚡ Green Energy AI Assistant")
sidebar_button("About", "ℹ About This App")


page = st.session_state["page"]

# ================================
# PAGE: HOME
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
# PAGE: CARBON CALCULATOR
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

        # PIE CHART VISUAL
        labels = ["Transport", "Electricity", "LPG", "AC", "Geyser", "Waste", "Food"]
        values = [transport, electricity, lpg_em, ac_em, gey_em, waste_em, food_em]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)


# ================================
# PAGE: AI ASSISTANT
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
# PAGE: ABOUT THIS APP
# ================================
elif page == "About":
    st.title("ℹ About This App")

    st.markdown("""
        ### 🎯 **Purpose of This App**
        This project has been created to help users:
        - Measure their **daily carbon footprint**
        - Understand how daily lifestyle choices impact the environment
        - Learn about **renewable energy, sustainability, and green technology**
        - Interact with an intelligent **Green Energy AI Assistant**
        - Visualize environmental impact using **pie charts & badges**
        - Develop curiosity toward **climate science & eco innovation**

        It aims to create awareness among students about:
        - Carbon emissions  
        - Climate change  
        - Energy conservation  
        - Practical methods of reducing personal environmental impact  
        - Green habits that can be adopted in everyday life  

        This app uses:
        - **Python + Streamlit** for UI  
        - **Gemini AI** for answering green energy questions  
        - **Advanced Carbon Emission formulas**  
        - **Dark premium interface** for modern presentation  
    """)

    st.markdown("---")

    st.markdown("""
        ### 👤 **Creator**
        This innovative science exhibition project is proudly created by:

        ## ⭐ **Arsh Kumar Gupta**  
        **Class XI–A**

        Kendriya Vidyalaya  
        Rashtriya Bal Vigyanik Utsav  
    """)

    st.markdown("---")

    st.markdown("""
        ### 🌟 **Vision**
        To inspire a generation of students to:
        - Think sustainably  
        - Use technology to solve real-world climate problems  
        - Build a greener future for India and the world  
    """)


