from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class AgentRole(str, Enum):
    PLANNER = "planner"
    RESEARCHER = "researcher"
    EXECUTOR = "executor"
    CRITIC = "critic"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    title: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    assigned_to: Optional[str] = None
    result: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class AgentMessage(BaseModel):
    agent_name: str
    agent_role: AgentRole
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    action: Optional[str] = None
    tools_used: List[str] = Field(default_factory=list)


class AgentState(BaseModel):
    agent_name: str
    role: AgentRole
    status: str = "idle"  # idle, thinking, acting
    current_task: Optional[Task] = None
    memory: List[Dict[str, Any]] = Field(default_factory=list)
    messages: List[AgentMessage] = Field(default_factory=list)
