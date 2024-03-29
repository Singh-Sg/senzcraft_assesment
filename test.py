
import unittest
from unittest.mock import MagicMock
from flask import Flask
from routes.contact_routes import contact_routes

class TestContactRoutes(unittest.TestCase):
    def setUp(self):
        # Create Flask app and register contact_routes blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(contact_routes)
        self.client = self.app.test_client()

    def test_upload_file(self):
        # Test uploading a file
        with self.app.test_request_context('/uploadfile', method='POST'):
            with self.app.test_client() as client:
                with open('contact.pdf', 'rb') as file:
                    data = {'file': (file, 'cantact.pdf')}
                    response = client.post('/uploadfile', data=data, content_type='multipart/form-data')
                    self.assertEqual(response.status_code, 201)  # Assuming successful upload returns 201 status code

    def test_get_contacts(self):
        # Test retrieving all contacts
        with self.app.test_request_context('/contact', method='GET'):
            response = self.client.get('/contact')
            self.assertEqual(response.status_code, 200)  # Assuming successful retrieval returns 200 status code

    def test_get_contact_by_id(self):
        # Test retrieving a contact by ID
        with self.app.test_request_context('/contact/1', method='GET'):
            response = self.client.get('/contact/1')
            self.assertEqual(response.status_code, 200)  # Assuming contact with ID 1 exists and returns 200 status code

    

if __name__ == '__main__':
    unittest.main()
