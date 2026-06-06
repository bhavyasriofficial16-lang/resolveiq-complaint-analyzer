def clean_text(text):
    return str(text).lower()


URGENCY_KEYWORDS = {
    "urgent": 3,
    "emergency": 5,
    "immediately": 3,
    "legal": 4,
    "police": 5,
    "fraud": 5,
    "scam": 5,
    "money": 2,
    "deducted": 2,
    "medical": 5,
    "unsafe": 5,
    "danger": 5,
    "critical": 4,
    "no response": 3,
    "two weeks": 2,
}


def get_urgency_score(text):
    text = clean_text(text)
    score = 0

    for keyword, weight in URGENCY_KEYWORDS.items():
        if keyword in text:
            score += weight

    return score


def classify_urgency(text):
    score = get_urgency_score(text)

    if score >= 4:
        return "High"

    if score >= 2:
        return "Medium"

    return "Low"