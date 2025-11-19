import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import os

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Green Energy & Carbon App",
    page_icon="🌱",
    layout="wide"
)

# ------------------------------------------------------
# CUSTOM UI (Aesthetic Light Theme + White Headings)
# ------------------------------------------------------
custom_css = """
<style>

.stApp {
    background-color: #f2f7f5 !important;
}

/* White headings */
h1, h2, h3, h4 {
    color: white !important;
}

/* Card containers */
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

/* Header Banner */
.banner {
    background: linear-gradient(135deg, #00c853, #009624);
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 25px;
}

/* Buttons */
.stButton>button {
    background-color: #00c853 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
}

textarea, input {
    background-color: #fafafa !important;
    border-radius: 6px !important;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------------------------------------
# GEMINI CONFIG
# ------------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None


# ------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Carbon Footprint Calculator", "Green Energy AI"]
)

# ------------------------------------------------------
# HOME
# ------------------------------------------------------
if page == "Home":
    st.markdown("<div class='banner'><h1>🌍 Green Energy & Carbon Footprint</h1></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='card'>
            <h3>Welcome!</h3>
            <p>This project helps calculate carbon emissions for transport, electricity, LPG, and food—
            perfect for Indian school science exhibitions.</p>

            <p>It also includes an AI section to learn about Renewable Energy, Solar Power, Wind Energy, EVs,
            and more!</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------
# COMBINED CARBON FOOTPRINT CALCULATOR
# ------------------------------------------------------
elif page == "Carbon Footprint Calculator":

    st.markdown("<div class='banner'><h1>🧮 Complete Carbon Footprint Calculator</h1></div>", unsafe_allow_html=True)

    st.markdown("<h3>Select & Enter Your Daily/Monthly Usage Below</h3>")

    # ------ Transport Section ------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🚗 Transport Emissions")

    km = st.number_input("Daily Travel Distance (km):", min_value=0.0)
    transport_emission = km * 0.12   # Indian avg = 0.12 kg CO2 per km

    st.markdown("</div>", unsafe_allow_html=True)

    # ------ Electricity & LPG ------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚡ Home Energy Emissions")

    elec_units = st.number_input("Monthly Electricity Usage (Units/kWh):", min_value=0.0)
    lpg = st.number_input("Monthly LPG Cylinders:", min_value=0.0)

    electricity_emission = elec_units * 0.82   # India avg
    lpg_emission = lpg * 2.75

    st.markdown("</div>", unsafe_allow_html=True)

    # ------ Food Emissions ------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🥗 Food Emissions (Common Indian Items)")

    foods = {
        "Rice": 2.7,
        "Wheat Flour (Atta)": 1.4,
        "Dal": 1.8,
        "Vegetables": 0.5,
        "Fruits": 0.7,
        "Milk": 1.3,
        "Paneer": 5.5,
        "Eggs": 4.8,
        "Chicken": 6.9,
        "Mutton": 24.0,
        "Beef": 27.0  # kept for scientific comparison
    }

    food_item = st.selectbox("Select Food Item:", list(foods.keys()))
    qty = st.number_input("Quantity per Month (kg):", min_value=0.0)

    food_emission = qty * foods[food_item]

    st.markdown("</div>", unsafe_allow_html=True)

    # ------ Total & PIE CHART ------
    if st.button("Calculate Total Carbon Footprint"):

        total = transport_emission + electricity_emission + lpg_emission + food_emission

        st.success(f"### 🌡 Your Total Monthly Carbon Emission: **{total:.2f} kg CO₂**")

        labels = ["Transport", "Electricity", "LPG", "Food"]
        values = [transport_emission, electricity_emission, lpg_emission, food_emission]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title("Carbon Footprint Breakdown")

        st.pyplot(fig)


# ------------------------------------------------------
# GREEN ENERGY AI
# ------------------------------------------------------
elif page == "Green Energy AI":
    st.markdown("<div class='banner'><h1>⚡ Green Energy AI Assistant</h1></div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.write("Choose a topic or type your own question:")

    topics = [
        "Solar Energy Basics",
        "How do solar panels work?",
        "Wind Energy in India",
        "Hydropower generation process",
        "What is green hydrogen?",
        "EV (Electric Vehicle) advantages",
        "Geothermal Energy",
        "Biogas & Biofuel",
        "Smart Grids",
        "Future of Renewable Energy"
    ]

    col1, col2 = st.columns(2)

    with col1:
        topic = st.selectbox("Popular Topics:", topics)

    query = st.text_area("Ask any question:")

    final_query = query if query.strip() else topic

    if st.button("Ask Gemini"):
        if not api_key:
            st.error("❌ GEMINI_API_KEY is missing.")
        else:
            response = model.generate_content(final_query)
            st.markdown("### ✨ Answer:")
            st.write(response.text)

    st.markdown("</div>", unsafe_allow_html=True)
