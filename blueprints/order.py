from flask import Blueprint, jsonify, request
from models import db, Order
from app import limiter

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('', methods=['POST'])
@limiter.limit("10/minute")
def create_order():
    data = request.get_json()
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'], total_price=data['total_price'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@order_bp.route('', methods=['GET'])
@limiter.limit("15/minute")
def get_orders():
    orders = Order.query.all()
    result = [{'id': ord.id, 'customer_id': ord.customer_id, 'product_id': ord.product_id, 'quantity': ord.quantity, 'total_price': ord.total_price} for ord in orders]
    return jsonify(result), 200
