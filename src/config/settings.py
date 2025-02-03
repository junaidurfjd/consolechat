import os

# Model settings
MODEL_PATH = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
N_THREADS = 4
N_CTX = 2048

# Agent settings
EXIT_COMMANDS = ["quit", "exit", "bye"]

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(ROOT_DIR, "models")

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True) 