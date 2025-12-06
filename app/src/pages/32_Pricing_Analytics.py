# pages/23_Pricing_Analytics.py
import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import numpy as np

st.set_page_config(layout="wide")
SideBarLinks()

st.title("💲 Pricing & Listing Quality Analysis")
st.write("Price distributions, suggested price ranges, and outlier detection.")

BASE = "http://web-api:4000"

# Filters
category = st.selectbox("Category (optional)", ["All", "Furniture", "Clothing", "Textbooks", "Other"])
min_price, max_price = st.slider("Filter price range", 0, 1000, (0, 1000))

params = {}
if category != "All":
    params["category"] = category
params["min_price"] = min_price
params["max_price"] = max_price

# Load price ranges / suggestions
try:
    r = requests.get(f"{BASE}/analytics/price-ranges", params=params, timeout=8)
    if r.status_code == 200:
        payload = r.json()
        # Expecting structure like: { "by_category": [...], "suggestions": [...], "products": [...] }
        st.subheader("Suggested Price Ranges")
        st.json(payload.get("suggestions", payload))

        # If products returned, compute outliers
        products = payload.get("products") or payload.get("items") or []
        if products:
            df = pd.json_normalize(products)
            st.write(f"Found {len(df)} products in this slice")
            st.dataframe(df.head(200))

            # Basic outlier detection using z-score on price
            if "price" in df.columns:
                prices = df["price"].astype(float)
                z = (prices - prices.mean()) / (prices.std(ddof=0) + 1e-9)
                df["zscore"] = z
                outliers = df[np.abs(df["zscore"]) > 3].sort_values("zscore", ascending=False)
                st.subheader("Detected Price Outliers (|z| > 3)")
                if outliers.empty:
                    st.success("No extreme price outliers detected.")
                else:
                    st.dataframe(outliers[["product_id", "name", "price", "zscore"]])
                    st.markdown("If desired, select outliers below to flag them for moderator review (frontend action).")

                    # Flagging UI (local only — you can wire to a report endpoint)
                    for _, row in outliers.iterrows():
                        key = f"flag_{row['product_id']}"
                        if st.button(f"⚠️ Flag {row.get('name')} (id:{row.get('product_id')})", key=key):
                            st.info(f"Flagged locally: {row.get('product_id')} - implement POST/PUT to report in backend")

        else:
            st.info("No product-level data returned from price-ranges endpoint.")

    else:
        st.error(f"Failed to fetch price ranges: {r.status_code}")
        st.text(r.text)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to analytics endpoint: {e}")

st.markdown("---")
st.caption("Notes: backend should return 'suggestions' and optionally product list with 'price' for outlier detection.")
