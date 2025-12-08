from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app, make_response

# Create a Blueprint for NGO routes
moderator_bp = Blueprint("moderator_bp", __name__)


# Get all NGOs with optional filtering by country, focus area, and founding year
# Example: /ngo/ngos?country=United%20States&focus_area=Environmental%20Conservation

@moderator_bp.route("/products", methods=["GET"])
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
@moderator_bp.route("/product-admin/<int:pid>", methods=["PUT"])
def put_verify_product(pid):
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
    
@moderator_bp.route("/delete-product/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    try:
        current_app.logger.info(f'Starting delete_product request for ProductID: {pid}')
        cursor = db.get_db().cursor()

        # Delete the product
        query = "DELETE FROM Product WHERE ProductID = %s"
        cursor.execute("DELETE FROM AnalystProductAnalysis WHERE ProductID = %s", (pid,))
        cursor.execute("DELETE FROM TagsOfProduct WHERE ProductID = %s", (pid,))
        cursor.execute("DELETE FROM ProductPhoto WHERE ProductID = %s", (pid,))
        cursor.execute("UPDATE Product SET OrderID = NULL WHERE ProductID = %s", (pid,))
       
        cursor.execute(query, (pid,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f'Successfully deleted ProductID: {pid}')
        return jsonify({"message": "Product deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_product: {str(e)}')
        return jsonify({"error": str(e)}), 500


@moderator_bp.route("/product/<int:pid>", methods=["GET"])
def get_product_detail(pid):
    try:
        cursor = db.get_db().cursor()
       
        query = """
            SELECT p.*, pp.PhotoURL
            FROM Product p
            LEFT JOIN ProductPhoto pp ON p.ProductID = pp.ProductID
            WHERE p.ProductID = %s
        """
        cursor.execute(query, (pid,))
        product = cursor.fetchone()
       
        if not product:
            cursor.close()
            return jsonify({"error": "Product not found"}), 404
       
        cursor.close()
        return jsonify(product), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@moderator_bp.route("/buyers", methods=["GET"])
def get_all_buyers():
    try:
        current_app.logger.info('Starting get_all_users request')
        cursor = db.get_db().cursor()

        # Prepare the Base query
        query = "SELECT * FROM Buyer"
        params = []

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(users)} users')
        the_response = make_response(users)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_users: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@moderator_bp.route("/sellers", methods=["GET"])
def get_all_sellers():
    try:
        current_app.logger.info('Starting get_all_sellers request')
        cursor = db.get_db().cursor()

        # Prepare the Base query
        query = "SELECT * FROM Seller"
        params = []

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query)
        sellers = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(sellers)} sellers')
        the_response = make_response(sellers)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_sellers: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@moderator_bp.route("/delete-buyer/<int:bid>", methods=["DELETE"])
def delete_buyer(bid):
    try:

        current_app.logger.info(f'Starting delete_buyer request for BuyerID: {bid}')
        cursor = db.get_db().cursor()

        cursor.execute("SELECT OrderID FROM Orders WHERE BuyerID = %s", (bid,))
        orders = cursor.fetchall()
        for order in orders:
            cursor.execute("UPDATE Product SET OrderID = NULL WHERE OrderID = %s", (order['OrderID'],))
        cursor.execute("DELETE FROM Orders WHERE BuyerID = %s", (bid,))
        cursor.execute("DELETE FROM History WHERE BuyerID = %s", (bid,))
        cursor.execute("DELETE FROM Messages WHERE BuyerID = %s", (bid,))
        cursor.execute("DELETE FROM PaymentMethod WHERE BuyerID = %s", (bid,))
        query = "DELETE FROM Buyer WHERE BuyerID = %s"
        cursor.execute(query, (bid,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f'Successfully deleted BuyerID: {bid}')
        return jsonify({"message": "Buyer deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_buyer: {str(e)}')
        return jsonify({"error": str(e)}), 500