# ------------------------------------------------------------
# GreenEnergy Streamlit App (Dark Mode Edition)
# ------------------------------------------------------------
# • Beautiful neon-green dark UI
# • Glassmorphism cards
# • Fully working Gemini integration
# • Offline fallback knowledge
# • Cleaner layout, animations, shadows
# ------------------------------------------------------------

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Try Gemini import
GEMINI_CLIENT_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_CLIENT_AVAILABLE = True
except:
    GEMINI_CLIENT_AVAILABLE = False


# ------------------------------------------------------------
# Dark Mode App Theme
# ------------------------------------------------------------
st.set_page_config(
    page_title="GreenEnergy Suite",
    page_icon="⚡",
    layout="wide"
)

# Inject DARK MODE CSS
st.markdown("""
<style>
/* Background gradient */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0f2027, #07161c 60%, #000000 100%);
    color: #e0e9e7;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027, #0d1b21);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #d2e6d7 !important;
}

/* Headings */
h1, h2, h3 {
    color: #99ffcc !important;
    font-weight: 700;
}

/* Glassmorphism Card */
.card {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 0 20px rgba(0,255,150,0.08);
}

/* Text */
body, p, label {
    color: #d9f8e6 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00ff99, #00cc88);
    padding: 10px 20px;
    color: #000;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    transition: 0.2s;
}
.stButton > button:hover {
    transform: scale(1.04);
    background: linear-gradient(90deg, #33ffbb, #00e699);
}

/* Input fields */
input, textarea, select {
    background: rgba(255,255,255,0.08) !important;
    color: #eafff4 !important;
}

/* DataFrames table */
.dataframe {
    color: white !important;
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
# Offline Knowledge Base
# ------------------------------------------------------------
LOCAL_KB = {
    "renewable energy": (
        "Renewable energy includes sources such as solar, wind, hydro, and geothermal. "
        "They replenish naturally and have extremely low carbon output."
    ),
    "solar panel": (
        "Solar panels convert sunlight into electricity. "
        "Their efficiency depends on angle, temperature, and irradiance."
    ),
    "reduce electricity": (
        "Use LED lights, energy-efficient appliances, natural ventilation, and unplug standby devices."
    ),
    "carbon footprint": (
        "A carbon footprint measures the total greenhouse gases emitted by a person or activity."
    ),
}


def local_answer(q: str) -> str:
    q = q.lower()
    for k in LOCAL_KB:
        if k in q:
            return LOCAL_KB[k]

    return (
        "I don’t have an exact offline answer for this. Try asking about:\n"
        "• Renewable energy\n• Solar panels\n• Electricity saving\n• Carbon footprint"
    )


# ------------------------------------------------------------
# Gemini Query (safe)
# ------------------------------------------------------------
def query_gemini(question, api_key=None):
    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        return "⚠️ No Gemini API key provided."

    if not GEMINI_CLIENT_AVAILABLE:
        return "⚠️ Gemini client not installed. Add `google-generativeai` to requirements."

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
# PAGE FUNCTIONS
# ------------------------------------------------------------
def home_page():
    st.title("⚡ GreenEnergy – Dark Mode Edition")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Welcome to the GreenEnergy App  
    Experience a futuristic carbon-awareness dashboard with:
    - 🧮 Smart Carbon Emission Calculator  
    - 💡 AI Knowledge (Gemini + Offline)  
    - 📤 CSV Bulk Calculator  
    - 🌑 Fully redesigned dark interface  

    Let's make the world greener — one click at a time. 🌱
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def calculator_page():
    st.title("🧮 Carbon Emission Calculator")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("Transport")
    mode = st.selectbox("Mode", ["Car", "Motorbike", "Bus", "Train", "Flight"])
    km = st.number_input("Distance (km)", 0.0)

    if mode == "Car":
        fuel = st.selectbox("Fuel type", ["petrol", "diesel"])
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
    st.write(f"Transport emissions: **{transport:.2f} kg CO₂e**")

    st.header("Electricity")
    kwh = st.number_input("Electricity usage (kWh/month)", 0.0)
    elec = kwh * EMISSION_FACTORS["electricity"]
    st.write(f"Electricity emissions: **{elec:.2f} kg CO₂e**")

    st.header("Food")
    beef = st.number_input("Beef (kg)", 0.0)
    poultry = st.number_input("Poultry (kg)", 0.0)
    veg = st.number_input("Vegetables (kg)", 0.0)
    food = (beef * 27) + (poultry * 6.9) + (veg * 2)

    st.write(f"Food emissions: **{food:.2f} kg CO₂e**")

    st.header("Waste")
    waste = st.number_input("Waste (kg)", 0.0)
    waste_em = waste * EMISSION_FACTORS["waste"]

    st.write(f"Waste emissions: **{waste_em:.2f} kg CO₂e**")

    total = transport + elec + food + waste_em
    st.success(f"🌍 Total Monthly Emissions: **{total:.2f} kg CO₂e**")

    st.markdown('</div>', unsafe_allow_html=True)


def knowledge_page():
    st.title("💡 Green Energy Knowledge (AI + Offline)")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    question = st.text_area("Your question:", height=120)

    st.subheader("Optional: Temporary Gemini API Key")
    temp_key = st.text_input("Enter API Key (not saved):", type="password")

    col1, col2 = st.columns(2)

    if col1.button("🌑 Offline Answer"):
        st.write("### Offline Response")
        st.write(local_answer(question))

    if col2.button("⚡ Gemini Answer"):
        st.write("### Gemini Response")
        st.write(query_gemini(question, api_key=temp_key))

    st.markdown('</div>', unsafe_allow_html=True)


def upload_page():
    st.title("📤 Bulk CSV Carbon Calculator")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write(df)

        results = []
        for _, row in df.iterrows():
            act = row["activity"].lower()
            value = float(row["value"])
            factor = EMISSION_FACTORS.get(act, 0)
            results.append({"activity": act, "value": value, "emissions": value * factor})

        out = pd.DataFrame(results)
        st.write(out)
        st.success(f"Total Emissions: {out['emissions'].sum():.2f} kg CO₂e")

    st.markdown('</div>', unsafe_allow_html=True)


def about_page():
    st.title("ℹ️ About")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("""
    **GreenEnergy Dark Mode Edition**  
    Built with Streamlit, Gemini AI, and offline knowledge features.

    **Setup for Gemini:**
    1. Add to `requirements.txt`:  
       `google-generativeai==0.5.2`
    2. Add Streamlit Cloud Secret:  
       `GEMINI_API_KEY = your_api_key`

    Enjoy the futuristic interface! ⚡🌱
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# NAVIGATION
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
