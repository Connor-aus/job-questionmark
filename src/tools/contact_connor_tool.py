from src.llms.llm import llm
from src.utils.logger import log
from src.utils.send_email import send_email

validationFailedMessage = "CONTACT-IS-NOT-A-GO"

def run_contact_connor(message: str) -> str:
    try:
        log.info("Running contact_connor_tool")
        prompt = f"""
    The user wnats to contact Connor. You must determine if the necessary information is present.

    Requirements:
    - The message must contain a message or question.
    - The message must contain a single contact email address e.g. john@google.com.

    Message:
    \"\"\"{message}\"\"\"

    Instructions:
    - If the requirements aren't met, please return '{validationFailedMessage}'.
    - If the requirements met, please return a only aJSON object with the following fields: EMAIL='contact email provide', MESSAGE='the intended message', SUBJECT='a short summary based on the message content'.
    """ 
        response = llm.invoke(prompt)

        log.info("Summary of contact_connor_tool response: " + response.content)

        content_str = str(response.content)
        if not str(response.content).__contains__(validationFailedMessage):
            send_email_response = send_email(content_str)

            log.info("Send email attempt response: " + str(send_email_response))

            if send_email_response.statusCode == 200:
                return "Your message has been sent to Connor. He will get back to you as soon as possible."
            else:
                return "Failed to contact Connor. Reason: " + send_email_response.body.get("response", "Unknown error")

        log.info("Failed to contact Connor")
        return "To message Connor, please ensure you enter an email and a message for him."

    except Exception as e:
        log.error(f"Error running Contact Connor Tool: {e}")
        return "Failed to contact Connor. Please try again."