@order_bp.route('/orders', methods=['GET'])
@swag_from({
    'summary': 'List all orders',
    'responses': {
        '200': {
            'description': 'A list of orders',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Order'
                }
            }
        }
    }
})
def list_orders():
    # Implement listing logic
    return jsonify([]), 200
