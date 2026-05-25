import json
import requests
from typing import Any, Dict, List
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from models import AgentRole, AgentMessage, AgentState, Task
from datetime import datetime


class AgentTools:
    """Tools available for agents to use"""

    @staticmethod
    def web_search(query: str) -> str:
        """Simulate web search"""
        return f"Search results for '{query}': Found 5 relevant sources (simulated)"

    @staticmethod
    def calculate(expression: str) -> str:
        """Evaluate mathematical expressions"""
        try:
            result = eval(expression)
            return f"Result: {result}"
        except:
            return "Invalid expression"

    @staticmethod
    def summarize_text(text: str) -> str:
        """Summarize given text"""
        words = text.split()
        summary = " ".join(words[: min(30, len(words))])
        return f"Summary: {summary}..." if len(words) > 30 else f"Summary: {text}"

    @staticmethod
    def get_current_info() -> str:
        """Get current system info"""
        return f"Current time: {datetime.now().isoformat()}, System ready"


AVAILABLE_TOOLS = {
    "web_search": AgentTools.web_search,
    "calculate": AgentTools.calculate,
    "summarize": AgentTools.summarize_text,
    "get_info": AgentTools.get_current_info,
}


class BaseAgent:
    """Base agent class with LLM integration"""

    def __init__(self, name: str, role: AgentRole):
        self.name = name
        self.role = role
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)
        self.state = AgentState(agent_name=name, role=role)
        self.message_history = []

    def add_message(self, message: str, action: str = None, tools: List[str] = None):
        """Add message to agent's history"""
        agent_msg = AgentMessage(
            agent_name=self.name,
            agent_role=self.role,
            message=message,
            action=action,
            tools_used=tools or [],
        )
        self.message_history.append(agent_msg)
        self.state.messages.append(agent_msg)
        return agent_msg

    def use_tool(self, tool_name: str, *args, **kwargs) -> str:
        """Execute a tool"""
        if tool_name not in AVAILABLE_TOOLS:
            return f"Tool '{tool_name}' not found"
        tool_func = AVAILABLE_TOOLS[tool_name]
        return tool_func(*args, **kwargs)

    def think(self, prompt: str) -> str:
        """Use LLM to generate thought/decision"""
        self.state.status = "thinking"
        try:
            response = self.llm.predict(prompt)
            self.state.status = "idle"
            return response
        except Exception as e:
            self.state.status = "idle"
            return f"Error: {str(e)}"

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role.value,
            "status": self.state.status,
            "messages": [
                {
                    "agent": msg.agent_name,
                    "role": msg.agent_role.value,
                    "message": msg.message,
                    "action": msg.action,
                    "tools_used": msg.tools_used,
                    "timestamp": msg.timestamp.isoformat(),
                }
                for msg in self.message_history[-10:]
            ],
        }


class PlannerAgent(BaseAgent):
    """Agent responsible for breaking down tasks into subtasks"""

    def plan(self, objective: str) -> List[Task]:
        """Create a plan for the given objective"""
        prompt = f"""You are a task planner. Break down this objective into 3-4 concrete subtasks:
        
Objective: {objective}

Return a JSON array of tasks with title and description."""

        response = self.think(prompt)
        self.add_message(f"Planning: {objective}", action="plan")

        try:
            tasks_data = json.loads(response)
            tasks = [
                Task(title=t["title"], description=t["description"])
                for t in tasks_data
            ]
            self.add_message(f"Created {len(tasks)} subtasks", action="task_creation")
            return tasks
        except:
            return [Task(title="Execute objective", description=objective)]


class ResearcherAgent(BaseAgent):
    """Agent responsible for research and analysis"""

    def research(self, topic: str) -> str:
        """Research a topic"""
        self.add_message(f"Researching: {topic}", action="research")
        
        search_result = self.use_tool("web_search", topic)
        self.add_message(search_result, action="search", tools=["web_search"])

        prompt = f"""Based on this search result, provide insights on '{topic}':
        
Search result: {search_result}

Provide 2-3 key insights."""

        analysis = self.think(prompt)
        self.add_message(analysis, action="analysis")
        return analysis


class ExecutorAgent(BaseAgent):
    """Agent responsible for executing tasks"""

    def execute(self, task: Task) -> str:
        """Execute a given task"""
        self.state.current_task = task
        self.state.status = "acting"
        self.add_message(f"Executing: {task.title}", action="execute")

        tools_used = []
        if "calculate" in task.description.lower():
            result = self.use_tool("calculate", "2 + 2")
            tools_used.append("calculate")
        elif "summarize" in task.description.lower():
            result = self.use_tool("summarize", task.description)
            tools_used.append("summarize")
        else:
            result = self.use_tool("get_info")
            tools_used.append("get_info")

        self.add_message(result, action="task_execution", tools=tools_used)
        self.state.status = "idle"
        task.status = "completed"
        task.result = result
        return result


class CriticAgent(BaseAgent):
    """Agent responsible for reviewing and critiquing work"""

    def review(self, work: str, context: str = "") -> str:
        """Review work and provide feedback"""
        self.add_message(f"Reviewing work", action="review")

        prompt = f"""You are a quality critic. Review this work and provide constructive feedback:
        
Work: {work}
Context: {context}

Provide 2-3 constructive points."""

        feedback = self.think(prompt)
        self.add_message(feedback, action="feedback")
        return feedback
