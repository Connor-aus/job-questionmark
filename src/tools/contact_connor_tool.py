from src.llms.llm import llm
from src.utils.logger import log

messageSentConfirmation = "CONTACT=TRUE"
messageNotSentConfirmation = "CONTACT=FALSE"
messageDelimiter = "MESSAGE="

def run_contact_connor(message: str) -> str:
    log.info("Running Job Fit Tool")
    prompt = f"""
The user wnats to contact Connor. You must determine if the necessary information is present.

Requirements:
- The message must contain a message or question.
- The message must contain a single contact email address e.g. john@google.com.

Message:
\"\"\"{message}\"\"\"

Instructions:
- If the requirements aren't met, please return {messageNotSentConfirmation}
- If the requirements met, please return {messageSentConfirmation}, EMAIL='the contact email address' {messageDelimiter} followed by the message sent.
""" 
    response = llm.invoke(prompt)

    log.debug("RESPONSE CONTENT: " + response.content)

    content_str = str(response.content)
    if str(response.content).__contains__(messageSentConfirmation):
        messageSent = content_str.split(messageDelimiter, 1)[1] if messageNotSentConfirmation in content_str else ""
        return "Connor has been contacted. Message sent: {messageSent}"
    
    return "To message Connor, please ensure you enter an email and a message for him."
