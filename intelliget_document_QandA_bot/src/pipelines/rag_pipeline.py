
from src.pipelines.ingest_pipeline import docs_ingestion
from src.chunking.text_splitter import split_markdown_into_chunks
from src.embeddings.embedding_client import embedding_model
from src.vectordb.weviate_connector import create_weaviate_vector_store
from src.retrieval.retriever import retrieve_relevant_chunks
from src.retrieval.reranker import rerank_chunks
from src.retrieval.context_builder import build_context_string

def retrieval_pipeline(dir_path):
    output_file_paths = docs_ingestion(dir_path)
    store = None
    for file_path in output_file_paths:
        chunks = split_markdown_into_chunks(file_path)
        store, client = create_weaviate_vector_store(chunks, embedding_model)
    return store, client


def agumentation_pipeline(store, query):
    # Retrieve relevant chunks for the query
    retrieved_chunks = retrieve_relevant_chunks(store, query)
    sorted_chunks = rerank_chunks(query, retrieved_chunks)
    prompt = build_context_string(query, sorted_chunks)
    return prompt


def rag_pipeline(dir_path, query):
    store, client = retrieval_pipeline(dir_path)
    # client.close()  # Close the Weaviate client connection after retrieval
    prompt = agumentation_pipeline(store, query)
    return prompt

