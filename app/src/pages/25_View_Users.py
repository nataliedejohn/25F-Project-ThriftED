import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests

from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header(f"User Details")

st.write('# Buyer Details')

# API endpoint
BUYER_URL = f"http://web-api:4000/moderator-routes/buyers"
SELLER_URL = f"http://web-api:4000/moderator-routes/sellers"

try:
    # Fetch product details
    response = requests.get(BUYER_URL)

    if response.status_code == 200:
        buyer = response.json()

        st.write(f"Found {len(buyer)} Buyers")

        for b in buyer:
            # Display basic information
             with st.expander(f"{b['FirstName']} {b['LastName']}"):

                st.subheader("Basic Information")
                st.write(f"**Email:** {b['Email']}")
                st.write(f"**Phone Number:** {b['PhoneNum']}")
                st.write(f"**Age** {b['Age']}")
                st.write(f"**Buyer Verified:** {'Yes' if b['Verification'] == 1 else 'No'}")

                if st.button("Delete Buyer", key=f"delete_buyer_{b['BuyerID']}"):
                    delete_response = requests.delete(f"http://web-api:4000/moderator-routes/delete-buyer/{b['BuyerID']}")
                    if delete_response.status_code == 200:
                        st.success(f"Buyer {b['FirstName']} {b['LastName']} deleted successfully.")
                        st.rerun() # refreshes the page to reflect the new change
                    else:
                        st.error(f"Failed to delete Buyer {b['FirstName']} {b['LastName']}.")
                        st.error(f"Error: {delete_response.json().get('error', 'Unknown error')}")

    else:
        st.error(
            f"Error fetching NGO data: {response.json().get('error', 'Unknown error')}"
        )

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the Buyer API: {str(e)}")
    st.info("Please ensure the API server is running")

st.write('# Seller Details')

try:
    # Fetch product details
    response = requests.get(SELLER_URL)

    if response.status_code == 200:
        seller = response.json()

        # Display basic information

        st.write(f"Found {len(seller)} Sellers")

        for s in seller:

             with st.expander(f"{s['FirstName']} {s['LastName']}"):

                st.subheader("Basic Information")
                st.write(f"**Email:** {s['Email']}")
                st.write(f"**Phone Number:** {s['PhoneNum']}")
                st.write(f"**Age** {s['Age']}")
                st.write(f"**Seller Verified:** {'Yes' if s['Verification'] == 1 else 'No'}")

    else:
        st.error(
            f"Error fetching NGO data: {response.json().get('error', 'Unknown error')}"
        )
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the Seller API: {str(e)}")
    st.info("Please ensure the API server is running")