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
    try:
        current_app.logger.info('Starting get_products_buyer request')
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Product"

        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(products)} Products')
        the_response = make_response(products)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500

@buyer_bp.route("/buyer-orders", methods=["GET"])
def get_orders():
    try:
        buyerid = request.args.get("BuyerID")
        current_app.logger.info("Starting get_orders request")
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Orders WHERE BuyerID = 2"
        cursor.execute(query)
        orders = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Successfully retrieved {len(orders)} orders")
        response = make_response(jsonify(orders))
        response.status_code = 200
        response.mimetype = "application/json"
        return response
    except Error as e:
        current_app.logger.error(f"Database error in get_orders: {str(e)}")
        return jsonify({"error": str(e)}), 500

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
    
@buyer_bp.route("/messages", methods=["GET"])
def get_all_messages():
    try:
        current_app.logger.info('Starting get_all_orders request')
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Messages WHERE BuyerID = 1"

        cursor.execute(query)
        messages = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(messages)} Orders')
        the_response = make_response(messages)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Create a new message 
@buyer_bp.route("/create-messages", methods=["POST"])
def create_message():
    try:
        data = request.get_json()

        # validate required fields
        required_fields = ["SellerID", "Body"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()

        # Insert new listing into database
        query = """INSERT INTO Messages (BuyerID, SellerID, Body) VALUES (%s, %s, %s)"""
        params = (
            2,
            data["SellerID"],
            data["Body"],
        )

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Product Successfully Listed"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500