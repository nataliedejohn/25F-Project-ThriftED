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

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Get query parameters for filtering
        #country = request.args.get("country")
        #focus_area = request.args.get("focus_area")
        #founding_year = request.args.get("founding_year")

        #current_app.logger.debug(f'Query parameters - country: {country}, focus_area: {focus_area}, founding_year: {founding_year}')

        # Prepare the Base query
        query = "SELECT * FROM Product"
        params = []
        '''
        # Add filters if provided
        if country:
            query += " AND Country = %s"
            params.append(country)
        if focus_area:
            query += " AND Focus_Area = %s"
            params.append(focus_area)
        if founding_year:
            query += " AND Founding_Year = %s"
            params.append(founding_year)
        '''

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
