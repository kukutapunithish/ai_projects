# Intelligent Document Q&A Agent

An AI-powered Document Intelligence platform that enables users to upload enterprise documents (PDF, DOCX, PPTX), ask natural language questions, and generate automated analytical reports.

## Overview

This project combines Retrieval-Augmented Generation (RAG), Machine Learning classification, and Large Language Models (LLMs) to transform unstructured documents into actionable insights. The system supports document ingestion, semantic search, multi-hop question answering, topic classification, entity extraction, and automated report generation through an interactive Streamlit interface.

## Key Features

- 📄 Multi-format document ingestion (PDF, DOCX, PPTX)
- 🔍 RAG-based semantic retrieval and multi-hop question answering
- 🤖 LLM-powered conversational document assistant
- 🏷️ Topic classification using a self-trained ML model
- 📊 Confidence scoring for retrieval and answers
- 🧠 Entity extraction (dates, numbers, named entities)
- 📑 Automated HTML report generation
- 🌐 Streamlit-based user interface
- 📈 RAGAS evaluation metrics for retrieval quality
- 🐳 Dockerized deployment

## Tech Stack

- **Frontend:** Streamlit
- **LLM Framework:** LangChain
- **Vector Store:** weviate
- **ML:** Scikit-learn, MLflow
- **NLP:** spaCy
- **Reporting:** Jinja2
- **Evaluation:** RAGAS
- **Deployment:** Docker compose

## Workflow

1. Upload documents.
2. Extract and chunk content.
3. Store embeddings in a vector database.
4. Retrieve relevant chunks for user queries.
5. Classify retrieved content into predefined topics.
6. Generate contextual answers with confidence scores.
7. Create downloadable analytical reports with summaries, topics, entities, and session insights.

## Project Structure

```text
ingestion/     # Document parsing, chunking, embeddings
classifier/    # Model training, evaluation, artifacts
agent/         # RAG agent, prompts, tools
report/        # HTML templates and report generation
app.py         # Streamlit application
```

## Setup
- Use the following command to download and run the model
```bash
ollama run gemma3:270m
```
- For building the docker image and running it
```bash
docker compose up --build -d
```