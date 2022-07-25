"""Test main"""
import unittest

from main import app


class TestMain(unittest.TestCase):
    """Test main"""

    def setUp(self):
        """Set up class"""
        self.app = app.test_client()

    def test_get_index_url(self):
        """Test get index url"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'API': 'Contemplato-tec-test'})

    def test_get_not_found_url(self):
        """Test get not found url"""
        response = self.app.get('/teste/teste/teste')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(), b'Sorry, Nothign at this URL.')


if __name__ == '__main__':
    unittest.main()
