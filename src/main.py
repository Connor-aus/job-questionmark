# src/api/main.py

try:
    import sys
    print("Python sys.path:", sys.path)

    from src.utils.logger import log
    import json
    import os
    from fastapi import FastAPI
    from fastapi import Request
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from mangum import Mangum
    from src.handlers.agent_handler import handle_agent_request
    from src.handlers.contact_handler import handle_contact_request


    app = FastAPI()

    origins = [
        os.getenv("DOMAIN_NAME")
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/agent")
    async def invoke_agent(request: Request):
        log.info("Received agent request")
        try:
            body = await request.json()
            input_text = body.get("message", "")
            result = handle_agent_request(input_text)
            
            if result["success"]:
                return {"response": result["response"]}
            else:
                return JSONResponse(
                    status_code=400 if "validation" in result.get("error", "").lower() else 500,
                    content={"error": result["error"]}
                )
        except Exception as e:
            log.exception("Unhandled exception in agent endpoint: %s", str(e))
            return JSONResponse(
                status_code=500, 
                content={"error": "An unexpected error occurred. Please try again later."}
            )

    @app.post("/contact")
    async def contact_form(request: Request):
        log.info("Received contact form request")
        try:
            body = await request.json()
            result = handle_contact_request(body)
            return JSONResponse(
                status_code=result["statusCode"],
                content=result["body"]
            )
        except Exception as e:
            log.exception("Unhandled exception in contact endpoint: %s", str(e))
            return JSONResponse(
                status_code=500, 
                content={"error": "An unexpected error occurred. Please try again later."}
            )

    asgi_handler = Mangum(app)

    def handler(event, context):
        log.info("Received event: %s", event)
        
        # Handle direct Lambda invocations
        if 'httpMethod' not in event:
            
            # Handle contact requests (direct invocation with email, subject, message)
            if 'email' in event and 'subject' in event and 'message' in event:
                try:
                    result = handle_contact_request(event)
                    return {
                        "statusCode": result["statusCode"],
                        "body": json.dumps(result["body"])
                    }
                except Exception as e:
                    log.exception("Unhandled exception in direct Lambda contact invocation: %s", str(e))
                    return {
                        "statusCode": 500, 
                        "body": json.dumps({"error": "An unexpected error occurred. Please try again later."})
                    }
                
            # Handle agent requests (direct invocation with message)
            elif 'message' in event:
                try:
                    input_text = event.get("message", "")
                    result = handle_agent_request(input_text)
                    
                    if result["success"]:
                        return {"statusCode": 200, "body": json.dumps({"response": result["response"]})}
                    else:
                        status_code = 400 if "validation" in result.get("error", "").lower() else 500
                        return {"statusCode": status_code, "body": json.dumps({"error": result["error"]})}
                except Exception as e:
                    log.exception("Unhandled exception in direct Lambda agent invocation: %s", str(e))
                    return {
                        "statusCode": 500, 
                        "body": json.dumps({"error": "An unexpected error occurred. Please try again later."})
                    }
            
        
        # Handle API Gateway requests
        return asgi_handler(event, context)

except Exception as e:
    import traceback
    print("Fatal error upon startup:", e)
    traceback.print_exc()
    raise