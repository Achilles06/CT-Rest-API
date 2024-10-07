import unittest
from unittest.mock import patch
from app import app

class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('models.Employee.query.all')
    def test_get_employees_success(self, mock_query_all):
        mock_query_all.return_value = [
            {'id': 1, 'name': 'John Doe', 'position': 'Manager'},
            {'id': 2, 'name': 'Jane Doe', 'position': 'Developer'}
        ]
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    @patch('models.Employee.query.get')
    def test_get_employee_by_id_not_found(self, mock_query_get):
        mock_query_get.return_value = None
        response = self.client.get('/employees/99')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Employee not found', response.data)

    @patch('models.db.session.add')
    @patch('models.db.session.commit')
    def test_create_employee_success(self, mock_commit, mock_add):
        data = {'name': 'John Smith', 'position': 'Intern'}
        response = self.client.post('/employees', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Employee created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
