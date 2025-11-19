import streamlit as st
import google.generativeai as genai
import os

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="Green Energy & Carbon Calculator",
    page_icon="🌱",
    layout="wide"
)

# ------------------------
# CUSTOM DARK THEME + TEXT COLORS
# ------------------------
custom_css = """
<style>

body, .stApp {
    background-color: #121212 !important;
}

/* Headings white */
h1, h2, h3, h4 {
    color: white !important;
}

/* All other text black */
p, label, span, .stMarkdown, .stTextInput, .stNumberInput label {
    color: black !important;
}

/* Card-style sections */
.block {
    background: #1e1e1e;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 25px;
    box-shadow: 0px 0px 10px #00000055;
}

/* Inputs */
textarea, input {
    background-color: #e6e6e6 !important;
    color: black !important;
    border-radius: 6px !important;
}

/* Buttons */
.stButton>button {
    background-color: #4caf50 !important;
    color: black !important;
    border-radius: 8px !important;
    font-weight: 600;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------
# GEMINI CONFIG
# ------------------------
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None

# ------------------------
# NAVIGATION
# ------------------------
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Carbon Calculator", "Food Emission", "Green Energy AI"]
)

# ------------------------
# HOME PAGE
# ------------------------
if page == "Home":
    st.markdown("<h1>🌍 Green Energy & Carbon Footprint App</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='block'>
        <h3>Welcome!</h3>
        <p>This app helps you calculate carbon emissions and learn about green energy.</p>
        <p>Use the menu to explore the tools.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------
# CARBON FOOTPRINT CALCULATOR
# ------------------------
elif page == "Carbon Calculator":
    st.markdown("<h1>🧮 Carbon Footprint Calculator</h1>", unsafe_allow_html=True)

    st.markdown("<h3>Enter your daily and monthly usage:</h3>", unsafe_allow_html=True)

    km = st.number_input("Daily travel (km):", min_value=0.0)
    electricity = st.number_input("Monthly electricity (units):", min_value=0.0)
    lpg = st.number_input("Monthly LPG cylinders:", min_value=0.0)

    if st.button("Calculate Emissions"):
        total = (km * 0.12) + (electricity * 0.82) + (lpg * 2.75)
        st.success(f"Your estimated monthly CO₂ emission is **{total:.2f} kg**")


# ------------------------
# FOOD EMISSION SECTION (Without Beef)
# ------------------------
elif page == "Food Emission":
    st.markdown("<h1>🥗 Food Carbon Emissions</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='block'>
        <h3>Food Emission Calculator</h3>
        <p>Select a food item to estimate its carbon footprint.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    foods = {
        "Rice": 2.7,
        "Dal": 1.8,
        "Vegetables": 0.5,
        "Fruits": 0.7,
        "Milk": 1.3,
        "Eggs": 4.8,
        "Chicken": 6.9,
        # ❌ Beef section removed as requested
    }

    choice = st.selectbox("Select food item:", list(foods.keys()))
    qty = st.number_input("Quantity (kg):", min_value=0.0)

    if st.button("Calculate Food Emission"):
        emission = qty * foods[choice]
        st.success(f"{choice} produces **{emission:.2f} kg CO₂** per {qty} kg.")


# ------------------------
# GREEN ENERGY KNOWLEDGE (GEMINI AI)
# ------------------------
elif page == "Green Energy AI":
    st.markdown("<h1>⚡ Ask AI About Green Energy</h1>", unsafe_allow_html=True)

    question = st.text_area("Ask your question:")

    if st.button("Ask Gemini"):
        if not api_key:
            st.error("❌ GEMINI_API_KEY not configured. Please set it in Streamlit secrets.")
        else:
            response = model.generate_content(question)
            st.markdown("### Answer:")
            st.write(response.text)

