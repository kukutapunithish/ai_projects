# AI Personal Assistant (Chatbot) – Learning Project

## 🎯 Project Goal
Develop a web-based chatbot that can:
- Answer user questions
- Summarize text
- Act as a persona (e.g., coding tutor, travel planner)
This project introduces you to the modern GenAI stack:
- LLMs (Large Language Models) for intelligence
- API integration for communication
- Streamlit for user interface
- LangChain/LlamaIndex for orchestration

## 🛠 Tools & Technologies
- Brain (LLM): OpenAI GPT-4o or Google Gemini API
- Interface: Streamlit (Python-based web app framework)
- Orchestration: LangChain or LlamaIndex for managing conversation flow

## 📌 Implementation Roadmap

1. Set Up Environment
- Install Python and required libraries (streamlit, openai, langchain).
- Ensure virtual environment setup for clean dependency management.
2. Obtain API Key
- Register for OpenAI or Google AI Studio.
- Securely store and load your API key (avoid hardcoding).
3. Hello World Chatbot
- Create a minimal app.py file.
- Accept user input, send it to the LLM, and display the response.
- Focus on understanding request/response flow.
4. Run & Test
- Launch with streamlit run app.py.
- Interact with your chatbot and validate basic functionality.

## 📚 Learning Focus
- Understand how APIs connect your app to an LLM.
- Learn Streamlit components for building interactive UIs.
- Explore LangChain/LlamaIndex for conversation memory and persona handling.
- Practice secure coding habits (API key management, error handling).

## 🚀 Extensions (Optional Challenges)
- Add persona modes (e.g., tutor, planner, storyteller).
- Implement summarization feature for pasted text.
- Store conversation history using LangChain memory.
- Deploy your chatbot online (e.g., Streamlit Cloud, Hugging Face Spaces)

## Setup
- Use the following command to download and run the model
```bash
ollama run gemma3:270m
```
- For building the docker image
```bash
docker build -t kukutapunithishkumar/support_chatbot .
```

## Run
- For running the docker container
```bash
docker run -p 8080:8080 kukutapunithishkumar/support_chatbot:latest
```

