import env_setup
from src.llms.llm import llm
from src.utils.print_agent_convo import print_agent_conversation

import os
from dotenv import load_dotenv

load_dotenv()

print("ANTHROPIC_API_KEY: " + os.getenv("ANTHROPIC_API_KEY"))

question = "Hello"
response = llm.invoke({"input": question})

print("Response:")
print(response)