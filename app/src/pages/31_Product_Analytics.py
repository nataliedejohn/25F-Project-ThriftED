# pages/22_Engagement_Analytics.py
import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("🔥 Engagement & Popularity Analytics")
st.write("Shows top products, categories, tags, searches and basic revenue metrics.")

API_URL = "http://web-api:4000/analyst-routes"

# Refresh button
if st.button("🔁 Refresh data"):
    st.rerun()

# --- Popular products category ---
st.header("Top Products by Category")
try:
    response = requests.get(f"{API_URL}/product-category")

    if response.status_code == 200:

        df=pd.DataFrame(response.json())
        st.dataframe(df)

    else:
        st.error(f"Failed to fetch popular products: {response.status_code}")
        st.text(response.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")

# --- Popular products by tags
st.header("Top Products by Tags")
try:
    response = requests.get(f"{API_URL}/product-tags")

    if response.status_code == 200:

        df=pd.DataFrame(response.json())
        st.dataframe(df)

    else:
        st.error(f"Failed to fetch popular products: {response.status_code}")
        st.text(response.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")