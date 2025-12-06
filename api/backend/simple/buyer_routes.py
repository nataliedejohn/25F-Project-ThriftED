from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
import json
from backend.db_connection import db
from mysql.connector import Error

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
    data = {"message": "Order successfully placed", "order_data": order_data}
    response = make_response(jsonify(data))
    response.status_code = 201
    return response

@buyer_bp.route("/product-buyer/<int:pid>", methods=["GET"])
def get_product_detail(pid):
    try:
        cursor = db.get_db().cursor()

        # Get NGO details
        query = """
            SELECT p.*, pp.PhotoURL
            FROM Product p
            LEFT JOIN ProductPhoto pp ON p.ProductID = pp.ProductID
            WHERE p.ProductID = %s
        """
        cursor.execute(query, (pid,))
        prod = cursor.fetchone()

        if not prod:
            return jsonify({"error": "Product not found"}), 404

        cursor.close()
        return jsonify(prod), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
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

@buyer_bp.route("/orders", methods=["GET"])
def get_all_orders():
    try:
        current_app.logger.info('Starting get_all_orders request')
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Orders"

        cursor.execute(query)
        orders = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(orders)} Orders')
        the_response = make_response(orders)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500
