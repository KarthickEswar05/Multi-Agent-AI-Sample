from flask import Flask, render_template, request, jsonify
from agents.orchestrator import MultiAgentOrchestrator
import json
import threading
from queue import Queue

app = Flask(__name__)
orchestrator = MultiAgentOrchestrator()
task_queue = Queue()
execution_results = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/agents-status")
def get_agents_status():
    """Get current status of all agents"""
    return jsonify(orchestrator.get_agents_status())


@app.route("/api/execute", methods=["POST"])
def execute_objective():
    """Execute an objective with multi-agent collaboration"""
    data = request.get_json()
    objective = data.get("objective", "").strip()

    if not objective:
        return jsonify({"error": "Objective cannot be empty"}), 400

    try:
        result = orchestrator.execute_objective(objective)
        execution_results[objective] = result
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/execution-log")
def get_execution_log():
    """Get execution log"""
    return jsonify(orchestrator.get_execution_log())


@app.route("/api/agent-messages/<agent_name>")
def get_agent_messages(agent_name):
    """Get messages from a specific agent"""
    agents = {
        "planner": orchestrator.planner,
        "researcher": orchestrator.researcher,
        "executor": orchestrator.executor,
        "critic": orchestrator.critic,
    }

    agent = agents.get(agent_name.lower())
    if not agent:
        return jsonify({"error": "Agent not found"}), 404

    messages = [
        {
            "agent": msg.agent_name,
            "role": msg.agent_role.value,
            "message": msg.message,
            "action": msg.action,
            "tools_used": msg.tools_used,
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in agent.message_history
    ]

    return jsonify({"agent": agent_name, "messages": messages})


if __name__ == "__main__":
    app.run(debug=True)
