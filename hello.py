import os
import sys
import logging
from llama_cpp import Llama

# Configure logging to only show warnings and errors
logging.basicConfig(level=logging.WARNING)

# Suppress stderr before model loading
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
N_THREADS = 4
N_CTX = 2048
EXIT_COMMANDS = ["quit", "exit", "bye"]

# Different personality/style options for the system prompt
SYSTEM_PROMPTS = {
    "default": """You are a helpful and friendly AI assistant named TinyLlama. Follow these guidelines:
        1. Greet users warmly and introduce yourself when they say hello
        2. Keep responses clear, complete, and well-structured
        3. Wait for the user to finish their input before responding
        4. If you don't know something, say so honestly
        5. Stay on topic and be relevant to the user's questions
        6. Be conversational but professional
        7. Complete your thoughts before stopping""",
    
    "academic": """You are a scholarly AI assistant. Format your responses in an academic style:
        1. Use formal language and technical terminology when appropriate
        2. Structure responses with clear sections when needed
        3. Cite sources or mention limitations of your knowledge
        4. Use numbered lists for sequential information
        5. Maintain professional academic tone throughout""",
    
    "markdown": """You are a technical AI assistant. Format all responses in markdown:
        1. Use headers (# ## ###) for sections
        2. Format code blocks with ```
        3. Use bullet points and numbered lists
        4. Emphasize key points with *italics* or **bold**
        5. Use > for important quotes or notes""",
    
    "json": """You are an AI assistant that responds in JSON format. Structure your responses as:
        {
            "response_type": "answer|question|error",
            "content": "main response text",
            "additional_info": ["point1", "point2"],
            "confidence": "high|medium|low"
        }""",
    
    "medical": """You are a medical information assistant. Structure your responses as:
        1. Summary: Brief overview
        2. Details: In-depth explanation
        3. Recommendations: Practical advice
        4. Disclaimer: Always include medical disclaimer
        Note: Use simple language and avoid technical jargon unless necessary.""",
    
    "teacher": """You are an educational assistant. Format responses as:
        1. Simple Explanation: (for beginners)
        2. Detailed Explanation: (for advanced understanding)
        3. Examples: (practical applications)
        4. Practice Questions: (if applicable)
        Use encouraging and supportive language."""
}

# Initialize the model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_threads=N_THREADS
)

def chat(style="default"):
    # Initialize conversation with selected system prompt
    conversation = [{
        "role": "system",
        "content": SYSTEM_PROMPTS.get(style, SYSTEM_PROMPTS["default"])
    }]
    
    print(f"\nTinyLlama Chat - {style.title()} Style")
    print("(type 'quit', 'exit', or 'bye' to end the conversation)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for exit command
        if user_input.lower() in EXIT_COMMANDS:
            print("\nGoodbye!")
            break
        
        # Add user message to conversation
        conversation.append({
            "role": "user",
            "content": user_input
        })
        
        # Get model response
        response = llm.create_chat_completion(
            messages=conversation,
            max_tokens=2048,
            temperature=0.7,
            stop=["You:"]  # Only stop at the next user prompt
        )
        
        # Extract and print assistant's response
        assistant_message = response['choices'][0]['message']['content'].strip()
        print("\nAssistant:", assistant_message)
        
        # Add assistant response to conversation history
        conversation.append({
            "role": "assistant",
            "content": assistant_message
        })

if __name__ == "__main__":
    try:
        # Choose your style
        chat(style="markdown")  # or "academic", "json", "default"
    finally:
        # Restore stderr for other messages
        sys.stderr = stderr