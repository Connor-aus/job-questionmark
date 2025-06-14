from langchain_core.messages import AIMessage
from src.agents.unified_agent import agent
from src.utils.logger import log
from src.api.validation import validate_input
from src.utils.print_agent_convo import print_agent_conversation

def handle_agent_request(input_text: str) -> str:
    log.info("Validating and processing agent request")

    try:
        validate_input(input_text)
        log.info("Agent request validated")        

        agent_inputs = {"messages": [{"role": "user", "content": input_text}]}
        log.info(f"Sending message to agent: {input_text}")
        
        final_response = None

        for chunk in agent.stream(agent_inputs, stream_mode="updates"):
            print_agent_conversation(chunk)
            # log.debug("Chunk received: %s", chunk)

            if "agent" in chunk and "messages" in chunk["agent"]:
                for msg in chunk["agent"]["messages"]:
                    if isinstance(msg, AIMessage):
                        final_response = msg.content

        if final_response is None:
            raise RuntimeError("Agent did not return a final response.")

        log.info(f"Final agent response: {final_response}")
        return final_response

    except ValueError as ve:
        log.warning("Validation error: %s", str(ve))
        raise
    except Exception:
        log.exception("Agent invocation failed")
        raise RuntimeError(f"Agent invocation failed")