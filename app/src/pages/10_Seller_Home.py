import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Seller, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Listings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_View_Listings.py')

if st.button('New Listing', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Add_Listing.py')

if st.button('View Messages', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_Messages.py')
  