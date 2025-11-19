import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt

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

        /* MAIN BACKGROUND */
        .stApp {
            background-color: #0c0c0c !important;
        }

        /* GENERAL TEXT */
        body, label, p, span, div {
            color: white !important;
        }

        /* HEADINGS */
        h1, h2, h3, h4 {
            color: white !important;
            font-weight: 700;
        }

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
import os
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# -----------------------------
# COOLEST NAVIGATION BAR
# -----------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

st.markdown('<div class="cool-navbar">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])

# HOME BUTTON
if col1.button("🏠 Home"):
    st.session_state["page"] = "Home"

# CALCULATOR BUTTON
if col2.button("🌍 Carbon Calculator"):
    st.session_state["page"] = "Carbon"

# AI BUTTON
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
    This tool calculates your **full carbon footprint**, shows a **pie-chart visualization**,  
    and teaches you about **renewable energy** using AI.
    """)

# =====================================================================
# PAGE 2 : CARBON FOOTPRINT CALCULATOR
# =====================================================================
elif page == "Carbon":
    st.title("🌍 Complete Carbon Footprint Calculator")

    st.write("### 📝 Detailed Questionnaire (Science Exhibition Level)")

    # --------------------------
    # TRANSPORT
    # --------------------------
    st.header("🚗 Transportation")
    km_daily = st.slider("How many KM do you travel per day?", 0, 200, 10)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
    st.caption("Transport accounts for up to 40% of emissions in Indian cities.")

    if fuel_type == "Petrol":
        transport_emission = km_daily * 0.118
    elif fuel_type == "Diesel":
        transport_emission = km_daily * 0.134
    else:
        transport_emission = km_daily * 0.02

    # --------------------------
    # ELECTRICITY
    # --------------------------
    st.header("💡 Electricity Usage")
    units_month = st.number_input("Electricity units per month (kWh)", 0, 2000, 150)
    st.caption("India’s grid emits ~0.82 kg CO₂ per unit.")
    electricity_emission = units_month * 0.82 / 30

    # --------------------------
    # LPG
    # --------------------------
    st.header("🔥 LPG Usage")
    lpg_refills = st.slider("LPG cylinders used per year", 0, 24, 6)
    lpg_emission = (lpg_refills * 42.5) / 365

    # --------------------------
    # AC USAGE
    # --------------------------
    st.header("❄ Air Conditioner Usage")
    ac_hours = st.slider("Daily AC usage (hours)", 0, 24, 4)
    ac_emission = ac_hours * 1.5 * 0.82

    # --------------------------
    # WATER HEATER
    # --------------------------
    st.header("🚿 Geyser / Water Heater")
    geyser_hours = st.slider("Daily geyser usage (hours)", 0.0, 5.0, 0.5)
    geyser_emission = geyser_hours * 2 * 0.82

    # --------------------------
    # WASTE GENERATION
    # --------------------------
    st.header("🗑 Waste Generation")
    waste_kg = st.slider("Daily waste generated (kg)", 0.0, 5.0, 0.5)
    waste_emission = waste_kg * 0.09

    # --------------------------
    # FOOD EMISSION
    # --------------------------
    st.header("🍽 Diet Based Emissions")
    food_choice = st.selectbox("Your Diet Type", 
        ["Vegetarian", "Eggs", "Chicken", "Fish", "Mixed Non-Veg"])
    food_emit_map = {
        "Vegetarian": 2.0,
        "Eggs": 3.0,
        "Chicken": 4.5,
        "Fish": 5.5,
        "Mixed Non-Veg": 6.5
    }
    food_emission = food_emit_map[food_choice]

    total = (transport_emission + electricity_emission + lpg_emission +
             ac_emission + geyser_emission + waste_emission + food_emission)

    if st.button("Calculate Footprint"):
        st.success(f"### 🌎 Total Daily Carbon Emission: **{total:.2f} kg CO₂/day**")

        labels = ["Transport", "Electricity", "LPG", "AC", "Geyser", "Waste", "Food"]
        values = [
            transport_emission,
            electricity_emission,
            lpg_emission,
            ac_emission,
            geyser_emission,
            waste_emission,
            food_emission
        ]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Carbon Emission Breakdown")
        st.pyplot(fig)

# =====================================================================
# PAGE 3 : GREEN ENERGY AI
# =====================================================================
elif page == "AI":
    st.title("⚡ Green Energy AI Assistant")

    if not GEMINI_KEY:
        st.error("Gemini API Key is missing. Add it in Streamlit Secrets.")
    else:
        st.write("Ask anything about green energy, sustainability, and renewable tech!")

        preset_topics = [
            "How does solar energy work?",
            "Explain wind turbines for students.",
            "What is net metering in India?",
            "How EVs help reduce carbon emissions?",
            "How does a biogas plant work?",
            "Explain hydrogen fuel cells.",
            "Is geothermal energy possible in India?",
            "How lithium-ion batteries store energy?",
            "How can homes become carbon-neutral?",
            "What is carbon trading?"
        ]

        topic = st.selectbox("Choose a topic:", preset_topics)
        question = st.text_area("Or type your own question:")

        final_q = question if question.strip() else topic

        if st.button("Ask AI"):
            model = genai.GenerativeModel("gemini-pro")
            res = model.generate_content(final_q)
            st.write(res.text)
