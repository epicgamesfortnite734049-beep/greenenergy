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

# Dark theme styling
st.markdown("""
    <style>
        body {
            color: black;
            background-color: #111;
        }
        .stApp {
            background-color: #111;
        }
        h1, h2, h3, h4 {
            color: white !important;
        }
        label, p, span, div {
            color: white !important;
        }
        .stSlider label, .stNumberInput label {
            color: white !important;
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
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Home", 
     "🌍 Carbon Footprint Calculator",
     "⚡ Green Energy AI"]
)

# =====================================================================
# PAGE 1 : HOME
# =====================================================================
if page == "🏠 Home":
    st.title("🌱 Carbon Footprint Analyzer & Green Energy Assistant")
    st.subheader("A Science Exhibition Project")
    st.write("""
    This app helps you calculate your **complete carbon footprint**, visualize it using **pie charts**,  
    and learn about **renewable energy technologies** using AI-powered explanations.
    """)

    st.write("Use the menu on the left to begin!")

# =====================================================================
# PAGE 2 : CARBON FOOTPRINT CALCULATOR
# =====================================================================
elif page == "🌍 Carbon Footprint Calculator":
    st.title("🌍 Full Carbon Footprint Calculator")

    st.write("### 📝 Exhibition-Grade Detailed Questionnaire")
    st.write("Answer the questions below to calculate your total emissions.")

    # --------------------------
    # TRANSPORT
    # --------------------------
    st.header("🚗 Transportation")
    km_daily = st.slider("How many KM do you travel per day (bike/scooter/car)?", 0, 150, 10)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
    note_transport = st.caption("Transport contributes 30–40% of personal carbon emissions in urban India.")

    if fuel_type == "Petrol":
        transport_emission = km_daily * 0.118
    elif fuel_type == "Diesel":
        transport_emission = km_daily * 0.134
    else:
        transport_emission = km_daily * 0.02  # EV grid emissions
    
    # --------------------------
    # ELECTRICITY
    # --------------------------
    st.header("💡 Electricity Usage")
    units_month = st.number_input("Monthly Electricity Consumption (in units)", 0, 2000, 150)
    st.caption("India’s electricity grid emits ~0.82 kg CO₂ per kWh.")
    electricity_emission = units_month * 0.82 / 30

    # --------------------------
    # LPG
    # --------------------------
    st.header("🔥 Cooking (LPG)")
    lpg_refills = st.slider("How many LPG cylinders do you use per year?", 0, 24, 6)
    st.caption("Each LPG cylinder = 42.5 kg CO₂")
    lpg_emission = (lpg_refills * 42.5) / 365

    # --------------------------
    # AC USAGE
    # --------------------------
    st.header("❄ Air Conditioner Usage")
    ac_hours = st.slider("Average AC usage per day (hours)", 0, 24, 4)
    st.caption("AC contributes heavily due to high electricity consumption.")
    ac_emission = ac_hours * 1.5 * 0.82  # 1.5 kW AC

    # --------------------------
    # WATER HEATER
    # --------------------------
    st.header("🚿 Water Heater (Geyser)")
    geyser_hours = st.slider("Geyser usage per day (hours)", 0.0, 5.0, 0.5)
    st.caption("Geyser = 2 kW load → major winter emission source.")
    geyser_emission = geyser_hours * 2 * 0.82

    # --------------------------
    # WASTE GENERATION
    # --------------------------
    st.header("🗑 Waste Generation")
    waste_kg = st.slider("Daily Waste Generated (kg)", 0.0, 5.0, 0.5)
    st.caption("Organic waste emits methane, 28× more harmful than CO₂.")
    waste_emission = waste_kg * 0.09

    # --------------------------
    # FOOD FOOTPRINT
    # --------------------------
    st.header("🍽 Food-Related Emissions")
    food_choice = st.selectbox("Your usual diet?", 
                               ["Vegetarian", "Eggs", "Chicken", "Fish", "Mixed Non-Veg"])

    food_emit_map = {
        "Vegetarian": 2.0,
        "Eggs": 3.0,
        "Chicken": 4.5,
        "Fish": 5.5,
        "Mixed Non-Veg": 6.5
    }
    food_emission = food_emit_map[food_choice]

    # --------------------------------------------------
    # TOTAL EMISSION
    # --------------------------------------------------
    total = (transport_emission + electricity_emission + lpg_emission +
             ac_emission + geyser_emission + waste_emission + food_emission)

    if st.button("Calculate My Carbon Footprint"):
        st.success(f"### 🌎 Your Total Daily Carbon Footprint: **{total:.2f} kg CO₂/day**")

        # PIE CHART VISUALIZATION
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
elif page == "⚡ Green Energy AI":
    st.title("⚡ AI Green Energy Assistant")

    if not GEMINI_KEY:
        st.error("Gemini API Key not configured!")
    else:
        st.write("Ask anything about Green Energy and Sustainability!")

        preset_topics = [
            "How does solar power work?",
            "Advantages of wind turbines",
            "What is net metering?",
            "How do electric vehicles reduce emissions?",
            "Biogas plant for home – explain",
            "Hydrogen fuel cells working principle",
            "Geothermal energy in India",
            "Battery storage and lithium-ion technology",
            "How can schools become carbon neutral?",
            "What is carbon trading?"
        ]

        topic = st.selectbox("Choose a topic", preset_topics)
        q = st.text_area("Or type your own question:")

        ask = q if q.strip() != "" else topic

        if st.button("Ask AI"):
            model = genai.GenerativeModel("gemini-pro")
            res = model.generate_content(ask)
            st.write(res.text)
