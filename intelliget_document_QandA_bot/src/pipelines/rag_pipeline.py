
from src.pipelines.ingest_pipeline import docs_ingestion
from src.chunking.text_splitter import split_markdown_into_chunks
from src.embeddings.embedding_client import get_embedding_model
from src.vectordb.weviate_connector import create_weaviate_vector_store, get_weaviate_vector_store
from src.retrieval.retriever import retrieve_relevant_chunks
from src.retrieval.reranker import rerank_chunks
from src.retrieval.context_builder import build_context_string
import streamlit as st
from src.utils.logger import logger

@st.cache_resource
def set_embedding_model():
    logger.info("Loading embedding model...")
    embedding_model = get_embedding_model()
    return embedding_model

def retrieval_pipeline(dir_path):
    embedding_model = set_embedding_model()
    output_file_paths = docs_ingestion(dir_path)
    store = None
    for file_path in output_file_paths:
        logger.info(f"Processing file: {file_path}")
        chunks = split_markdown_into_chunks(file_path)
        store, client = create_weaviate_vector_store(chunks, embedding_model)
    return store, client


def augmentation_pipeline(store, query):
    # Retrieve relevant chunks for the query
    logger.info(f"Retrieving relevant chunks")
    retrieved_chunks = retrieve_relevant_chunks(store, query)
    logger.info(f"Reranking retrieved chunks")
    sorted_chunks = rerank_chunks(query, retrieved_chunks)
    logger.info(f"Building context string for LLM prompt")
    prompt = build_context_string(query, sorted_chunks)
    return prompt


def rag_pipeline(dir_path, query):
    logger.info(f"Starting RAG pipeline with directory")
    store, client = retrieval_pipeline(dir_path)
    logger.info(f"Retrieval pipeline completed successfully")
    # client.close()  # Close the Weaviate client connection after retrieval
    prompt = augmentation_pipeline(store, query)
    logger.info(f"Augmentation pipeline completed successfully")
    client.close()
    return prompt


def augmentation_isolation_pipeline(query):
    embedding_model = set_embedding_model()
    logger.info(f"Connecting to existing Weaviate collection")
    store = get_weaviate_vector_store(embedding_model)
    # Retrieve relevant chunks for the query
    retrieved_chunks = retrieve_relevant_chunks(store, query)
    if (len(retrieved_chunks) == 0)  or (retrieved_chunks is None):
        return "No relevant chunks found."
    sorted_chunks = rerank_chunks(query, retrieved_chunks)
    prompt = build_context_string(query, sorted_chunks)
    return prompt

