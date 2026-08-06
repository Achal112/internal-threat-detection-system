import streamlit as st
import pandas as pd

from database.database import DatabaseManager
from modules.timeline_engine import TimelineEngine
from modules.mitre_mapper import MitreMapper

st.set_page_config(
    page_title="Incident Investigation",
    # page_icon="",
    layout="wide"
)

db = DatabaseManager()
timeline_engine = TimelineEngine()
mapper = MitreMapper()

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

for item in timeline:

    technique = mapper.map_event(item["event"])

    st.markdown(f"""
        ### {item["icon"]} {item["event"]}

        **User:** {selected_user}

        **Time:** {item["time"]}

        **MITRE ID:** {technique["id"]}

        **Technique:** {technique["name"]}

        **Description:**

        {item["description"]}

        ---
        """)

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