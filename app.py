# ------------------------------------------------------------
# GreenEnergy Streamlit App (Dark Mode + Black Text Version)
# ------------------------------------------------------------
# • Dark background
# • Black text everywhere
# • Updated UI styling
# ------------------------------------------------------------

import os
import streamlit as st
import pandas as pd

# Try Gemini import
GEMINI_CLIENT_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_CLIENT_AVAILABLE = True
except:
    GEMINI_CLIENT_AVAILABLE = False


# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="GreenEnergy Suite",
    page_icon="⚡",
    layout="wide"
)

# ------------------------------------------------------------
# DARK BACKGROUND + BLACK TEXT
# ------------------------------------------------------------
st.markdown("""
<style>
/* Dark background */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0f2027, #07161c 60%, #000000 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #0d1b21);
}

/* Black text everywhere */
*, body, label, p, div, span, .stMarkdown, .stText, .markdown-text-container {
    color: black !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: black !important;
    font-weight: 700;
}

/* Glassmorphism Cards */
.card {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(8px);
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00ff99, #00cc88);
    padding: 10px 20px;
    color: black !important;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    transition: 0.2s;
}
.stButton > button:hover {
    transform: scale(1.04);
    background: linear-gradient(90deg, #33ffbb, #00e699);
}

/* Inputs */
input, textarea, select {
    background: rgba(255,255,255,0.85) !important;
    color: black !important;
}

/* Table text */
.dataframe {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Emission Factors
# ------------------------------------------------------------
EMISSION_FACTORS = {
    "car_petrol": 0.192,
    "car_diesel": 0.171,
    "motorbike": 0.103,
    "bus": 0.089,
    "train": 0.041,
    "electricity": 0.82,
    "flight_short": 0.255,
    "flight_long": 0.195,
    "beef": 27.0,
    "poultry": 6.9,
    "vegetables": 2.0,
    "waste": 0.45
}


# ------------------------------------------------------------
# Local Knowledge Base
# ------------------------------------------------------------
LOCAL_KB = {
    "renewable energy": (
        "Renewable energy includes solar, wind, hydro, and geothermal sources."
    ),
    "solar panel": (
        "Solar panels convert sunlight into usable electricity."
    ),
    "reduce electricity": (
        "Use LED bulbs, energy-efficient appliances, and unplug devices."
    ),
    "carbon footprint": (
        "Carbon footprint = total greenhouse gases produced by an activity."
    ),
}


def local_answer(q):
    q = q.lower()
    for k in LOCAL_KB:
        if k in q:
            return LOCAL_KB[k]
    return "No exact offline answer found. Try asking about renewable energy, solar panels, or electricity saving."


# ------------------------------------------------------------
# Gemini Query
# ------------------------------------------------------------
def query_gemini(question, api_key=None):
    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        return "⚠️ No Gemini API key provided."

    if not GEMINI_CLIENT_AVAILABLE:
        return "⚠️ Gemini library missing."

    try:
        genai.configure(api_key=key)
        response = genai.generate(
            model="gemini-1.5-pro",
            prompt=question,
            max_output_tokens=600
        )
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"❌ Gemini Error: {e}"


# ------------------------------------------------------------
# Pages
# ------------------------------------------------------------
def home_page():
    st.title("⚡ GreenEnergy – Dark Mode (Black Text Edition)")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Welcome to GreenEnergy  
    - Carbon emission calculator  
    - AI knowledge (Gemini + Offline)  
    - CSV bulk calculator  
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def calculator_page():
    st.title("🧮 Carbon Emission Calculator")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("Transport")
    mode = st.selectbox("Mode", ["Car", "Motorbike", "Bus", "Train", "Flight"])
    km = st.number_input("Distance (km)", 0.0)

    if mode == "Car":
        fuel = st.selectbox("Fuel Type", ["petrol", "diesel"])
        factor = EMISSION_FACTORS[f"car_{fuel}"]
    elif mode == "Motorbike":
        factor = EMISSION_FACTORS["motorbike"]
    elif mode == "Bus":
        factor = EMISSION_FACTORS["bus"]
    elif mode == "Train":
        factor = EMISSION_FACTORS["train"]
    else:
        factor = EMISSION_FACTORS["flight_short"] if km <= 1500 else EMISSION_FACTORS["flight_long"]

    transport = km * factor

    st.write(f"Transport: **{transport:.2f} kg CO₂e**")

    st.header("Electricity")
    kwh = st.number_input("Electricity (kWh)", 0.0)
    elec = kwh * EMISSION_FACTORS["electricity"]
    st.write(f"Electricity: **{elec:.2f} kg CO₂e**")

    st.header("Food")
    beef = st.number_input("Beef (kg)", 0.0)
    poultry = st.number_input("Poultry (kg)", 0.0)
    veg = st.number_input("Vegetables (kg)", 0.0)
    food = beef * 27 + poultry * 6.9 + veg * 2

    st.write(f"Food: **{food:.2f} kg CO₂e**")

    st.header("Waste")
    waste = st.number_input("Waste (kg)", 0.0)
    waste_em = waste * 0.45

    st.write(f"Waste: **{waste_em:.2f} kg CO₂e**")

    total = transport + elec + food + waste_em
    st.success(f"🌍 **Total: {total:.2f} kg CO₂e**")

    st.markdown('</div>', unsafe_allow_html=True)


def knowledge_page():
    st.title("💡 Green Energy Knowledge")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    question = st.text_area("Ask your question:", height=120)

    temp_key = st.text_input("Gemini API Key (optional):", type="password")

    col1, col2 = st.columns(2)

    if col1.button("Offline Answer"):
        st.write(local_answer(question))

    if col2.button("Gemini Answer"):
        st.write(query_gemini(question, api_key=temp_key))

    st.markdown('</div>', unsafe_allow_html=True)


def upload_page():
    st.title("📤 Bulk CSV Calculator")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write(df)

        results = []
        for _, row in df.iterrows():
            act = row["activity"].lower()
            val = float(row["value"])
            factor = EMISSION_FACTORS.get(act, 0)
            results.append({"activity": act, "value": val, "emissions": val * factor})

        out = pd.DataFrame(results)
        st.write(out)
        st.success(f"Total: {out['emissions'].sum():.2f} kg CO₂e")

    st.markdown('</div>', unsafe_allow_html=True)


def about_page():
    st.title("ℹ️ About")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("""
    GreenEnergy Dark Mode with Black Text.  
    Add this to requirements:
    - google-generativeai==0.5.2

    Add secret in Streamlit Cloud:
    `GEMINI_API_KEY = your_key`
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------
pages = {
    "Home": home_page,
    "Calculator": calculator_page,
    "Knowledge": knowledge_page,
    "Upload CSV": upload_page,
    "About": about_page
}

choice = st.sidebar.radio("Navigation", list(pages.keys()))
pages[choice]()
