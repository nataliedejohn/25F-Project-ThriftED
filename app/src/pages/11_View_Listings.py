import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header(f'{st.session_state["first_name"]}\'s Listings')


# add button that goes to new listing page
if st.button('Add New Listing', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Add_Listing.py')

# Having widgets showing views, saves, earnings, and rating
# connect to get products blueprints
# if click on product, go to update product information page