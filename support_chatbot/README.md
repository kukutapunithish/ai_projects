# AI Personal Assistant (Chatbot) – Learning Project

## 🎯 Project Goal
Develop a web-based chatbot that can:
- Answer user questions related to python lanaguage
- Summarize text
- Acts as a expert software engineer and technical assistant.

This project introduces you to the modern GenAI stack:
- LLMs (Large Language Models) for intelligence
- API integration for communication
- Streamlit for user interface

## 🛠 Tools & Technologies
- Brain (LLM): Gemma model
- Interface: Streamlit (Python-based web app framework)

## 📚 Learning Focus
- Understand how APIs connect your app to an LLM.
- Learn Streamlit components for building interactive UIs.
- Explore conversation memory and persona handling.
- Practice secure coding habits (API key management, error handling).

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

