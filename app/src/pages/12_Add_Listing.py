import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Sidebar
SideBarLinks()

st.header("Create New Listing 🛍️")

# ---------------------------------------------------
# Session State Setup
# ---------------------------------------------------
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_listing_name" not in st.session_state:
    st.session_state.success_listing_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "listing_counter" not in st.session_state:
    st.session_state.listing_counter = 0

# ---------------------------------------------------
# Success Dialog
# ---------------------------------------------------
@st.dialog("Success 🎉")
def show_success_dialog(product_name):
    st.markdown(f"### **{product_name}** has been successfully listed!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Return to Your Listings", use_container_width=True):
            st.session_state.show_success_modal = False
            st.switch_page("pages/11_View_Listings.py")

    with col2:
        if st.button("➕ List Another Product", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.reset_form = True
            st.rerun()

# Reset Form
if st.session_state.reset_form:
    st.session_state.listing_counter += 1
    st.session_state.reset_form = False

# ---------------------------------------------------
# Dropdown Options (could come from API later)
# ---------------------------------------------------
CATEGORY_OPTIONS = ["Furniture", "Clothing", "Textbooks", "Electronics", "Other"]
CONDITION_OPTIONS = ["New", "Used", "Refurbished", "Open Box", "Broken"]

# ---------------------------------------------------
# Product Form
# ---------------------------------------------------
with st.form(f"create_listing_{st.session_state.listing_counter}"):
    st.subheader("Product Information")

    product_name = st.text_input("Product Name *")
    category = st.selectbox("Category *", CATEGORY_OPTIONS)
    description = st.text_area("Product Description *")
    price = st.number_input("Price ($) *", min_value=0.0, format="%.2f")
    condition = st.selectbox("Condition *", CONDITION_OPTIONS)
    tags_raw = st.text_input("Tags (comma separated) *")

    submitted = st.form_submit_button("Submit Listing")

    if submitted:
        # Validate required fields
        if not all([product_name, category, description, price, condition, tags_raw]):
            st.error("⚠️ Please fill in all required fields.")
        else:
            tags = [tag.strip() for tag in tags_raw.split(",")]

            # Build API payload according to matrix
            product_data = {
                "seller_id": st.session_state.get("user_id"),
                "name": product_name,
                "description": description,
                "price": price,
                "category": category,
                "condition": condition,
                "tags": tags
            }

            try:
                API_URL = "http://web-api:4000/listings"
                response = requests.post(API_URL, json=product_data)

                if response.status_code == 201:
                    st.session_state.show_success_modal = True
                    st.session_state.success_listing_name = product_name
                    show_success_dialog(product_name)
                else:
                    st.error(f"❌ Failed to create listing. Status {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
                st.info("Ensure the API server is running.")

# Show success dialog if returning
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_listing_name)
