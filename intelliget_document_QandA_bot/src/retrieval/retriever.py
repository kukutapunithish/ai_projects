from src.config import RETRIEVAL_CONFIG


def retriever_client(store):

    # Create a retriever that uses MMR over the ProGit Weaviate index
    retriever = store.as_retriever(
        search_type=RETRIEVAL_CONFIG['retriever']['search_type'],
        search_kwargs={
            "k": RETRIEVAL_CONFIG['retriever']['search_kwargs']['k'],       # number of final documents to return
            "fetch_k": RETRIEVAL_CONFIG['retriever']['search_kwargs']['fetch_k'] # number of candidate documents to retrieve before reranking
        }
    )
    return retriever


def retrieve_relevant_chunks(store,query):
    retriever = retriever_client(store)
    # Retrieve documents for the query
    docs = retriever.invoke(query)
    return docs
