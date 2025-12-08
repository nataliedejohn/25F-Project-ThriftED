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

analyst_bp = Blueprint("analyst-routes", __name__)

# GET popular products by category
@analyst_bp.route("/product-category", methods=["GET"])
def get_popular_category():
    try:
        current_app.logger.info('Starting get_products_buyer request')
        cursor = db.get_db().cursor()

        query = """SELECT Title, COUNT(Title) FROM ProductTag 
                    GROUP BY Title
                    ORDER BY COUNT(Title) DESC"""

        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(data)} tags')
        the_response = make_response(data)
        the_response.status_code = 200
        the_response.mimetype = "application/json"
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
# GET popular products by category
@analyst_bp.route("/product-tags", methods=["GET"])
def get_popular_products():
    try:
        current_app.logger.info('Starting get_products_buyer request')
        cursor = db.get_db().cursor()

        query = """SELECT Category, COUNT(Category) FROM Product 
                    GROUP BY Category
                    ORDER BY COUNT(Category) DESC"""

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


# GET price similarity and price suggestions
@analyst_bp.route("/analytics/price-ranges", methods=["GET"])
def get_price_ranges():
    try:
        category = request.args.get("Category")
        if not category:
            return jsonify({"error": "Category parameter is required"}), 400
        current_app.logger.info("Starting get_price_ranges request")
        cursor = db.get_db().cursor()

        query = """SELECT MIN(Price) as MinPrice, MAX(Price) as MaxPrice, AVG(Price) as AvgPrice
                    FROM Product
                    WHERE Category = %s """
        cursor.execute(query, (category,))
        products = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Successfully retrived {len(products)} products.")
        response = make_response(products)
        response.status_code = 200
        response.mimetype = "application/json"
        return response
    except Error as e:
        current_app.logger.error(f"Database error in get_price_ranges: {str(e)}")
        return jsonify({"error": str(e)}), 500


# GET analyze search history and viewed items for a specific buyer
@analyst_bp.route("/analytics/user-search-history", methods=["GET"])
def get_user_search_history():
    try:
        current_app.logger.info(f"Starting get_user_search_history request")
        cursor = db.get_db().cursor()

        query = """ SELECT h.BuyerID, COUNT(h.BuyerID) as NumSearches, COUNT(o.BuyerID) AS NumOrders
                    FROM History h JOIN Buyer b ON h.BuyerID = b.BuyerID
                    JOIN Orders o ON b.BuyerID = o.BuyerID
                    GROUP BY h.BuyerID
                    ORDER BY NumSearches DESC """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close

        current_app.logger.info(f"Successfully retrived data on {len(data)} buyers")
        response = make_response(jsonify(data))
        response.status_code = 200
        response.mimetype = "application/json"
        return response
    except Error as e:
        current_app.logger.info(f"Database error in get_user_search_history: {str(e)}")
        return jsonify({"error": str(e)}), 500


# GET app ratings and feedback
@analyst_bp.route("/ratings", methods=["GET"])
def get_seller_ratings():
    try:
        current_app.logger.info("Starting get_seller_ratings")
        cursor = db.get_db().cursor()

        query = """ SELECT s.SellerID, s.Rating, COUNT(p.SellerID) as TotalProducts
                    FROM Seller s JOIN Product p ON s.SellerID = p.SellerID
                    GROUP BY s.SellerID, s.Rating
                    ORDER BY s.Rating DESC"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Successfully retrived data on {len(data)} sellers.")
        response = make_response(jsonify(data))
        response.status_code = 200
        response.mimetype="application/json"
        return response
    except Error as e:
        current_app.logger.error(f"Database error in get_seller_ratings: {str(e)}")
        return jsonify({"error": str(e)}), 500