"""
agents.py
Intent classifier, department agents, and supervisor agent.
Tasks 3, 5, 9
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)


# Task 3: Intent Classification
def classify_intent(query: str) -> str:
    prompt = f"""Classify the customer query into EXACTLY ONE category:
Sales, Technical Support, Billing, Account

Rules:
- Sales: pricing, plans, features, trial
- Technical Support: errors, crashes, login issues, installation
- Billing: invoices, payments, refunds
- Account: password reset, profile, account settings

Query: "{query}"

Reply with ONLY the category name, nothing else."""

    response = llm.invoke(prompt)
    intent = response.content.strip()

    for category in ["Sales", "Technical Support", "Billing", "Account"]:
        if category.lower() in intent.lower():
            return category
    return "Technical Support"


# Task 5: Department Agents
def _run_agent(department: str, query: str, context: str, memory: str) -> str:
    prompt = f"""You are a {department} support agent at ABC Technologies.

Company Information:
{context}

Customer History:
{memory if memory else "No prior history."}

Customer Query: "{query}"

Write a helpful, professional response in 3-5 sentences."""

    response = llm.invoke(prompt)
    return response.content.strip()


def sales_agent(query, context, memory):
    return _run_agent("Sales", query, context, memory)

def technical_support_agent(query, context, memory):
    return _run_agent("Technical Support", query, context, memory)

def billing_agent(query, context, memory):
    return _run_agent("Billing", query, context, memory)

def account_agent(query, context, memory):
    return _run_agent("Account", query, context, memory)


# Task 8: Human-in-the-loop check
RISKY_KEYWORDS = [
    "refund", "cancel", "cancellation", "close my account",
    "compensation", "escalate", "manager"
]

def needs_human_approval(query: str) -> bool:
    return any(keyword in query.lower() for keyword in RISKY_KEYWORDS)


# Task 9: Supervisor Agent
def supervisor_review(query: str, draft: str) -> str:
    prompt = f"""You are a quality-control supervisor at ABC Technologies.
Review and improve this draft response for tone, clarity, and professionalism.
Keep it 3-5 sentences. Return ONLY the final response text.

Customer Query: "{query}"
Draft Response: "{draft}"
"""
    response = llm.invoke(prompt)
    return response.content.strip()