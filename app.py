import pandas as pd
import plotly.express as px
import streamlit as st
from docx import Document
from pypdf import PdfReader
from auth import sign_in, sign_up

from src.analyzer import analyze_complaints, build_summary
from src.agent import add_agent_decisions, build_action_plan


st.set_page_config(
    page_title="ResolveIQ",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(59,130,246,0.18), transparent 35%),
        radial-gradient(circle at 85% 25%, rgba(139,92,246,0.16), transparent 35%),
        radial-gradient(circle at 50% 85%, rgba(6,182,212,0.14), transparent 40%),
        #ffffff;
    color: #0f172a;
}

header[data-testid="stHeader"] {
    background: transparent;
}

div[data-testid="stToolbar"] {
    display: none;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1 {
    color: #0f172a !important;
    font-size: 48px !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    letter-spacing: 0 !important;
}

h2, h3 {
    color: #111827 !important;
    font-weight: 750 !important;
}

p, label, span {
    color: #475569;
}

.hero-simple {
    text-align: center;
    max-width: 940px;
    margin: 0 auto;
    padding: 56px 0 34px 0;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #0f2a5f;
    padding: 12px 22px;
    border-radius: 999px;
    font-size: 22px;
    font-weight: 850;
    margin-bottom: 24px;
    letter-spacing: 0;
    box-shadow: 0 0 25px rgba(37,99,235,0.25);
    transition: all 0.3s ease;
}

.hero-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 40px rgba(37,99,235,0.4);
}

.hero-simple h1 {
    color: #0f172a !important;
    font-size: 56px !important;
    font-weight: 850 !important;
    line-height: 1.08 !important;
    margin-bottom: 20px;
}

.hero-simple p {
    color: #64748b;
    font-size: 19px;
    line-height: 1.65;
    max-width: 760px;
    margin: 0 auto;
}

.hero-visual {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    max-width: 860px;
    margin: 38px auto 0 auto;
}

.signal-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 16px;
    padding: 18px;
    text-align: left;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    animation: floatCard 4s ease-in-out infinite;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.signal-card:nth-child(2) {
    animation-delay: 0.4s;
}

.signal-card:nth-child(3) {
    animation-delay: 0.8s;
}

.signal-card:nth-child(4) {
    animation-delay: 1.2s;
}

.signal-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
}

.signal-value {
    color: #0f2a5f;
    font-size: 20px;
    font-weight: 850;
}

@keyframes floatCard {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-8px);
    }
    100% {
        transform: translateY(0);
    }
}

.upload-panel {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 18px;
    padding: 26px;
    margin: 12px auto 34px auto;
    text-align: center;
    max-width: 760px;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.upload-panel p {
    color: #64748b;
}

div[data-testid="stFileUploader"] {
    max-width: 760px;
    margin: 0 auto 34px auto;
}

div[data-testid="stFileUploader"] section {
    background: #ffffff !important;
    border: 1px dashed #2563eb !important;
    border-radius: 16px !important;
    padding: 22px !important;
}

div[data-testid="stFileUploader"] button,
div.stButton > button,
.stDownloadButton > button {
    background: #0f2a5f !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
}

div[data-testid="stFileUploader"] button p,
div[data-testid="stFileUploader"] button span,
div.stButton > button p,
.stDownloadButton > button p {
    color: #ffffff !important;
}

div[data-testid="stFileUploader"] button:hover,
div.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #1d4ed8 !important;
    color: #ffffff !important;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.5);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-6px);
    box-shadow: 0 24px 60px rgba(15,23,42,0.12);
}

div[data-testid="stMetric"] label {
    color: #64748b !important;
}

div[data-testid="stMetric"] div {
    color: #0f172a !important;
}

.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
    box-shadow: 0 14px 34px rgba(15, 23, 42, 0.06);
}

