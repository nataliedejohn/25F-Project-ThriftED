import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Sidebar for Seller Role
SideBarLinks()

# -------------------------------
# Header
# -------------------------------
st.title(f"Welcome Seller, {st.session_state['first_name']}!")
st.write("")
st.write("### What would you like to do today?")


# -------------------------------
# Seller Actions
# -------------------------------
st.write("")

# View Listings
if st.button("📦 View My Listings", type="primary", use_container_width=True):
    # According to API Matrix → GET /listings (seller-specific handled in backend)
    st.switch_page("pages/11_View_Listings.py")

# Create Listing
if st.button("➕ Add New Listing", type="primary", use_container_width=True):
    # According to API Matrix → POST /listings (done in the Add Listing page)
    st.switch_page("pages/12_Add_Listing.py")

# View Messages
if st.button("💬 View Messages", type="primary", use_container_width=True):
    # According to API Matrix → GET /messages and GET /messages/{chat-id}
    st.switch_page("pages/03_Messages.py")
