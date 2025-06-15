from src.utils.logger import log
from collections.abc import Callable

def print_agent_conversation(data, logger: Callable[[str], None] = log.info):
    """
    Print agent conversation data in a simple, readable format.
    """
    def safe_get(obj, key, default=None):
        """Safely get attribute from dict or object"""
        if isinstance(obj, dict):
            return obj.get(key, default)
        elif hasattr(obj, key):
            return getattr(obj, key, default)
        else:
            return default
    
    logger("AGENT CONVERSATION")
    
    total_tokens = 0
    
    # Print agent messages
    if "agent" in data:
        agent_data = data.get("agent", {})
        messages = safe_get(agent_data, "messages", [])
        
        for i, message in enumerate(messages, 1):
            logger(f"\n📤 AGENT MESSAGE {i}:")
            
            # Get content safely
            content = safe_get(message, "content")
            
            # Print text content
            if isinstance(content, list):
                for content_item in content:
                    content_type = safe_get(content_item, "type")
                    if content_type == "text":
                        logger(f"Text: {safe_get(content_item, 'text')}")
                    elif content_type == "tool_use":
                        logger(f"🔧 Tool Call: {safe_get(content_item, 'name')}")
                        logger(f"   Input: {safe_get(content_item, 'input')}")
            elif isinstance(content, str):
                logger(f"Text: {content}")
            
            # Print tokens
            usage_metadata = safe_get(message, "usage_metadata", {})
            tokens = safe_get(usage_metadata, "total_tokens", 0)
            if tokens:
                logger(f"Tokens: {tokens}")
                total_tokens += tokens
    
    # Print tool responses
    if "tools" in data:
        tools_data = data.get("tools", {})
        tool_messages = safe_get(tools_data, "messages", [])
        
        for i, tool_msg in enumerate(tool_messages, 1):
            logger(f"\n🔧 TOOL RESPONSE {i}:")
            logger(f"Tool: {safe_get(tool_msg, 'name')}")
            logger(f"Status: {safe_get(tool_msg, 'status', 'success')}")
            logger(f"Response: {safe_get(tool_msg, 'content')}")
    
    # Print follow-up agent responses
    if "agent_response" in data:
        agent_response_data = data.get("agent_response", {})
        response_messages = safe_get(agent_response_data, "messages", [])
        
        for i, message in enumerate(response_messages, 1):
            logger(f"\n📤 AGENT FOLLOW-UP {i}:")
            logger(f"Text: {safe_get(message, 'content')}")
            
            usage_metadata = safe_get(message, "usage_metadata", {})
            tokens = safe_get(usage_metadata, "total_tokens", 0)
            if tokens:
                logger(f"Tokens: {tokens}")
                total_tokens += tokens
    
    # Print summary
    logger(f"TOTAL TOKENS USED: {total_tokens}")
