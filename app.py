"""
app.py — Flask entry point for the Outing Planner Agent web UI.
"""

from flask import Flask, render_template, request, jsonify, session
import uuid
from agent.orchestrator import OutingAgent

app = Flask(__name__, template_folder="ui/templates", static_folder="ui/static")
app.secret_key = "change-this-in-production"

# In-memory session store (use Redis in production)
agent_sessions: dict[str, OutingAgent] = {}


@app.route("/")
def index():
    session.setdefault("session_id", str(uuid.uuid4()))
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message: str = data.get("message", "").strip()
    session_id: str = session.get("session_id", str(uuid.uuid4()))

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Get or create agent for this session
    if session_id not in agent_sessions:
        agent_sessions[session_id] = OutingAgent()

    agent = agent_sessions[session_id]

    try:
        response = agent.chat(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    session_id = session.get("session_id")
    if session_id and session_id in agent_sessions:
        del agent_sessions[session_id]
    session["session_id"] = str(uuid.uuid4())
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
