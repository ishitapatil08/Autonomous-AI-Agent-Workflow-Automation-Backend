from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes.agent import agent_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Basic Config
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-agent-key")
app.config["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
app.config["CELERY_RESULT_BACKEND"] = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://agent_user:agent_password@localhost:5432/agent_db")

# Initialize Extensions
jwt = JWTManager(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Register Blueprints
app.register_blueprint(agent_bp, url_prefix='/agent')

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Agent API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
