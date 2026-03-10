CREATE TABLE IF NOT EXISTS agent_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS agent_memory (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    memory_key VARCHAR(100) NOT NULL,
    memory_value JSONB,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES agent_sessions(id),
    nlp_intent VARCHAR(50),
    task_description TEXT NOT NULL,
    reasoning_trace JSONB,
    final_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES task_history(id),
    workflow_name VARCHAR(100) NOT NULL,
    parameters JSONB,
    outcome JSONB,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scheduled_tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    cron_expression VARCHAR(50) NOT NULL,
    task_description TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
