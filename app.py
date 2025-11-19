import streamlit as st
import google.generativeai as genai

# ------------------------
# CONFIGURATION
# ------------------------
st.set_page_config(
    page_title="Green Energy & Carbon Calculator",
    page_icon="🌱",
    layout="wide"
)

# Apply dark mode + custom text styling
custom_css = """
<style>

/* Dark background */
body, .stApp {
    background-color: #121212 !important;
}

/* White headline */
h1, h2, h3 {
    color: white !important;
}

/* All other text black */
p, span, label, .stMarkdown, .stTextInput label {
    color: black !important;
}

/* Card-like section */
.block {
    background: #1e1e1e;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0px 0px 10px #00000050;
}

/* Input and text areas */
textarea, input {
    background-color: #e6e6e6 !important;
    color: black !important;
}

.stButton>button {
    background-color: #00c853 !important;
    color: black !important;
    border-radius: 8px;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------
# GEMINI API CONFIG
# ------------------------
import os
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
    "Navigation",
    ["Home", "Carbon Emission Calculator", "Green Energy Knowledge"]
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
            <p>This app helps you calculate your carbon footprint and learn more about clean, green energy sources.</p>
            <p>Use the menu on the left to get started.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------
# CARBON EMISSION CALCULATOR
# ------------------------
elif page == "Carbon Emission Calculator":
    st.markdown("<h1>🧮 Carbon Emissions Calculator</h1>", unsafe_allow_html=True)

    st.markdown("<h3>Enter your details below:</h3>", unsafe_allow_html=True)

    transport_km = st.number_input("Daily transport distance (km):", min_value=0.0)
    electricity_units = st.number_input("Monthly electricity usage (units):", min_value=0.0)
    lpg_cylinders = st.number_input("LPG cylinders per month:", min_value=0.0)

    if st.button("Calculate Carbon Footprint"):
        total_emissions = (transport_km * 0.12) + (electricity_units * 0.82) + (lpg_cylinders * 2.75)

        st.success(f"Your estimated monthly carbon emission is **{total_emissions:.2f} kg CO₂**")


# ------------------------
# GREEN ENERGY KNOWLEDGE PAGE (GEMINI)
# ------------------------
elif page == "Green Energy Knowledge":
    st.markdown("<h1>⚡ Green Energy Knowledge (Gemini Powered)</h1>", unsafe_allow_html=True)

    question = st.text_area("Ask anything about green energy:")

    if st.button("Ask Gemini"):
        if not api_key:
            st.error("❌ GEMINI_API_KEY not configured. Please set it in Streamlit secrets.")
        else:
            response = model.generate_content(question)
            st.write("### Answer:")
            st.write(response.text)
