"""
state.py
Defines the shared State structure for the LangGraph workflow.
Task 2: State Management
"""

from typing import TypedDict, Optional


class SupportState(TypedDict):
    # Customer's name for memory lookup
    customer_name: str

    # The original customer query
    query: str

    # Classified department: Sales, Technical Support, Billing, Account
    intent: Optional[str]

    # Context retrieved from company documents (RAG)
    retrieved_context: Optional[str]

    # Past conversation history from SQLite
    memory_context: Optional[str]

    # Draft response from department agent
    draft_response: Optional[str]

    # Whether human approval is needed
    needs_approval: bool

    # Human decision: "approved" or "rejected"
    approval_status: Optional[str]

    # Final response sent to customer
    final_response: Optional[str]