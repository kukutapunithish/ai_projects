import streamlit as st
import os
import uuid

from src.llm.llm_client import chat_with_model
from utils.logger import logger
from handlers.error_handler import ChatBotError
from src.pipelines.rag_pipeline import rag_pipeline

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Q&A Chatbot",
    layout="centered"
)

st.title("Q&A Chatbot")


# -----------------------------------------------------------------------------
# APP INITIALIZATION
# -----------------------------------------------------------------------------

if "app_initialized" not in st.session_state:
    logger.info("Q&A Chatbot started successfully")
    st.session_state.app_initialized = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_folder" not in st.session_state:
    st.session_state.user_folder = str(uuid.uuid4())


# -----------------------------------------------------------------------------
# FILE STORAGE
# -----------------------------------------------------------------------------

UPLOAD_BASE_DIR = "user_docs"
user_dir = os.path.join(
    UPLOAD_BASE_DIR,
    st.session_state.user_folder
)

os.makedirs(user_dir, exist_ok=True)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------

def render_file_badges(files):
    """Render uploaded file badges."""

    if not files:
        return

    color_map = {
        "PDF": "#E53935",
        "DOCX": "#2B579A",
        "DOC": "#2B579A",
        "PPTX": "#D24726",
        "PPT": "#D24726",
        "XLSX": "#217346",
        "XLS": "#217346",
    }

    attachments_html = ""

    for file_name in files:
        ext = file_name.split(".")[-1].upper()

        badge_color = color_map.get(ext, "#6B7280")

        attachments_html += f"""
        <div style="
            display:inline-flex;
            align-items:center;
            gap:6px;
            padding:4px 8px;
            margin-right:6px;
            margin-bottom:4px;
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

            <span>{file_name}</span>
        </div>
        """

    st.html(attachments_html)


def build_llm_history(messages):
    """
    Convert session messages into a format suitable
    for the LLM API.
    """

    history = []

    for msg in messages:
        history.append(
            {
                "role": msg["role"],
                "content": msg["content"]["text"]
            }
        )

    return history


# -----------------------------------------------------------------------------
# CHAT HISTORY DISPLAY
# -----------------------------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        text = message["content"].get("text", "")
        files = message["content"].get("files", [])

        if text:
            st.markdown(text)

        if files:
            render_file_badges(files)


# -----------------------------------------------------------------------------
# USER INPUT
# -----------------------------------------------------------------------------

if prompt := st.chat_input(
    "Ask a question about the uploaded document!",
    accept_file="multiple",
    file_type=["pdf", "docx", "ppt", "pptx"]
):

    user_text = prompt.text if hasattr(prompt, "text") else str(prompt)

    uploaded_files = (
        prompt.files
        if hasattr(prompt, "files")
        else []
    )

    uploaded_file_names = []

    # -------------------------------------------------------------------------
    # SAVE FILES
    # -------------------------------------------------------------------------

    for uploaded_file in uploaded_files:

        uploaded_file_names.append(uploaded_file.name)

        save_path = os.path.join(
            user_dir,
            uploaded_file.name
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        logger.info(
            f"Saved file: {uploaded_file.name}"
        )

    # -------------------------------------------------------------------------
    # STORE USER MESSAGE
    # -------------------------------------------------------------------------

    user_message = {
        "role": "user",
        "content": {
            "text": user_text,
            "files": uploaded_file_names
        }
    }
    if len(user_message["content"]["files"]) > 0:
        prompt_with_context = rag_pipeline(user_dir, user_message["content"]["text"])
        user_message["content"]["text"] = prompt_with_context

    st.session_state.messages.append(user_message)

    # -------------------------------------------------------------------------
    # DISPLAY USER MESSAGE
    # -------------------------------------------------------------------------

    with st.chat_message("user"):

        if user_text:
            st.markdown(user_text)

        if uploaded_file_names:
            render_file_badges(uploaded_file_names)

    # -------------------------------------------------------------------------
    # GENERATE ASSISTANT RESPONSE
    # -------------------------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            llm_history = build_llm_history(
                st.session_state.messages
            )

            response_text = chat_with_model(
                llm_history
            )

            response_stream = (
                chunk for chunk in [response_text]
            )

            final_response = st.write_stream(
                response_stream
            )

        except ChatBotError as e:

            logger.error(
                f"Error occurred while chatting with model: {e}"
            )

            final_response = (
                "Sorry, I encountered an error "
                "while processing your request."
            )

            st.markdown(final_response)

        except Exception as e:

            logger.exception(
                f"Unexpected error: {e}"
            )

            final_response = (
                "An unexpected error occurred."
            )

            st.markdown(final_response)

    # -------------------------------------------------------------------------
    # STORE ASSISTANT MESSAGE
    # -------------------------------------------------------------------------

    assistant_message = {
        "role": "assistant",
        "content": {
            "text": final_response,
            "files": []
        }
    }

    st.session_state.messages.append(
        assistant_message
    )


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------

with st.sidebar:

    st.subheader("Chat Controls")

    if st.button("🗑️ Clear Chat History"):

        st.session_state.messages = []

        logger.info(
            "Chat history cleared"
        )

        st.rerun()

    st.divider()

    st.write(
        f"Session Folder:\n`{st.session_state.user_folder}`"
    )


# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------

st.caption(
    f"💬 {len(st.session_state.messages)} messages in conversation"
)