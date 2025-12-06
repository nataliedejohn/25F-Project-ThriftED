from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)
import json

data_analyst_bp = Blueprint("data_analyst_bp", __name__)

# GET popular products by views, category, revenue
@data_analyst_bp.route("/analytics/popular-products", methods=["GET"])
def get_popular_products():
    current_app.logger.info("GET /analytics/popular-products")
  
    data = {
        "products": [
            {"product_id": 1, "name": "Desk Lamp", "views": 230, "revenue": 540.00},
            {"product_id": 2, "name": "Office Chair", "views": 180, "revenue": 720.00},
        ]
    }
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET price similarity and price suggestions
@data_analyst_bp.route("/analytics/price-ranges", methods=["GET"])
def get_price_ranges():
    current_app.logger.info("GET /analytics/price-ranges")

    data = {
        "price_ranges": [
            {
                "category": "Home Furniture",
                "suggested_min": 50.0,
                "suggested_max": 250.0,
                "average": 140.0,
            },
            {
                "category": "Electronics",
                "suggested_min": 20.0,
                "suggested_max": 300.0,
                "average": 110.0,
            },
        ]
    }
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET analyze search history and viewed items for a specific buyer
@data_analyst_bp.route("/analytics/user-search-history/<int:user_id>", methods=["GET"])
def get_user_search_history(user_id):
    current_app.logger.info(f"GET /analytics/user-search-history/{user_id}")

    data = {
        "user_id": user_id,
        "recent_search_terms": ["desk", "lamp", "bookshelf"],
        "recent_viewed_products": [3, 5, 8, 13],  # product IDs, for example
    }
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET app ratings and feedback
@data_analyst_bp.route("/analytics/app-feedback", methods=["GET"])
def get_app_feedback():
    current_app.logger.info("GET /analytics/app-feedback")

    data = {
        "feedback": [
            {"rating": 5, "comment": "Super easy to use", "user_id": 101},
            {"rating": 3, "comment": "Search is a bit slow", "user_id": 202},
        ]
    }
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# GET a list of categories and product counts (for demand / supply insights)
@data_analyst_bp.route("/categories", methods=["GET"])
def get_category_stats():
    current_app.logger.info("GET /categories")

    data = {
        "categories": [
            {"name": "Home Furniture", "product_count": 42},
            {"name": "Electronics", "product_count": 57},
            {"name": "Clothing", "product_count": 33},
        ]
    }
    response = make_response(jsnoify(data))
    response.status_code = 200
    return response
