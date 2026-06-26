# AI-Powered Customer Support Automation System

An agentic AI system built with LangGraph that automatically classifies customer support queries, routes them to the appropriate department, retrieves relevant information from company documents (RAG), remembers past conversations, and pauses for human approval on sensitive requests.

## Tech Stack
- Python 3.x
- LangGraph — workflow orchestration
- LangChain — LLM integration
- Groq (Llama 3.3 70B) — free LLM inference
- SQLite — conversation memory
- RAG — knowledge base retrieval

## Project Structure
- state.py — Shared LangGraph state (Task 2)
- memory.py — SQLite memory (Task 7)
- agents.py — Intent classifier + department agents (Tasks 3, 5, 9)
- graph.py — LangGraph workflow (Tasks 1, 4, 8)
- main.py — Demo with 5 queries (Task 10)
- knowledge_base/ — Company documents for RAG (Task 6)

## Setup
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. Add your Groq API key in `.env`: `GROQ_API_KEY=your-key`
6. Run: `python main.py`

## Demo Queries
1. Pricing plans (Sales)
2. Forgot password (Account)
3. App crash on upload (Technical Support)
4. Refund request (Billing — Human Approval required)
5. Previous issue recall (Memory Recall)

## Author
Varshitha Maddinala — IBM Agentic AI Course Assignment 2