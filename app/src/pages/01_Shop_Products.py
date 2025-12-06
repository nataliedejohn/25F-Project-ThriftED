import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests

from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Sidebar links
SideBarLinks()

# Page title
st.header("Products")

# Layout: left = products, right = filters
product_column, filter_column = st.columns([0.70, 0.30])

# -------------------------------
# SAFE SESSION STATE INITIALIZATION
# -------------------------------
defaults = {
    "category": "All",
    "price": (0, 500),
    "tags": [],
    "condition": "Any",
    "verified": False,
}

for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# -------------------------------
# FILTER COLUMN (Right)
# -------------------------------
with filter_column:
    st.subheader("Filters")

    # Category pills
    st.session_state.category = st.pills(
        "Category",
        ["All", "Furniture", "Clothing", "Textbooks", "Other"],
        selection_mode="single",
        default=st.session_state.get("category")
    )

    # Price Range
    st.session_state.price = st.slider(
        "Price Range",
        0, 500,
        value=st.session_state.price
    )

    # Tags (placeholder list until API is connected)
    st.session_state.tags = st.multiselect(
        "Tags",
        ["Popular", "Campus", "Brand New", "Handmade"],
        default=st.session_state.tags,
    )

    # Condition
    st.session_state.condition = st.selectbox(
        "Condition",
        ["Any", "New", "Used", "Refurbished/Open Box", "Broken"],
        index=["Any", "New", "Used", "Refurbished/Open Box", "Broken"].index(st.session_state.condition)
    )

    # Verified sellers only
    st.session_state.verified = st.checkbox(
        "Verified Sellers Only",
        value=st.session_state.verified
    )


# -------------------------------
# PRODUCT COLUMN (Left)
# -------------------------------
with product_column:

    st.subheader(f"Showing: {st.session_state.category} Products")

    # Prepare API params
    params = {
        "category": None if st.session_state.category == "All" else st.session_state.category,
        "min_price": st.session_state.price[0],
        "max_price": st.session_state.price[1],
        "tags": ",".join(st.session_state.tags),
        "condition": None if st.session_state.condition == "Any" else st.session_state.condition,
        "verified": st.session_state.verified,
    }

    # API endpoint (from REST API matrix: GET /product-buyer)
    API_URL = "http://web-api:4000/buyer-routes/product-buyer"

    # Fetch products
    try:
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            products = response.json()

            st.write(f"Found **{len(products)}** products")

            # Display each product
            for product in products:
                with st.container(border=True):
                    st.markdown(f"### {product['Name']}")
                    st.write(f"**Price:** ₱{product.get('Price', 'N/A')}")
                    st.write(f"**Category:** {product.get('Category', 'N/A')}")
                    st.write(f"**Condition:** {product.get('Condition', 'N/A')}")
                    st.write(f"**Seller Verified:** {'Yes' if product['Verified'] == 1 else 'No'}")

                    # Button to view a specific product
                    if st.button("View Details", key=f"btn-{product.get('ProductID')}"):
                        st.session_state.selected_product = product.get("ProductID")
                        st.switch_page("pages/04_View_Single_Product.py")

        else:
            st.error(f"Error fetching products ({response.status_code})")
            st.text(response.text)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
