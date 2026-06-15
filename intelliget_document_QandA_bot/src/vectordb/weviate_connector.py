from weaviate.classes.config import Property, DataType, Configure
import weaviate as wc
from langchain_weaviate import WeaviateVectorStore
from src.utils.logger import logger


def local_weaviate_client():
    logger.info("Connecting to Weaviate container...")

    return wc.connect_to_custom(
        http_host="weaviate",
        http_port=8080,
        http_secure=False,
        grpc_host="weaviate",
        grpc_port=50051,
        grpc_secure=False,
    )


def document_exists(client, source_file: str, collection_name="KnowledgeBase"):
    collection = client.collections.get(collection_name)

    result = collection.query.fetch_objects(
        filters=wc.query.Filter.by_property("file_name").equal(source_file),
        limit=1
    )

    return len(result.objects) > 0

def initialize_collection():
    client = local_weaviate_client()

    if not client.collections.exists("KnowledgeBase"):
        logger.info("Creating Weaviate collection: KnowledgeBase")
        client.collections.create(
            name="KnowledgeBase",
            vector_config=Configure.Vectors.self_provided(),
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                # Property(name="topic", data_type=DataType.TEXT),
                Property(name="file_name", data_type=DataType.TEXT),
                Property(
                    name="page_number",
                    data_type=DataType.INT,
                    skip_vectorization=True,
                ),
            ],
        )

    return client

def create_weaviate_vector_store(chunks, embeddings):
    client = initialize_collection()

    store = WeaviateVectorStore(
        client=client,
        index_name="KnowledgeBase",
        text_key="text",
        embedding=embeddings,
    )
    logger.info("Adding documents to Weaviate vector store...")

    store.add_documents(chunks)
    return store,client



def get_weaviate_vector_store(embeddings):
    client = local_weaviate_client() # connect to existing Weaviate instance

    store = WeaviateVectorStore(
        client=client,
        index_name="KnowledgeBase",
        text_key="text",
        embedding=embeddings,
    )

    return store