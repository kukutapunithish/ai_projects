from langchain_huggingface import HuggingFaceEmbeddings
from src.config import RETRIEVAL_CONFIG

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=RETRIEVAL_CONFIG['vector_model']['embedding_model_name'])
