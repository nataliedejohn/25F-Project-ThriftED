import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Products Admin")

# API endpoint
API_URL = "http://web-api:4000/admin-routes/products"

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        products = response.json()
        
        st.write(f"Found {len(products)} Products")
        for product in products:
            with st.expander(f"{product['Name']}"):
                #st.write(f"**University:** {product['University']}")
                st.write(f"**Description:** {product['Description']}")
                st.write(f"**Price:** ${product['Price']}")

                #Edit listing button
                if st.button("✏️ Edit Product", key=f"edit_{product['ProductID']}"):
                    st.session_state["edit_listing_id"] = product["ProductID"]
                    st.session_state.selected_product = product.get("ProductID")
                    st.switch_page("pages/21_View_Product.py")

    else:
        st.write("Status:", response.status_code)
        st.write("Response:", response.text)
        st.error("Failed to fetch Product data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
