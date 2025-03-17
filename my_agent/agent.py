from typing import Dict, TypedDict
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, END
from .utils.state import AgentState
from .utils.nodes import (
    route_request,
    check_balance,
    send_tokens,
    generate_response,
    handle_error
)

def create_agent() -> StateGraph:
    """Create the Solana wallet assistant agent workflow."""
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add the nodes
    workflow.add_node("route", route_request)
    workflow.add_node("check_balance", check_balance)
    workflow.add_node("send_tokens", send_tokens)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("handle_error", handle_error)
    
    # Add the edges
    # From route node
    workflow.add_edge("route", "check_balance", condition=lambda x: x["current_action"] == "CHECK_BALANCE")
    workflow.add_edge("route", "send_tokens", condition=lambda x: x["current_action"] == "SEND_TOKENS")
    workflow.add_edge("route", "handle_error", condition=lambda x: x["current_action"] == "ERROR")
    workflow.add_edge("route", END, condition=lambda x: x["current_action"] == "END")
    
    # From action nodes to response generation
    workflow.add_edge("check_balance", "generate_response")
    workflow.add_edge("send_tokens", "generate_response")
    
    # From error handler and response generator to end
    workflow.add_edge("handle_error", END)
    workflow.add_edge("generate_response", END)
    
    # Set entry point
    workflow.set_entry_point("route")
    
    return workflow.compile()

def create_initial_state() -> AgentState:
    """Create the initial state for the agent."""
    return AgentState(
        messages=[],
        current_action="",
        wallet_address="",
        command_outcome=None,
        error=None
    )

# Create the agent instance
agent = create_agent()

def process_input(user_input: str, state: Dict = None) -> Dict:
    """Process user input through the agent workflow.
    
    Args:
        user_input: The user's message
        state: Optional existing state to continue a conversation
        
    Returns:
        Dict: The final state after processing
    """
    # Initialize or use existing state
    if state is None:
        state = create_initial_state()
    
    # Add user input to messages
    state["messages"].append(HumanMessage(content=user_input))
    
    # Run the workflow
    final_state = agent.invoke(state)
    
    return final_state