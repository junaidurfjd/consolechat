from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class BaseAgent(ABC):
    """Base class for all conversation agents."""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.context = {}
    
    @abstractmethod
    def can_handle(self, user_input: str, context: Dict[str, Any]) -> bool:
        """Determine if this agent can handle the current input."""
        pass
    
    @abstractmethod
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and return response with metadata."""
        pass
    
    def transfer_control(self) -> Optional[str]:
        """Determine if control should be transferred to another agent."""
        return None
    
    def update_context(self, new_context: Dict[str, Any]):
        """Update agent's context with new information."""
        self.context.update(new_context) 