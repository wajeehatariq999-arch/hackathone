"""
SPG — Smart Pharma Guider
=========================
A polished, AI-powered Streamlit application providing general pharmaceutical
guidance across five dedicated features. See README.md for setup instructions.

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # loads OPENAI_API_KEY from a local .env file, if present

from utils.ai import get_ai_response
from utils.prompts import FEATURES
from utils.validation import (
    validate_medicine_name,
    validate_question,
    validate_symptom_text,
)

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="SPG — Smart Pharma Guider",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# Global styling
# --------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --spg-primary: #0F766E;
    --spg-primary-dark: #0B5A54;
    --spg-primary-light: #CCFBF1;
    --spg-accent: #2563EB;
    --spg-bg: #F5F8F8;
    --spg-card-bg: #FFFFFF;
    --spg-text-dark: #0F172A;
    --spg-text-muted: #5B6472;
    --spg-border: #E4E9EC;
    --spg-warning-bg: #FFF7E6;
    --spg-warning-border: #F5C56B;
    --spg-radius: 16px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--spg-bg);
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ---------- Hero ---------- */
.spg-hero {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
}
.spg-hero .spg-logo {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: 1px;
    color: var(--spg-primary);
    margin-bottom: 0.2rem;
}
.spg-hero .spg-subtitle {
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--spg-text-dark);
    margin-bottom: 0.6rem;
}
.spg-hero .spg-tagline {
    font-size: 1.05rem;
    color: var(--spg-text-muted);
    font-style: italic;
    margin-bottom: 1.1rem;
}
.spg-hero .spg-intro {
    font-size: 0.98rem;
    color: var(--spg-text-muted);
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.55;
}

/* ---------- Section heading ---------- */
.spg-section-heading {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--spg-text-dark);
    margin: 2rem 0 1.4rem 0;
}

/* ---------- Feature cards ---------- */
.spg-card {
    background: var(--spg-card-bg);
    border: 1px solid var(--spg-border);
    border-radius: var(--spg-radius);
    padding: 1.6rem 1.4rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    height: 210px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    transition: box-shadow 0.15s ease, transform 0.15s ease;
    margin-bottom: 0.9rem;
}
.spg-card:hover {
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.09);
    transform: translateY(-2px);
}
.spg-card .spg-card-icon {
    font-size: 2rem;
    margin-bottom: 0.55rem;
}
.spg-card .spg-card-title {
    font-size: 1.08rem;
    font-weight: 700;
    color: var(--spg-text-dark);
    margin-bottom: 0.4rem;
}
.spg-card .spg-card-desc {
    font-size: 0.9rem;
    color: var(--spg-text-muted);
    line-height: 1.45;
    flex-grow: 1;
}

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 10px !important;
    height: 2.7rem;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: 1px solid var(--spg-primary) !important;
    transition: all 0.15s ease;
}
.stButton > button[kind="primary"] {
    background: var(--spg-primary) !important;
    color: white !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--spg-primary-dark) !important;
}
.stButton > button[kind="secondary"] {
    background: white !important;
    color: var(--spg-primary) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: var(--spg-primary-light) !important;
}

/* ---------- Feature page header ---------- */
.spg-feature-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.4rem 0 0.3rem 0;
}
.spg-feature-header .spg-feature-icon {
    font-size: 2rem;
}
.spg-feature-header .spg-feature-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--spg-text-dark);
}
.spg-feature-desc {
    color: var(--spg-text-muted);
    font-size: 0.98rem;
    margin-bottom: 1.3rem;
    line-height: 1.5;
}

/* ---------- Input labels ---------- */
.spg-label {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--spg-text-dark);
    margin-bottom: 0.3rem;
    margin-top: 0.9rem;
}

.stTextInput input, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1px solid var(--spg-border) !important;
    font-size: 0.96rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--spg-primary) !important;
    box-shadow: 0 0 0 2px var(--spg-primary-light) !important;
}

.spg-examples {
    font-size: 0.85rem;
    color: var(--spg-text-muted);
    margin-top: 0.4rem;
    line-height: 1.6;
}
.spg-examples b {
    color: var(--spg-text-dark);
}

/* ---------- AI response card ---------- */
.spg-response-card {
    background: var(--spg-card-bg);
    border: 1px solid var(--spg-primary-light);
    border-left: 5px solid var(--spg-primary);
    border-radius: var(--spg-radius);
    padding: 1.4rem 1.6rem;
    margin-top: 1.3rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
    line-height: 1.65;
    font-size: 0.98rem;
    color: var(--spg-text-dark);
}
.spg-response-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--spg-primary);
    margin-bottom: 0.6rem;
}

.spg-notice-card {
    background: var(--spg-warning-bg);
    border: 1px solid var(--spg-warning-border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-top: 1.1rem;
    font-size: 0.92rem;
    color: #7A5B15;
}

.spg-error-card {
    background: #FDECEC;
    border: 1px solid #F3B4B4;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-top: 1.1rem;
    font-size: 0.92rem;
    color: #8A2A2A;
}

.spg-disclaimer {
    text-align: center;
    color: var(--spg-text-muted);
    font-size: 0.82rem;
    margin-top: 2.4rem;
    padding-top: 1rem;
    border-top: 1px solid var(--spg-border);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "last_result" not in st.session_state:
    st.session_state.last_result = {}


def go_to(page_key: str):
    st.session_state.page = page_key
    st.session_state.last_result = {}


# --------------------------------------------------------------------------
# Shared UI pieces
# --------------------------------------------------------------------------
def render_top_nav(show_back: bool):
    if show_back:
        cols = st.columns([1, 5])
        with cols[0]:
            if st.button("← Back to Home", key="back_home"):
                go_to("home")


def render_response_block(feature_key: str):
    result = st.session_state.last_result
    if not result:
        return

    status = result.get("status")
    if status == "answered":
        st.markdown(
            f"""
            <div class="spg-response-card">
                <div class="spg-response-label">SPG AI Guidance</div>
                {result['answer_html']}
            </div>
            <div class="spg-disclaimer">
                SPG provides general information only and is not a substitute
                for professional medical or pharmacist advice.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif status == "rejected":
        st.markdown(
            f"""<div class="spg-notice-card">🙏 {result['message']}</div>""",
            unsafe_allow_html=True,
        )
    elif status == "error":
        st.markdown(
            f"""<div class="spg-error-card">⚠️ {result['message']}</div>""",
            unsafe_allow_html=True,
        )
    elif status == "validation":
        st.markdown(
            f"""<div class="spg-notice-card">✏️ {result['message']}</div>""",
            unsafe_allow_html=True,
        )


