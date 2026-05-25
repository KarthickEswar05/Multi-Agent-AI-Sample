from agents.base_agent import PlannerAgent, ResearcherAgent, ExecutorAgent, CriticAgent
from models import Task
from typing import List, Dict, Any
import json


class MultiAgentOrchestrator:
    """Orchestrates multiple agents working together"""

    def __init__(self):
        self.planner = PlannerAgent("Planner", "planner")
        self.researcher = ResearcherAgent("Researcher", "researcher")
        self.executor = ExecutorAgent("Executor", "executor")
        self.critic = CriticAgent("Critic", "critic")
        self.execution_log = []

    def execute_objective(self, objective: str) -> Dict[str, Any]:
        """Execute a complete objective with multi-agent collaboration"""
        
        # Step 1: Planner creates plan
        tasks = self.planner.plan(objective)
        self.execution_log.append(
            {"step": "planning", "agent": "Planner", "result": f"Created {len(tasks)} tasks"}
        )

        # Step 2: Researcher gathers information
        if any("research" in t.description.lower() for t in tasks):
            research_results = self.researcher.research(objective)
            self.execution_log.append(
                {"step": "research", "agent": "Researcher", "result": research_results[:100]}
            )

        # Step 3: Executor executes tasks
        results = []
        for task in tasks:
            result = self.executor.execute(task)
            results.append(result)
            self.execution_log.append(
                {"step": "execution", "agent": "Executor", "task": task.title, "result": result[:100]}
            )

        # Step 4: Critic reviews results
        combined_results = "\n".join(results)
        feedback = self.critic.review(combined_results, objective)
        self.execution_log.append(
            {"step": "review", "agent": "Critic", "result": feedback[:100]}
        )

        return {
            "objective": objective,
            "tasks": [{"title": t.title, "status": t.status, "result": t.result} for t in tasks],
            "execution_log": self.execution_log,
            "final_feedback": feedback,
        }

    def get_agents_status(self) -> List[Dict[str, Any]]:
        """Get current status of all agents"""
        return [
            self.planner.to_dict(),
            self.researcher.to_dict(),
            self.executor.to_dict(),
            self.critic.to_dict(),
        ]

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get execution log"""
        return self.execution_log
