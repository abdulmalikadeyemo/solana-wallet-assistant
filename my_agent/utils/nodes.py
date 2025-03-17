from typing import Annotated, Dict, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from .state import AgentState, VALID_ACTIONS
from .prompts import chat_prompt, ROUTING_PROMPT, RESPONSE_PROMPT
from .tools import (
    get_wallet_address,
    get_wallet_balance,
    get_token_balance,
    get_all_token_balances,
    transfer_tokens
)

# Initialize the language model
model = ChatOpenAI(temperature=0)

def route_request(state: AgentState) -> Dict:
    """Determine the next action based on user input."""
    # Get the latest user message
    last_message = state["messages"][-1].content
    
    # Use the routing prompt to determine action
    response = model.invoke(ROUTING_PROMPT.format(
        input=last_message,
        context=str(state)
    ))
    
    action = response.content.strip()
    if action not in VALID_ACTIONS:
        action = "ERROR"
        
    return {"current_action": action}

def check_balance(state: AgentState) -> Dict:
    """Handle balance checking requests."""
    try:
        # Get wallet address first
        address_info = get_wallet_address()
        state["wallet_address"] = address_info["address"]
        
        # Get SOL balance
        sol_balance = get_wallet_balance()
        
        # Get all token balances
        token_balances = get_all_token_balances()
        
        return {
            "command_outcome": {
                "address": address_info,
                "sol_balance": sol_balance,
                "token_balances": token_balances
            },
            "error": None
        }
    except Exception as e:
        return {
            "command_outcome": None,
            "error": str(e)
        }

def send_tokens(state: AgentState) -> Dict:
    """Handle token transfer requests."""
    try:
        # Extract transfer details from the last message
        last_message = state["messages"][-1].content
        
        # Use LLM to extract transfer parameters
        extract_prompt = """Extract the transfer details from the following message:
        Message: {message}
        
        Return a JSON object with:
        - destination: destination address
        - amount: amount to send
        - token_mint: (optional) token mint address if not SOL
        
        If any required information is missing, return "MISSING_INFO"
        """
        
        response = model.invoke(extract_prompt.format(message=last_message))
        transfer_data = eval(response.content.strip())
        
        if transfer_data == "MISSING_INFO":
            return {
                "command_outcome": None,
                "error": "Missing transfer information. Please provide destination address and amount."
            }
            
        # Execute transfer
        result = transfer_tokens(transfer_data)
        
        return {
            "command_outcome": result,
            "error": None
        }
    except Exception as e:
        return {
            "command_outcome": None,
            "error": str(e)
        }

def generate_response(state: AgentState) -> Dict:
    """Generate a response based on the action results."""
    response = model.invoke(RESPONSE_PROMPT.format(
        context=str(state),
        results=state["command_outcome"]
    ))
    
    return {"messages": state["messages"] + [SystemMessage(content=response.content)]}

def handle_error(state: AgentState) -> Dict:
    """Handle any errors that occur during processing."""
    error_msg = state.get("error", "An unknown error occurred")
    
    response = f"I apologize, but I encountered an error: {error_msg}\n"
    response += "Please try again or rephrase your request."
    
    return {"messages": state["messages"] + [SystemMessage(content=response)]}