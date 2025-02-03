# ConsoleChat

A modular chat application built with TinyLlama, featuring an agentic architecture for handling different conversation aspects.

## Features

- Modular agent-based architecture
- Configurable system prompts
- Easy to extend with new agents
- Lightweight and efficient

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download the TinyLlama model and place it in the `models/` directory

3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

- `src/agents/`: Different conversation agents
- `src/config/`: Configuration and settings
- `src/core/`: Core application logic
- `src/utils/`: Utility functions
