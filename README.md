# SPG — Smart Pharma Guider

## 1. Project Purpose

SPG (Smart Pharma Guider) is an AI-powered Streamlit application that gives
**general pharmaceutical and health guidance**. It helps everyday users think
through common medicine-related questions — food interactions, missed doses,
alternatives, storage, and general symptom guidance — through a clean,
dedicated interface for each topic.

SPG is **not** a doctor, pharmacist, or diagnostic tool. It provides general
information only and always encourages users to confirm anything important
with a qualified healthcare professional.

## 2. Features

SPG has five separate, AI-powered features, each with its own page:

| Feature | What it does |
|---|---|
| 🍽️ Food–Medicine Interaction | Ask how a medicine interacts with foods, drinks, or alcohol. |
| ⏰ Missed Dose Guide | Ask what to generally consider after a missed or late dose. |
| 💊 Alternative Options | Ask about possible alternative medicines or related options. |
| 🌡️ Storage & Handling | Ask how to store or handle a medicine safely. |
| 🩺 Quick Self-Assessment | Describe symptoms and get general, non-diagnostic guidance. |

Every feature uses a **two-stage AI flow**:

1. **Relevance check** — the AI decides (by meaning/intent, not just
   keywords) whether your question genuinely belongs to that feature.
2. **Answer generation** — only if it's relevant, the AI generates a real,
   dynamic answer scoped to that feature's purpose.

Off-topic or unrelated questions (sports, entertainment, homework, etc.) are
politely rejected instead of answered.

## 3. Technology Used

- **Python 3.10+**
- **Streamlit** — UI framework
- **OpenAI API** (`gpt-4o-mini` by default) — powers the two-stage AI flow
- **python-dotenv** — loads your API key from a local `.env` file

## 4. Project Structure

```text
SPG/
│
├── app.py                       # Main Streamlit app (UI + navigation)
├── requirements.txt
├── .env.example                 # Copy to .env and add your API key
├── README.md
│
├── .streamlit/
│   └── secrets.toml.example     # Alternative to .env for Streamlit Cloud
│
└── utils/
    ├── __init__.py
    ├── ai.py                    # Two-stage AI flow + error handling
    ├── validation.py            # Input validation helpers
    └── prompts.py                # Feature-specific prompts and copy
```

## 5. Installation

1. Make sure you have Python 3.10 or newer installed.
2. Download or clone this project folder.
3. Open a terminal in the `SPG/` folder.
4. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```
5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 6. API Key Setup

SPG uses the OpenAI API. You need your own API key — SPG never ships with a
real key hard-coded.

**Option A — using a `.env` file (recommended for local use):**

1. Copy `.env.example` to a new file named `.env`.
2. Open `.env` and replace the placeholder:
   ```text
   OPENAI_API_KEY=ENTER YOUR API KEY HERE
   ```
   with your real key:
   ```text
   OPENAI_API_KEY=sk-your-real-key-here
   ```
3. Never commit or share your `.env` file.

**Option B — using Streamlit secrets (recommended for Streamlit Cloud):**

1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
2. Replace the placeholder value with your real key.

## 7. Running the Application

From the `SPG/` folder, run:

```bash
streamlit run app.py
```

Streamlit will open the app in your browser (usually at
`http://localhost:8501`).

## 8. Safety Disclaimer

SPG provides **general pharmaceutical and health information only**. It:

- does **not** provide medical diagnoses,
- does **not** guarantee any treatment outcome,
- does **not** replace advice from a licensed doctor or pharmacist,
- does **not** replace emergency medical care.

If you are experiencing a medical emergency, contact your local emergency
services or go to the nearest emergency room immediately. Always confirm
medicine changes, dosing decisions, and serious symptoms with a qualified
healthcare professional.

## 9. Notes on Customization

- To use a different AI provider, edit `utils/ai.py` only — keep the
  `check_relevance()` and `generate_answer()` function signatures the same
  and the rest of the app will keep working unchanged.
- Feature descriptions, prompts, and example questions live in
  `utils/prompts.py` if you want to adjust wording or add examples.
