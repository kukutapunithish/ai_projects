from sentence_transformers import CrossEncoder
from src.config import RETRIEVAL_CONFIG


def get_reranker():
    """
    Placeholder function for the reranker component of the RAG pipeline.
    This function can be implemented to take retrieved chunks and re-rank them based on relevance to the query.

    Returns:
        None
    """
    reranker = CrossEncoder(RETRIEVAL_CONFIG['vector_model']['cross_encoder_model_name'])
    return reranker

def rerank_chunks(query, retrieved_chunks):
    reranker = get_reranker()
    # Create pairs of (query, chunk) for reranking
    pairs = [[query, chunk.page_content] for chunk in retrieved_chunks]
    # Rerank the chunks based on their relevance to the query
    scores = reranker.predict(pairs)
    # Sort the chunks by their reranked scores
    sorted_chunks = [chunk for chunk, _ in sorted(zip(retrieved_chunks, scores), key=lambda item: item[1], reverse=True)][:3]
    return sorted_chunks