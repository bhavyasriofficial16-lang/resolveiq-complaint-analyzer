import re


POSITIVE_WORDS = {
    "good",
    "great",
    "excellent",
    "helpful",
    "resolved",
    "quick",
    "fast",
    "satisfied",
    "thanks",
    "thank",
    "smooth",
    "polite",
}

NEGATIVE_WORDS = {
    "bad",
    "terrible",
    "poor",
    "angry",
    "disappointed",
    "worst",
    "broken",
    "damaged",
    "late",
    "delayed",
    "rude",
    "fraud",
    "scam",
    "error",
    "failed",
    "issue",
    "problem",
    "not",
    "never",
    "no",
}


def get_words(text):
    text = str(text).lower()
    words = re.findall(r"[a-zA-Z]+", text)
    return words


def get_sentiment_score(text):
    words = get_words(text)

    positive_count = 0
    negative_count = 0

    for word in words:
        if word in POSITIVE_WORDS:
            positive_count += 1

        if word in NEGATIVE_WORDS:
            negative_count += 1

    score = positive_count - negative_count
    return score


def classify_sentiment(text):
    score = get_sentiment_score(text)

    if score > 0:
        return "Positive"

    if score < 0:
        return "Negative"

    return "Neutral"