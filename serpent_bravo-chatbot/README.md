
# Serpent_Bravo Chatbot - Streamlit Version

This is an AI chatbot dedicated to helping users understand and reduce their carbon footprints. It's built with Python, Streamlit, and the Google Gemini API.

## 🚀 How to Deploy on Streamlit Community Cloud

Deploying this app is easy!

### 1. Create a GitHub Repository

Create a new repository on your GitHub account and upload the following files:
- `streamlit_app.py`
- `gamification.py`
- `requirements.txt`
- `README.md`

### 2. Get a Gemini API Key

If you don't have one already, get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3. Deploy on Streamlit

1.  Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
2.  Click "**New app**" and select the GitHub repository you just created.
3.  Click "**Advanced settings...**"
4.  In the "Secrets" section, add your Gemini API key. It should look exactly like this:

    ```toml
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
    (Replace `YOUR_API_KEY_HERE` with your actual key).

5.  Click "**Deploy!**". Streamlit will handle the rest, and your app will be live in a few moments.

## 💻 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a secrets file:**
    - Create a folder named `.streamlit` in your project root.
    - Inside that folder, create a file named `secrets.toml`.
    - Add your Gemini API key to `secrets.toml`:
      ```toml
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

5.  **Run the app:**
    ```bash
    streamlit run streamlit_app.py
    ```
