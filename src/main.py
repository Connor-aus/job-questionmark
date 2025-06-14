# src/api/main.py

import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utils.logger import log
from src.handlers.agent_handler import handle_agent_request
from mangum import Mangum


app = FastAPI()

@app.post("/agent")
async def invoke_agent(request: Request):
    try:
        body = await request.json()
        input_text = body.get("input", "")
        response = handle_agent_request(input_text)
        return {"response": response}
    except ValueError as ve:
        log.exception("Request failed: %s", str(ve))
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        log.exception("Request failed: %s", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})

# AWS Lambda handler using Mangum
def handler(event, context):
    # Handle direct Lambda invocations (not through API Gateway)
    if 'httpMethod' not in event and 'input' in event:
        try:
            input_text = event.get("input", "")
            response = handle_agent_request(input_text)
            return {"statusCode": 200, "body": json.dumps({"response": response})}
        except Exception as e:
            log.exception("Direct Lambda invocation failed: %s", str(e))
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    
    # Handle API Gateway events through Mangum
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)