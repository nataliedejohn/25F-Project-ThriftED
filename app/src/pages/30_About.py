import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is a demo app for students at Universities across the world to buy and sell used items. 

    The goal of this demo app is to provide an easy-to-use platform for students to find affordable items while
    promoting sustainability by encouraging the reuse of goods. Oftentimes students need items for a short period of time
    and buying new itms can be costly and wasteful. This app aims to solve that problem by connecting students
    who want to sell their used items with other students who are looking for affordable options.

    Stay tuned for more information and features to come!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
