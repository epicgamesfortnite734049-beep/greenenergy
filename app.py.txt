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

# Streamlit page setup
st.set_page_config(page_title="GreenEnergy - Carbon Calculator", page_icon="🌱", layout="wide")

# Emission Factors (kg CO₂e)
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
        return "⚠️ GEMINI_API_KEY not configured. Set it in Streamlit Cloud."

    if not GEMINI_AVAILABLE:
        return "⚠️ Gemini library not installed. Add google-generative-ai to requirements.txt"

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


# ---------------- Streamlit UI Pages ---------------- #
def home_page():
    st.title("🌱 GreenEnergy Suite")
    st.subheader("Carbon Emission Calculator + Green Energy Knowledge")

    st.markdown("""
    ### What this app offers:
    - 🚗 **Carbon Emission Calculator**
    - 💡 **Green Energy Q&A powered by Gemini**
    - 📊 **Upload CSV to calculate multiple activities**
    """)


def calculator_page():
    st.title("🧮 Carbon Emission Calculator")

    st.subheader("Transport Emissions")
    mode = st.selectbox("Transport Type", ["Car", "Motorbike", "Bus", "Train", "Flight"])

    if mode == "Car":
        km = st.number_input("Distance (km)", 0.0)
        fuel = st.selectbox("Fuel Type", ["petrol", "diesel"])
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

    elif mode == "Flight":
        km = st.number_input("Flight Distance (km)", 0.0)
        transport_em = km * (EMISSION_FACTORS["flight_short"] if km <= 1500 else EMISSION_FACTORS["flight_long"])

    st.write(f"**Transport Emissions:** {transport_em:.2f} kg CO₂e")

    st.markdown("---")

    st.subheader("Electricity Usage")
    kwh = st.number_input("Monthly electricity (kWh)", 0.0)
    elec_em = kwh * EMISSION_FACTORS["electricity"]
    st.write(f"**Electricity Emissions:** {elec_em:.2f} kg CO₂e")

    st.markdown("---")

    st.subheader("Food Emissions (Monthly)")
    beef = st.number_input("Beef (kg)", 0.0)
    poultry = st.number_input("Poultry (kg)", 0.0)
    veg = st.number_input("Vegetables/Other (kg)", 0.0)

    food_em = beef * EMISSION_FACTORS["beef"] + poultry * EMISSION_FACTORS["poultry"] + veg * EMISSION_FACTORS["vegetables"]
    st.write(f"**Food Emissions:** {food_em:.2f} kg CO₂e")

    st.markdown("---")

    st.subheader("Waste Emissions (Monthly)")
    waste = st.number_input("Waste (kg)", 0.0)
    waste_em = waste * EMISSION_FACTORS["waste"]
    st.write(f"**Waste Emissions:** {waste_em:.2f} kg CO₂e")

    st.markdown("---")

    total = transport_em + elec_em + food_em + waste_em
    st.header(f"🌍 Total Monthly Emissions: **{total:.2f} kg CO₂e**")

    breakdown = pd.DataFrame({
        "Category": ["Transport", "Electricity", "Food", "Waste"],
        "CO2 (kg)": [transport_em, elec_em, food_em, waste_em]
    })

    fig = px.pie(breakdown, values="CO2 (kg)", names="Category", title="Emission Breakdown")
    st.plotly_chart(fig)


def knowledge_page():
    st.title("💡 Green Energy Knowledge (Gemini)")

    prompt = st.text_area("Ask something about green energy:", height=120)

    if st.button("Ask Gemini"):
        with st.spinner("Getting answer..."):
            answer = query_gemini(prompt)
        st.subheader("Answer:")
        st.write(answer)


def upload_page():
    st.title("📤 Upload CSV for Bulk Emission Calculation")

    st.write("Format required:")
    st.code("activity, subtype, value, unit, extra")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.write(df.head())

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
                em = val * (EMISSION_FACTORS["flight_short"] if val < 1500 else EMISSION_FACTORS["flight_long"])
            elif act == "electricity":
                em = val * EMISSION_FACTORS["electricity"]
            elif act in ["beef", "poultry", "vegetables"]:
                em = val * EMISSION_FACTORS.get(act, 0)
            else:
                em = 0

            results.append({"activity": act, "value": val, "emissions": em})

        out = pd.DataFrame(results)
        st.write(out)

        st.success(f"Total emissions: {out['emissions'].sum():.2f} kg CO₂e")

        st.download_button(
            "Download Results CSV",
            out.to_csv(index=False),
            "results.csv",
            "text/csv"
        )


def about_page():
    st.title("ℹ️ About")
    st.write("""
    **GreenEnergy App**
    - Carbon footprint calculator  
    - Gemini-powered knowledge assistant  
    - CSV bulk emission analysis  
    """)

# ---------------- Navigation ---------------- #
pages = {
    "Home": home_page,
    "Calculator": calculator_page,
    "Knowledge (Gemini)": knowledge_page,
    "Upload CSV": upload_page,
    "About": about_page,
}

choice = st.sidebar.radio("Navigate", list(pages.keys()))
pages[choice]()
