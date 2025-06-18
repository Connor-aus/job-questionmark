import json
import re
import boto3
from src.utils.logger import log

lambda_client = boto3.client("lambda")

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

        payload = {
            "email": email,
            "subject": subject,
            "message": message
        }

        log.info("Invoking Lambda function job-questionmark-dev-contact")
        response = lambda_client.invoke(
            FunctionName="job-questionmark-dev-contact",
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )

        result_payload = response["Payload"].read()
        result = json.loads(result_payload)

        log.info(f"Success calling Lambda. Response: {result}")

        return Response(
            statusCode=200,
            body=json.dumps({
                "response": result
            })
        )

    except Exception as e:
        log.error(f"Error calling Lambda: {e}")
        return Response(
            statusCode=500,
            body=json.dumps({
                "response": "Internal server error"
            })
        )

# Optional: clean up parse_error_response if unused
def parse_error_response(response: dict) -> str:
    try:
        match = re.search(r'Value error, (.*?) \[type=value', response.get("error", ""))
        if match:
            return match.group(1)
    except Exception:
        pass
    return "Unknown error"