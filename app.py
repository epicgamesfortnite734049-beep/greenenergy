# app.py
"""
GreenEnergy Streamlit app (updated Robust Knowledge page).
- Graceful handling when Gemini API key or client library is missing.
- Allows one-off API key input (session-only) for testing.
- Provides local FAQ/fallback answers so the Knowledge page remains useful offline.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Optional

# Try to import Gemini client (correct package name: google.generativeai)
GEMINI_CLIENT_AVAILABLE = False
try:
    import google.generativeai as genai
    GEMINI_CLIENT_AVAILABLE = True
except Exception:
    GEMINI_CLIENT_AVAILABLE = False

# Basic Streamlit config
st.set_page_config(page_title="GreenEnergy - Carbon Calculator", page_icon="🌿", layout="wide")

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

# ---------------- Utility helpers ---------------- #
def format_kg(x: float) -> str:
    return f"{x:,.2f} kg CO₂e"

# Small local knowledge base / FAQ for offline fallback
LOCAL_KB = {
    "what is renewable energy": (
        "Renewable energy comes from sources that naturally replenish, like solar, wind, hydro, "
        "and geothermal. These sources produce electricity with much lower lifecycle greenhouse gas "
        "emissions than fossil fuels."
    ),
    "benefits of rooftop solar": (
        "Rooftop solar reduces grid electricity consumption, lowers electricity bills, and cuts CO₂ emissions. "
        "Its effectiveness depends on rooftop orientation, local solar insolation, and system size."
    ),
    "how to reduce home electricity consumption": (
        "Key actions: switch to LED lighting, use energy-efficient appliances (check star ratings), "
        "improve insulation, use smart thermostats, and avoid phantom loads by unplugging idle devices."
    ),
    "what is carbon footprint": (
        "A carbon footprint measures total greenhouse gas emissions caused directly and indirectly by an activity, "
        "usually expressed in kg CO₂-equivalent."
    ),
    "how is electricity emission factor determined": (
        "Grid emission factors depend on the local mix of generation (coal, gas, renewables, nuclear), "
        "transmission losses and lifecycle emissions. Many countries publish updated factors annually."
    ),
}

def local_answer(question: str) -> str:
    q = question.strip().lower()
    # simple exact / partial matching
    for key in LOCAL_KB:
        if key in q:
            return LOCAL_KB[key]
    # fallback: produce a short structured answer by splitting key topics heuristically
    if "solar" in q:
        return LOCAL_KB.get("benefits of rooftop solar")
    if "reduce" in q and "electricity" in q:
        return LOCAL_KB.get("how to reduce home electricity consumption")
    return (
        "I don't have an exact match in the local knowledge base. "
        "Try rephrasing (for example: 'What is renewable energy?', 'Benefits of rooftop solar', "
        "or 'How to reduce home electricity'). "
        "If you want a detailed, up-to-date answer, provide a Gemini API key in the box below or set the GEMINI_API_KEY "
        "environment variable in Streamlit Cloud and install the `google-generativeai` package."
    )

# ---------------- Gemini query helper (safe) ---------------- #
def query_gemini(prompt: str, api_key: Optional[str] = None, model: str = "gemini-1.5-pro", max_output_tokens: int = 512) -> str:
    """
    Query Gemini if client library + api_key are available.
    - api_key param is optional and used for session-only testing (not persisted).
    - Returns user-friendly error messages when unavailable.
    """
    # prefer explicit api_key param, otherwise environment
    effective_key = api_key or os.getenv("GEMINI_API_KEY")
    if not effective_key:
        return "⚠️ Gemini API key not configured. Provide a key in the box below or set GEMINI_API_KEY in Streamlit Cloud."

    if not GEMINI_CLIENT_AVAILABLE:
        return (
            "⚠️ Gemini client library not installed in this environment. "
            "Install the package `google-generativeai` (note exact PyPI name) in requirements.txt and redeploy."
        )

    try:
        # configure client (stateless)
        genai.configure(api_key=effective_key)
        # The shape of the API may vary by version. This is a common pattern.
        response = genai.generate(model=model, prompt=prompt, max_output_tokens=max_output_tokens)
        # try common attributes
        if hasattr(response, "text") and response.text:
            return response.text
        # some client versions return a dict-like object
        try:
            # try to extract a sensible string
            return str(response)
        except Exception:
            return "Received an unexpected response shape from Gemini client. Inspect logs."
    except Exception as e:
        return f"Error while calling Gemini: {e}"

# ---------------- UI : Header / Aesthetic ---------------- #
st.markdown("""
<style>
/* subtle background gradient */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #f0f7f2 0%, #eef6fb 100%);
}

/* card */
.card {
  background: white;
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 6px 20px rgba(30,50,80,0.08);
}
.small-muted {
  color: #5b6b72;
  font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 GreenEnergy — Carbon Calculator & Knowledge")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Home", "Calculator", "Knowledge", "Upload CSV", "About"])

