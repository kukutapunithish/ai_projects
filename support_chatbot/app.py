import streamlit as st
import random
import time
from src.llm.llm_client import chat_with_model
from utils.logger import logger
from handlers.error_handler import ChatBotError

# Log app startup ONLY ONCE (Streamlit reruns on every interaction)
if "app_initialized" not in st.session_state:
    logger.info("Advisory Chatbot started successfully")
    st.session_state.app_initialized = True

st.set_page_config(
    page_title="Advisory Chatbot",
    layout="centered"
)

st.title("Advisory Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about software development, programming, or technical topics!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("User"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("Assistant"):
        try:
            response = chat_with_model(st.session_state.messages)
            response = (chunk for chunk in [response])
        except ChatBotError as e:
            logger.error(f"Error occurred while chatting with the model: {e}")
            error_text = "Sorry, I encountered an error while processing your request."
            response = (chunk for chunk in [error_text])
        response = st.write_stream(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# SIDEBAR
with st.sidebar:    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Show how many messages are in history
st.caption(f"💬 {len(st.session_state.messages)} messages in conversation")