import requests
from src.config import MODEL_CONFIG
from handlers.error_handler import ChatBotError
from core.prompts import SYSTEM_PROMPT

SYSTEM_DICT = {
            "role": "system",
            "content": SYSTEM_PROMPT
}

def chat_with_model(messages):
    """
    Function to interact with the Ollama API for chat-based interactions.
    
    Parameters:
    - messages: A list of dictionaries representing the conversation history. Each dictionary should have a 'role' (e.g., 'user', 'assistant') and 'content' (the message text).
    - context: Additional context to include in the system message.
    
    Returns:
    - The response from the model as a string.
    """
    try:
        URL = MODEL_CONFIG["model"]["url"]
        data = {
            "model": MODEL_CONFIG["model"]["name"],
            "messages": [SYSTEM_DICT] + messages,
            "options": {
                "temperature": MODEL_CONFIG["model"]["temperature"],
                "top_k": MODEL_CONFIG["model"]["top_k"],
                "top_p": MODEL_CONFIG["model"]["top_p"]
            },
            "stream": False
        }

        response = requests.post(URL, json=data)

        if response.status_code != 200:
            raise ChatBotError(f"Ollama HTTP {response.status_code} error",response.status_code)

        res = dict(response.json())
        content = res['message']['content']
        # if content:
        #     yield content
        return content
    except Exception as e:
        raise ChatBotError(f"Failed to connect to Ollama server: {e}",500) from e