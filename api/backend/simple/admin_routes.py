from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app, make_response

# Create a Blueprint for NGO routes
admin_route = Blueprint("admin-routes", __name__)


# Get all NGOs with optional filtering by country, focus area, and founding year
# Example: /ngo/ngos?country=United%20States&focus_area=Environmental%20Conservation

@admin_route.route("/products", methods=["GET"])
def get_all_products():
    try:
        current_app.logger.info('Starting get_all_products request')
        cursor = db.get_db().cursor()

        # Prepare the Base query
        query = "SELECT * FROM Product"
        params = []

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(products)} NGOs')
        the_response = make_response(products)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Update product listing for a specific product
@admin_route.route("/product-admin/<int:pid>", methods=["PUT"])
def put_seller_product(pid):
    try:
        data = request.get_json()

        # Check if product exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (pid,))
        if not cursor.fetchone():
            return jsonify({"error": "Product not found"}), 404
        
        # Update query
        query = f"UPDATE Product SET Verified WHERE ProductID = %s"
        cursor.execute(query, (pid,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message", "Product updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500