"""
graph.py
Builds the LangGraph workflow.
Tasks 1, 4
"""

from langgraph.graph import StateGraph, END
from state import SupportState
import memory
import agents


def classify_node(state: SupportState) -> dict:
    intent = agents.classify_intent(state["query"])
    print(f"[Intent Classifier] -> {intent}")
    return {"intent": intent}


def memory_node(state: SupportState) -> dict:
    history = memory.get_history(state["customer_name"])
    print(f"[Memory Lookup] -> {'Found history' if history else 'No prior history'}")
    return {"memory_context": history}


def retrieve_node(state: SupportState) -> dict:
    import os
    query_words = state["query"].lower().split()
    context_parts = []
    kb_path = "knowledge_base"
    for filename in os.listdir(kb_path):
        if filename.endswith(".txt"):
            with open(os.path.join(kb_path, filename), "r") as f:
                content = f.read()
                lines = [l for l in content.split("\n") if any(w in l.lower() for w in query_words)]
                if lines:
                    context_parts.append("\n".join(lines[:8]))
    context = "\n\n".join(context_parts)[:1500] or "No relevant info found."
    print(f"[RAG Retrieval] -> Retrieved {len(context)} characters")
    return {"retrieved_context": context}


def department_node(state: SupportState) -> dict:
    intent = state["intent"]
    query = state["query"]
    context = state.get("retrieved_context", "")
    mem = state.get("memory_context", "")

    if intent == "Sales":
        draft = agents.sales_agent(query, context, mem)
    elif intent == "Technical Support":
        draft = agents.technical_support_agent(query, context, mem)
    elif intent == "Billing":
        draft = agents.billing_agent(query, context, mem)
    else:
        draft = agents.account_agent(query, context, mem)

    needs_approval = agents.needs_human_approval(query)
    print(f"[{intent} Agent] -> Draft created. Needs approval: {needs_approval}")
    return {"draft_response": draft, "needs_approval": needs_approval}


def human_approval_node(state: SupportState) -> dict:
    print("\n" + "="*60)
    print("  HUMAN-IN-THE-LOOP APPROVAL REQUIRED")
    print("="*60)
    print(f"  Customer: {state['customer_name']}")
    print(f"  Query: {state['query']}")
    print(f"  Draft: {state['draft_response']}")
    decision = input("\n  Approve this response? (yes/no): ").strip().lower()
    status = "approved" if decision == "yes" else "rejected"
    print(f"[Human Supervisor] -> {status}")
    return {"approval_status": status}


def supervisor_node(state: SupportState) -> dict:
    if state.get("approval_status") == "rejected":
        final = "We're sorry, but this request requires further review. A representative will contact you shortly."
    else:
        final = agents.supervisor_review(state["query"], state["draft_response"])
    print(f"[Supervisor Review] -> Final response ready")
    return {"final_response": final}


def save_memory_node(state: SupportState) -> dict:
    memory.save_interaction(
        customer_name=state["customer_name"],
        query=state["query"],
        intent=state["intent"],
        response=state["final_response"],
    )
    print(f"[Memory Saved] -> Interaction saved for {state['customer_name']}")
    return {}


def route_after_department(state: SupportState) -> str:
    return "human_approval" if state.get("needs_approval") else "supervisor"


def build_graph():
    graph = StateGraph(SupportState)

    graph.add_node("classify", classify_node)
    graph.add_node("memory_lookup", memory_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("department", department_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("save_memory", save_memory_node)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "memory_lookup")
    graph.add_edge("memory_lookup", "retrieve")
    graph.add_edge("retrieve", "department")
    graph.add_conditional_edges(
        "department",
        route_after_department,
        {"human_approval": "human_approval", "supervisor": "supervisor"}
    )
    graph.add_edge("human_approval", "supervisor")
    graph.add_edge("supervisor", "save_memory")
    graph.add_edge("save_memory", END)

    return graph.compile()