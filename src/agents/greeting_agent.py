from typing import Dict, Any, Optional
import re
from .base_agent import BaseAgent
from ..config.prompts import SYSTEM_PROMPTS

class GreetingAgent(BaseAgent):
    def __init__(self):
        super().__init__("greeting", SYSTEM_PROMPTS["greeting"])
        # Common greeting patterns
        self.greeting_patterns = [
            r'\b(hi|hello|hey|greetings|good\s*(morning|afternoon|evening))\b',
            r'^(hi|hello|hey)[\s!]*$'
        ]
        self.has_greeted = False
        
    def can_handle(self, user_input: str, context: Dict[str, Any]) -> bool:
        """Check if input contains greetings or if we haven't greeted yet."""
        if not self.has_greeted:
            return True
            
        return any(re.search(pattern, user_input.lower()) 
                  for pattern in self.greeting_patterns)
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process greetings and ask about user's needs."""
        self.has_greeted = True
        
        # If this is first interaction or contains greeting
        if not context.get('greeted'):
            response = {
                'response': "Hello! I'm your AI assistant. How can I help you today?",
                'context': {'greeted': True},
                'metadata': {'action': 'greeting', 'confidence': 'high'}
            }
        else:
            response = {
                'response': "Hi again! What can I do for you?",
                'context': {},
                'metadata': {'action': 'greeting', 'confidence': 'high'}
            }
            
        return response
    
    def transfer_control(self) -> Optional[str]:
        """Transfer to task agent after greeting."""
        if self.has_greeted:
            return 'task'
        return None 