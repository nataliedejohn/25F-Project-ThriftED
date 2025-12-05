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

# Correct API endpoint (from REST API matrix)
API_URL = "http://web-api:4000/orders"

# Fetch Orders
try:
    response = requests.get(API_URL)

    if response.status_code == 200:
        orders = response.json()

        if isinstance(orders, dict):
            # In case backend wraps response ({"data": [...]})
            orders = orders.get("data", [])

        st.write(f"Found **{len(orders)}** orders.")

        for order in orders:
            order_id = order.get("OrderID", "Unknown Order")
            buyer_id = order.get("BuyerID", "N/A")

            with st.expander(f"Order {order_id} — Buyer {buyer_id}"):
                st.write(f"**Order ID:** {order_id}")
                st.write(f"**Buyer ID:** {buyer_id}")
                st.write(f"**Product ID:** {order.get('ProductID', 'N/A')}")
                st.write(f"**Order Date:** {order.get('OrderDate', 'N/A')}")
                st.write(f"**Pickup Spot:** {order.get('PickupSpot', 'N/A')}")
                st.write(f"**Status:** {order.get('Status', 'N/A')}")

    else:
        st.error(f"Failed to fetch order data (Status {response.status_code})")
        st.write(response.text)

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Make sure the API server is running at http://web-api:4000")
