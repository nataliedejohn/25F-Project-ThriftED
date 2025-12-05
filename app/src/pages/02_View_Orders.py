import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('View Orders')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# connect to orders blueprints

# API endpoint
API_URL = "http://web-api:4000/buyer-routes/orders"

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        orders = response.json()
        
        st.write(f"Found {len(orders)} Orders")
        for order in orders:
            with st.expander(f"{order['BuyerID']}"):
                st.write(f"**BuyerID:** {order['BuyerID']}")
                st.write(f"**OrderDate:** {order['OrderDate']}")

    else:
        st.write("Status:", response.status_code)
        st.write("Response:", response.text)
        st.error("Failed to fetch Product data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")