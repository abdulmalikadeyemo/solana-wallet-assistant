import requests
from typing import Dict, Any
from langchain_core.tools import tool

BASE_URL = "https://sonic-agent-kit.onrender.com"

@tool
def get_wallet_address() -> Dict:
    """Retrieves the current wallet address.
    
    Returns:
        dict: A dictionary containing the wallet address information
    """
    endpoint = f"{BASE_URL}/api/wallet/address"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error getting wallet address: {e}")

@tool
def get_wallet_balance() -> Dict:
    """Retrieves the current wallet's SOL balance.
    
    Returns:
        dict: A dictionary containing the wallet's SOL balance information
    """
    endpoint = f"{BASE_URL}/api/wallet/balance"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error getting wallet balance: {e}")

@tool
def get_token_balance(mint_address: str) -> Dict:
    """Get token balance for a specific token mint.
    
    Args:
        mint_address: The mint address of the token to check
        
    Returns:
        dict: A dictionary containing the token balance information
    """
    endpoint = f"{BASE_URL}/api/token/balance/{mint_address}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error getting token balance for {mint_address}: {e}")

@tool
def get_all_token_balances() -> Dict:
    """Get balances for all tokens in the wallet.
    
    Returns:
        dict: A dictionary containing all token balance information
    """
    endpoint = f"{BASE_URL}/api/token/balances"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error getting all token balances: {e}")

@tool
def transfer_tokens(transfer_data: Dict[str, Any]) -> Dict:
    """Transfer tokens to another wallet.
    
    Args:
        transfer_data: Dictionary containing:
            - destination: Destination wallet address
            - amount: Amount to transfer
            - token_mint: (Optional) Token mint address for SPL tokens. If not provided, transfers SOL
            
    Returns:
        dict: A dictionary containing the transfer confirmation
    """
    endpoint = f"{BASE_URL}/api/token/transfer"
    try:
        response = requests.post(endpoint, json=transfer_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error transferring tokens: {e}")