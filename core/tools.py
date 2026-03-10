from langchain.tools import Tool
import requests
import json

# --- 1. n8n Workflow Trigger Tool ---
def n8n_trigger(query: str) -> str:
    """
    Triggers an n8n workflow. The agent passes a JSON string containing the workflow details.
    Mock implementation: we just echo the JSON back. The real one would POST to a Webhook URL.
    """
    try:
        data = json.loads(query)
        # Real implementation: 
        # response = requests.post("http://localhost:5678/webhook/agent-trigger", json=data)
        # return response.json()
        return f"Successfully triggered workflow '{data.get('workflow')}' with data: {data.get('parameters')}"
    except Exception as e:
        return f"Failed to trigger n8n: {e}. Ensure query is valid JSON."

# --- 2. HuggingFace NLP Tool (Mocked) ---
def hf_nlp(query: str) -> str:
    """
    Mock HuggingFace integration. Categorizes intents or extracts entities.
    Real implementation uses requests to HF Inference endpoints or local pipeline.
    """
    if "complain" in query.lower() or "issue" in query.lower():
        return "Intent: Support Ticket. Entities: User Issue"
    return "Intent: General Query"

# --- 3. PostgreSQL Query Tool ---
def db_query(query: str) -> str:
    """
    Allows the agent to safely read from the database using SQL.
    Mock implementation to prevent actual db truncation during dev.
    """
    # Real use case requires SQLAlchemy engine connection here.
    if "select" in query.lower():
        return "[{'id': 1, 'metric': 100}]"
    return "Read-only mode enabled for safety."

# --- 4. Document Processing Tool ---
def doc_processor(filepath: str) -> str:
    """
    Extracts text from PDF/CSV.
    """
    return f"Extracted 500 words of text from {filepath}"

# --- 5. Web Search Tool ---
def web_search(query: str) -> str:
    """
    Mocks Tavily/SerpAPI search results.
    """
    return f"Search results for '{query}': Found 5 relevant articles."

def get_agent_tools() -> list[Tool]:
    """Returns the list of custom tools for the LangChain agent."""
    return [
        Tool(
            name="n8n_workflow_trigger",
            func=n8n_trigger,
            description="Use this to trigger external workflows (Email, Jira, Slack). Input should be a JSON string with 'workflow' and 'parameters'."
        ),
        Tool(
            name="huggingface_nlp",
            func=hf_nlp,
            description="Use for summarizing text, entity extraction, or intent classification. Input is raw text."
        ),
        Tool(
            name="postgres_query",
            func=db_query,
            description="Use to query the database. Input is a raw SQL SELECT query."
        ),
        Tool(
            name="document_processor",
            func=doc_processor,
            description="Use to extract text from a document. Input is the file path."
        ),
        Tool(
            name="web_search",
            func=web_search,
            description="Use to search the web for missing information. Input is a search query string."
        )
    ]
