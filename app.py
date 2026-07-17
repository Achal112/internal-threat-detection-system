import streamlit as st

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SentinelAI")
st.subheader("AI-Based Insider Threat Detection")

st.success("System Status: Running")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Users", 0)

with col2:
    st.metric("Threat Alerts", 0)

with col3:
    st.metric("Risk Level", "LOW")