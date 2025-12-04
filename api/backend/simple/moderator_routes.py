from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
import json

moderator_bp = Blueprint("moderator_bp", __name__)

# Update seller information
@moderator_bp.route("/seller-<id>", methods=["PUT"])
def put_seller_info():
    current_app.logger.info("PUT "/seller-<int>")
    data = {"Verification": "verified", "Restrictions", "Unrestricted"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Update buyer information
@moderator_bp.route("/buyer-<id>", methods=["PUT"])
def put_buyer_info():
    current_app.logger.info("PUT "/buyer-<int>")
    data = {"Verification": "verified", "Restrictions", "Unrestricted"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Delete a specific product listing
@seller_bp.route("/product-seller/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    current_app.logger.info(f"DELETE /product-seller/{pid}") 
    data = {"message": f"Product {pid} listing is no longer available"}
    response = make_response(jsonify(data))
    response.status_code = 200 
    return response

# Update product status
@moderator_bp.route("/product-seller/<id>", methods=["PUT"])
def put_product_status():
    current_app.logger.info("PUT "/product-seller/<int>")
    data = {"Product Status": "Available", "Category": "Home Furniture", "Verification": "Verified"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Create guideline entry
@moderator_bp.route("/buyer-<id>", methods=["PUT"])
def put_product_status():
    current_app.logger.info("PUT "/buyer-<int>")
    data = {"Terms and Conditions": "Enter text"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
