from flask import Blueprint, jsonify, request
from models import db, Product
from app import limiter

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('', methods=['POST'])
@limiter.limit("10/minute")
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('', methods=['GET'])
@limiter.limit("15/minute")
def get_products():
    products = Product.query.all()
    result = [{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]
    return jsonify(result), 200
