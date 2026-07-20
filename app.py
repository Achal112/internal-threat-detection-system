import streamlit as st

from database.database import DatabaseManager

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

db = DatabaseManager()
db.create_tables()

st.title("🛡 SentinelAI")

st.success("Database Connected")

col1, col2, col3 = st.columns(3)

col1.metric("Users", 0)
col2.metric("Alerts", 0)
col3.metric("Risk", "LOW")

db.close()