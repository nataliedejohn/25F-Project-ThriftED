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

# API endpoint
API_URL = f"http://web-api:4000/moderator-routes/user-guidelines"
try:
    # Fetch user details
    response = requests.get(API_URL)
    if response.status_code == 200:
        
        data = response.json()
        st.dataframe(data)

    else:
        st.error(f"Error fetching buyer guidelines data: {response.status_code}")
        st.text(response.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the Buyer API: {str(e)}")
    st.info("Please ensure the API server is running")

st.write('1. **Respectful Communication**: Always communicate respectfully with sellers and other buyers. ' \
'Harassment, discrimination, or abusive language will not be tolerated.')