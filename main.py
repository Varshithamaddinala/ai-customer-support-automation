"""
main.py
Runs the 5 demo queries for the Customer Support AI System.
Task 10: System Demonstration
"""

from memory import init_db
from graph import build_graph

DEMO_QUERIES = [
    {"customer_name": "Alice", "query": "What are the pricing plans available for your software?"},
    {"customer_name": "Bob", "query": "I forgot my account password."},
    {"customer_name": "Carol", "query": "My application crashes whenever I upload a file."},
    {"customer_name": "David", "query": "I need a refund for my annual subscription."},
    {"customer_name": "David", "query": "What was my previous support issue?"},
]

LABELS = ["Sales", "Account", "Technical Support", "Billing/Refund (Human Approval)", "Memory Recall"]


def run_demo():
    print("Initializing database...")
    init_db()

    app = build_graph()

    for i, (item, label) in enumerate(zip(DEMO_QUERIES, LABELS), start=1):
        print("\n" + "#"*70)
        print(f"  DEMO QUERY {i} — {label}")
        print(f"  Customer: {item['customer_name']}")
        print(f"  Query: {item['query']}")
        print("#"*70)

        initial_state = {
            "customer_name": item["customer_name"],
            "query": item["query"],
            "intent": None,
            "retrieved_context": None,
            "memory_context": None,
            "draft_response": None,
            "needs_approval": False,
            "approval_status": None,
            "final_response": None,
        }

        result = app.invoke(initial_state)

        print("\n--- FINAL RESPONSE TO CUSTOMER ---")
        print(result["final_response"])
        print()


if __name__ == "__main__":
    run_demo()