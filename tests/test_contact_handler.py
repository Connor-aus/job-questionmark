import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
from src.handlers.contact_handler import handle_contact_request, ContactRequest

class TestContactHandler(unittest.TestCase):
    
    def setUp(self):
        # Set up environment variables for testing
        os.environ["CONTACT_EMAIL"] = "test@example.com"
        
    @patch('src.handlers.contact_handler.send_email')
    def test_valid_contact_request(self, mock_send_email):
        # Test data
        contact_data = {
            "email": "sender@example.com",
            "subject": "Test Subject",
            "message": "This is a test message"
        }
        
        # Call the handler
        result = handle_contact_request(contact_data)
        
        # Check that send_email was called with correct parameters
        mock_send_email.assert_called_once_with(
            "test@example.com",
            "sender@example.com",
            "Test Subject",
            "This is a test message"
        )
        
        # Check the response
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"]["message"], "Your message has been sent successfully")
    
    def test_invalid_email(self):
        # Test data with invalid email
        contact_data = {
            "email": "not-an-email",
            "subject": "Test Subject",
            "message": "This is a test message"
        }
        
        # Call the handler
        result = handle_contact_request(contact_data)
        
        # Check the response
        self.assertEqual(result["statusCode"], 400)
        self.assertIn("Invalid email format", str(result["body"]["error"]))
    
    def test_empty_subject(self):
        # Test data with empty subject
        contact_data = {
            "email": "sender@example.com",
            "subject": "",
            "message": "This is a test message"
        }
        
        # Call the handler
        result = handle_contact_request(contact_data)
        
        # Check the response
        self.assertEqual(result["statusCode"], 400)
        self.assertIn("Subject cannot be empty", str(result["body"]["error"]))
    
    def test_missing_field(self):
        # Test data with missing field
        contact_data = {
            "email": "sender@example.com",
            "subject": "Test Subject"
            # Missing message field
        }
        
        # Call the handler
        result = handle_contact_request(contact_data)
        
        # Check the response
        self.assertEqual(result["statusCode"], 400)
        self.assertIn("field required", str(result["body"]["error"]).lower())
    
    @patch('os.environ.get')
    def test_missing_contact_email_config(self, mock_get_env):
        # Simulate missing CONTACT_EMAIL environment variable
        mock_get_env.return_value = None
        
        # Test data
        contact_data = {
            "email": "sender@example.com",
            "subject": "Test Subject",
            "message": "This is a test message"
        }
        
        # Call the handler
        result = handle_contact_request(contact_data)
        
        # Check the response
        self.assertEqual(result["statusCode"], 400)
        self.assertIn("Contact email configuration is missing", str(result["body"]["error"]))
    
    @patch('src.handlers.contact_handler.send_email')
    def test_email_sending_error(self, mock_send_email):
        # Make send_email raise an exception
        mock_send_email.side_effect = Exception("Failed to send email")
        
        # Test data
        contact_data = {
            "email": "sender@example.com",
            "subject": "Test Subject",
            "message": "This is a test message"
        }
        
        # Call the handler
        result = handle_contact_request(contact_data)
        
        # Check the response
        self.assertEqual(result["statusCode"], 500)
        self.assertIn("Failed to process your request", str(result["body"]["error"]))

if __name__ == "__main__":
    unittest.main() 