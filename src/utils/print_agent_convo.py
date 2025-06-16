from src.utils.logger import log
import json
from typing import Callable

def print_agent_conversation(data, logger: Callable[[str], None] = log.info):
    def safe_get(obj, key, default=None):
        if isinstance(obj, dict):
            return obj.get(key, default)
        elif hasattr(obj, key):
            return getattr(obj, key, default)
        else:
            return default

    logger("AGENT CONVERSATION")

    total_tokens = 0
    agent_messages = safe_get(data.get("agent", {}), "messages", [])
    tool_responses = {i: tool for i, tool in enumerate(safe_get(data.get("tools", {}), "messages", []))}
    agent_followups = {i: msg for i, msg in enumerate(safe_get(data.get("agent_response", {}), "messages", []))}

    for i, message in enumerate(agent_messages):
        message_obj = {
            "agent_message_index": i + 1,
            "agent_message": {},
            "tool_response": {},
            "agent_followup": {}
        }

        content = safe_get(message, "content")
        message_content = []

        if isinstance(content, list):
            for content_item in content:
                content_type = safe_get(content_item, "type")
                if content_type == "text":
                    message_content.append({
                        "type": "text",
                        "text": safe_get(content_item, "text")
                    })
                elif content_type == "tool_use":
                    message_content.append({
                        "type": "tool_use",
                        "name": safe_get(content_item, "name"),
                        "input": safe_get(content_item, "input")
                    })
        elif isinstance(content, str):
            message_content.append({
                "type": "text",
                "text": content
            })

        message_obj["agent_message"]["content"] = message_content

        tokens = safe_get(safe_get(message, "usage_metadata", {}), "total_tokens", 0)
        message_obj["agent_message"]["tokens"] = tokens
        total_tokens += tokens

        # Tool response
        if i in tool_responses:
            tool = tool_responses[i]
            message_obj["tool_response"] = {
                "name": safe_get(tool, "name"),
                "status": safe_get(tool, "status", "success"),
                "response": safe_get(tool, "content")
            }

        # Agent follow-up
        if i in agent_followups:
            followup = agent_followups[i]
            message_obj["agent_followup"] = {
                "text": safe_get(followup, "content"),
                "tokens": safe_get(safe_get(followup, "usage_metadata", {}), "total_tokens", 0)
            }
            total_tokens += message_obj["agent_followup"]["tokens"]

        logger(json.dumps(message_obj, indent=2))

    logger(f"TOTAL TOKENS USED: {total_tokens}")
