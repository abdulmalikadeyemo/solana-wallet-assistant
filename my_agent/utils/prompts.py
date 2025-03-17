from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# System prompt that defines the agent's behavior
SYSTEM_PROMPT = """You are a helpful Solana wallet assistant that helps users check their balances and send tokens.
You have access to the following capabilities:

1. Check wallet balances:
   - Get wallet address
   - Get SOL balance
   - Get balance of specific tokens
   - Get all token balances

2. Send tokens:
   - Transfer SOL or other tokens to specified addresses

Always verify you have all required information before performing transfers.
For transfers, you must confirm:
- Destination address
- Amount to send
- Token type (SOL or token mint address)

If you encounter errors, explain them clearly to the user and suggest solutions.

Never make up wallet addresses or token amounts - only use verified information from the tools."""

# Create the chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])

# Prompt for help in routing user requests
ROUTING_PROMPT = """Based on the user's request, determine the next appropriate action:

Options:
- CHECK_BALANCE: For any balance checking requests
- SEND_TOKENS: For token transfer requests
- ERROR: If the request is unclear or there's an error
- END: If the request has been completed

Current request: {input}
Current context: {context}

Return only one of the above options."""

# Prompt for formatting responses
RESPONSE_PROMPT = """Given the action results and context, formulate a clear and helpful response to the user.

Context: {context}
Action Results: {results}

Format the response to be:
1. Clear and concise
2. Include relevant numerical values
3. Highlight any important information
4. Suggest next steps if appropriate

Response:"""