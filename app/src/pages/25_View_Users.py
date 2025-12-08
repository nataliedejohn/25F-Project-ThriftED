import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import requests

from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header(f"{st.session_state['first_name']} Details")

view_column, update_column = st.columns([0.7, 0.3])

with view_column:
# display on product page for individual selected product:
    pid = st.session_state.get("selected_product")

    if pid is None:
        st.error("No Product selected")
    else:
        # API endpoint
        API_URL = f"http://web-api:4000/buyer-routes/product-buyer/{pid}"

        try:
            # Fetch product details
            response = requests.get(API_URL)

            if response.status_code == 200:
                product = response.json()

                # Display basic information
                st.header(product["Name"])

                st.subheader("Basic Information")
                st.write(f"**Description:** {product['Description']}")
                st.write(f"**Category:** {product['Category']}")
                st.write(f"**Condition:** {product['Condition']}")
                st.write(f"**Status:** {product['Status']}")
                st.write(f"**Price:** ${product['Price']}")
                st.write(f"**Posted Date:** {product['PostedDate']}")
                st.write(f"**Views:** {product['Views']}")
                st.write(f"**Saves:** {product['Saves']}")
                st.write(f"**Seller Verified:** {'Yes' if product['Verified'] == 1 else 'No'}")
                photo_url = product.get("PhotoURL", "")
                if photo_url:
                    try:
                        st.image(photo_url, caption="Product Photo", use_container_width=True)
                    except Exception as e:
                        st.info("📷 Product photo not available")

            elif response.status_code == 404:
                st.error("Product not found")
            else:
                st.error(
                    f"Error fetching NGO data: {response.json().get('error', 'Unknown error')}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the Buyer API: {str(e)}")
            st.info("Please ensure the API server is running")