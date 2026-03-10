import os
from celery import Celery
import time

celery_app = Celery("agent_tasks",
                    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
                    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"))

@celery_app.task(bind=True)
def execute_agent_task_async(self, user_id, instruction):
    """
    Background task to run the ReAct Agent logic.
    Actual LangChain code would go here or be imported from core.agent
    """
    # Import inside task to avoid circular imports
    from core.agent import run_react_agent
    
    # Update task state to running
    self.update_state(state='PROGRESS', meta={'progress': 10, 'status': 'Starting Agent reasoning...'})
    
    # Run the actual LangChain Loop
    try:
        result, trace = run_react_agent(instruction)
        
        # Save to DB here ideally:
        # save_task_history(user_id, instruction, result, trace)
        
        return {"result": result, "trace": trace, "status": "Success"}
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise e
