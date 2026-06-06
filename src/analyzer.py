from collections import Counter
import re

import pandas as pd

from src.categories import classify_category
from src.sentiment import classify_sentiment, get_sentiment_score
from src.urgency import classify_urgency, get_urgency_score


STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "this",
    "with",
    "from",
    "have",
    "has",
    "was",
    "were",
    "are",
    "but",
    "not",
    "you",
    "your",
    "our",
    "they",
    "them",
    "their",
    "please",
    "about",
    "after",
    "before",
    "into",
    "been",
    "will",
    "would",
    "could",
    "should",
}


def get_words(text):
    text = str(text).lower()
    return re.findall(r"[a-zA-Z]+", text)


def analyze_complaints(df, text_column):
    analyzed_df = df.copy()

    analyzed_df["category"] = analyzed_df[text_column].apply(classify_category)
    analyzed_df["sentiment_score"] = analyzed_df[text_column].apply(get_sentiment_score)
    analyzed_df["sentiment"] = analyzed_df[text_column].apply(classify_sentiment)
    analyzed_df["urgency_score"] = analyzed_df[text_column].apply(get_urgency_score)
    analyzed_df["urgency"] = analyzed_df[text_column].apply(classify_urgency)

    return analyzed_df


def get_top_keywords(df, text_column, top_n=8):
    all_words = []

    for complaint in df[text_column]:
        words = get_words(complaint)

        for word in words:
            if len(word) > 3 and word not in STOPWORDS:
                all_words.append(word)

    word_counts = Counter(all_words)
    top_words = word_counts.most_common(top_n)

    return [word for word, count in top_words]


def build_summary(analyzed_df, text_column):
    total_complaints = len(analyzed_df)

    high_urgency_count = len(analyzed_df[analyzed_df["urgency"] == "High"])
    negative_count = len(analyzed_df[analyzed_df["sentiment"] == "Negative"])

    if total_complaints > 0:
        top_category = analyzed_df["category"].mode()[0]
    else:
        top_category = "No complaints"

    top_keywords = get_top_keywords(analyzed_df, text_column)

    summary_text = (
        f"The dataset contains {total_complaints} complaints. "
        f"The most common complaint category is {top_category}. "
        f"There are {high_urgency_count} high urgency complaints and "
        f"{negative_count} negative complaints. "
        f"Common keywords include: {', '.join(top_keywords)}."
    )

    summary = {
        "total_complaints": total_complaints,
        "high_urgency_count": high_urgency_count,
        "negative_count": negative_count,
        "top_category": top_category,
        "top_keywords": top_keywords,
        "summary_text": summary_text,
    }

    return summary