# -------------- Home Page (keeps it brief + aesthetic) -------------- #
def page_home():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Welcome to GreenEnergy")
    st.markdown("Estimate your carbon footprint and get quick, practical green-energy guidance.")
    st.markdown("<div class='small-muted'>Tip: Visit Knowledge to ask about renewable energy. If you want the AI assistant to answer, configure Gemini (instructions in Knowledge page).</div>", unsafe_allow_html=True)
    st.markdown('</div>')
    st.write("")
    cols = st.columns([1,1,1])
    with cols[0]:
        st.info("🧮 Calculator")
        if st.button("Open Calculator"):
            st.experimental_set_query_params(page="Calculator")
            st.experimental_rerun()
    with cols[1]:
        st.info("💡 Knowledge")
        if st.button("Open Knowledge"):
            st.experimental_set_query_params(page="Knowledge")
            st.experimental_rerun()
    with cols[2]:
        st.info("📤 Upload CSV")
        if st.button("Upload CSV"):
            st.experimental_set_query_params(page="Upload CSV")
            st.experimental_rerun()

# -------------- Calculator Page (unchanged core logic) -------------- #
def page_calculator():
    st.header("🧮 Carbon Emission Calculator")
    st.write("Estimate emissions for common activities. Edit emission factors in the code for local accuracy.")

    st.subheader("Transport")
    transport_mode = st.selectbox("Transport mode", ["Car", "Motorbike", "Bus", "Train", "Flight"])
    transport_em = 0.0
    if transport_mode == "Car":
        km = st.number_input("Distance (km)", min_value=0.0, value=20.0)
        fuel = st.selectbox("Fuel type", ["petrol", "diesel"])
        factor = EMISSION_FACTORS["car_petrol"] if fuel == "petrol" else EMISSION_FACTORS["car_diesel"]
        transport_em = km * factor
    elif transport_mode == "Motorbike":
        km = st.number_input("Distance (km)", min_value=0.0, value=15.0)
        transport_em = km * EMISSION_FACTORS["motorbike"]
    elif transport_mode == "Bus":
        km = st.number_input("Distance (km)", min_value=0.0, value=10.0)
        passengers = st.number_input("Passengers (including you)", min_value=1, value=10)
        transport_em = (km * EMISSION_FACTORS["bus"]) / max(1, passengers)
    elif transport_mode == "Train":
        km = st.number_input("Distance (km)", min_value=0.0, value=30.0)
        transport_em = km * EMISSION_FACTORS["train"]
    else:
        km = st.number_input("Flight distance (km)", min_value=0.0, value=800.0)
        transport_em = km * (EMISSION_FACTORS["flight_short"] if km <= 1500 else EMISSION_FACTORS["flight_long"])

    st.write("Transport emissions:", format_kg(transport_em))

    st.markdown("---")
    st.subheader("Electricity")
    kwh = st.number_input("Monthly electricity (kWh)", min_value=0.0, value=150.0)
    grid_factor = st.number_input("Grid emission factor (kg CO₂/kWh) — override optional", value=float(EMISSION_FACTORS["electricity"]))
    elec_em = kwh * grid_factor
    st.write("Electricity emissions:", format_kg(elec_em))

    st.markdown("---")
    st.subheader("Food (monthly)")
    beef = st.number_input("Beef (kg)", min_value=0.0, value=1.0)
    poultry = st.number_input("Poultry (kg)", min_value=0.0, value=3.0)
    veg = st.number_input("Vegetables (kg)", min_value=0.0, value=8.0)
    food_em = beef * EMISSION_FACTORS["beef"] + poultry * EMISSION_FACTORS["poultry"] + veg * EMISSION_FACTORS["vegetables"]
    st.write("Food emissions:", format_kg(food_em))

    st.markdown("---")
    st.subheader("Waste (monthly)")
    waste = st.number_input("Waste (kg)", min_value=0.0, value=12.0)
    waste_em = waste * EMISSION_FACTORS["waste"]
    st.write("Waste emissions:", format_kg(waste_em))

    total = transport_em + elec_em + food_em + waste_em
    st.markdown(f"### **Estimated total monthly emissions: {format_kg(total)}**")
    st.info("Multiply by 12 for a rough annual estimate.")

    breakdown = pd.DataFrame({
        "Category": ["Transport", "Electricity", "Food", "Waste"],
        "kg_co2e": [transport_em, elec_em, food_em, waste_em]
    })
    fig = px.pie(breakdown, values="kg_co2e", names="Category", title="Monthly Emissions Breakdown")
    st.plotly_chart(fig, use_container_width=True)

