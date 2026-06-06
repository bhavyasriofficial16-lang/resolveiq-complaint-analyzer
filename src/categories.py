def clean_text(text):
    return str(text).lower()


CATEGORY_KEYWORDS = {
    "Delivery Issue": [
        "delivery",
        "delayed",
        "late",
        "shipping",
        "tracking",
        "package",
        "courier",
    ],
    "Payment Issue": [
        "payment",
        "charged",
        "transaction",
        "billing",
        "invoice",
        "money",
        "deducted",
        "card",
    ],
    "Refund Issue": [
        "refund",
        "return",
        "cashback",
        "replacement",
    ],
    "Product Quality": [
        "broken",
        "damaged",
        "defective",
        "quality",
        "faulty",
        "missing",
        "wrong item",
    ],
    "Technical Problem": [
        "app",
        "website",
        "login",
        "otp",
        "server",
        "crash",
        "bug",
        "error",
        "password",
    ],
    "Staff Behavior": [
        "staff",
        "agent",
        "rude",
        "manager",
        "employee",
        "support",
        "behavior",
    ],
}


def classify_category(text):
    text = clean_text(text)

    category_scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        category_scores[category] = score

    best_category = max(category_scores, key=category_scores.get)
    best_score = category_scores[best_category]

    if best_score == 0:
        return "Other"

    return best_category