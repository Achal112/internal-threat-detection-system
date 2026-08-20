import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import DatabaseManager
from modules.timeline_engine import TimelineEngine
from modules.mitre_mapper import MitreMapper
from modules.behavior_engine import BehaviorEngine
from modules.report_generator import IncidentReportGenerator
from modules.behavior_analyzer import BehaviorAnalyzer

st.set_page_config(
    page_title="Incident Investigation",
    # page_icon="",
    layout="wide"
)

db = DatabaseManager()
timeline_engine = TimelineEngine()
mapper = MitreMapper()
behavior_engine = BehaviorEngine()
report_generator = IncidentReportGenerator()
behavior_analyzer = BehaviorAnalyzer()

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

# Get employee selected from Alerts page
default_user = st.session_state.get(
    "investigation_user"
)

# Find the correct default index
if default_user in users:
    default_index = users.index(default_user)
else:
    default_index = 0

selected_user = st.selectbox(
    "Select Employee",
    users,
    index=default_index
)

profile = db.get_user_profile(selected_user)
baseline = db.get_user_baseline(selected_user)

events = db.get_events()

events = [
    e for e in events
    if e["username"] == selected_user
]

# ------------------------------------
# MITRE ATT&CK Mapping
# ------------------------------------

st.divider()

st.subheader("MITRE ATT&CK Mapping")

mitre_results = mapper.map_events(events)

mitre_table = []

for result in mitre_results:

    mitre_table.append({
        "Event": result["event"],
        "Technique": result["name"],
        "MITRE ID": result["id"],
        "Tactic": result["tactic"]
    })

mitre_df = pd.DataFrame(mitre_table)

if not mitre_df.empty:

    st.dataframe(
        mitre_df,
        hide_index=True,
        use_container_width=True
    )

else:

    st.info(
        "No MITRE ATT&CK techniques detected."
    )

timeline = timeline_engine.build_timeline(events)

# ------------------------------------
# Behavioral Deviations
# ------------------------------------

st.divider()

st.subheader("Behavioral Deviations")

if baseline is not None and events:

    # Use the most recent relevant activity
    latest_event = events[0]

    # Activity data may not exist in the database event row,
    # so use the latest generated activity when available.
    activity = st.session_state.get(
        "latest_activity"
    )

    if activity is not None:

        deviations = behavior_analyzer.analyze(
            activity,
            baseline
        )

        if deviations:

            deviation_table = []

            for deviation in deviations:

                deviation_table.append({
                    "Category": deviation["category"],
                    "Normal": deviation["normal"],
                    "Observed": deviation["observed"],
                    "Severity": deviation["severity"],
                    "Deviation": deviation["message"]
                })

            deviation_df = pd.DataFrame(
                deviation_table
            )

            st.dataframe(
                deviation_df,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.success(
                "No significant behavioral deviations detected."
            )

    else:

        st.info(
            "Generate a scenario first to analyze behavioral deviations."
        )

else:

    st.info(
        "Behavioral baseline is not available for this employee."
    )

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

# Employee Profile--------------------------------------!

st.subheader("Employee Profile")

if profile and baseline:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Department",
        profile["department"] or "Unknown"
    )

    col2.metric(
        "Working Hours",
        f'{baseline["login_start"]} - {baseline["login_end"]}'
    )

    col3.metric(
        "USB Allowed",
        "Yes" if baseline["usb_allowed"] else "No"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Avg Downloads",
        baseline["avg_downloads"]
    )

    col5.metric(
        "Avg Files Opened",
        baseline["avg_files_opened"]
    )

else:

    st.warning("Employee profile or baseline not found.")

st.divider()

# behavior analytics----------------------------------------!

st.subheader("Behavior Analytics")

if "latest_activity" in st.session_state and baseline:

    comparison = behavior_engine.compare(
        st.session_state["latest_activity"],
        baseline
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

st.subheader("Risk Trend")

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
# Incident Report
# ------------------------------------

st.divider()

st.subheader("Incident Report")

if events:

    # --------------------------------
    # Get selected user's risk
    # --------------------------------

    selected_risk = 0

    for row in risk_rows:

        if row["username"] == selected_user:
            selected_risk = row["risk_score"]
            break

    # --------------------------------
    # Determine threat level
    # --------------------------------

    if selected_risk >= 80:
        threat_level = "Critical"

    elif selected_risk >= 50:
        threat_level = "High"

    elif selected_risk >= 20:
        threat_level = "Medium"

    else:
        threat_level = "Low"

    # --------------------------------
    # Get MITRE mappings
    # --------------------------------

    mitre_results = mapper.map_events(events)

    # --------------------------------
    # Get explanation
    # --------------------------------

    explanation = st.session_state.get(
        "last_explanation",
        "No AI explanation available."
    )

    # --------------------------------
    # Risk reasons
    # --------------------------------

    reasons = []

    for event in events:

        if event["severity"].lower() in [
            "high",
            "critical"
        ]:

            reasons.append(
                event["description"]
            )

    # Remove duplicates
    reasons = list(dict.fromkeys(reasons))

    # --------------------------------
    # Generate PDF
    # --------------------------------

    if st.button("Generate Incident Report"):

        profile = db.get_user_profile(selected_user)

        department = "Unknown"

        if profile:
            department = profile["department"] or "Unknown"

            pdf = report_generator.generate(

                username=selected_user,

                risk_score=selected_risk,

                threat_level=threat_level,

                department=department,

                events=events,

                mitre_results=mitre_results,

                explanation=explanation,

                reasons=reasons
            )

        st.download_button(
            label="Download Incident Report",
            data=pdf,
            file_name=f"{selected_user}_incident_report.pdf",
            mime="application/pdf"
        )

else:

    st.info(
        "No activity available for report generation."
    )

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