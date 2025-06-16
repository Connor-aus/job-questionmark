import os
import re
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError
from src.utils.logger import log
from pydantic import BaseModel, Field, field_validator

class ContactRequest(BaseModel):
    email: str
    subject: str
    message: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        # Simple email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v
    
    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v):
        if not v or not v.strip():
            raise ValueError("Subject cannot be empty")
        if len(v) > 100:  # Standard email subject length
            raise ValueError("Subject exceeds maximum length of 100 characters")
        return v
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        if len(v) > 5000:  # Reasonable message length limit
            raise ValueError("Message exceeds maximum length of 5000 characters")
        return v

def handle_contact_request(contact_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a contact form submission and send an email
    """
    log.info("Processing contact form submission")
    
    try:
        # Validate request data
        contact_request = ContactRequest(**contact_data)
        
        # Get recipient email from environment variable
        recipient_email = os.environ.get("CONTACT_EMAIL")
        if not recipient_email:
            log.error("CONTACT_EMAIL environment variable not set")
            raise ValueError("Contact email configuration is missing")
        
        # Send email using AWS SES
        send_email(
            recipient_email,
            contact_request.email,
            contact_request.subject,
            contact_request.message
        )
        
        log.info(f"Contact email sent successfully from {contact_request.email}")
        return {
            "statusCode": 200,
            "body": {"message": "Your message has been sent successfully"}
        }
        
    except ValueError as ve:
        log.warning(f"Contact form validation error: {str(ve)}")
        return {
            "statusCode": 400,
            "body": {"error": str(ve)}
        }
    except Exception as e:
        log.exception(f"Failed to process contact request: {str(e)}")
        return {
            "statusCode": 500,
            "body": {"error": "Failed to process your request. Please try again later."}
        }

def send_email(recipient: str, sender_email: str, subject: str, message_body: str) -> None:
    """
    Send an email using AWS SES
    """
    # Create a new SES client
    client = boto3.client('ses', region_name=os.environ.get('AWS_REGION_DEPLOYMENT', 'ap-southeast-2'))
    
    # Format the email body
    email_body = f"""
    New contact form submission:
    
    From: {sender_email}
    
    Message:
    {message_body}
    """
    
    try:
        response = client.send_email(
            Source=recipient,  # Must be a verified SES identity
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {
                    'Data': f"Contact Form: {subject}"
                },
                'Body': {
                    'Text': {
                        'Data': email_body
                    }
                }
            },
            ReplyToAddresses=[sender_email]
        )
        log.info(f"Email sent! Message ID: {response['MessageId']}")
    except ClientError as e:
        log.error(f"Failed to send email: {e.response['Error']['Message']}")
        raise Exception(f"Failed to send email: {e.response['Error']['Message']}") 