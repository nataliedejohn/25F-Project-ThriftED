import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo

from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header(f"{st.session_state['first_name']} Details")

view_column, update_column = st.columns([0.7, 0.3])

with view_column:
# display on product page for individual selected product:
    product_id = st.text_input("Product ID")
    st.write(f"### product details for single product, clicked on from shop products")
    st.write(f"### **Item Name**")
    st.write(f"# **Price**")
    st.write(f"Category | Posted date")
    st.write(f"**Images**")

# update product information
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
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Return to Product", use_container_width=True):
                st.session_state.show_success_modal = False
                st.session_state.reset_form = True
                st.rerun()
        with col2:
            if st.button("Return Home", use_container_width=True):
                st.session_state.show_success_modal = False
                st.switch_page("pages/20_Admin_Home.py")

    # Handle form reset
    if st.session_state.reset_form:
        st.session_state.reset_form = False

    # Form to change product information
    with st.form("update_product_form"):
        st.subheader("Update Product Information")

        category = st.text_area("Change category: ")
        status = st.selectbox("Change status: ", ["these options"], index=None)
        verified = st.selectbox("Product verified?", ["True", "False"], index=None)

        submitted = st.form_submit_button("Submit Changes")

        if submitted:

            if not category:
                category = "get products current category?"
            if not status:
                status = "get products current status?"
            if not verified:
                verified = "get product's current verified?"

            query = "UPDATE Products SET category=category, status=status, verified=verified WHERE product_id=product_id"
            # cursor execute query to update product info

            st.session_state.show_success_modal = True
            show_success_dialog()

