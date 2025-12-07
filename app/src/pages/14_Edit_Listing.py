import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import requests

from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Get product ID from session state
pid = st.session_state.get("selected_product")

if pid is None:
    st.error("No Product selected")
else:
    # API endpoint for product info
    API_URL = f"http://web-api:4000/buyer-routes/product-buyer/{pid}"

    # view product column and update product info column
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
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
            st.error(f"Error connecting to the API: {str(e)}")
            st.info("Please ensure the API server is running")

    with col2:
        
        # intitialize session state for submitting product form
        if "show_success_modal" not in st.session_state:
            st.session_state.show_success_modal = False
        if "reset_form" not in st.session_state:
            st.session_state.reset_form = False

        # define success dialog function
        @st.dialog("Listing information updated.")
        def show_success_dialog():
            st.markdown(f"## Product information has been successfully updated!")
            
            # two buttons to return to listing info or home
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Return to Listing", use_container_width=True):
                    st.session_state.show_success_modal = False
                    st.session_state.reset_form = True
                    st.rerun()
            with col2:
                if st.button("Return Home", use_container_width=True):
                    st.session_state.show_success_modal = False
                    st.switch_page("pages/10_Seller_Home.py")

        # Handle form reset
        if st.session_state.reset_form:
            st.session_state.reset_form = False

        # API endpoint for updating product info


        # Form to change product information
        with st.form("update_listing_form"):
            st.subheader("Update Listing Information")

            status = st.selectbox("Change status: ", ["Sold", "Available", "Pending"], index=None)

            submitted = st.form_submit_button("Submit Changes")

            if submitted:

                if not status:
                   st.error("Please select a status to update.")
                else:
                    data = {"Status" : status}
                    try: 
                        requests.put(API_URL, json=data)
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")
                        st.info("Please ensure the API server is running")



                query = "UPDATE Products SET category=category, status=status, verified=verified WHERE product_id=product_id"
                # cursor execute query to update product info

                st.session_state.show_success_modal = True
                show_success_dialog()

# Add a button to return to the NGO Directory
if st.button("Return to Listings"):
    # Clear the selected NGO ID from session state
    if "selected_pid" in st.session_state:
        del st.session_state["selected_pid"]
    st.switch_page("pages/11_View_Listings.py")

