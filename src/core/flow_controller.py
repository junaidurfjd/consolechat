from typing import Dict, List, Any
from ..agents.base_agent import BaseAgent

class FlowController:
    """Manages conversation flow between agents."""
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = {agent.name: agent for agent in agents}
        self.current_agent = None
        self.conversation_history = []
        self.context = {}
    
    def determine_agent(self, user_input: str) -> BaseAgent:
        """Determine which agent should handle the input."""
        if self.current_agent and self.current_agent.can_handle(user_input, self.context):
            return self.current_agent
            
        for agent in self.agents.values():
            if agent.can_handle(user_input, self.context):
                return agent
        
        return self.agents.get('task')  # Default to task agent
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input with appropriate agent."""
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Get appropriate agent
        agent = self.determine_agent(user_input)
        self.current_agent = agent
        
        # Process input
        response = agent.process(user_input, self.context)
        
        # Check for agent transfer
        next_agent = agent.transfer_control()
        if next_agent and next_agent in self.agents:
            self.current_agent = self.agents[next_agent]
        
        # Update context and history
        self.context.update(response.get('context', {}))
        self.conversation_history.append({
            "role": "assistant",
            "content": response['response']
        })
        
        return response 