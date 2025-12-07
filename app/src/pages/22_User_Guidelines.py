import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('User Guidelines Page')

st.write('\n\n')
st.write('# Guidelines for Sellers')
st.write("Welcome to the ThriftED User Guidelines page. Here, we outline the rules and best practices to ensure a safe and " \
"enjoyable experience for all members of our community." )

st.write('# Guidelines for Buyers')
st.write('1. **Respectful Communication**: Always communicate respectfully with sellers and other buyers. ' \
'Harassment, discrimination, or abusive language will not be tolerated.')