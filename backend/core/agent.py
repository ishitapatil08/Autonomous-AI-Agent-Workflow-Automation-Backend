from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from core.tools import get_agent_tools

# We will use a mock LLM or basic fallback if API keys are missing, 
# but LangChain works best with a real LLM like OpenAI to do the ReAct reasoning.
# For demo purposes, if OPENAI_API_KEY is not set, we can simulate the agent trace.

import os

def run_react_agent(instruction: str):
    """
    Initializes the LangChain ReAct agent with 5 custom tools
    and runs the instruction through the agent reasoning loop.
    """
    
    # If we don't have an OpenAI key, we simulate the agent loop to 
    # demonstrate the architecture without paying for tokens.
    if not os.getenv("OPENAI_API_KEY"):
        return simulate_agent(instruction)
        
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    tools = get_agent_tools()
    
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
    )
    
    # In a real app we would capture the exact thought/action/observation trace from LangChain using callbacks.
    # For now, we'll run it and return the final string.
    try:
        final_answer = agent.run(instruction)
        trace = [{"action": "Agent Completed", "observation": final_answer}]
        return final_answer, trace
    except Exception as e:
        return f"Error: {e}", [{"error": str(e)}]


def simulate_agent(instruction: str):
    """Simulates a ReAct reasoning trace when no LLM is available."""
    print(f"Simulating Agent for instruction: {instruction}")
    
    trace = [
        {"thought": f"The user requested: '{instruction}'"},
        {"action": "HuggingFace NLP Tool", "observation": "Extracted intent: Data Summarization & Notification"},
        {"thought": "I need to summarize the data first."},
        {"action": "Document Processing Tool", "observation": "Processed and chunks extracted."},
        {"thought": "Now I will send this to n8n to notify the user."},
        {"action": "n8n Workflow Trigger Tool", "observation": "Successfully triggered n8n workflow webhook."}
    ]
    
    final_result = "Task execution completed via Agent Simulator (Mock Tools)."
    return final_result, trace
