import boto3
import os
import json
from pydantic import BaseModel
from typing import List

# Ensure region is set via env
BEDROCK_REGION = os.getenv("AWS_REGION", "ap-southeast-2")

# Use Titan Text Lite ARN (latest public)
MODEL_ID = "amazon.titan-text-lite-v1"

# Create the Bedrock client (assumes AWS credentials are configured)
bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

# Request schema
class TextGenerationConfig(BaseModel):
    maxTokenCount: int = 3072
    stopSequences: List[str] = []
    temperature: float = 0.7
    topP: float = 0.9

class TitanPromptRequest(BaseModel):
    inputText: str
    textGenerationConfig: TextGenerationConfig = TextGenerationConfig()


def call_titan_llm(prompt: str) -> str:
    request_body = TitanPromptRequest(inputText=prompt).model_dump()

    print(str(request_body))

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(request_body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body.get("results", [{}])[0].get("outputText", "")


# Example usage (manual test):
if __name__ == "__main__":
    prompt = "Explain the role of a cloud architect in one paragraph."
    output = call_titan_llm(prompt)
    print("\n=== Titan Text Lite Output ===\n")
    print(output)