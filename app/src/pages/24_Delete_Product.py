import streamlit as st
import requests
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Delete Product")

pid = st.session_state.get("selected_pid")

if pid is None:
    st.error("No Product selected")
else:
    GET_URL = f"http://api:4000/moderator-routes/product/{pid}"
    
    try:
        response = requests.get(GET_URL)
        
        if response.status_code == 200:
            product = response.json()
            
            st.header(f"Delete: {product['Name']}")
            
            st.warning("Are you sure you want to delete this product?")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Product Details")
                st.write(f"**Description:** {product['Description']}")
                st.write(f"**Category:** {product['Category']}")
                st.write(f"**Condition:** {product['Condition']}")
                st.write(f"**Price:** ${product['Price']}")
            
            with col2:
                photo_url = product.get("PhotoURL", "")
                if photo_url and "example.com" not in photo_url:
                    try:
                        st.image(photo_url, caption="Product Photo", use_container_width=True)
                    except Exception:
                        st.info("📷 Product photo not available")
            
            # Delete button
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Delete Product", type="primary"):
                    DELETE_URL = f"http://api:4000/moderator-routes/delete-product/{pid}"
                    
                    try:
                        delete_response = requests.delete(DELETE_URL)
                        
                        if delete_response.status_code == 200:
                            st.success("Product deleted successfully!")
                            # Clear session state
                            if "selected_pid" in st.session_state:
                                del st.session_state["selected_pid"]
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"Failed to delete: {delete_response.json().get('error', 'Unknown error')}")
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to API: {str(e)}")
            
            with col2:
                if st.button("Cancel"):
                    if "selected_pid" in st.session_state:
                        del st.session_state["selected_pid"]
                    st.switch_page("pages/23_Product_Admin.py")
        
        elif response.status_code == 404:
            st.error("Product not found")
        else:
            st.error(f"Error fetching product: {response.json().get('error', 'Unknown error')}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

# Return button
if st.button("Return to All Products"):
    if "selected_pid" in st.session_state:
        del st.session_state["selected_pid"]
    st.switch_page("pages/23_Product_Admin.py")