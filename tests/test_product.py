import unittest
from unittest.mock import patch
from app import app

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('models.Product.query.all')
    def test_get_products_success(self, mock_query_all):
        mock_query_all.return_value = [
            {'id': 1, 'name': 'Product A', 'price': 10.99},
            {'id': 2, 'name': 'Product B', 'price': 15.99}
        ]
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product A', response.data)

    @patch('models.Product.query.get')
    def test_get_product_by_id_not_found(self, mock_query_get):
        mock_query_get.return_value = None
        response = self.client.get('/products/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found', response.data)

    @patch('models.db.session.add')
    @patch('models.db.session.commit')
    def test_create_product_success(self, mock_commit, mock_add):
        data = {'name': 'Product C', 'price': 25.99}
        response = self.client.post('/products', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Product created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
