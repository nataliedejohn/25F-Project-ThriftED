# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def BuyerHomeNav():
    st.sidebar.page_link(
        "pages/00_Buyer_Home.py", label="Buyer Home", icon="👤"
    )


def ShopProductsNav():
    st.sidebar.page_link(
        "pages/01_Shop_Products.py", label="Shop Products", icon="🏦"
    )


def ViewOrdersNav():
    st.sidebar.page_link("pages/02_View_Orders.py", label="View Orders", icon="🗺️")


def ViewMessagesNav():
    st.sidebar.page_link("pages/03_Buyer_Messages.py", label="View Messages", icon="🛜")

## ------------------------ Examples for Role of Seller ------------------------

def SellerHomeNav():
    st.sidebar.page_link(
      "pages/10_Seller_Home.py", label="Seller Home", icon="🏠"
    )

def ViewListingsNav():
    st.sidebar.page_link("pages/11_View_Listings.py", label="View Listings", icon="📁")

def AddListingNav():
    st.sidebar.page_link("pages/12_Add_Listing.py", label="Add New Listing", icon="➕")

def ViewMessagesNav():
    st.sidebar.page_link("pages/13_Seller_Messages.py", label="View Messages", icon="🛜")


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")

def AdminProductNav():
    st.sidebar.page_link("pages/23_Product_Admin.py", label="View Products")

def AdminUserNav():
    st.sidebar.page_link("pages/25_View_Users.py", label="View Users")

def UserGuidelinesNav():
    st.sidebar.page_link("pages/22_User_Guidelines.py", label="View User Guidelines")

#### ------------------------ Data Analyst Role ------------------------
def AnalystPageNav():
    st.sidebar.page_link("pages/30_Analyst_Home.py", label="System Admin", icon="🖥️")

def PopularProductsNav():
    st.sidebar.page_link("pages/31_Product_Analytics.py", label="Product Analytics")

def PricingNav():
    st.sidebar.page_link("pages/32_Pricing_Analytics.py", label="Pricing Analytics")

def OrdersNav():
    st.sidebar.page_link("pages/33_Order_History_Analytics.py", label="Order Analytics")

def RatigngsNav():
    st.sidebar.page_link("pages/34_Seller_Ratings.py", label="Rating Analytics")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/ThriftED Image.png", width=200)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "buyer":
            BuyerHomeNav()
            ShopProductsNav()
            ViewOrdersNav()
            ViewMessagesNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "seller":
            ViewListingsNav()
            AddListingNav()
            ViewMessagesNav()
            

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
            AdminProductNav()
            AdminUserNav()
            UserGuidelinesNav()

        if st.session_state["role"] == "data_analyst":
            AnalystPageNav()
            PopularProductsNav()
            PricingNav()
            OrdersNav()
            RatigngsNav()
            

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
