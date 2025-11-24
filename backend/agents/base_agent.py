from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class AgentResponse:
    success: bool
    message: str
    data: Dict[str, Any] = None
    next_actions: List[str] = None

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.context = {}
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> AgentResponse:
        pass
    
    def update_context(self, new_context: Dict[str, Any]):
        self.context.update(new_context)