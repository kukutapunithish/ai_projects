import streamlit as st
import random
import time
import os
import uuid
from src.llm.llm_client import chat_with_model
from utils.logger import logger
from handlers.error_handler import ChatBotError

# Log app startup ONLY ONCE (Streamlit reruns on every interaction)
if "app_initialized" not in st.session_state:
    logger.info("Q&A Chatbot started successfully")
    st.session_state.app_initialized = True

st.set_page_config(
    page_title="Q&A Chatbot",
    layout="centered"
)

st.title("Q&A Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Assign a unique folder per session
if "user_folder" not in st.session_state:
    st.session_state.user_folder = str(uuid.uuid4())

UPLOAD_BASE_DIR = "user_docs"
user_dir = os.path.join(UPLOAD_BASE_DIR, st.session_state.user_folder)
os.makedirs(user_dir, exist_ok=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    
    with st.chat_message(message["role"]):
        logger.info("Displayed message from history: ", message.content.text)
        st.markdown(message.content.text)
        # if message["content"].text:
        #     st.markdown(message["content"].text)
        # if message["content"].files:
        #     attachments_html = ""
        #     for uploaded_file in message["content"].files:
        #         ext = uploaded_file.name.split(".")[-1].upper()

        #         color_map = {
        #             "PDF": "#E53935",
        #             "DOCX": "#2B579A",
        #             "DOC": "#2B579A",
        #             "PPTX": "#D24726",
        #             "PPT": "#D24726",
        #             "XLSX": "#217346",
        #             "XLS": "#217346",
        #         }

        #         badge_color = color_map.get(ext, "#6B7280")

        #         attachments_html += f"""
        #         <div style="
        #             display:inline-flex;
        #             align-items:center;
        #             gap:6px;
        #             padding:4px 8px;
        #             margin-right:6px;
        #             border:1px solid #d1d5db;
        #             border-radius:16px;
        #             background:#f8f9fa;
        #             font-size:13px;">
        #             <span style="
        #                 background:{badge_color};
        #                 color:white;
        #                 font-size:10px;
        #                 font-weight:bold;
        #                 padding:2px 5px;
        #                 border-radius:3px;">
        #                 {ext}
        #             </span>
        #             <span>{uploaded_file.name}</span>
        #         </div>
        #         """

# Accept user input
if prompt := st.chat_input("Ask a question about the uploaded document!"
                            , accept_file="multiple"
                            , file_type=["pdf", "docx", "ppt", "pptx"],):
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("User"):
        if prompt.text:
            st.markdown(prompt.text)
        if prompt.files:
            attachments_html = ""
            for uploaded_file in prompt.files:
                ext = uploaded_file.name.split(".")[-1].upper()

                color_map = {
                    "PDF": "#E53935",
                    "DOCX": "#2B579A",
                    "DOC": "#2B579A",
                    "PPTX": "#D24726",
                    "PPT": "#D24726",
                    "XLSX": "#217346",
                    "XLS": "#217346",
                }

                badge_color = color_map.get(ext, "#6B7280")

                attachments_html += f"""
                <div style="
                    display:inline-flex;
                    align-items:center;
                    gap:6px;
                    padding:4px 8px;
                    margin-right:6px;
                    border:1px solid #d1d5db;
                    border-radius:16px;
                    background:#f8f9fa;
                    font-size:13px;">
                    <span style="
                        background:{badge_color};
                        color:white;
                        font-size:10px;
                        font-weight:bold;
                        padding:2px 5px;
                        border-radius:3px;">
                        {ext}
                    </span>
                    <span>{uploaded_file.name}</span>
                </div>
                """

                # Save uploaded file to user-specific folder
                save_path = os.path.join(user_dir, uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

            st.html(attachments_html)
    
    # Display assistant response in chat message container
    with st.chat_message("Assistant"):
        # try:
        #     pass
            
        # except ChatBotError as e:
        #     logger.error(f"Error occurred while storing embeddings: {e}")
        #     error_text = "Sorry, I encountered an error while processing your request."
        #     response = (chunk for chunk in [error_text])
        
        try:
            response = chat_with_model(st.session_state.messages)
            response = (chunk for chunk in [response])
        except ChatBotError as e:
            logger.error(f"Error occurred while chatting with the model: {e}")
            error_text = "Sorry, I encountered an error while processing your request."
            response = (chunk for chunk in [error_text])
        response = st.write_stream(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": {"text":response, "files": []}})

# SIDEBAR
with st.sidebar:    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Show how many messages are in history
st.caption(f"💬 {len(st.session_state.messages)} messages in conversation")