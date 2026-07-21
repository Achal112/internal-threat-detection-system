import streamlit as st

from database.database import DatabaseManager
from modules.activity_simulator import ActivitySimulator
from modules.risk_engine import RiskEngine

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# Initialize
# -------------------------

db = DatabaseManager()
db.create_tables()

simulator = ActivitySimulator()
risk_engine = RiskEngine()

# -------------------------
# Title
# -------------------------

st.title("🛡 SentinelAI")
st.write("AI-Based Insider Threat Detection System")

# -------------------------
# Generate Scenario
# -------------------------

if st.button("Generate Scenario"):

    activities = simulator.generate_scenario()

    for activity in activities:

        # Save event
        db.insert_event(
            activity["username"],
            activity["event_type"],
            activity["description"],
            activity["severity"]
        )

        # Get user's baseline
        baseline = db.get_baseline(activity["username"])

        if baseline is None:
            continue

        # Calculate risk
        risk, reasons = risk_engine.calculate_risk(
            activity,
            baseline
        )

        # Store risk
        db.insert_risk(
            activity["username"],
            risk
        )

        # Store alert if needed
        if risk > 0:

            db.insert_alert(
                activity["username"],
                risk,
                risk_engine.alert_level(risk),
                ", ".join(reasons)
            )

# -------------------------
# Activity Logs
# -------------------------

st.divider()

st.subheader("📄 Employee Activity Logs")

events = db.get_events()

event_table = []

for event in events:

    event_table.append({
        "User": event["username"],
        "Event": event["event_type"],
        "Description": event["description"],
        "Severity": event["severity"],
        "Time": event["timestamp"]
    })

st.dataframe(
    event_table,
    use_container_width=True
)

# -------------------------
# Alerts
# -------------------------

st.divider()

st.subheader("🚨 Threat Alerts")

alerts = db.get_alerts()

alert_table = []

for alert in alerts:

    alert_table.append({
        "User": alert["username"],
        "Risk Score": alert["risk_score"],
        "Alert Level": alert["alert_level"],
        "Reason": alert["reason"],
        "Time": alert["timestamp"]
    })

st.dataframe(
    alert_table,
    use_container_width=True
)

# -------------------------
# Close Database
# -------------------------

db.close()