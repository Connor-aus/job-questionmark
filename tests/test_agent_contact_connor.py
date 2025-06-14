import env_setup
from src.agents.unified_agent import agent
from src.utils.print_agent_convo import print_agent_conversation

inputs = {"messages": [{"role": "user", "content": "Ask Connor when he is available for work. He can contact me at test@google.com"}]}
for chunk in agent.stream(inputs, stream_mode="updates"):
    print_agent_conversation(chunk)