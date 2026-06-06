def calculate_priority_score(row):
    score = 0

    if row["urgency"] == "High":
        score += 50
    elif row["urgency"] == "Medium":
        score += 25
    else:
        score += 5

    if row["sentiment"] == "Negative":
        score += 25
    elif row["sentiment"] == "Neutral":
        score += 10

    category = row["category"]

    if category in ["Payment Issue", "Refund Issue"]:
        score += 20
    elif category in ["Technical Problem", "Product Quality"]:
        score += 15
    elif category == "Staff Behavior":
        score += 10

    text = str(row.get("complaint", "")).lower()

    risk_words = ["fraud", "legal", "police", "unsafe", "emergency", "critical"]

    for word in risk_words:
        if word in text:
            score += 30

    return score


def assign_priority_level(score):
    if score >= 80:
        return "Critical"

    if score >= 55:
        return "High"

    if score >= 30:
        return "Medium"

    return "Low"


def choose_escalation_team(row):
    category = row["category"]
    complaint_text = str(row.get("complaint", "")).lower()

    if "fraud" in complaint_text or "legal" in complaint_text:
        return "Risk & Compliance Team"

    if category == "Payment Issue":
        return "Billing Team"

    if category == "Refund Issue":
        return "Refunds Team"

    if category == "Technical Problem":
        return "Technical Support Team"

    if category == "Product Quality":
        return "Quality Assurance Team"

    if category == "Staff Behavior":
        return "Customer Relations Team"

    if category == "Delivery Issue":
        return "Logistics Team"

    return "General Support Team"


def recommend_action(row):
    priority = row["priority_level"]
    category = row["category"]

    if priority == "Critical":
        return "Escalate immediately and contact the customer within 1 hour."

    if category == "Payment Issue":
        return "Verify transaction status and share payment resolution update."

    if category == "Refund Issue":
        return "Check refund status and provide expected completion timeline."

    if category == "Delivery Issue":
        return "Track shipment, contact logistics partner, and update customer."

    if category == "Technical Problem":
        return "Create technical ticket and ask customer for device/app details."

    if category == "Product Quality":
        return "Arrange replacement, return pickup, or quality inspection."

    if category == "Staff Behavior":
        return "Escalate to customer relations and review staff interaction."

    return "Review complaint manually and respond with next steps."


def assign_sla(priority_level):
    if priority_level == "Critical":
        return "1 hour"

    if priority_level == "High":
        return "4 hours"

    if priority_level == "Medium":
        return "24 hours"

    return "48 hours"


def generate_reply(row):
    category = row["category"]
    sla = row["sla"]

    return (
        f"Dear Customer, we are sorry for the inconvenience caused. "
        f"Your complaint has been identified as a {category}. "
        f"Our team will review it and get back to you within {sla}. "
        f"Thank you for your patience."
    )


def add_agent_decisions(analyzed_df):
    action_df = analyzed_df.copy()

    action_df["priority_score"] = action_df.apply(calculate_priority_score, axis=1)
    action_df["priority_level"] = action_df["priority_score"].apply(assign_priority_level)
    action_df["escalation_team"] = action_df.apply(choose_escalation_team, axis=1)
    action_df["recommended_action"] = action_df.apply(recommend_action, axis=1)
    action_df["sla"] = action_df["priority_level"].apply(assign_sla)
    action_df["suggested_reply"] = action_df.apply(generate_reply, axis=1)

    action_df = action_df.sort_values(
        by="priority_score",
        ascending=False,
    )

    return action_df


def build_action_plan(action_df):
    total = len(action_df)
    critical_count = len(action_df[action_df["priority_level"] == "Critical"])
    high_count = len(action_df[action_df["priority_level"] == "High"])

    top_team = action_df["escalation_team"].mode()[0]

    plan = (
        f"The AI agent reviewed {total} complaints. "
        f"{critical_count} complaints require critical attention and "
        f"{high_count} complaints are high priority. "
        f"The team receiving the most escalations is {top_team}. "
        f"Recommended next step: handle Critical and High complaints first, "
        f"then resolve Medium and Low priority complaints based on SLA."
    )

    return plan