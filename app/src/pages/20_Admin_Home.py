import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Moderator Home Page')

if st.button('View All Products', 
            type='primary',
            use_container_width=True):
    st.switch_page('pages/23_Product_Admin.py')

if st.button('View All Users',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/22_User_Guidelines.py')

if st.button('View User Guidelines', 
             type='primary', 
             use_container_width=True):
    st.switch_page('pages/22_User_Guidelines.py')