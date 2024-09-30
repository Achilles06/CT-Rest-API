from flask import Blueprint, jsonify, request
from models import db, Product, Order
from sqlalchemy import func
from app import limiter

# Define the blueprint
product_bp = Blueprint('product_bp', __name__)

# Route to create a new product
@product_bp.route('', methods=['POST'])
@limiter.limit("10/minute")
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Bad request. Name and price are required.'}), 400

    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# Route to fetch all products
@product_bp.route('', methods=['GET'])
@limiter.limit("15/minute")
def get_products():
    products = Product.query.all()
    result = [{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]
    return jsonify(result), 200

# Task 2: Identify Top-Selling Products
@product_bp.route('/top-selling', methods=['GET'])
def identify_top_selling_products():
    # Query to calculate total quantity ordered for each product, grouped by product name
    result = db.session.query(
        Product.name,
        func.sum(Order.quantity).label('total_quantity_ordered')
    ).join(Order, Product.id == Order.product_id) \
     .group_by(Product.name) \
     .order_by(func.sum(Order.quantity).desc()).all()

    # Format the result into a list of dictionaries
    top_products = [{'product': row.name, 'total_quantity_ordered': row.total_quantity_ordered} for row in result]
    
    return jsonify(top_products), 200
