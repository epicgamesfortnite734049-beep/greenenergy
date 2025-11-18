import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Try Gemini import
GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# Streamlit config
st.set_page_config(
    page_title="GreenEnergy - Carbon Calculator",
    page_icon="🌿",
    layout="wide"
)

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
/* Background gradient */
body {
    background: linear-gradient(to bottom right, #e8f5e9, #e3f2fd);
}

/* Big title styling */
.big-title {
    font-size: 3.2rem;
    font-weight: 700;
    color: #2e7d32;
    text-align: center;
    margin-top: 20px;
}

/* Subtitle */
.sub-title {
    font-size: 1.4rem;
    text-align: center;
    color: #4e5d6c;
    margin-bottom: 40px;
}

/* Card container */
.feature-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.1);
    transition: 0.25s;
    height: 230px;
    border: 1px solid #dcedc8;
}

.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
}

/* Buttons */
.stButton>button {
    background-color: #1b5e20;
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
}

.stButton>button:hover {
    background-color: #2e7d32;
}

/* Footer */
.footer {
    text-align: center;
    color: #546e7a;
    margin-top: 50px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)


# ---------------- Emission Factors ---------------- #
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

# ---------------- Gemini Query Function ---------------- #
def query_gemini(prompt, model="gemini-1.5-pro", max_output_tokens=500):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ GEMINI_API_KEY not configured."
    if not GEMINI_AVAILABLE:
        return "⚠️ Gemini library not installed."

    try:
        genai.configure(api_key=api_key)
        response = genai.generate(
            model=model,
            prompt=prompt,
            max_output_tokens=max_output_tokens
        )
        if hasattr(response, "text"):
            return response.text
        return str(response)
    except Exception as e:
        return f"Error: {e}"


# ------------------- Pages -------------------

# ⭐ AESTHETIC HOME PAGE ⭐
def home_page():
    st.markdown('<div class="big-title">🌍 GreenEnergy Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Calculate. Learn. Act — for a Cleaner Planet.</div>', unsafe_allow_html=True)

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h2>🧮 Calculator</h2>
                <p>Estimate CO₂ emissions from transport, food, electricity & more.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("Open Calculator", key="calc"):
            st.session_state.page = "Calculator"

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h2>💡 AI Knowledge</h2>
                <p>Ask Gemini anything about green energy, climate & sustainability.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("Ask Gemini", key="gem"):
            st.session_state.page = "Knowledge (Gemini)"

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h2>📤 Bulk Upload</h2>
                <p>Upload CSV activity data and get full emission analysis instantly.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("Upload CSV", key="upload"):
            st.session_state.page = "Upload CSV"

    st.markdown('<div class="footer">Made with ❤️ for a sustainable future.</div>', unsafe_allow_html=True)



# ---------------- Calculator Page ----------------
def calculator_page():
    st.title("🧮 Carbon Emission Calculator")
    st.write("Estimate your emissions from different lifestyle activities.")

    mode = st.selectbox("Transport Mode", ["Car", "Motorbike", "Bus", "Train", "Flight"])

    if mode == "Car":
        km = st.number_input("Distance (km)", 0.0)
        fuel = st.selectbox("Fuel", ["petrol", "diesel"])
        ef = EMISSION_FACTORS["car_petrol"] if fuel == "petrol" else EMISSION_FACTORS["car_diesel"]
        transport_em = km * ef

    elif mode == "Motorbike":
        km = st.number_input("Distance (km)", 0.0)
        transport_em = km * EMISSION_FACTORS["motorbike"]

    elif mode == "Bus":
        km = st.number_input("Distance (km)", 0.0)
        transport_em = km * EMISSION_FACTORS["bus"]

    elif mode == "Train":
        km = st.number_input("Distance (km)", 0.0)
        transport_em = km * EMISSION_FACTORS["train"]

    else:  # Flight
        km = st.number_input("Flight Distance (km)", 0.0)
        transport_em = km * (EMISSION_FACTORS["flight_short"] if km <= 1500 else EMISSION_FACTORS["flight_long"])

    st.write(f"**Transport Emissions:** {transport_em:.2f} kg CO₂e")

    st.markdown("---")

    kwh = st.number_input("Electricity (kWh/month)", 0.0)
    elec_em = kwh * EMISSION_FACTORS["electricity"]

    beef = st.number_input("Beef (kg/month)", 0.0)
    poultry = st.number_input("Poultry (kg/month)", 0.0)
    veg = st.number_input("Vegetables (kg/month)", 0.0)

    food_em = beef * EMISSION_FACTORS["beef"] + poultry * EMISSION_FACTORS["poultry"] + veg * EMISSION_FACTORS["vegetables"]

    waste = st.number_input("Waste (kg/month)", 0.0)
    waste_em = waste * EMISSION_FACTORS["waste"]

    total = transport_em + elec_em + food_em + waste_em

    st.header(f"🌿 Total Monthly Emissions: **{total:.2f} kg CO₂e**")

    breakdown = pd.DataFrame({
        "Category": ["Transport", "Electricity", "Food", "Waste"],
        "CO₂ (kg)": [transport_em, elec_em, food_em, waste_em]
    })

    fig = px.pie(breakdown, values="CO₂ (kg)", names="Category", title="Emissions Breakdown")
    st.plotly_chart(fig)


# ---------------- Knowledge Page ----------------
def knowledge_page():
    st.title("💡 Green Energy Knowledge (Gemini)")
    prompt = st.text_area("Ask something about sustainability:", height=120)

    if st.button("Ask Gemini"):
        st.write(query_gemini(prompt))


# ---------------- Upload CSV Page ----------------
def upload_page():
    st.title("📤 Upload CSV to Analyze Emissions")
    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write(df)

        results = []

        for _, r in df.iterrows():
            act = str(r.get("activity", "")).lower()
            val = float(r.get("value", 0))

            if act == "car":
                fuel = r.get("subtype", "petrol")
                ef = EMISSION_FACTORS["car_petrol"] if fuel == "petrol" else EMISSION_FACTORS["car_diesel"]
                em = val * ef

            elif act == "motorbike":
                em = val * EMISSION_FACTORS["motorbike"]

            elif act == "bus":
                em = val * EMISSION_FACTORS["bus"]

            elif act == "train":
                em = val * EMISSION_FACTORS["train"]

            elif act == "flight":
                em = val * (EMISSION_FACTORS["flight_short"] if val <= 1500 else EMISSION_FACTORS["flight_long"])

            elif act == "electricity":
                em = val * EMISSION_FACTORS["electricity"]

            elif act in ["beef", "poultry", "vegetables"]:
                em = val * EMISSION_FACTORS.get(act, 0)

            else:
                em = 0

            results.append({"activity": act, "value": val, "emissions": em})

        out = pd.DataFrame(results)
        st.write(out)

        st.success(f"Total Emissions: {out['emissions'].sum():.2f} kg CO₂e")

        st.download_button("Download Results CSV", out.to_csv(index=False), "results.csv")


# ---------------- About Page ----------------
def about_page():
    st.title("ℹ️ About")
    st.write("""
    **GreenEnergy App**
    - Calculates carbon footprint  
    - Offers green energy knowledge via Gemini  
    - Supports CSV uploads  
    """)


# ---------------- Navigation ----------------
PAGES = {
    "Home": home_page,
    "Calculator": calculator_page,
    "Knowledge (Gemini)": knowledge_page,
    "Upload CSV": upload_page,
    "About": about_page,
}

choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
PAGES[choice]()
