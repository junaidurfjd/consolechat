from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from ..config.prompts import SYSTEM_PROMPTS
from ..utils.llm_wrapper import LLMWrapper
import re

class TaskAgent(BaseAgent):
    def __init__(self, llm: LLMWrapper):
        super().__init__("task", SYSTEM_PROMPTS["task"])
        self.llm = llm
        self.exit_patterns = [
            r'\b(bye|goodbye|exit|quit|end)\b',
            r'^(bye|goodbye)[\s!]*$'
        ]
        
    def can_handle(self, user_input: str, context: Dict[str, Any]) -> bool:
        """Task agent can handle most inputs except greetings and goodbyes."""
        # Check if input matches exit patterns
        if any(re.search(pattern, user_input.lower()) 
              for pattern in self.exit_patterns):
            return False
        return True
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user query using LLM."""
        # Prepare conversation context
        conversation = context.get('conversation_history', [])
        conversation.append({
            "role": "user",
            "content": user_input
        })
        
        # Get response from LLM
        llm_response = self.llm.create_chat_completion(
            messages=conversation,
            max_tokens=2048,
            temperature=0.7
        )
        
        response = {
            'response': llm_response['choices'][0]['message']['content'],
            'context': {'last_query': user_input},
            'metadata': {'action': 'task_response', 'confidence': 'medium'}
        }
        
        return response
    
    def transfer_control(self) -> Optional[str]:
        """Transfer to farewell agent if exit is detected."""
        last_query = self.context.get('last_query', '').lower()
        if any(re.search(pattern, last_query) 
              for pattern in self.exit_patterns):
            return 'farewell'
        return None 