# pages/25_Feedback_Analytics.py
import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("💬 Seller Ratings")
st.write("Seller Ratings and Products Listed")

# API endpoint for getting seller rating data
API_URL = "http://web-api:4000/analyst-routes/ratings"

# Refresh
if st.button("🔁 Refresh"):
    st.rerun()

try:
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        st.dataframe(data)
    else:
        st.error(f"Failed to fetch feedback: {response.status_code}")
        st.text(response.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")

st.markdown("---")
st.caption("Notes: for advanced sentiment analysis, backend can return 'sentiment' field per comment, or you can run on the analyst workstation.")
