import os
import sys
import logging
from src.utils.llm_wrapper import LLMWrapper
from src.agents.greeting_agent import GreetingAgent
from src.agents.task_agent import TaskAgent
from src.agents.farewell_agent import FarewellAgent
from src.core.flow_controller import FlowController
from src.config.settings import MODEL_PATH, N_CTX, N_THREADS, MODEL_DIR

def setup_logging():
    """Configure logging to show only warnings and errors."""
    logging.basicConfig(level=logging.WARNING)

def initialize_agents():
    """Initialize all agents and the LLM."""
    model_path = os.path.join(MODEL_DIR, MODEL_PATH)
    
    # Suppress stderr during model loading
    stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    
    try:
        llm = LLMWrapper(
            model_path=model_path,
            n_ctx=N_CTX,
            n_threads=N_THREADS
        )
        
        agents = [
            GreetingAgent(),
            TaskAgent(llm),
            FarewellAgent()
        ]
        
        return agents
    finally:
        sys.stderr = stderr

def main():
    """Main entry point for the chat application."""
    setup_logging()
    
    print("\nInitializing TinyLlama Chat System...")
    agents = initialize_agents()
    
    # Create flow controller
    controller = FlowController(agents)
    
    print("\nTinyLlama Chat System Ready!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Process input
            response = controller.process_input(user_input)
            
            # Print response
            print("\nAssistant:", response['response'])
            
            # Check if conversation should end
            if response.get('context', {}).get('conversation_ended', False):
                break
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            break

if __name__ == "__main__":
    main() 