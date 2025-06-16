# src/api/main.py

try:
    import sys
    print("Python sys.path:", sys.path)

    from src.utils.logger import log
    import json
    from fastapi import FastAPI
    from fastapi import Request
    from fastapi.responses import JSONResponse
    from src.handlers.agent_handler import handle_agent_request
    from src.handlers.contact_handler import handle_contact_request
    from mangum import Mangum

    app = FastAPI()

    @app.post("/agent")
    async def invoke_agent(request: Request):
        try:
            body = await request.json()
            input_text = body.get("input", "")
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
        if 'httpMethod' not in event and 'input' in event:
            try:
                input_text = event.get("input", "")
                result = handle_agent_request(input_text)
                
                if result["success"]:
                    return {"statusCode": 200, "body": json.dumps({"response": result["response"]})}
                else:
                    status_code = 400 if "validation" in result.get("error", "").lower() else 500
                    return {"statusCode": status_code, "body": json.dumps({"error": result["error"]})}
            except Exception as e:
                log.exception("Unhandled exception in direct Lambda invocation: %s", str(e))
                return {
                    "statusCode": 500, 
                    "body": json.dumps({"error": "An unexpected error occurred. Please try again later."})
                }
        
        return asgi_handler(event, context)

except Exception as e:
    import traceback
    print("Fatal error upon startup:", e)
    traceback.print_exc()
    raise
