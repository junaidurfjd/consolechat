from typing import Dict, Any, Optional
import re
from .base_agent import BaseAgent
from ..config.prompts import SYSTEM_PROMPTS

class FarewellAgent(BaseAgent):
    def __init__(self):
        super().__init__("farewell", SYSTEM_PROMPTS["farewell"])
        self.farewell_patterns = [
            r'\b(bye|goodbye|exit|quit|end)\b',
            r'^(bye|goodbye)[\s!]*$'
        ]
        
    def can_handle(self, user_input: str, context: Dict[str, Any]) -> bool:
        """Check if input contains farewell patterns."""
        return any(re.search(pattern, user_input.lower()) 
                  for pattern in self.farewell_patterns)
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process farewells and provide closing message."""
        # Get conversation summary if available
        conversation_history = context.get('conversation_history', [])
        
        if len(conversation_history) > 2:
            response = {
                'response': "Thank you for chatting! I hope I was able to help. Have a great day!",
                'context': {'conversation_ended': True},
                'metadata': {'action': 'farewell', 'confidence': 'high'}
            }
        else:
            response = {
                'response': "Goodbye! Have a great day!",
                'context': {'conversation_ended': True},
                'metadata': {'action': 'farewell', 'confidence': 'high'}
            }
            
        return response
    
    def transfer_control(self) -> Optional[str]:
        """No transfer needed as this is the end of conversation."""
        return None 