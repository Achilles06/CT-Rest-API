import unittest
from unittest.mock import patch
from app import app

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('models.Order.query.all')
    def test_get_orders_success(self, mock_query_all):
        mock_query_all.return_value = [
            {'id': 1, 'customer_id': 1, 'product_id': 1, 'quantity': 2, 'total_price': 21.98},
            {'id': 2, 'customer_id': 2, 'product_id': 2, 'quantity': 1, 'total_price': 15.99}
        ]
        response = self.client.get('/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'21.98', response.data)

    @patch('models.Order.query.get')
    def test_get_order_by_id_not_found(self, mock_query_get):
        mock_query_get.return_value = None
        response = self.client.get('/orders/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order not found', response.data)

    @patch('models.db.session.add')
    @patch('models.db.session.commit')
    def test_create_order_success(self, mock_commit, mock_add):
        data = {'customer_id': 1, 'product_id': 1, 'quantity': 2, 'total_price': 21.98}
        response = self.client.post('/orders', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Order created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
