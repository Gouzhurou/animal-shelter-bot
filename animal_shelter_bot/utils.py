import re

def validate_name(text):
    return text.isalpha()

def validate_age(text):
    return text.isdigit() and 0 < int(text) < 120

def validate_email(text):
    return '@' in text and '.' in text

def validate_city(text):
    return text.replace("-", "").isalpha()

def validate_phone(text: str) -> bool:
    return re.fullmatch(r"\+7\d{10}", text) is not None
