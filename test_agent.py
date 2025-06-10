from dotenv import load_dotenv
from src.agents.llm import llm

load_dotenv()

import os

#from langchain_openai import ChatOpenAI
#from langchain_core.prompts import ChatPromptTemplate

print(os.getenv("AWS_PROFILE"))

# test_agent.py


# Send a test message to Claude 3 Sonnet
response = llm.invoke("Hello! What is your name? Please reply politely.")

print("LLM Response:")
print(response)