def text_to_html_paragraphs(text: str) -> str:
    """Turn plain AI text (with possible '-' bullets) into simple safe HTML."""
    import html as html_lib

    lines = [ln.strip() for ln in text.split("\n")]
    html_parts = []
    in_list = False

    for line in lines:
        if not line:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue
        escaped = html_lib.escape(line)
        # bold **text**
        import re

        escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
        if line.startswith(("-", "•", "*")):
            if not in_list:
                html_parts.append("<ul style='margin:0.3rem 0 0.6rem 1.2rem;'>")
                in_list = True
            html_parts.append(f"<li>{escaped.lstrip('-•* ').strip()}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<p style='margin:0.4rem 0;'>{escaped}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "".join(html_parts)


# --------------------------------------------------------------------------
# Home / Dashboard
# --------------------------------------------------------------------------
def render_home():
    st.markdown(
        """
        <div class="spg-hero">
            <div class="spg-logo">SPG</div>
            <div class="spg-subtitle">Smart Pharma Guider</div>
            <div class="spg-tagline">Your intelligent guide for safer medicine use.</div>
            <div class="spg-intro">
                SPG provides AI-powered general pharmaceutical guidance to help you
                understand your medicines better — from food interactions to storage
                tips. It offers general information only and does not replace advice
                from a licensed doctor or pharmacist.
            </div>
        </div>
        <div class="spg-section-heading">How can we help you today?</div>
        """,
        unsafe_allow_html=True,
    )

    feature_order = [
        "food_interaction",
        "missed_dose",
        "alternatives",
        "storage",
        "self_assessment",
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)
    slots = list(row1) + list(row2)

    for i, key in enumerate(feature_order):
        feature = FEATURES[key]
        with slots[i]:
            st.markdown(
                f"""
                <div class="spg-card">
                    <div class="spg-card-icon">{feature['icon']}</div>
                    <div class="spg-card-title">{feature['display_name']}</div>
                    <div class="spg-card-desc">{feature['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open", key=f"open_{key}", use_container_width=True):
                go_to(key)
                st.rerun()


# --------------------------------------------------------------------------
# Generic feature page (used by 4 of the 5 features)
# --------------------------------------------------------------------------
def render_medicine_question_feature(feature_key: str):
    feature = FEATURES[feature_key]

    render_top_nav(show_back=True)

    st.markdown(
        f"""
        <div class="spg-feature-header">
            <div class="spg-feature-icon">{feature['icon']}</div>
            <div class="spg-feature-title">{feature['display_name']}</div>
        </div>
        <div class="spg-feature-desc">{feature['description']}</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="spg-label">Medicine Name</div>', unsafe_allow_html=True)
    medicine_name = st.text_input(
        "Medicine name",
        placeholder="Enter medicine name",
        label_visibility="collapsed",
        key=f"{feature_key}_medicine",
    )

    st.markdown('<div class="spg-label">Your Question</div>', unsafe_allow_html=True)
    question = st.text_area(
        "Your question",
        placeholder=feature["placeholder"],
        label_visibility="collapsed",
        height=110,
        key=f"{feature_key}_question",
    )

    examples_html = "<br>".join(f"• {ex}" for ex in feature["examples"])
    st.markdown(
        f"""<div class="spg-examples"><b>Example questions:</b><br>{examples_html}</div>""",
        unsafe_allow_html=True,
    )

    ask_col, _ = st.columns([1, 3])
    with ask_col:
        submit = st.button("Ask AI", key=f"{feature_key}_submit", type="primary", use_container_width=True)

    if submit:
        name_ok, name_msg = validate_medicine_name(medicine_name)
        q_ok, q_msg = validate_question(question)

        if not name_ok:
            st.session_state.last_result = {"status": "validation", "message": name_msg}
        elif not q_ok:
            st.session_state.last_result = {"status": "validation", "message": q_msg}
        else:
            with st.spinner("Analyzing your question..."):
                result = get_ai_response(feature_key, medicine_name.strip(), question.strip())
            if result.get("status") == "answered":
                result["answer_html"] = text_to_html_paragraphs(result["answer"])
            st.session_state.last_result = result

    render_response_block(feature_key)


# --------------------------------------------------------------------------
# Self-assessment page (slightly different: no medicine name field)
# --------------------------------------------------------------------------
def render_self_assessment():
    feature_key = "self_assessment"
    feature = FEATURES[feature_key]

    render_top_nav(show_back=True)

    st.markdown(
        f"""
        <div class="spg-feature-header">
            <div class="spg-feature-icon">{feature['icon']}</div>
            <div class="spg-feature-title">{feature['display_name']}</div>
        </div>
        <div class="spg-feature-desc">{feature['description']}</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="spg-label">Describe your symptoms or health concern</div>', unsafe_allow_html=True)
    symptoms = st.text_area(
        "Symptoms",
        placeholder="Describe your symptoms or health concern...",
        label_visibility="collapsed",
        height=140,
        key="self_assessment_symptoms",
    )

    st.markdown(
        """<div class="spg-examples">
        This assessment provides general health information and is not a medical diagnosis.
        </div>""",
        unsafe_allow_html=True,
    )

    ask_col, _ = st.columns([1, 3])
    with ask_col:
        submit = st.button("Assess with AI", key="assess_submit", type="primary", use_container_width=True)

    if submit:
        ok, msg = validate_symptom_text(symptoms)
        if not ok:
            st.session_state.last_result = {"status": "validation", "message": msg}
        else:
            with st.spinner("Thinking..."):
                result = get_ai_response(feature_key, "", symptoms.strip())
            if result.get("status") == "answered":
                result["answer_html"] = text_to_html_paragraphs(result["answer"])
            st.session_state.last_result = result

    render_response_block(feature_key)


# --------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------
page = st.session_state.page

if page == "home":
    render_home()
elif page == "self_assessment":
    render_self_assessment()
elif page in FEATURES:
    render_medicine_question_feature(page)
else:
    st.session_state.page = "home"
    st.rerun()
