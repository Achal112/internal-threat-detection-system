import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import DatabaseManager
from modules.activity_simulator import ActivitySimulator
from modules.risk_engine import RiskEngine
from modules.anomaly_detector import AnomalyDetector
from modules.mitre_mapper import MitreMapper
from modules.explanation_engine import ExplanationEngine


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------
# Initialize
# ---------------------------------------------------

db = DatabaseManager()
db.create_tables()

simulator = ActivitySimulator()
risk_engine = RiskEngine()
ai_detector = AnomalyDetector()
explanation_engine = ExplanationEngine()
mitre = MitreMapper()


# ---------------------------------------------------
# Train AI Model
# ---------------------------------------------------

training_data = [
    [8, 5, 20, 0, 0],
    [9, 4, 18, 0, 1],
    [8, 6, 22, 1, 0],
    [9, 5, 19, 0, 2],
    [8, 5, 21, 0, 0],
    [9, 4, 20, 1, 1],
    [8, 6, 18, 0, 0],
    [9, 5, 23, 1, 1]
]

ai_detector.train(training_data)


# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("🛡️ SentinelAI")
st.write("### AI-Based Insider Threat Detection & UEBA Dashboard")


# ---------------------------------------------------
# Generate Scenario
# ---------------------------------------------------

if st.button("Generate Scenario"):

    activities = simulator.generate_scenario()

    for activity in activities:

        # ---------------------------------------------
        # Store Event
        # ---------------------------------------------

        db.insert_event(
            activity["username"],
            activity["event_type"],
            activity["description"],
            activity["severity"]
        )

        # ---------------------------------------------
        # Get Baseline
        # ---------------------------------------------

        baseline = db.get_baseline(
            activity["username"]
        )

        if baseline is None:
            continue

        # ---------------------------------------------
        # Risk Engine
        # ---------------------------------------------

        risk, reasons = risk_engine.calculate_risk(
            activity,
            baseline
        )

        # ---------------------------------------------
        # AI Anomaly Detection
        # ---------------------------------------------

        sample = [
            activity.get("login_hour", 0),
            activity.get("downloads", 0),
            activity.get("files_opened", 0),
            activity.get("usb_used", 0),
            activity.get("failed_logins", 0)
        ]

        try:
            prediction = ai_detector.predict(sample)
        except Exception:
            prediction = "Unknown"

        # ---------------------------------------------
        # Save Latest Activity
        # ---------------------------------------------

        st.session_state["latest_activity"] = activity

        # ---------------------------------------------
        # AI Explanation
        # ---------------------------------------------

        explanation = explanation_engine.explain(
            activity,
            baseline,
            risk,
            reasons
        )

        st.session_state["last_explanation"] = explanation

        # ---------------------------------------------
        # Store Risk
        # ---------------------------------------------

        db.insert_risk(
            activity["username"],
            risk
        )

        # ---------------------------------------------
        # Store Alert
        # ---------------------------------------------

        if risk > 0:

            db.insert_alert(
                activity["username"],
                risk,
                risk_engine.alert_level(risk),
                ", ".join(reasons)
            )

    st.success("Scenario generated successfully!")

# ---------------------------------------------
# AI Detection Result
# ---------------------------------------------

st.subheader("AI Detection Result")

activity = st.session_state.get(
    "latest_activity"
)

if activity:

    sample = [
        activity.get("login_hour", 0),
        activity.get("downloads", 0),
        activity.get("files_opened", 0),
        activity.get("usb_used", 0),
        activity.get("failed_logins", 0)
    ]

    try:
        prediction = ai_detector.predict(sample)

    except Exception:
        prediction = "Unknown"


# ---------------------------------------------
# Save AI Analysis
# ---------------------------------------------

    if prediction in ["Anomaly", "Normal"]:

        db.insert_ai_analysis(
            username=activity["username"],
            login_hour=activity.get("login_hour", 0),
            downloads=activity.get("downloads", 0),
            files_opened=activity.get("files_opened", 0),
            usb_used=activity.get("usb_used", 0),
            failed_logins=activity.get("failed_logins", 0),
            prediction=prediction
        )


# ---------------------------------------------
# Display AI Result
# ---------------------------------------------

    if prediction == "Anomaly":

        st.error(
            f"{activity['username']} → "
            "AI detected anomalous behaviour"
        )

    elif prediction == "Normal":

        st.success(
            f"{activity['username']} → "
            "Normal behaviour"
        )

    else:

        st.info(
            f"{activity['username']} → "
            f"AI result: {prediction}"
        )

# ---------------------------------------------------
# Dashboard Metrics
# ---------------------------------------------------

user_count = db.get_user_count()
event_count = db.get_event_count()
alert_count = db.get_alert_count()

risk_rows = db.get_latest_risks()

average_risk = 0

