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
    try:
        data = request.get_json()

        # Check if product exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (pid,))
        if not cursor.fetchone():
            return jsonify({"error": "Product not found"}), 404
        
        # Update query
        query = f"UPDATE Product SET Status WHERE ProductID = %s"
        cursor.execute(query, (pid,))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message", "Product updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Create a new product listing
@seller_bp.route("/listings", methods=["POST"])
def create_listing():
    try:
        data = request.get_json()

        # validate required fields
        required_fields = ["Name", "Description", "Category", "Condition", "Price"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()

        # Insert new listing into database
        query = """INSERT INTO Product (SellerID, Name, Description, Category, `Condition`, Price) VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (
            data["SellerID"],
            data["Name"],
            data["Description"],
            data["Category"],
            data["Condition"],
            data["Price"],
        )

        cursor.execute(query, params)
        product_id = cursor.lastrowid

        # Insert tags into database
        for tag in data["Tags"]:
            tag_query = """ INSERT INTO ProductTag (Title)
                            VALUES (%s) """
            cursor.execute(tag_query, (tag,))
            tag_id = cursor.lastrowid
            product_tag_query = """ INSERT INTO TagsOfProduct (ProductID, ProductTagID)
                                    VALUES (%s, %s)"""
            cursor.execute(product_tag_query, (product_id, tag_id))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Product Successfully Listed"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Create a new message 
@seller_bp.route("/create-messages", methods=["POST"])
def create_message():
    try:
        data = request.get_json()

        # validate required fields
        required_fields = ["BuyerID", "Body"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()

        # Insert new listing into database
        query = """INSERT INTO Messages (SellerID, BuyerID, Body) VALUES (%s, %s, %s)"""
        params = (
            1,
            data["BuyerID"],
            data["Body"],
        )

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Product Successfully Listed"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Delete listing
@seller_bp.route("/remove_listing", methods=["DELETE"])
def delete_product(pid):
    try:
        # Check if product exists
        cursor = db.get_db.cursor()
        cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (pid,))
        if not cursor.fetchone():
            return jsonify({"error": "Product not found"}), 404
        
        # Delete query
        query = f"DELETE Product WHERE ProductID = %s"
        cursor.execute(query, (pid))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Product deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@seller_bp.route("/messages", methods=["GET"])
def get_messages():
    try:
        user_id = request.args.get("user_id")
        
        cursor = db.get_db().cursor()

        query = """
            SELECT 
                m.ConvoID as chat_id,
                m.Body as last_message,
                m.ConvoStartDate,
                CONCAT(b.FirstName, ' ', b.LastName) as buyer_name,
                CONCAT(s.FirstName, ' ', s.LastName) as seller_name,
                m.BuyerID,
                m.SellerID
            FROM Messages m
            LEFT JOIN Buyer b ON m.BuyerID = b.BuyerID
            LEFT JOIN Seller s ON m.SellerID = s.SellerID
            WHERE m.SellerID = 1
            ORDER BY m.ConvoStartDate DESC
        """
        
        cursor.execute(query)
        messages = cursor.fetchall()
        cursor.close()

        return jsonify(messages), 200
        
    except Error as e:
        current_app.logger.error(f'Database error in get_messages: {str(e)}')
        return jsonify({"error": str(e)}), 500
    