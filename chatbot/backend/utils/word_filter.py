import json
import os
import re

WORD_FILTER_PATH = os.path.join(os.path.dirname(__file__), "./word_filter.json")

# Load từ data file JSON
with open(WORD_FILTER_PATH, "r", encoding="utf-8") as f:
    BAD_WORDS = set(json.load(f).keys())

def contains_bad_word(text: str) -> bool:
    text = text.lower().replace("_", " ")
    for word in BAD_WORDS:
        # Match từng từ, kể cả biến thể dấu cách hoặc gạch dưới
        pattern = rf"\b{re.escape(word.replace('_', ' '))}\b"
        if re.search(pattern, text):
            return True
    return False