if len(risk_rows) > 0:

    average_risk = sum(
        row["risk_score"]
        for row in risk_rows
    ) / len(risk_rows)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Employees",
    user_count
)

col2.metric(
    "Events",
    event_count
)

col3.metric(
    "Alerts",
    alert_count
)

col4.metric(
    "Avg Risk",
    round(average_risk, 1)
)


st.divider()


# ---------------------------------------------------
# Charts
# ---------------------------------------------------

chart1, chart2 = st.columns(2)


# ---------------------------------------------------
# Risk Distribution
# ---------------------------------------------------

with chart1:

    st.subheader("User Risk Distribution")

    risk_df = pd.DataFrame(
        [dict(row) for row in risk_rows]
    )

    if not risk_df.empty:

        fig = px.bar(
            risk_df,
            x="username",
            y="risk_score",
            color="risk_score",
            title="Current Risk Score by User",
            labels={
                "username": "Employee",
                "risk_score": "Risk Score"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No risk data available yet.")


# ---------------------------------------------------
# Event Distribution
# ---------------------------------------------------

with chart2:

    st.subheader("Event Type Distribution")

    event_stats = db.get_event_statistics()

    event_df = pd.DataFrame(
        [dict(row) for row in event_stats]
    )

    if not event_df.empty:

        fig = px.pie(
            event_df,
            names="event_type",
            values="total",
            title="Security Events"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No event data available yet.")


st.divider()


# ---------------------------------------------------
# Top Risk Users
# ---------------------------------------------------

st.subheader("Top Risk Users")

risk_table = []

for row in risk_rows:

    score = row["risk_score"]

    if score >= 80:

        level = "🔴 Critical"

    elif score >= 50:

        level = "🟠 High"

    elif score >= 20:

        level = "🟡 Medium"

    else:

        level = "🟢 Low"

    risk_table.append({

        "User": row["username"],
        "Risk Score": score,
        "Threat Level": level

    })


if risk_table:

    st.dataframe(
        risk_table,
        hide_index=True,
        use_container_width=True
    )

else:

    st.info("No risk scores available yet.")


st.divider()


# ---------------------------------------------------
# Latest Alerts
# ---------------------------------------------------

st.subheader("Latest Alerts")

alerts = db.get_alerts()

alert_table = []


for alert in alerts:

    # ---------------------------------------------
    # Use actual stored reason/event information
    # ---------------------------------------------

    reason = alert["reason"]

    technique = {
        "id": "N/A",
        "name": "Unclassified",
        "tactic": "Unknown"
    }

    # Try mapping the reason directly
    reason_lower = reason.lower()

    if "usb" in reason_lower:

        technique = mitre.map_event("usb")

    elif "failed login" in reason_lower:

        technique = mitre.map_event(
            "failed_login"
        )

    elif "login" in reason_lower:

        technique = mitre.map_event(
            "login"
        )

    elif "download" in reason_lower:

        technique = mitre.map_event(
            "mass_download"
        )

    elif "file" in reason_lower:

        technique = mitre.map_event(
            "file_access"
        )


    alert_table.append({

        "User": alert["username"],
        "Risk Score": alert["risk_score"],
        "Level": alert["alert_level"],
        "MITRE ID": technique["id"],
        "Technique": technique["name"],
        "Tactic": technique["tactic"],
        "Reason": reason,
        "Time": alert["timestamp"]

    })


alert_df = pd.DataFrame(alert_table)


if not alert_df.empty:

    st.dataframe(
        alert_df.head(20),
        hide_index=True,
        use_container_width=True
    )

else:

    st.info(
        "No alerts generated yet."
    )


st.divider()


# ---------------------------------------------------
# Employee Activity Logs
# ---------------------------------------------------

st.subheader("Recent Employee Activity")

events = db.get_events()

event_table = []


for event in events:

    severity = event["severity"]

    if severity.lower() == "critical":

        severity_display = "🔴 Critical"

    elif severity.lower() == "high":

        severity_display = "🟠 High"

    elif severity.lower() == "medium":

        severity_display = "🟡 Medium"

    else:

        severity_display = "🟢 Low"


    # ---------------------------------------------
    # MITRE Mapping
    # ---------------------------------------------

    technique = mitre.map_event(
        event["event_type"]
    )


    event_table.append({

        "User": event["username"],
        "Event": event["event_type"],
        "MITRE ID": technique["id"],
        "Technique": technique["name"],
        "Tactic": technique["tactic"],
        "Description": event["description"],
        "Severity": severity_display,
        "Time": event["timestamp"]

    })


event_df = pd.DataFrame(event_table)


if not event_df.empty:

    st.dataframe(
        event_df.head(20),
        hide_index=True,
        use_container_width=True
    )

else:

    st.info(
        "No activity recorded yet."
    )


# ---------------------------------------------------
# Close Database
# ---------------------------------------------------

db.close()