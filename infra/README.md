# Infrastructure for job-questionmark

This directory contains the infrastructure-as-code configuration for deploying the FastAPI app to AWS Lambda using the Serverless Framework.

## Deployment

1. Install the Serverless Framework:
   ```bash
   npm install -g serverless
   ```
2. Deploy to AWS:
   ```bash
   sls deploy
   ```

## serverless.yml
- Packages the FastAPI app (with Mangum adapter) as a Lambda function.
- Exposes the `/agent` POST endpoint via API Gateway HTTP API.
- Uses Python 3.11 runtime.
- Loads environment variables from the `environment` section or `.env` file.

See the main project README for more details. 