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

    with update_column:
        # intitialize session state for submitting product form
        if "show_success_modal" not in st.session_state:
            st.session_state.show_success_modal = False
        if "reset_form" not in st.session_state:
            st.session_state.reset_form = False

        # define success dialog function
        @st.dialog("Product information updated.")
        def show_success_dialog():
            st.markdown(f"## Product information has been successfully updated!")
            
            # two buttons to return to listing info or home
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Return to Product", use_container_width=True):
                    st.session_state.show_success_modal = False
                    st.session_state.reset_form = True
                    st.rerun()
            with col2:
                if st.button("Return to All Products", use_container_width=True):
                    st.session_state.show_success_modal = False
                    st.switch_page("pages/23_Product_Admin.py")
        
        # Handle form reset
        if st.session_state.reset_form:
            st.session_state.reset_form = False
        
        # API endpoint for updating product info
        UPDATE_URL = f"http://web-api:4000/admin-routes/product-admin/{pid}"

        # Form to change product information
        with st.form("[update_product_form]"):
            st.subheader("Update Product Information")

            status = st.selectbox("Change Verification: ", ["Verified", "Not Verified"], index=None)

            submitted = st.form_submit_button("Submit Changes")

            if submitted:

                if not status:
                   st.error("Please select a status to update.")
                else:
                    stat = False
                    if status == "Verified":
                        stat = True
                    data = {"Status" : stat}
                    try: 
                        requests.put(UPDATE_URL, json=data)
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")
                        st.info("Please ensure the API server is running")

                st.session_state.show_success_modal = True
                show_success_dialog()

        # Button to delete product
        if st.button("Delete Product Listing", key=f"btn-{product.get('ProductID')}"):
            st.session_state.selected_pid = product.get("ProductID")
            st.switch_page("pages/24_Delete_Product.py")

# Button to return to Product Admin
if st.button("Return to All Products"):
    # Clear the selected NGO ID from session state
    if "selected_pid" in st.session_state:
        del st.session_state["selected_pid"]
    st.switch_page("pages/23_Product_Admin.py")
