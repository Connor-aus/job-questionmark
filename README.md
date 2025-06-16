# Job-Questionmark

A serverless AI agent assistant built with LangChain, FastAPI, and AWS Lambda that helps evaluate job fit and answer questions about Connor McSweeney's professional experience.

## Overview

Job-Questionmark is an AI-powered assistant that provides the following capabilities:
- Analyze how well Connor fits a specific job description
- Answer questions about Connor's professional capabilities and experience
- Allow users to contact Connor with a message

The application is built as a serverless API using AWS Lambda and can be accessed via HTTP endpoints.

## Architecture

- **Framework**: FastAPI with Mangum adapter for AWS Lambda
- **AI/ML**: LangChain with Anthropic Claude models
- **Deployment**: AWS Lambda via Serverless Framework
- **Runtime**: Python 3.11

## Prerequisites

- Python 3.11+
- Node.js and npm (for Serverless Framework)
- AWS CLI configured with appropriate permissions
- Anthropic API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/job-questionmark.git
   cd job-questionmark
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```
   LLM_MODEL_ID=claude-3-5-sonnet-latest
   AGENT_ROLE_ARN=your-agent-role-arn
   ANTHROPIC_API_KEY=your-anthropic-api-key
   MAX_INPUT_LENGTH=4000
   LOGGING_LEVEL=INFO
   ```

## Local Development

Run the API locally with:
```bash
serverless offline
```

The API will be available at `http://localhost:3000/agent`

## Deployment

1. Install Serverless Framework if not already installed:
   ```bash
   npm install -g serverless
   ```

2. Deploy to AWS:
   ```bash
   serverless deploy
   ```

3. The deployment will output the endpoint URL for your API.

## API Usage

Send a POST request to the `/agent` endpoint:

```bash
curl -X POST https://your-api-endpoint/agent \
  -H "Content-Type: application/json" \
  -d '{"input": "What are Connor's skills in Python?"}'
```

## Project Structure

- `src/`: Source code
  - `main.py`: Entry point for the Lambda function
  - `agents/`: Agent definitions and configurations
  - `api/`: API endpoints and validation
  - `handlers/`: Request handlers
  - `llms/`: Language model configurations
  - `tools/`: Custom tools for the agent
  - `utils/`: Utility functions
- `infra/`: Infrastructure as code
- `tests/`: Unit and integration tests
- `serverless.yml`: Serverless Framework configuration

## License

This project is provided for public viewing and inspiration only. All rights are reserved by Connor McSweeney. No part of this repository may be copied, modified, or redistributed without explicit written permission.

© Connor McSweeney 2025. All rights reserved.

## Contact

Connor McSweeney - whoisconnor.net
