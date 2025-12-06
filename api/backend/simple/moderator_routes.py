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
@moderator_bp.route("/seller/<int:seller_id>", methods=["PUT"])
def put_seller_info(seller_id):
    current_app.logger.info(f"PUT /seller/{seller_id}")
    data = {"seller_id": seller_id, "verification": "verified", "restrictions": "unrestricted"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Update buyer information
@moderator_bp.route("/buyer/<int:buyer_id>", methods=["PUT"])
def put_buyer_info(buyer_id):
    current_app.logger.info(f"PUT /buyer/{buyer_id}")
    data = {"buyer_id": buyer_id, "verification": "verified", "restrictions": "unrestricted"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Delete a specific product listing
@moderator_bp.route("/product-seller/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    current_app.logger.info(f"DELETE /product-seller/{pid}")
    data = {"message": f"Product {pid} listing is no longer available"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Update product status/category/verification
@moderator_bp.route("/product-seller/<int:pid>", methods=["PUT"])
def put_product_status(pid):
    current_app.logger.info(f"PUT /product-seller/{pid}")
    data = {
        "product_id": pid,
        "product_status": "Available",
        "category": "Home Furniture",
        "verification": "Verified",
    }
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Update guidelines (terms & conditions)
@moderator_bp.route("/guidelines", methods=["PUT"])
def update_guidelines():
    current_app.logger.info("PUT /guidelines")

    data = {"terms_and_conditions": "Enter text"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
