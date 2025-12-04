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

# You can access the session state to make a more customized/personalized app experience
st.write(f"### product details for single product, clicked on from shop products")
st.write(f"### **Item Name**")
st.write(f"# **Price**")
st.write(f"Category | Posted date")
st.write(f"**Images**")

description_column, seller_column = st.columns([0.7, 0.3])
with description_column:
    st.write(f"Tags")   
    st.write(f"Description")

with seller_column:
    st.write(f"**Seller Informatoin**")
    if st.button("Start Message"):
        st.switch_page("pages/03_Messages.py")
    if st.button("Add to Order"):
        st.write("Added to order... write to API/order page")

# get product details