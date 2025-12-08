# pages/33_Order_History_Analytics.py
import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import numpy as np

st.set_page_config(layout="wide")
SideBarLinks()

st.title("💲 Buyer History and Order Analytics")
st.write("Comparing buyer search history to orders placed")

# API endpoint 
API_URL = "http://web-api:4000/analyst-routes/analytics/user-search-history"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
         
        st.header("Number of searches and orders placed per buyer")
        st.dataframe(data)
        
    else:
        st.error(f"Failed to fetch price ranges: {response.status_code}")
        st.text(response.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")