.chat-panel {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 18px;
    padding: 22px;
    margin: 28px 0;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

div[data-testid="stChatMessage"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    color: #0f172a !important;
}

div[data-testid="stChatMessage"] p {
    color: #0f172a !important;
}

textarea {
    color: #0f172a !important;
    background: #ffffff !important;
}

section[data-testid="stSidebar"] {
    background: #07172f;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: #e5f0ff !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    border-radius: 12px;
    padding: 8px 10px;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] {
    background: #07172f;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: #e5f0ff !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.08);
}

@media (max-width: 900px) {
    h1 {
        font-size: 38px !important;
    }

    .hero-simple h1 {
        font-size: 40px !important;
    }

    .hero-visual {
        grid-template-columns: 1fr 1fr;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)


def load_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
        complaints = [line.strip() for line in text.splitlines() if line.strip()]
        return pd.DataFrame({"complaint": complaints})

    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        complaints = [
            line.strip()
            for line in text.splitlines()
            if len(line.strip()) > 10
        ]

        return pd.DataFrame({"complaint": complaints})

    if file_name.endswith(".docx"):
        document = Document(uploaded_file)
        complaints = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if len(paragraph.text.strip()) > 10
        ]

        return pd.DataFrame({"complaint": complaints})

    return None


def detect_text_column(df):
    possible_columns = [
        "complaint",
        "message",
        "text",
        "review",
        "description",
        "ticket",
        "feedback",
    ]

    lowercase_columns = {}

    for column in df.columns:
        lowercase_columns[column.lower()] = column

    for possible_column in possible_columns:
        if possible_column in lowercase_columns:
            return lowercase_columns[possible_column]

    return None


def answer_chat_question(question, action_df, action_plan):
    question = question.lower()

    if "critical" in question:
        critical_cases = action_df[action_df["priority_level"] == "Critical"]
        return f"There are {len(critical_cases)} critical complaints. These should be handled first."

    if "high" in question or "priority" in question or "prioritize" in question:
        priority_cases = action_df[action_df["priority_level"].isin(["Critical", "High"])]
        return (
            f"There are {len(priority_cases)} critical/high-priority complaints. "
            "Start with Critical cases first, then High, then Medium and Low."
        )

    if "team" in question or "escalation" in question:
        team_counts = action_df["escalation_team"].value_counts()
        top_team = team_counts.index[0]
        count = team_counts.iloc[0]
        return f"The top escalation team is {top_team} with {count} complaints assigned."

    if "category" in question or "common issue" in question:
        category_counts = action_df["category"].value_counts()
        top_category = category_counts.index[0]
        count = category_counts.iloc[0]
        return f"The most common complaint category is {top_category} with {count} complaints."

    if "sentiment" in question or "negative" in question:
        sentiment_counts = action_df["sentiment"].value_counts().to_dict()
        return f"Sentiment distribution: {sentiment_counts}"

    if "urgency" in question:
        urgency_counts = action_df["urgency"].value_counts().to_dict()
        return f"Urgency distribution: {urgency_counts}"

    if "sla" in question or "time" in question:
        sla_counts = action_df["sla"].value_counts().to_dict()
        return f"SLA distribution: {sla_counts}"

    if "reply" in question:
        top_case = action_df.sort_values("priority_score", ascending=False).iloc[0]
        return f"Suggested reply for the highest-priority complaint: {top_case['suggested_reply']}"

    if "action" in question or "what should" in question:
        top_case = action_df.sort_values("priority_score", ascending=False).iloc[0]
        return (
            f"Recommended first action: {top_case['recommended_action']} "
            f"This should go to the {top_case['escalation_team']}."
        )

    if "summary" in question or "plan" in question:
        return action_plan

    return (
        "You can ask me things like: 'Which category is most common?', "
        "'How many critical complaints are there?', 'Which team should handle them?', "
        "'What is the SLA?', or 'What action should we take first?'"
    )


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user" not in st.session_state:
    st.session_state.user = None

if "analysis_ready" not in st.session_state:
    st.session_state.analysis_ready = False

if "report_history" not in st.session_state:
    st.session_state.report_history = []

if "recent_files" not in st.session_state:
    st.session_state.recent_files = []


def show_login_page():
    st.html(
        """
<div class="hero-simple">
    <div class="hero-badge">ResolveIQ</div>
    <h1>AI Complaint Intelligence & Action Planner</h1>
    <p>
        Login to analyze complaint files, generate action plans,
        view reports, and chat with your complaint intelligence agent.
    </p>
</div>
        """
    )

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        auth_mode = st.radio(
            "Select",
            ["Login", "Sign Up"],
            horizontal=True,
        )

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if auth_mode == "Login":
            if st.button("Login", use_container_width=True):
                user = sign_in(email, password)

                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid email or password")

        else:
            if st.button("Create Account", use_container_width=True):
                user = sign_up(email, password)

                if user:
                    st.success("Account created successfully. Please login.")
                else:
                    st.error("Signup failed")


def save_current_report(source_name, analyzed_df, action_df, summary, action_plan):
    report = {
        "source_name": source_name,
        "total_complaints": summary["total_complaints"],
        "top_category": summary["top_category"],
        "high_urgency_count": summary["high_urgency_count"],
        "negative_count": summary.get(
            "negative_count",
            summary.get("negative_sentiment_count", 0),
        ),
        "action_plan": action_plan,
        "analyzed_df": analyzed_df,
        "action_df": action_df,
    }

    st.session_state.report_history.insert(0, report)
    st.session_state.recent_files.insert(0, source_name)


def show_new_analysis():
    st.html(
        """
<div class="hero-simple">
    <div class="hero-badge">ResolveIQ</div>
    <h1>New Complaint Analysis</h1>
    <p>
        Upload a complaint file and generate structured signals,
        AI priorities, escalation teams, replies, and action plans.
    </p>
</div>
        """
    )

    st.html(
        """
<div class="upload-panel">
    <h3>Start Analysis</h3>
    <p>Upload CSV, TXT, PDF, or DOCX complaint files.</p>
</div>
        """
    )

    uploaded_file = st.file_uploader(
        "Choose complaint file",
        type=["csv", "txt", "pdf", "docx"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.info("Upload a complaint file to begin analysis.")
        return

    df = load_uploaded_file(uploaded_file)

    if df is None or df.empty:
        st.error("Could not read this file. Please upload a valid file.")
        return

    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

    text_column = detect_text_column(df)

    if text_column is None:
        st.error(
            "No complaint text column found. Use complaint, message, text, "
            "review, description, ticket, or feedback."
        )
        return

    st.success(f"Using '{text_column}' as the complaint text column.")

    if st.button("Analyze Complaints", use_container_width=True):
        analyzed_df = analyze_complaints(df, text_column)

        if text_column != "complaint":
            analyzed_df["complaint"] = analyzed_df[text_column]

        summary = build_summary(analyzed_df, text_column)
        action_df = add_agent_decisions(analyzed_df)
        action_plan = build_action_plan(action_df)

        st.session_state.df = df
        st.session_state.text_column = text_column
        st.session_state.analyzed_df = analyzed_df
        st.session_state.summary = summary
        st.session_state.action_df = action_df
        st.session_state.action_plan = action_plan
        st.session_state.analysis_ready = True
        st.session_state.chat_history = []

        save_current_report(
            uploaded_file.name,
            analyzed_df,
            action_df,
            summary,
            action_plan,
        )

        st.success("Analysis complete. Open Dashboard from the sidebar.")


def show_dashboard():
    st.title("Dashboard")

    if not st.session_state.analysis_ready:
        st.info("Run a new analysis first.")
        return

    analyzed_df = st.session_state.analyzed_df
    summary = st.session_state.summary
    action_df = st.session_state.action_df
    action_plan = st.session_state.action_plan

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Complaints", summary["total_complaints"])
    col2.metric("High Urgency", summary["high_urgency_count"])
    col3.metric(
        "Negative Complaints",
        summary.get("negative_count", summary.get("negative_sentiment_count", 0)),
    )
    col4.metric("Top Category", summary["top_category"])

    agent_col1, agent_col2, agent_col3 = st.columns(3)

    agent_col1.metric(
        "Critical Cases",
        len(action_df[action_df["priority_level"] == "Critical"]),
    )
    agent_col2.metric(
        "High Priority Cases",
        len(action_df[action_df["priority_level"] == "High"]),
    )
    agent_col3.metric("Top Team", action_df["escalation_team"].mode()[0])

    st.subheader("Management Summary")
    st.write(summary.get("summary_text", summary.get("executive_summary", "")))

    st.subheader("AI Agent Action Plan")
    st.write(action_plan)

    chart_col1, chart_col2, chart_col3 = st.columns(3)

    with chart_col1:
        category_counts = analyzed_df["category"].value_counts().reset_index()
        category_counts.columns = ["category", "count"]

        fig = px.bar(
            category_counts,
            x="category",
            y="count",
            title="Categories",
        )
        fig.update_layout(font_color="#0f172a")
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        sentiment_counts = analyzed_df["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["sentiment", "count"]

        fig = px.pie(
            sentiment_counts,
            names="sentiment",
            values="count",
            title="Sentiment",
        )
        fig.update_layout(font_color="#0f172a")
        st.plotly_chart(fig, use_container_width=True)

    with chart_col3:
        urgency_counts = analyzed_df["urgency"].value_counts().reset_index()
        urgency_counts.columns = ["urgency", "count"]

        fig = px.bar(
            urgency_counts,
            x="urgency",
            y="count",
            title="Urgency",
        )
        fig.update_layout(font_color="#0f172a")
        st.plotly_chart(fig, use_container_width=True)


def show_history():
    st.title("History")

    if not st.session_state.report_history:
        st.info("No report history yet.")
        return

    history_rows = []

    for report in st.session_state.report_history:
        history_rows.append(
            {
                "File": report["source_name"],
                "Total Complaints": report["total_complaints"],
                "Top Category": report["top_category"],
                "High Urgency": report["high_urgency_count"],
                "Negative": report["negative_count"],
            }
        )

    st.dataframe(pd.DataFrame(history_rows), use_container_width=True)


def show_uploads():
    st.title("Uploads")

    if not st.session_state.recent_files:
        st.info("No uploaded files yet.")
        return

    for file_name in st.session_state.recent_files:
        st.write(f"Uploaded file: {file_name}")


def show_reports():
    st.title("Reports")

    if not st.session_state.analysis_ready:
        st.info("Analyze a file first to download reports.")
        return

    analyzed_df = st.session_state.analyzed_df
    action_df = st.session_state.action_df

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download Analyzed CSV",
            data=analyzed_df.to_csv(index=False).encode("utf-8"),
            file_name="analyzed_complaints.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="Download AI Action Plan",
            data=action_df.to_csv(index=False).encode("utf-8"),
            file_name="ai_action_plan.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.subheader("Analyzed Complaints")
    st.dataframe(analyzed_df, use_container_width=True)

    st.subheader("AI Agent Decisions")
    st.dataframe(action_df, use_container_width=True)


def show_chat_booth():
    st.title("Chat Booth")

    if not st.session_state.analysis_ready:
        st.info("Analyze a file first, then ask questions.")
        return

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_question = st.chat_input(
        "Ask about priorities, teams, replies, SLA, or action plan..."
    )

    if user_question:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_question}
        )

        answer = answer_chat_question(
            user_question,
            st.session_state.action_df,
            st.session_state.action_plan,
        )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)


def show_recents():
    st.title("Recents")

    if not st.session_state.recent_files:
        st.info("No recent files yet.")
        return

    for index, file_name in enumerate(st.session_state.recent_files[:5], start=1):
        st.write(f"{index}. {file_name}")


if st.session_state.user is None:
    show_login_page()
    st.stop()


with st.sidebar:
    st.markdown("## ResolveIQ")
    st.caption("Complaint Intelligence Workspace")

    selected_page = st.radio(
        "Menu",
        [
            "New Analysis",
            "Dashboard",
            "History",
            "Uploads",
            "Reports",
            "Chat Booth",
            "Recents",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.analysis_ready = False
        st.rerun()


if selected_page == "New Analysis":
    show_new_analysis()
elif selected_page == "Dashboard":
    show_dashboard()
elif selected_page == "History":
    show_history()
elif selected_page == "Uploads":
    show_uploads()
elif selected_page == "Reports":
    show_reports()
elif selected_page == "Chat Booth":
    show_chat_booth()
elif selected_page == "Recents":
    show_recents()