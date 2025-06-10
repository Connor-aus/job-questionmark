# src/agents/llm.py

from langchain_aws import ChatBedrock

# Instantiate the LLM (Claude 3 Sonnet in Bedrock)
llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="ap-southeast-2"  # Change if using a different region
)
