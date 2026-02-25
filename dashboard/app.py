import streamlit as st
import random

st.title("🛒 Retail AI Monitoring Dashboard")

risk_level = random.choice(["LOW", "MEDIUM", "HIGH"])
score = round(random.uniform(0, 1), 2)

st.metric("Current Risk Level", risk_level)
st.metric("Behavior Score", score)

st.write("Live suspicious activity alerts will appear here.")
