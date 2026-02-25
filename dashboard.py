import streamlit as st
import pandas as pd
import os
from PIL import Image
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="XYRA LABS",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0f0f0f;
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center; font-size:60px;'>XYRA LABS</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#9ca3af;'>Retail Intelligence Dashboard</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Enter Dashboard", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()

    st.stop()

st.title("XYRA LABS")
st.caption("AI Surveillance & Detection System")

page = st.radio(
    "",
    ["Overview", "Live Cameras", "Events"],
    horizontal=True
)

st.divider()

st_autorefresh(interval=3000, key="refresh")

RESULTS_PATH = "output_stream/results.csv"
IMAGE_FOLDER = "stream_input"

if page == "Overview":

    if os.path.exists(RESULTS_PATH):
        df = pd.read_csv(RESULTS_PATH)

        if not df.empty:
            latest = df.iloc[-1]
            label = latest["label"]
            confidence = float(latest["confidence"])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Current Status",
                "Threat" if label == "🚨 SHOPLIFTING" else "Normal"
            )

            col2.metric(
                "Confidence",
                f"{confidence}%"
            )

            col3.metric(
                "Total Events",
                len(df)
            )
        else:
            st.info("No detections yet.")
    else:
        st.info("Waiting for detection data...")

elif page == "Live Cameras":

    image_files = sorted(os.listdir(IMAGE_FOLDER)) if os.path.exists(IMAGE_FOLDER) else []

    if image_files:
        latest_image = image_files[-1]
        image_path = os.path.join(IMAGE_FOLDER, latest_image)
        img = Image.open(image_path)

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        for col in [col1, col2, col3, col4]:
            with col:
                st.image(img, use_container_width=True)
    else:
        st.info("No camera feed available.")

elif page == "Events":

    if os.path.exists(RESULTS_PATH):
        df = pd.read_csv(RESULTS_PATH)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No event data available.")