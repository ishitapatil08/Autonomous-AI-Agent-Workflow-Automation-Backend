# Autonomous AI Agent Workflow Automation Backend

This project is a production-grade backend system where a **LangChain ReAct Agent** acts as an intelligent brain. It reasons through complex multi-step tasks, selects the right tools (including HuggingFace NLP and Web Search), and delegates execution to external integrations (like n8n workflows). Users can describe tasks in plain English, and the system autonomously plans, executes, and delivers results.

It comes with a modern, glassmorphic **React Dashboard (Vite)** to visualize the Agent's "Thought -> Action -> Observation" execution trace in real-time.

---

## 🌟 Key Features

- **LangChain ReAct Agent Core**: The reasoning engine that thinks out loud and decides which tools to use based on the user's natural language request.
- **Custom Tool Belt**:
  - `n8n Workflow Trigger`: Fires webhook events to external workflow automation platforms.
  - `HuggingFace NLP Tool`: Runs intent detection, summarization, and entity extraction.
  - `PostgreSQL Query Tool`: Safe database interactions.
  - `Document Processing Tool`: Extracts text from provided files (PDF/CSV).
  - `Web Search Tool`: Queries real-world data to supplement the agent's knowledge.
- **Flask REST API**: Features endpoints for synchronous (`/agent/run`) and asynchronous (`/agent/run-async`) task execution, protected with CORS and `Flask-Limiter` for rate limiting.
- **Asynchronous Execution**: Integrates **Celery** and **Redis** for executing long-running agent tasks in background workers without blocking the main API thread.
- **Agent Memory System**: Uses **PostgreSQL** to store task history, session data, and the complete ReAct reasoning traces as JSONB.
- **Beautiful Dashboard Interface**: A React application built with Vite, styled with modern CSS and glassmorphism, offering a chat-like interface to trigger tasks and view live execution logs.

---

## 🏗 System Architecture

1. **User Input** → React Frontend Dashboard
2. **API Gateway** → Flask REST API (Handles Auth & Rate Limiting)
3. **Task Queue** → Celery Worker & Redis Broker (For async long-running tasks)
4. **Agent Brain** → LangChain ReAct Agent Loop
5. **Tool Execution** → Python functions (Mock HuggingFace, n8n webhooks, DB queries)
6. **Data Storage** → PostgreSQL (Stores execution traces and memory)

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.8+
- Node.js & npm
- Docker Desktop (for Postgres, Redis, and n8n)
- Git

### 1. Database & Infrastructure Setup
Start the required background services using Docker Compose from the root directory:
```bash
docker-compose up -d
```
*(This starts PostgreSQL on port 5432, Redis on port 6379, and n8n on port 5678)*.

### 2. Backend Setup (Flask & Celery)
Open a terminal and navigate to the `backend` directory:
```bash
cd backend

# Create and activate a Virtual Environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask API
python app.py
```
*The Backend API will run on `http://localhost:5000`.*

### 3. Frontend Setup (React/Vite)
Open a new terminal window and navigate to the `frontend` directory:
```bash
cd frontend

# Install Node modules
npm install

# Start the development server
npm run dev -- --host 127.0.0.1 --port 5174
```
*The Dashboard will be running at `http://127.0.0.1:5174`.*

---

## 🧪 Testing the Agent

1. Open the UI at [http://127.0.0.1:5174/](http://127.0.0.1:5174/)
2. In the "New Task Execution" panel, enter a complex prompt. For example:
   > *"Summarize all customer complaints from this week, group by category, create a Jira ticket for each group, and email the report to the manager"*
3. Click **Execute Task**.
4. Watch the **Agent Trace & Output** panel populate in real-time as the LangChain Agent thinks, takes action using the mock tools, observes the output, and formulates a final answer!

---

## 📝 Technologies Used
- **Backend:** Python, Flask, Celery, Redis, SQLAlchemy, LangChain
- **Frontend:** React, Vite, CSS (Glassmorphism)
- **Infrastructure:** Docker Compose, PostgreSQL
- **AI/ML (Simulated):** HuggingFace Transformers, OpenAI (via LangChain interfaces)
