from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
import json

seller_bp = Blueprint("seller_bp", __name__)

# Retrieve all products for seller
@seller_bp.route("/product-seller", methods=["GET"])
def get_products_seller():
    current_app.logger.info("GET /product-seller")
    data = {"products": ["item1", "item2"], "filter": "seller view"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
  
# Get seller information 
@seller_bp.route("/seller-<int:pid>", methods=["GET"])
def get_seller_info(pid):
    current_app.logger.info(f"GET /seller-{pid}")
    data = {"seller_name": ["first_name", "last_name"], "ratings": ["rating"],"product_views": ["views"], "product_saves": ["saves"]}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
  
# Update product listing for a specific product
@seller_bp.route("/product-seller/<int:pid>", methods=["PUT"])
def put_seller_product(pid):
    current_app.logger.info(f"PUT /product-seller/{pid}")
    data = {"product_status": "available", "category": "electronics", "verification", "verified"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response



