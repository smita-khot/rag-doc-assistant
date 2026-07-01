import json
import os

HISTORY_FILE = "data/processed/chat_history.json"

def load_history():
    """Load conversation history from file, or start fresh if none exists."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """Save conversation history to file."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def add_message(history, role, content):
    """Add a message to history. role is 'user' or 'assistant'."""
    history.append({"role": role, "content": content})
    return history