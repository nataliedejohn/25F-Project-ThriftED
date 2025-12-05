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

seller_bp = Blueprint("seller_bp", __name__)

# Retrieve all products for seller
@seller_bp.route("/product-seller", methods=["GET"])
def get_products_seller():
    try:
        current_app.logger.info('Starting get_all_orders request')
        cursor = db.get_db().cursor()

        query = "SELECT * FROM Product WHERE SellerID = 2;"

        cursor.execute(query)
        listing = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(listing)} Orders')
        the_response = make_response(listing)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500
  
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
    data = {"product_status": "available", "category": "electronics"}
    response = make_response(jsonify(data))
    response.status_code = 200
    return response



