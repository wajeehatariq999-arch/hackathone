"""
ai.py
-----
AI backend for SPG (Smart Pharma Guider).

Implements the two-stage AI flow required by the spec:
  Stage 1 - Relevance / scope check (is this question on-topic and safe?)
  Stage 2 - Answer generation (only runs if Stage 1 passes)

Uses the OpenAI Chat Completions API. The API key is never hard-coded — it is
read from an environment variable (see .env.example) or Streamlit secrets.

If you want to use a different provider, this is the only file you need to
change: keep the same function signatures (`check_relevance`, `generate_answer`)
and the rest of the app will keep working.
"""

import json
import os

from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)

from utils.prompts import build_answer_prompt, build_relevance_prompt

MODEL_NAME = "gpt-4o-mini"
REQUEST_TIMEOUT = 30


class AIError(Exception):
    """Raised for any AI-related failure, with a user-friendly message."""

    def __init__(self, friendly_message: str):
        self.friendly_message = friendly_message
        super().__init__(friendly_message)


def _get_api_key() -> str:
    """
    Reads the OpenAI API key from environment variables, or from Streamlit
    secrets if available. Never hard-code a real key in this file.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        try:
            import streamlit as st

            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            api_key = ""

    return api_key


def _get_client() -> OpenAI:
    api_key = _get_api_key()
    if not api_key or api_key == "ENTER YOUR API KEY HERE":
        raise AIError(
            "SPG is not fully set up yet: no API key was found. "
            "Please add your OPENAI_API_KEY in the .env file or Streamlit secrets."
        )
    return OpenAI(api_key=api_key, timeout=REQUEST_TIMEOUT)


def _call_chat(system_prompt: str, user_content: str) -> str:
    """Low-level call to the chat completion endpoint with error handling."""
    client = _get_client()

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=0.4,
            max_tokens=700,
        )
    except AuthenticationError:
        raise AIError(
            "Your API key appears to be invalid. Please check your OPENAI_API_KEY setting."
        )
    except RateLimitError:
        raise AIError(
            "SPG is receiving too many requests right now. Please wait a moment and try again."
        )
    except APITimeoutError:
        raise AIError("The request took too long to respond. Please try again.")
    except APIConnectionError:
        raise AIError(
            "SPG couldn't connect to the AI service. Please check your internet connection and try again."
        )
    except OpenAIError:
        raise AIError("Something went wrong while contacting the AI service. Please try again.")
    except Exception:
        raise AIError("An unexpected error occurred. Please try again in a moment.")

    if not response or not response.choices:
        raise AIError("The AI service returned an empty response. Please try again.")

    content = (response.choices[0].message.content or "").strip()
    if not content:
        raise AIError("The AI service returned an empty response. Please try again.")

    return content


def check_relevance(feature_key: str, medicine_name: str, question: str) -> dict:
    """
    Stage 1: Ask the AI whether the question is relevant, in-scope, and safe
    to answer for the given feature. Returns a dict:
        {"relevant": bool, "reason": str}
    Falls back to a safe default (not relevant) if the AI response can't be
    parsed, rather than silently letting an unrelated question through.
    """
    system_prompt = build_relevance_prompt(feature_key)
    user_content = (
        f"Medicine name (may be blank for self-assessment): {medicine_name or 'N/A'}\n"
        f"User question: {question}"
    )

    raw = _call_chat(system_prompt, user_content)

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        parsed = json.loads(cleaned)
        relevant = bool(parsed.get("relevant", False))
        reason = str(parsed.get("reason", ""))
        return {"relevant": relevant, "reason": reason}
    except (json.JSONDecodeError, AttributeError, TypeError):
        # If we can't confidently parse the classifier's answer, default to
        # rejecting rather than risk answering an off-topic question.
        return {"relevant": False, "reason": "Could not verify relevance."}


def generate_answer(feature_key: str, medicine_name: str, question: str) -> str:
    """
    Stage 2: Generate the actual guidance for a question that has already
    passed the relevance check.
    """
    system_prompt = build_answer_prompt(feature_key)
    user_content = (
        f"Medicine name (may be blank for self-assessment): {medicine_name or 'N/A'}\n"
        f"User question: {question}"
    )
    return _call_chat(system_prompt, user_content)


def get_ai_response(feature_key: str, medicine_name: str, question: str) -> dict:
    """
    Full two-stage pipeline used by the UI.
    Returns:
        {"status": "answered", "answer": str}
        {"status": "rejected", "message": str}
        {"status": "error", "message": str}
    """
    try:
        relevance = check_relevance(feature_key, medicine_name, question)
    except AIError as e:
        return {"status": "error", "message": e.friendly_message}

    if not relevance.get("relevant"):
        from utils.prompts import FEATURES

        rejection = FEATURES[feature_key]["rejection_message"]
        return {"status": "rejected", "message": rejection}

    try:
        answer = generate_answer(feature_key, medicine_name, question)
    except AIError as e:
        return {"status": "error", "message": e.friendly_message}

    return {"status": "answered", "answer": answer}