# -------------- Knowledge Page (robust + friendly) -------------- #
def page_knowledge():
    st.header("💬 Green Energy Knowledge")

    st.markdown(
        """
        Use Gemini (if configured) for long, up-to-date answers, or use the local fallback for quick factual summaries.
        """
    )

    # Display status of Gemini client + env var
    env_key = os.getenv("GEMINI_API_KEY")
    st.markdown("**Gemini integration status:**")
    status_cols = st.columns(3)
    status_cols[0].metric("Client installed", "Yes" if GEMINI_CLIENT_AVAILABLE else "No")
    status_cols[1].metric("GEMINI_API_KEY env var", "Set" if env_key else "Not set")
    status_cols[2].metric("Can use Gemini now", "Yes" if (GEMINI_CLIENT_AVAILABLE and env_key) else "No")

    st.markdown("---")

    st.subheader("Ask a question")
    user_q = st.text_area("Type your question about green energy or carbon (e.g., 'Benefits of rooftop solar')", height=140)

    st.markdown("**Temporary API key (session-only)** — paste here to test Gemini without changing deployment settings.")
    temp_key = st.text_input("Paste Gemini API key (optional; will not be saved)", type="password", placeholder="Paste a Gemini API key for testing")

    col_a, col_b = st.columns(2)
    with col_a:
        ask_local = st.button("Get local answer (fast, offline)")
    with col_b:
        ask_gemini = st.button("Ask Gemini (if available)")

    if ask_local:
        if not user_q or user_q.strip() == "":
            st.warning("Please type a question first.")
        else:
            with st.spinner("Generating local answer..."):
                ans = local_answer(user_q)
            st.subheader("Local answer")
            st.write(ans)

    if ask_gemini:
        if not user_q or user_q.strip() == "":
            st.warning("Please type a question first.")
        else:
            # prefer temporary key if supplied
            effective_key = temp_key or env_key
            if not effective_key:
                st.error("No API key provided. Either paste a temporary key in the box above or set GEMINI_API_KEY in your deployment environment.")
                st.info("Instructions: In Streamlit Cloud go to 'Settings → Secrets' and add GEMINI_API_KEY, or add it as an environment variable.")
            elif not GEMINI_CLIENT_AVAILABLE:
                st.error("Gemini client library not installed in this environment. Add `google-generativeai` (exact PyPI name) to requirements.txt and redeploy.")
            else:
                with st.spinner("Querying Gemini..."):
                    response = query_gemini(user_q, api_key=effective_key)
                st.subheader("Gemini response")
                st.write(response)

    st.markdown("---")
    st.subheader("Quick example prompts")
    st.write("- What are practical ways to reduce home electricity use?")
    st.write("- Give a 5-step plan for installing rooftop solar on a 3kW system.")
    st.write("- Differences between short-haul and long-haul flight emissions.")

    st.markdown("---")
    st.subheader("How to enable Gemini (Streamlit Cloud)")
    st.markdown(
        """
        1. Add this line to your `requirements.txt`:  
           `google-generativeai==0.5.2` (or a compatible version).  
        2. In Streamlit Cloud, go to your app → Settings → Secrets/Environment Variables → Add `GEMINI_API_KEY` with your API key.  
        3. Push changes and restart the app.
        """
    )

# -------------- Upload CSV Page -------------- #
def page_upload():
    st.header("📤 Upload CSV for Bulk Emission Calculation")
    st.write("Expected CSV columns (simple): `activity, subtype, value` where activity can be car, flight, electricity, beef, etc.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.write(df.head())
        results = []
        for _, row in df.iterrows():
            act = str(row.get("activity", "")).lower()
            subtype = str(row.get("subtype", "")).lower() if "subtype" in row else ""
            val = row.get("value", 0)
            try:
                val = float(val)
            except Exception:
                val = 0.0
            em = 0.0
            if act == "car":
                ef = EMISSION_FACTORS["car_petrol"] if "petrol" in subtype else EMISSION_FACTORS["car_diesel"]
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
            results.append({"activity": act, "value": val, "kg_co2e": em})
        out = pd.DataFrame(results)
        st.write(out)
        st.success(f"Total emissions: {out['kg_co2e'].sum():.2f} kg CO₂e")
        csv = out.to_csv(index=False).encode("utf-8")
        st.download_button("Download results CSV", csv, "emissions_results.csv", "text/csv")

# -------------- About Page -------------- #
def page_about():
    st.header("ℹ️ About & Deployment Notes")
    st.markdown(
        """
        **GreenEnergy** helps estimate carbon emissions and provides green-energy knowledge.
        The Knowledge page works best with Gemini configured; otherwise the app provides a local FAQ fallback.

        **Requirements tip**: Use the correct PyPI package name in requirements.txt:
        ```
        google-generativeai==0.5.2
        ```
        Not: `google-generative-ai` (this will fail).
        """
    )

# ----------------- Page routing ----------------- #
if page == "Home":
    page_home()
elif page == "Calculator":
    page_calculator()
elif page == "Knowledge":
    page_knowledge()
elif page == "Upload CSV":
    page_upload()
elif page == "About":
    page_about()
else:
    st.write("Page not found.")
