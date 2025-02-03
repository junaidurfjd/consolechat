from typing import Dict, List, Any
from llama_cpp import Llama

class LLMWrapper:
    """Wrapper for the Llama model to standardize interactions."""
    
    def __init__(self, model_path: str, n_ctx: int = 2048, n_threads: int = 4):
        self.model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads
        )
    
    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stop: List[str] = None
    ) -> Dict[str, Any]:
        """Wrapper for the create_chat_completion method."""
        return self.model.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop
        ) 