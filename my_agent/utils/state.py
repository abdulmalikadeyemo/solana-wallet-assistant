from typing import List, Dict, TypedDict, Union
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Type definition for agent state."""
    messages: List[BaseMessage]  # Conversation history
    current_action: str  # Current action being performed
    wallet_address: str  # User's wallet address
    command_outcome: Union[Dict, str, None]  # Outcome of the last command
    error: Union[str, None]  # Any error messages

# Define valid next actions
VALID_ACTIONS = [
    "CHECK_BALANCE",
    "SEND_TOKENS",
    "ERROR",
    "END"
]