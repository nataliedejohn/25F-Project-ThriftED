""" Message page for both buyers and sellers to communicate with each other"""

import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Messages Home Page')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}")

# see all message conversations? how to implement this - 
# start new message button? pop up an add message box - to senderID and message body - follow Add_NGO page
message_column, new_message_column = st.columns([0.6, 0.4])

# is there a way to differentiate between sent and recieved? If not just show all messages
with message_column:
    st.write("### Sent")
    # get sent messages from api
    st.write("### Received")
    # get received messages from api

# start a new message form - add to api 
with new_message_column:
    
    # Initialize session state for new listing
    if "show_success_modal" not in st.session_state:
        st.session_state.show_success_modal = False
    if "success_message_" not in st.session_state:
        st.session_state.success_convoID = ""
    if "reset_form" not in st.session_state:
        st.session_state.reset_form = False
    if "listing_counter" not in st.session_state:
        st.session_state.message_counter = 0

    # define success dialog function
    @st.dialog("Message Sent")
    def show_success_dialog(convoID):
        st.markdown(f"### Message has been successfully sent!")
        
        if st.button("Return to Messages Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_convoID = ""
            st.session_state.reset_form = True
            st.rerun()

    # Handle form reset
    if st.session_state.reset_form:
        st.session_state.message_counter += 1
        st.session_state.reset_form = False

    # TODO : API endpoint for adding messages to database

    with st.form(f"create_message_{st.session_state.message_counter}"):
        st.subheader("Start New Message")

        # Required message details
        recipient = st.radio("Select Recipient *", options=["Buyer", "Seller"])
        recipient_id = st.text_input("Recipient ID *")
        body = st.text_area("Message Body *")

        submitted = st.form_submit_button("Send Message")

        if submitted:
            # Validate required fields
            if not all ([recipient, recipient_id, body]):
                st.error("Please fill in all required fields marked with *")
            else:
                message_data = {
                    "recipient" : recipient,
                    "recipient_id" : recipient_id,
                    "body" : body
                }

                st.session_state.show_success_modal = True
                st.session_state.success_convoID = "convoID"
                show_success_dialog(st.session_state.success_convoID)

    if st.session_state.show_success_modal:
        show_success_dialog(st.session_state.success_convoID)
