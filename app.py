import streamlit as st
import google.generativeai as genai
import os

# ----------------------------
# PAGE SETTINGS
# ----------------------------
st.set_page_config(
    page_title="Green Energy & Carbon App",
    page_icon="🌱",
    layout="wide"
)

# ----------------------------
# CUSTOM CSS (Aesthetic Light UI + White Headings)
# ----------------------------
custom_css = """
<style>

/* Full white background for aesthetic look */
.stApp {
    background-color: #f2f7f5 !important;
}

/* White headings */
h1, h2, h3, h4 {
    color: white !important;
}

/* Section cards */
.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Heading banner bar */
.banner {
    background: linear-gradient(135deg, #00c853, #009624);
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    background-color: #00c853 !important;
    color: white !important;
    font-weight: bold;
    border-radius: 8px !important;
}

/* Inputs */
textarea, input {
    background-color: #fafafa !important;
    border-radius: 6px !important;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------------
# GEMINI API CONFIG
# ----------------------------
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Carbon Calculator", "Food Emission", "Green Energy AI"]
)

# ----------------------------
# HOME PAGE
# ----------------------------
if page == "Home":
    st.markdown("<div class='banner'><h1>🌍 Green Energy & Carbon Footprint</h1></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='card'>
            <h3>Welcome!</h3>
            <p>This app helps you calculate carbon emissions and learn more about clean green energy.</p>
            <p>Use the navigation menu to get started.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# CARBON FOOTPRINT CALCULATOR
# ----------------------------
elif page == "Carbon Calculator":
    st.markdown("<div class='banner'><h1>🧮 Carbon Footprint Calculator</h1></div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Enter your usage below to estimate carbon emissions.")
    st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        km = st.number_input("Daily travel (km):", min_value=0.0)
        electricity = st.number_input("Monthly electricity units:", min_value=0.0)
        lpg = st.number_input("LPG cylinders per month:", min_value=0.0)

        if st.button("Calculate Emissions"):
            total = (km * 0.12) + (electricity * 0.82) + (lpg * 2.75)
            st.success(f"Your estimated monthly CO₂ emission is **{total:.2f} kg**")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# FOOD EMISSIONS (NO BEEF)
# ----------------------------
elif page == "Food Emission":
    st.markdown("<div class='banner'><h1>🥗 Food Emission Calculator</h1></div>", unsafe_allow_html=True)

    foods = {
        "Rice": 2.7,
        "Dal": 1.8,
        "Vegetables": 0.5,
        "Fruits": 0.7,
        "Milk": 1.3,
        "Eggs": 4.8,
        "Chicken": 6.9,
        # ❌ Beef Removed
    }

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    food = st.selectbox("Select a food item:", list(foods.keys()))
    qty = st.number_input("Quantity (kg):", min_value=0.0)

    if st.button("Calculate Food Emission"):
        emission = qty * foods[food]
        st.success(f"{food} produces **{emission:.2f} kg CO₂** for {qty} kg.")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# GREEN ENERGY KNOWLEDGE (GEMINI)
# ----------------------------
elif page == "Green Energy AI":
    st.markdown("<div class='banner'><h1>⚡ Ask Gemini About Green Energy</h1></div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    query = st.text_area("Ask anything related to clean/green energy:")

    if st.button("Ask Gemini"):
        if not api_key:
            st.error("❌ GEMINI_API_KEY not configured. Set it in Streamlit Secrets.")
        else:
            response = model.generate_content(query)
            st.markdown("### Answer:")
            st.write(response.text)
    st.markdown("</div>", unsafe_allow_html=True)
