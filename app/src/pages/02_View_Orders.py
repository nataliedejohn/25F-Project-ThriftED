import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

# Sidebar
SideBarLinks()

# Header
st.header("View Orders")
st.write(f"### Hi, {st.session_state.get('first_name', 'User')}!")

# API endpoint
API_URL = "http://web-api:4000/buyer-routes/buyer-orders"
# buyerid = st.text_area("BuyerID: ")


# Fetch Orders
try:
    # response = requests.get(f"{API_URL}?BuyerID={buyerid}")
    response = requests.get(API_URL)

    if response.status_code == 200:
        orders = response.json()

        st.write(f"Found **{len(orders)}** orders.")
        for order in orders:
            with st.container(border=True):
                st.write(f"**Order ID:** {order['OrderID']}")
                st.write(f"**Order Date:** {order['OrderDate']}")
                st.write(f"**Pickup Street:** {order['PickupStreet']}")
                st.write(f"**Pickup City:** {order['PickupCity']}")
                st.write(f"**Pickup State:** {order['PickupState']}")
                st.write(f"**Pickup Zip:** {order['PickupZip']}")

    else:
        st.error(f"Failed to fetch order data (Status {response.status_code})")
        st.write(response.text)

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")