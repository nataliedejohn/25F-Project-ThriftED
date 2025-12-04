import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Create New Listing')

# Initialize session state for new listing
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_product_name" not in st.session_state:
    st.session_state.success_listing_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "listing_counter" not in st.session_state:
    st.session_state.listing_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(product_name):
    st.markdown(f"### {product_name} has been successfully listed!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to your listings", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_ngo_name = ""
            st.switch_page("pages/11_View_Listings.py")
    
    with col2:
        if st.button("List another product", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_listing_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.listing_counter += 1
    st.session_state.reset_form = False

# TODO : API endpoint for adding products to listings

# follow Add_NGO form
# Create a form to list a product
with st.form(f"create_listing_{st.session_state.listing_counter}"):
    st.subheader("Product Information")

    # Required product details
    # photo = st.file_uploader("Upload Product Photos *", accept_multiple_files=True)
    product_name = st.text_input("Product Name *")
    category = st.selectbox("Category *", options=['placeholder', 'need database', 'get category names'])
    description = st.text_area("Product Description *")
    price = st.number_input("Price ($) *", min_value=0.0, format="%.2f")
    condition = st.selectbox("Condition *", options=['placeholder', 'need database', 'get condition options'])
    tags = st.text_input("Tags, what is best input? *")

    submitted = st.form_submit_button("Submit Listing")

    if submitted:
        # Validate required fields
        if not all([product_name, category, description, price, condition, tags]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            product_data = {
                "product_name": product_name,
                "category": category,
                "description": description,
                "price": price,
                "condition": condition,
                "tags": tags,
            }

            st.show_success_modal = True
            st.success_listing_name = product_name
            show_success_dialog(product_name)

            # TODO: try / except to send data to the API endpoint

# Show success modal if NGO was added successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_listing_name)