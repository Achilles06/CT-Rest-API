import unittest
from unittest.mock import patch
from app import app

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('models.Customer.query.all')
    def test_get_customers_success(self, mock_query_all):
        mock_query_all.return_value = [
            {'id': 1, 'name': 'Customer A', 'email': 'a@example.com', 'phone': '123-456-7890'},
            {'id': 2, 'name': 'Customer B', 'email': 'b@example.com', 'phone': '987-654-3210'}
        ]
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer A', response.data)

    @patch('models.Customer.query.get')
    def test_get_customer_by_id_not_found(self, mock_query_get):
        mock_query_get.return_value = None
        response = self.client.get('/customers/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Customer not found', response.data)

    @patch('models.db.session.add')
    @patch('models.db.session.commit')
    def test_create_customer_success(self, mock_commit, mock_add):
        data = {'name': 'Customer C', 'email': 'c@example.com', 'phone': '555-555-5555'}
        response = self.client.post('/customers', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Customer created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
