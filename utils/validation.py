"""
validation.py
--------------
Simple, dependency-free input validation helpers for SPG.
"""

MIN_QUESTION_LENGTH = 3
MAX_QUESTION_LENGTH = 800
MAX_MEDICINE_NAME_LENGTH = 120


def clean_text(value: str) -> str:
    """Strip and collapse whitespace."""
    if not value:
        return ""
    return " ".join(value.strip().split())


def validate_medicine_name(name: str) -> tuple[bool, str]:
    name = clean_text(name)
    if not name:
        return False, "Please enter a medicine name."
    if len(name) > MAX_MEDICINE_NAME_LENGTH:
        return False, "That medicine name looks too long. Please shorten it."
    return True, ""


def validate_question(question: str) -> tuple[bool, str]:
    question = clean_text(question)
    if not question:
        return False, "Please enter your question."
    if len(question) < MIN_QUESTION_LENGTH:
        return False, "Please enter a more complete question."
    if len(question) > MAX_QUESTION_LENGTH:
        return False, "Please shorten your question a little and try again."
    return True, ""


def validate_symptom_text(text: str) -> tuple[bool, str]:
    text = clean_text(text)
    if not text:
        return False, "Please describe your symptoms or health concern."
    if len(text) < MIN_QUESTION_LENGTH:
        return False, "Please share a little more detail about how you're feeling."
    if len(text) > MAX_QUESTION_LENGTH:
        return False, "Please shorten your description a little and try again."
    return True, ""
