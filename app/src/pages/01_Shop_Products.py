import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Shopping Products')
product_column, filter_column = st.columns([0.7, 0.3])


# Initialize session state for filters
st.session_state.category = ""
st.session_state.price = None
st.session_state.tags = []
st.session_state.condition = ""
st.session_state.verified = None

# Implement filtering widgets - category drop down to the selected, then says (3 selected underneath); price, tags, etc. follow suit
# Select a category filter
with product_column:
    st.session_state.category = st.pills("Category", ["Options", "get/categories", "from api"], )
    st.write(f"### You selected: {st.session_state.category}") # turn into get/products filtered by that category

# Select price/tag/condition filters
with filter_column:
    # price slider - replace value with tuple from api min/max of price range
    st.session_state.price = st.slider("Price Range", 0, 500, value=(0, 500))
    st.write(f"Price range set to: {st.session_state.price}")
    # tags multi select
    st.session_state.tags = st.multiselect("Tags", ["tag options", "get/tags", "from api"])
    st.write(f"Tags selected: {st.session_state.price} and tags")
    # condition selection box - default to all
    st.session_state.condition = st.selectbox("Condition", ["Options", "get/products{conditions}", "from api"])
    st.write(f"Condition set to: {st.session_state.condition}")
    # verified checkbox
    st.session_state.verified = st.checkbox("Verified Sellers Only")
    st.write(f"Verified sellers only: {st.session_state.verified}")

    # other attributes of products


    # connect to get products blueprints



# if product clicked, go to view_single_product page
if st.button("Product clicked"):
    st.switch_page('pages/04_View_Single_Product.py')