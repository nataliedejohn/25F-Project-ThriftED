import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Data Analyst Dashboard')

st.markdown("Use the tools below to analyze activity across the ThriftED platform.")

col1, col2 = st.columns(2)

# Row 1
with col1:
    if st.button("🔥 Engagement & Popularity Analytics", 
                 type="primary", use_container_width=True):
        st.switch_page("pages/31_Product_Analytics.py")

with col2:
    if st.button("💲 Pricing & Listing Quality Analysis", 
                 type="primary", use_container_width=True):
        st.switch_page("pages/32_Pricing_Analytics.py")

# Row 2
with col1:
    if st.button("🛡️ Safety & Risk Ratings Analysis", 
                 type="primary", use_container_width=True):
        st.switch_page("pages/33_Order_History_Analytics.py")

with col2:
    if st.button("💬 User Satisfaction & Feedback", 
                 type="primary", use_container_width=True):
        st.switch_page("pages/34_Seller_Ratings.py")