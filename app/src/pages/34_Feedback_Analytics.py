# pages/25_Feedback_Analytics.py
import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
SideBarLinks()

st.title("💬 User Satisfaction & Feedback")
st.write("App ratings, recent comments, and basic sentiment overview (if available).")

BASE = "http://web-api:4000"

# Refresh
if st.button("🔁 Refresh"):
    st.experimental_rerun()

try:
    r = requests.get(f"{BASE}/analytics/app-feedback", timeout=8)
    if r.status_code == 200:
        payload = r.json()
        # Expecting list of feedback items: {rating, comment, user_id, created_at}
        feedback = payload if isinstance(payload, list) else payload.get("feedback", [])
        if not feedback:
            st.info("No feedback found.")
        else:
            df = pd.json_normalize(feedback)
            st.write("### Recent Feedback")
            st.dataframe(df.head(200))

            if "rating" in df.columns:
                st.subheader("Rating Distribution")
                counts = df["rating"].value_counts().sort_index()
                st.bar_chart(counts)

            if "comment" in df.columns:
                st.subheader("Sample Comments")
                for idx, row in df.head(10).iterrows():
                    st.markdown(f"- **User {row.get('user_id','?')}** ({row.get('created_at','')}) — {row.get('comment','')}")
    else:
        st.error(f"Failed to fetch feedback: {r.status_code}")
        st.text(r.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")

st.markdown("---")
st.caption("Notes: for advanced sentiment analysis, backend can return 'sentiment' field per comment, or you can run on the analyst workstation.")
