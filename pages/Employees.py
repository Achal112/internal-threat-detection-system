import streamlit as st
import pandas as pd

from database.database import DatabaseManager


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Employees | SentinelAI",
    page_icon="",
    layout="wide"
)


# ---------------------------------------------------
# Initialize
# ---------------------------------------------------

db = DatabaseManager()
db.create_tables()


# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("Employee Intelligence")

st.write(
    "Behavioral profiles, security baselines and risk intelligence "
    "for monitored employees."
)

st.divider()


# ---------------------------------------------------
# Get Employees
# ---------------------------------------------------

users = db.get_all_users()

if not users:

    st.warning("No employees found in the database.")
    db.close()
    st.stop()


# ---------------------------------------------------
# Employee Selector
# ---------------------------------------------------

user_names = [
    user["username"]
    for user in users
]

selected_user = st.selectbox(
    "Select Employee",
    user_names
)


# ---------------------------------------------------
# Employee Profile
# ---------------------------------------------------

profile = db.get_user_profile(
    selected_user
)

baseline = db.get_baseline(
    selected_user
)


# ---------------------------------------------------
# Current Risk
# ---------------------------------------------------

risk_rows = db.get_latest_risks()

current_risk = 0

for row in risk_rows:

    if row["username"] == selected_user:

        current_risk = row["risk_score"]
        break


# ---------------------------------------------------
# Threat Level
# ---------------------------------------------------

if current_risk >= 80:

    threat_level = "🔴 Critical"

elif current_risk >= 50:

    threat_level = "🟠 High"

elif current_risk >= 20:

    threat_level = "🟡 Medium"

else:

    threat_level = "🟢 Low"


# ---------------------------------------------------
# Profile Header
# ---------------------------------------------------

st.subheader("Employee Profile")


profile_col1, profile_col2, profile_col3 = st.columns(3)


with profile_col1:

    st.metric(
        "Employee",
        selected_user
    )


with profile_col2:

    department = "Unknown"

    if profile:

        department = (
            profile["department"]
            or "Unknown"
        )

    st.metric(
        "Department",
        department
    )


with profile_col3:

    role = "Unknown"

    if profile:

        role = (
            profile["role"]
            or "Unknown"
        )

    st.metric(
        "Role",
        role
    )


# ---------------------------------------------------
# Risk Overview
# ---------------------------------------------------

st.subheader("Risk Overview")


risk_col1, risk_col2, risk_col3 = st.columns(3)


with risk_col1:

    st.metric(
        "Current Risk Score",
        current_risk
    )


with risk_col2:

    st.metric(
        "Threat Level",
        threat_level
    )


with risk_col3:

    if baseline:

        login_window = (
            f"{baseline['login_start']} - "
            f"{baseline['login_end']}"
        )

    else:

        login_window = "Unknown"

    st.metric(
        "Normal Login Window",
        login_window
    )


st.divider()


# ---------------------------------------------------
# Behavioral Baseline
# ---------------------------------------------------

st.subheader("Behavioral Baseline")


if baseline:

    baseline_col1, baseline_col2, baseline_col3, baseline_col4 = (
        st.columns(4)
    )

    with baseline_col1:

        st.metric(
            "Avg Downloads",
            baseline["avg_downloads"]
        )

    with baseline_col2:

        st.metric(
            "Avg Files Opened",
            baseline["avg_files_opened"]
        )

    with baseline_col3:

        usb_policy = (
            "Allowed"
            if baseline["usb_allowed"]
            else "Not Allowed"
        )

        st.metric(
            "USB Policy",
            usb_policy
        )

    with baseline_col4:

        st.metric(
            "Login Window",
            f"{baseline['login_start']} - "
            f"{baseline['login_end']}"
        )

else:

    st.info(
        "Behavioral baseline not available."
    )


st.divider()


# ---------------------------------------------------
# Employee Activity
# ---------------------------------------------------

st.subheader("Employee Activity")


all_events = db.get_events()

user_events = [

    event
    for event in all_events
    if event["username"] == selected_user

]


total_events = len(user_events)

critical_events = sum(
    1
    for event in user_events
    if str(event["severity"]).lower()
    == "critical"
)

high_events = sum(
    1
    for event in user_events
    if str(event["severity"]).lower()
    == "high"
)


activity_col1, activity_col2, activity_col3 = st.columns(3)


with activity_col1:

    st.metric(
        "Total Events",
        total_events
    )


with activity_col2:

    st.metric(
        "Critical Events",
        critical_events
    )


with activity_col3:

    st.metric(
        "High Events",
        high_events
    )


# ---------------------------------------------------
# Activity Table
# ---------------------------------------------------

if user_events:

    activity_table = []

    for event in user_events:

        severity = str(
            event["severity"]
        ).lower()

        if severity == "critical":

            display_severity = "🔴 Critical"

        elif severity == "high":

            display_severity = "🟠 High"

        elif severity == "medium":

            display_severity = "🟡 Medium"

        else:

            display_severity = "🟢 Low"

        activity_table.append({

            "Event": event["event_type"],

            "Description": event["description"],

            "Severity": display_severity,

            "Time": event["timestamp"]

        })


    activity_df = pd.DataFrame(
        activity_table
    )

    st.dataframe(
        activity_df.head(20),
        hide_index=True,
        use_container_width=True
    )

else:

    st.info(
        "No activity recorded for this employee."
    )


# ---------------------------------------------------
# Risk History
# ---------------------------------------------------

st.divider()

st.subheader("Risk History")

risk_history = db.get_user_risk_history(
    selected_user
)

risk_history_df = pd.DataFrame(
    [dict(row) for row in risk_history]
)

if not risk_history_df.empty:

    st.line_chart(
        risk_history_df,
        x="timestamp",
        y="risk_score"
    )

else:

    st.info(
        "No risk history available for this employee."
    )

# ---------------------------------------------------
# Close Database
# ---------------------------------------------------

db.close()