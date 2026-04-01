from src.handlers.error_handler import ChatBotError

try:
    # Raising the custom exception
    raise ChatBotError("Something went wrong on the server", 500)

except ChatBotError as e:
    print(f"Error Message: {e}")
    print(f"HTTP Status Code: {e.error_code}")
