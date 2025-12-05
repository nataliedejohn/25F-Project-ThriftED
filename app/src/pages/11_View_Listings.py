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
st.header(f'{st.session_state["first_name"]}\'s Listings')

# API endpoint
API_URL = "http://web-api:4000/seller-routes/product-seller"

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        listings = response.json()
        
        st.write(f"Found {len(listings)} Listings")
        for product in listings:
            with st.expander(f"{product['Name']}"):
                st.write(f"**Status:** {product['Status']}")
                st.write(f"**Description:** {product['Description']}")
                st.write(f"**Price:** ${product['Price']}")
                st.write(f"**Posted Date:** {product['PostedDate']}")

    else:
        st.write("Status:", response.status_code)
        st.write("Response:", response.text)
        st.error("Failed to fetch Product data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")


# add button that goes to new listing page
if st.button('Add New Listing', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Add_Listing.py')

# Having widgets showing views, saves, earnings, and rating
# connect to get products blueprints
# if click on product, go to update product information page