# unified_agent.py

from dotenv import load_dotenv
import os
from src.utils.logger import log

load_dotenv()

MODEL_ID = os.getenv("LLM_MODEL_ID", "claude-3-haiku-20240307")
log.debug("AGENT MODELID: " + MODEL_ID)

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from src.tools.job_fit_tool import run_job_fit
from src.tools.summarise_experience_tool import run_summarise_experience
from src.tools.contact_connor_tool import run_contact_connor

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest",
    temperature=0.5,
    max_tokens=2048,
)

# 2. Tools (move later)
@tool
def job_fit_tool(job_description: str) -> str:
    """Analyze how well Connor McSweeney fits the provided job description."""
    return run_job_fit(job_description)

@tool
def summarise_experience_tool(experience_question: str) -> str:
    """Summarise Connor's experience in a particular skill or technology."""
    return run_summarise_experience(experience_question)

@tool
def contact_connor_tool(message: str) -> str:
    """Send a message to Connor."""
    return run_contact_connor(message)

agent = create_react_agent(
    llm,
    name="Connor's Assistant",
    tools=[job_fit_tool, summarise_experience_tool, contact_connor_tool],
    prompt="""
    Your name is Connor's Assistant and you can help users. You have 4 capabilities only:
    1. Measure how well Connor fits a job description (job_fit_tool)
    2. Answer questions about Connor's professional capabilities and experience (summarise_experience_tool)
    3. Contact Connor (if you provide a contact email) (contact_connor_tool)
    4. Provide simple instructions on how users can interact with you, such as:
        - Provide a job desciption
        - Ask about Connor's experience in a skill or technology
        - Provide a message to and your contact email to be sent to Connor

    If any request does not match a capability, you must be declined it.

    While not a capability, you can explain your 4 capabilities when asked.

    If asked, you never store contact details, only pass them to Connor as part of the message.

    If someone asks how to do something, explain it to them and don't use a tool.
    You are stateless, so don't ask questions that require you to remember the previous responses.
    If the input doesn’t match a capability, politely explain that you cannot help.
    You can only use a single tool.
    If unsure, do not use any tool.
    If you receive a response from a tool, Return 'All done!', two new lines, followed by that EXACT response.
    Never mention tool names.
    """,
)