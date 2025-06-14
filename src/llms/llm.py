# src/agents/llm.py
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = os.getenv("LLM_MODEL_ID", "claude-3-haiku-20240307")

print("LLM MODELID: " + MODEL_ID)

llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0.5,
    top_p=0.7
)