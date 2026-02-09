import re

def clean_phone(phone: str) -> str:
    return re.sub(r'\D', '', phone)