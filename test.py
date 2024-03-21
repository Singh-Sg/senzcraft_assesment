import unittest
import json
from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True

    def test_uploadfile_endpoint(self):
        pdf_file = open("interest.pdf", "rb")
        response = self.app.post("/uploadfile", data={"file": pdf_file})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"success", response.data)
        self.assertIn(b"true", response.data)

    def test_get_contacts(self):
        response = self.app.get("/contact")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        for contact in data:
            self.assertIn("Sl_NO", contact)
            self.assertIn("phone", contact)
            self.assertIn("Contact_First_Name", contact)
            self.assertIn("Contact_Last_Name", contact)
            self.assertIn("Contact_Designation", contact)
            self.assertIn("Contact_eMail", contact)
            self.assertIn("interests", contact)
            self.assertIsInstance(contact["interests"], list)

    def test_get_contact_existing_by_id(self):
        response = self.app.get("/contact/2")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sl_NO", data)
        self.assertIn("phone", data)
        self.assertIn("Contact_First_Name", data)
        self.assertIn("Contact_Last_Name", data)
        self.assertIn("Contact_Designation", data)
        self.assertIn("Contact_eMail", data)
        self.assertIn("interest", data)

    def test_get_contact_non_existing_by_id(self):
        response = self.app.get("/contact/999")
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Contact not found")

        print(data)


if __name__ == "__main__":
    unittest.main()
