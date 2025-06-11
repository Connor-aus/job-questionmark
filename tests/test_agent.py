import env_setup
from src.agents.llm import call_titan_llm

#from langchain_openai import ChatOpenAI
#from langchain_core.prompts import ChatPromptTemplate

print(env_setup.os.getenv("AWS_PROFILE"))

# Send a test message to Titan Text Lite via boto3
prompt = "Hello! What is your name? Please reply politely."

response = call_titan_llm(prompt)

print("LLM Response:")
print(response)