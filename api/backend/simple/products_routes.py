from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
)

products_bp = Blueprint("products_bp", __name__)

# /product-buyer  GET
@products_bp.route("/product-buyer", methods=["GET"])
def get_products_buyer():
    current_app.logger.info("GET /product-buyer")
    data = {"products": ["item1", "item2"], "filter": "buyer view"}
    return make_response(jsonify(data), 200)

# /product-seller  GET, POST
@products_bp.route("/product-seller", methods=["GET"])
def get_products_seller():
    current_app.logger.info("GET /product-seller")
    return make_response(jsonify({"products": ["seller-item1"]}), 200)

@products_bp.route("/product-seller", methods=["POST"])
def create_product_listing():
    current_app.logger.info("POST /product-seller")
    data = request.get_json()
    return make_response(jsonify({"message": "product created", "data": data}), 201)

# /product-seller/<id>   PUT, DELETE
@products_bp.route("/product-seller/<int:pid>", methods=["PUT"])
def update_product(pid):
    current_app.logger.info(f"PUT /product-seller/{pid}")
    data = request.get_json()
    return make_response(jsonify({"msg": "updated", "id": pid, "new": data}), 200)

@products_bp.route("/product-seller/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    current_app.logger.info(f"DELETE /product-seller/{pid}")
    return make_response(jsonify({"msg": "product removed", "id": pid}), 200)

# /product-buyer/<id> GET
@products_bp.route("/product-buyer/<int:pid>", methods=["GET"])
def get_product_detail(pid):
    current_app.logger.info(f"GET /product-buyer/{pid}")
    return make_response(jsonify({"product_id": pid}), 200)

if __name__ == "__main__":
  app.run(debug=True)
