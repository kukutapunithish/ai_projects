from langchain_huggingface import HuggingFaceEmbeddings
from src.config import RETRIEVAL_CONFIG

embedding_model = HuggingFaceEmbeddings(model_name=RETRIEVAL_CONFIG['vector_model']['embedding_model_name'])
