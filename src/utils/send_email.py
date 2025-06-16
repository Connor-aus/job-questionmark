from src.utils.logger import log
import json
import os
import requests
import re

API_BASE_URL = os.getenv("APP_API_BASE_URL", "https://api-dev.whoisconnor.net/")
X_API_KEY_DEV = os.getenv("APP_API_KEY_DEV")

class Response:
    def __init__(self, statusCode: int = 500, body: str = "Unknown error"):
        self.statusCode = statusCode
        self.body = body

def send_email(email_content: str) -> Response:
    try:
        log.info(f"Attempting to send email. Parsing email content: {email_content}")

        email_content_json = json.loads(email_content)
        email = email_content_json.get("EMAIL")
        subject = email_content_json.get("SUBJECT")
        message = email_content_json.get("MESSAGE")

        log.info(f"Successfully parsed email content. Email: {email}, Subject: {subject}, Message: {message}")

        # Payload to send to Lambda B
        payload = {
            "email": email,
            "subject": subject,
            "message": message
        }

        # Headers for the HTTP request (e.g., shared secret auth)
        headers = {
            "Content-Type": "application/json",
            "x-api-key": X_API_KEY_DEV
        }

        # Make the HTTP POST request to the other Lambda
        response = requests.post(
            f"{API_BASE_URL}/contact",
            data=json.dumps(payload),
            headers=headers,
            timeout=10
        )

        response.raise_for_status()  # Raises error for 4xx/5xx

        log.info(f"Success calling Contact API. Response: {response.json()}")

        return Response(
            statusCode=200,
            body=json.dumps({
                "response": response.json()
            })
        )

    except Exception as e:
        log.error(f"Error calling Contact Connor: {e}")
        return Response(
            statusCode=500,
            body=json.dumps({
                "response": parse_error_response(response)
            })
        )

def parse_error_response(response: requests.Response) -> str:
    try:
        match = re.search(r'Value error, (.*?) \[type=value', response['error'])
        if match:
            message = match.group(1)
            return str(message)
        else:
            return Response(
                statusCode=500,
                body=json.dumps({
                    "response": "Unknown error"
                })
            )
    except:
        return Response(
                statusCode=500,
                body=json.dumps({
                    "response": "Unknown error"
                })
            )