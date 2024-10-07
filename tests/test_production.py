import unittest
from unittest.mock import patch
from app import app

class TestProductionEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('models.Production.query.all')
    def test_get_production_success(self, mock_query_all):
        mock_query_all.return_value = [
            {'id': 1, 'product_id': 1, 'quantity_produced': 100, 'date_produced': '2023-09-01'},
            {'id': 2, 'product_id': 2, 'quantity_produced': 200, 'date_produced': '2023-09-02'}
        ]
        response = self.client.get('/production')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'100', response.data)

    @patch('models.Production.query.get')
    def test_get_production_by_id_not_found(self, mock_query_get):
        mock_query_get.return_value = None
        response = self.client.get('/production/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Production record not found', response.data)

    @patch('models.db.session.add')
    @patch('models.db.session.commit')
    def test_create_production_success(self, mock_commit, mock_add):
        data = {'product_id': 1, 'quantity_produced': 150, 'date_produced': '2023-09-03'}
        response = self.client.post('/production', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Production record created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
