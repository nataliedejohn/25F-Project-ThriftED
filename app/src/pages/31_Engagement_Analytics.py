# pages/22_Engagement_Analytics.py
import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("🔥 Engagement & Popularity Analytics")
st.write("Shows top products, categories, tags, searches and basic revenue metrics.")

BASE = "http://web-api:4000"

# Refresh button
if st.button("🔁 Refresh data"):
    st.experimental_rerun()

# --- Popular products (by views/category/revenue) ---
st.header("Top Products")
try:
    r = requests.get(f"{BASE}/analytics/popular-products", timeout=8)
    if r.status_code == 200:
        data = r.json()
        # Expecting either a list of products or {"products": [...]}
        products = data if isinstance(data, list) else data.get("products", [])
        if len(products) == 0:
            st.info("No popular-product data returned from the API.")
        else:
            # Normalize to DataFrame (fields expected: product_id, name, views, revenue, category, tags)
            df = pd.json_normalize(products)
            st.dataframe(df)
            # Simple charts
            if "views" in df.columns:
                st.subheader("Top by Views")
                top_views = df.sort_values("views", ascending=False).head(10).set_index("name")["views"]
                st.bar_chart(top_views)
            if "revenue" in df.columns:
                st.subheader("Top by Revenue")
                top_rev = df.sort_values("revenue", ascending=False).head(10).set_index("name")["revenue"]
                st.bar_chart(top_rev)
    else:
        st.error(f"Failed to fetch popular products: {r.status_code}")
        st.text(r.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")

# --- Category breakdown (counts or totals) ---
st.header("Category Breakdown")
try:
    r = requests.get(f"{BASE}/categories", timeout=6)
    if r.status_code == 200:
        cats = r.json()
        # Expecting list of {category, product_count} or similar
        dfc = pd.json_normalize(cats)
        st.dataframe(dfc)
        if "product_count" in dfc.columns and "category" in dfc.columns:
            st.subheader("Products per Category")
            st.bar_chart(dfc.set_index("category")["product_count"])
    else:
        st.warning("Could not fetch categories (non-critical).")
except requests.exceptions.RequestException:
    st.warning("Categories endpoint not reachable.")

# --- Quick user search-history lookup (example drilldown) ---
st.header("Drilldown: User Search & View History")
user_for_lookup = st.text_input("Enter user id to inspect search history (optional):")
if st.button("Load user history"):
    if not user_for_lookup.strip():
        st.warning("Please enter a user id.")
    else:
        try:
            r = requests.get(f"{BASE}/analytics/user-search-history/{user_for_lookup}", timeout=8)
            if r.status_code == 200:
                uh = r.json()
                st.write("### Search & View History")
                st.dataframe(pd.json_normalize(uh))
            else:
                st.error(f"Failed to load user search history: {r.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Notes: backend should return product fields: product_id, name, category, tags, views, revenue. The user-search-history endpoint should return searches, viewed product ids, timestamps, and durations.")
