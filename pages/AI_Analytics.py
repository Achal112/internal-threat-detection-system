import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import DatabaseManager


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Analytics | SentinelAI",
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

st.title("AI Analytics")

st.write(
    "Machine-learning based behavioral anomaly detection "
    "for monitored employees."
)

st.divider()


# ---------------------------------------------------
# Load Historical AI Analysis
# ---------------------------------------------------

ai_rows = db.get_ai_analysis()

analysis_results = [
    dict(row)
    for row in ai_rows
]


# ---------------------------------------------------
# AI Detection Overview
# ---------------------------------------------------

st.subheader("AI Detection Overview")


total_analyzed = len(analysis_results)


anomalies = sum(
    1
    for result in analysis_results
    if str(result["prediction"]).lower() == "anomaly"
)


normal = sum(
    1
    for result in analysis_results
    if str(result["prediction"]).lower() == "normal"
)


if total_analyzed > 0:

    anomaly_rate = (
        anomalies / total_analyzed
    ) * 100

else:

    anomaly_rate = 0


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Activities Analyzed",
    total_analyzed
)


col2.metric(
    "Normal",
    normal
)


col3.metric(
    "Anomalies",
    anomalies
)


col4.metric(
    "Anomaly Rate",
    f"{anomaly_rate:.1f}%"
)


st.divider()


# ---------------------------------------------------
# Employee-wise AI Analysis
# ---------------------------------------------------

st.subheader("Employee-wise AI Analysis")


if analysis_results:

    employee_table = []

    usernames = sorted(
        set(
            result["username"]
            for result in analysis_results
        )
    )


    for username in usernames:

        user_results = [
            result
            for result in analysis_results
            if result["username"] == username
        ]


        user_anomalies = sum(
            1
            for result in user_results
            if str(result["prediction"]).lower()
            == "anomaly"
        )


        user_total = len(user_results)


        user_anomaly_rate = (
            user_anomalies / user_total
        ) * 100


        employee_table.append({

            "Employee": username,

            "Activities Analyzed":
                user_total,

            "Normal":
                user_total - user_anomalies,

            "Anomalies":
                user_anomalies,

            "Anomaly Rate":
                f"{user_anomaly_rate:.1f}%"

        })


    employee_df = pd.DataFrame(
        employee_table
    )


    st.dataframe(
        employee_df,
        hide_index=True,
        use_container_width=True
    )


else:

    st.info(
        "No AI analysis available. "
        "Generate a scenario from Home first."
    )


st.divider()


# ---------------------------------------------------
# AI Prediction History
# ---------------------------------------------------

st.subheader("AI Prediction History")


if analysis_results:

    history_table = []


    for result in analysis_results:

        prediction = str(
            result["prediction"]
        )


        if prediction.lower() == "anomaly":

            display_prediction = "Anomaly"

        else:

            display_prediction = "Normal"


        history_table.append({

            "Employee":
                result["username"],

            "Prediction":
                display_prediction,

            "Login Hour":
                result["login_hour"],

            "Downloads":
                result["downloads"],

            "Files Opened":
                result["files_opened"],

            "USB Used":
                result["usb_used"],

            "Failed Logins":
                result["failed_logins"],

            "Time":
                result["timestamp"]

        })


    history_df = pd.DataFrame(
        history_table
    )


    st.dataframe(
        history_df.head(50),
        hide_index=True,
        use_container_width=True
    )


else:

    st.info(
        "No prediction history available."
    )


st.divider()

# ---------------------------------------------------
# Employee Anomaly Trend
# ---------------------------------------------------

st.subheader("Employee Anomaly Trend")

if analysis_results:

    trend_data = []

    for result in analysis_results:

        trend_data.append({
            "Employee": result["username"],
            "Time": result["timestamp"],
            "Prediction": result["prediction"]
        })

    trend_df = pd.DataFrame(trend_data)

    # Convert prediction into numeric value
    # Normal = 0
    # Anomaly = 1

    trend_df["Anomaly"] = trend_df["Prediction"].apply(
        lambda x: 1 if str(x).lower() == "anomaly" else 0
    )

    # Employee-wise anomaly count
    employee_trend = (
        trend_df
        .groupby("Employee")
        .agg(
            Activities=("Prediction", "count"),
            Anomalies=("Anomaly", "sum")
        )
        .reset_index()
    )

    employee_trend["Normal"] = (
        employee_trend["Activities"]
        - employee_trend["Anomalies"]
    )

    employee_trend["Anomaly Rate"] = (
        employee_trend["Anomalies"]
        / employee_trend["Activities"]
        * 100
    )

    employee_trend["Anomaly Rate"] = (
        employee_trend["Anomaly Rate"]
        .round(1)
    )

    st.dataframe(
        employee_trend,
        hide_index=True,
        use_container_width=True
    )

    # -----------------------------------------------
    # Anomaly count chart
    # -----------------------------------------------

    fig = px.bar(
        employee_trend,
        x="Employee",
        y="Anomalies",
        title="Anomalies Detected by Employee",
        labels={
            "Anomalies": "Anomaly Count"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No historical AI analysis available."
    )

st.divider()


# ---------------------------------------------------
# Anomaly Distribution
# ---------------------------------------------------

st.subheader("AI Prediction Distribution")


if analysis_results:

    prediction_counts = pd.DataFrame({

        "Prediction": [
            "Normal",
            "Anomaly"
        ],

        "Count": [
            normal,
            anomalies
        ]

    })


    fig = px.pie(
        prediction_counts,
        names="Prediction",
        values="Count",
        title="Normal vs Anomalous Activities"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.info(
        "No AI predictions available."
    )


st.divider()


# ---------------------------------------------------
# Behavioral Feature Analysis
# ---------------------------------------------------

st.subheader("Behavioral Feature Analysis")


if analysis_results:

    feature_averages = {

        "Feature": [
            "Login Hour",
            "Downloads",
            "Files Opened",
            "USB Usage",
            "Failed Logins"
        ],

        "Average": [

            sum(
                result["login_hour"]
                for result in analysis_results
            ) / total_analyzed,

            sum(
                result["downloads"]
                for result in analysis_results
            ) / total_analyzed,

            sum(
                result["files_opened"]
                for result in analysis_results
            ) / total_analyzed,

            sum(
                result["usb_used"]
                for result in analysis_results
            ) / total_analyzed,

            sum(
                result["failed_logins"]
                for result in analysis_results
            ) / total_analyzed

        ]

    }


    feature_df = pd.DataFrame(
        feature_averages
    )


    fig = px.bar(
        feature_df,
        x="Feature",
        y="Average",
        title="Average Behavioral Features"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.info(
        "No behavioral data available."
    )


st.divider()


# ---------------------------------------------------
# AI Model Information
# ---------------------------------------------------

st.subheader("AI Model Information")


model_col1, model_col2 = st.columns(2)


with model_col1:

    st.write("**Detection Approach**")

    st.write(
        "Machine-learning based behavioral "
        "classification."
    )


    st.write("**Behavioral Features**")

    st.write(
        "Login hour, downloads, files opened, "
        "USB usage and failed login attempts."
    )


with model_col2:

    st.write("**Analysis Type**")

    st.write(
        "Historical behavioral analysis."
    )


    st.write("**Purpose**")

    st.write(
        "Identify activities that differ from "
        "learned normal behavioral patterns."
    )


# ---------------------------------------------------
# Close Database
# ---------------------------------------------------

db.close()