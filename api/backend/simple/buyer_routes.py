from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
import json

buyer_bp = Blueprint("buyer_bp", __name__)

@buyer_bp.route("/product-buyer", methods=["GET"])
def get_products_buyer():
    current_app.logger.info("GET /product-buyer")
    data = {"products": ["item1", "item2"], "filter": "buyer view"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

@buyer_bp.route("/orders", methods=["POST"])
def create_orders():
    current_app.logger.info("POST /orders")
    order_data = request.get_json()
    data = {"message": "Order successfully placed", "order_data": order_data]}
    response = make_response(jsonify(data))
    response.status_code = 201
    return response

@buyer_bp.route("/product-buyer/<int:pid>", methods=["GET"])
def get_product_detail(pid):
    current_app.logger.info(f"GET /product-buyer/{pid}")
    product_data = {"product_id": pid, "name": "Example Product", "price": 50.0}
    response = make_response(jsonify(product_data))
    response.status_code = 200
    return response
    
@buyer_bp.route("/orders/<int:order_id>/cancel", methods=["PUT"])
def cancel_order(order_id):
    current_app.logger.info(f"PUT /orders/{order_id}/cancel")
    canceled = {"message": f"Order {order_id} canceled"}
    response = make_response(jsonify(canceled))
    response.status_code = 200
    return response
    
@buyer_bp.route("/buyer-profile", methods=["GET"])
def get_buyer_profile():
    current_app.logger.info("GET /buyer-profile")
    buyer_profile = {"buyer_id": 123, "name": "Chloe Kim", "email": "chloe.kim@nu.edu"}
    response = make_response(jsonify(buyer_profile))
    response.status_code = 200
    return response
