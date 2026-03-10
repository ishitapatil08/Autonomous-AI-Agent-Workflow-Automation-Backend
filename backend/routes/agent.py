from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks.tasks import execute_agent_task_async
import uuid

agent_bp = Blueprint('agent_bp', __name__)

# In a real app we would use PostgreSQL for task states. Mocking here for simplicity until DB is fully wired.
__mock_task_db = {}

@agent_bp.route('/run', methods=['POST'])
# @jwt_required()
def run_agent_sync():
    """Runs the agent synchronously and returns the final result"""
    data = request.json
    instruction = data.get("instruction")
    if not instruction:
        return jsonify({"error": "Instruction is required."}), 400
    
    # user_id = get_jwt_identity()
    user_id = "test_user"
    
    # We will trigger the actual agent core logic here synchronously
    # For now, return a mock response
    trace = [
        {"thought": f"User asked to: {instruction}"},
        {"action": "HuggingFace NLP Tool Mock", "observation": "Mocked intent extracted"},
        {"thought": "Now triggering workflow"},
        {"action": "n8n Workflow Trigger Mock", "observation": "Workflow complete"}
    ]
    
    return jsonify({
        "status": "completed",
        "instruction": instruction,
        "result": "Task executed successfully",
        "trace": trace
    }), 200

@agent_bp.route('/run-async', methods=['POST'])
# @jwt_required()
def run_agent_async():
    """Starts the agent as a background Celery task and returns a task ID"""
    data = request.json
    instruction = data.get("instruction")
    if not instruction:
        return jsonify({"error": "Instruction is required."}), 400
    
    # user_id = get_jwt_identity()
    user_id = "test_user"
    
    # Using Celery Task
    task = execute_agent_task_async.delay(user_id, instruction)
    
    return jsonify({"task_id": task.id, "status": "queued"}), 202

@agent_bp.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Poll for the background task status"""
    task = execute_agent_task_async.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending execution"}
    elif task.state != 'FAILURE':
        response = {"state": task.state, "result": task.info.get('result', '') if type(task.info) == dict else task.info}
    else:
        response = {"state": task.state, "error": str(task.info)}
    return jsonify(response)

@agent_bp.route('/history', methods=['GET'])
# @jwt_required()
def get_history():
    """Returns the agent task execution history from PostgreSQL"""
    # This will query the `task_history` table.
    return jsonify({"history": []})
