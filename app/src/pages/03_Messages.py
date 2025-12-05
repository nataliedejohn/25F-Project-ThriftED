"""
Unified Messages Page for Buyers and Sellers
Automatically switches UI based on user role
"""

import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

# ----------------------------
# Role + User Info
# ----------------------------
role = st.session_state.get("role")          # "buyer" or "seller"
user_id = st.session_state.get("user_id")
first_name = st.session_state.get("first_name")

st.header("📨 Messages")
st.write(f"### Hi, {first_name}!")

# ----------------------------
# API Endpoints
# ----------------------------
BASE_URL = "http://web-api:4000"
MESSAGES_URL = f"{BASE_URL}/messages"


# ----------------------------
# Retrieve User Threads
# ----------------------------
def load_message_threads():
    try:
        response = requests.get(MESSAGES_URL, params={"user_id": user_id, "role": role})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch messages. Status: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []


threads = load_message_threads()

# =========================================
# 🧵 VIEW MESSAGE THREAD LIST
# =========================================

st.subheader("Your Conversations")

if len(threads) == 0:
    st.info("You have no messages yet.")
else:
    for t in threads:
        other_party = t["buyer_name"] if role == "seller" else t["seller_name"]
        preview = t["last_message"][:40] + "..."
        chat_id = t["chat_id"]

        if st.button(f"💬 Chat with {other_party}\n*{preview}*", key=f"thread_{chat_id}", use_container_width=True):
            st.session_state["open_chat_id"] = chat_id
            st.rerun()


# ==================================================
# 🗨️ OPEN A CONVERSATION (IF SELECTED)
# ==================================================
if "open_chat_id" in st.session_state:

    chat_id = st.session_state["open_chat_id"]

    # Retrieve messages for selected conversation
    def load_single_thread(chat_id):
        try:
            url = f"{MESSAGES_URL}/{chat_id}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Unable to load conversation.")
                return []
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return []

    messages = load_single_thread(chat_id)

    st.divider()
    st.subheader("📩 Conversation")

    # Display messages
    for msg in messages:
        is_user = msg["sender_id"] == user_id

        st.chat_message("user" if is_user else "assistant").write(msg["body"])

    st.write("")

    # Send new message
    new_message = st.text_area("Write a message...", key="message_input")

    if st.button("Send Message ➤", use_container_width=True):
        if new_message.strip() == "":
            st.warning("Message cannot be empty.")
        else:
            try:
                url = f"{MESSAGES_URL}/{chat_id}"
                payload = {"sender_id": user_id, "body": new_message}

                response = requests.post(url, json=payload)

                if response.status_code == 201:
                    st.success("Message sent!")
                    st.session_state["message_input"] = ""  # clear input
                    st.rerun()
                else:
                    st.error("Failed to send message.")
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ==================================================
# 🆕 START NEW MESSAGE (ROLE-AWARE)
# ==================================================
st.divider()

st.subheader("🆕 Start New Conversation")

with st.form("new_message_form"):
    st.write("Select the recipient and write your message:")

    if role == "buyer":
        recipient_id = st.text_input("Seller ID *")
    else:
        recipient_id = st.text_input("Buyer ID *")

    message_body = st.text_area("Message Body *")

    submitted = st.form_submit_button("Start Conversation")

    if submitted:
        if not recipient_id or not message_body:
            st.error("All fields are required.")
        else:
            try:
                payload = {
                    "sender_id": user_id,
                    "recipient_id": recipient_id,
                    "role": role,
                    "body": message_body
                }
                response = requests.post(MESSAGES_URL, json=payload)

                if response.status_code == 201:
                    st.success("Conversation started!")
                    st.rerun()
                else:
                    st.error("Failed to start conversation.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
