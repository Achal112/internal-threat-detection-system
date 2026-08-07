import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import DatabaseManager
from modules.timeline_engine import TimelineEngine
from modules.mitre_mapper import MitreMapper
from modules.behavior_engine import BehaviorEngine

st.set_page_config(
    page_title="Incident Investigation",
    # page_icon="",
    layout="wide"
)

db = DatabaseManager()
timeline_engine = TimelineEngine()
mapper = MitreMapper()
behavior_engine = BehaviorEngine()

st.title("Incident Investigation")

# ------------------------------------
# Select User
# ------------------------------------

users = [
    "Alice",
    "Bob",
    "Charlie",
    "David"
]

selected_user = st.selectbox(
    "Select Employee",
    users
)

profile = db.get_user_profile(selected_user)

events = db.get_events()

events = [
    e for e in events
    if e["username"] == selected_user
]

timeline = timeline_engine.build_timeline(events)

# ------------------------------------
# Attack Timeline
# ------------------------------------

st.subheader("Attack Timeline")

timeline_table = []

for item in timeline:

    timeline_table.append({

        "Time": item["time"],
        "Event": f'{item["icon"]} {item["event"]}',
        "Severity": item["severity"],
        "Description": item["description"]

    })

timeline_df = pd.DataFrame(timeline_table)

st.dataframe(
    timeline_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("👤 Employee Profile")

if profile:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Department",
        profile["department"]
    )

    col2.metric(
        "Working Hours",
        f'{profile["login_start"]} - {profile["login_end"]}'
    )

    col3.metric(
        "USB Allowed",
        "Yes" if profile["usb_allowed"] else "No"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Avg Downloads",
        profile["avg_downloads"]
    )

    col5.metric(
        "Avg Files Opened",
        profile["avg_files_opened"]
    )

else:

    st.warning("Baseline profile not found.")

st.divider()

st.subheader("📊 Behavior Analytics")

if "latest_activity" in st.session_state:

    comparison = behavior_engine.compare(
        st.session_state["latest_activity"],
        profile
    )

    behavior_df = pd.DataFrame(comparison)

    st.dataframe(
        behavior_df,
        hide_index=True,
        use_container_width=True
    )

else:

    st.info("Generate a scenario first.")

# ------------------------------------
# Current Risk
# ------------------------------------

st.subheader("Current Risk")

risk_rows = db.get_latest_risks()

for row in risk_rows:

    if row["username"] == selected_user:

        score = row["risk_score"]

        if score >= 80:
            st.error(f"🔴 Critical Risk ({score})")

        elif score >= 50:
            st.warning(f"🟠 High Risk ({score})")

        elif score >= 20:
            st.info(f"🟡 Medium Risk ({score})")

        else:
            st.success(f"🟢 Low Risk ({score})")


st.divider()

st.subheader("📈 Risk Trend")

risk_history = db.get_user_risk_history(
    selected_user
)

risk_df = pd.DataFrame(
    [dict(row) for row in risk_history]
)

if not risk_df.empty:

    fig = px.line(
        risk_df,
        x="timestamp",
        y="risk_score",
        markers=True,
        title=f"{selected_user} Risk Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No risk history available.")

# ------------------------------------
# Threat Timeline
# ------------------------------------

st.divider()

st.subheader("Threat Timeline")

with st.expander("View Attack Timeline", expanded=False):

    if len(timeline) == 0:

        st.info("No activity found.")

    else:

        for item in timeline:

            st.markdown(f"""
        ### {item["icon"]} {item["event"]}

        **Time**

        {item["time"]}

        **Description**

        {item["description"]}

        ---
        """)
    
# ------------------------------------
# Calculate Investigation Statistics
# ------------------------------------

total_events = len(events)

critical_events = sum(
    1
    for e in events
    if e["severity"].lower() == "critical"
)

high_events = sum(
    1
    for e in events
    if e["severity"].lower() == "high"
)

medium_events = sum(
    1
    for e in events
    if e["severity"].lower() == "medium"
)

low_events = sum(
    1
    for e in events
    if e["severity"].lower() == "low"
)

# ------------------------------------
# Investigation Summary
# ------------------------------------

st.divider()

with st.expander("Investigation Summary", expanded=False):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Events", total_events)
    c2.metric("Critical", critical_events)
    c3.metric("High", high_events)
    c4.metric("Medium", medium_events)
# ------------------------------------
# AI Explanation
# ------------------------------------

st.divider()

with st.expander("AI Explanation", expanded=False):

    if "last_explanation" in st.session_state:

        for line in st.session_state["last_explanation"]:

            st.write(line)

    else:

        st.info("Generate a scenario first.")


db.close()