from weaviate.classes.config import Property, DataType, Configure
import weaviate as wc
from langchain_weaviate import WeaviateVectorStore



def local_weaviate_client():
    """
    Create a local Weaviate client instance.

    Returns:
        weaviate.Client: A Weaviate client connected to the local instance.
    """
    return wc.connect_to_local()


# def create_weaviate_vector_store(chunks, embeddings):

#     client = local_weaviate_client()
#     index_name = "KnowledgeBase"
    
#     # 2. Recreate/Reset the collection using the native client to apply custom configurations
#     if client.collections.exists(index_name):
#         client.collections.delete(index_name)
        
#     client.collections.create(
#         name=index_name,
#         # We handle text embeddings via LangChain client side, so we select no server vectorizer
#         vectorizer_config=None, 
        
#         # Explicitly declare your target database properties
#         properties=[
#             # LangChain v4 writes document.page_content into "text" by default
#             wc.Property(name="text", data_type=wc.DataType.TEXT),
            
#             # Metadata fields mapped from document.metadata
#             wc.Property(name="topic", data_type=wc.DataType.TEXT),
#             wc.Property(name="source_file", data_type=wc.DataType.TEXT),
            
#             # Explicitly force Weaviate to skip vector calculations on integer page counts
#             wc.Property(name="page_number", data_type=wc.DataType.INT, skip_vectorization=True)
#         ]
#     )

#     # 3. Stream data chunks into the custom schema using the LangChain wrapper
#     store = WeaviateVectorStore.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         client=client,
#         index_name=index_name,
#         text_key="text" # Tells LangChain to map page_content to your explicit "text" property
#     )
    
#     return store







def document_exists(client, source_file: str, collection_name="KnowledgeBase"):
    collection = client.collections.get(collection_name)

    result = collection.query.fetch_objects(
        filters=wc.query.Filter.by_property("source_file").equal(source_file),
        limit=1
    )

    return len(result.objects) > 0

def initialize_collection():
    client = local_weaviate_client()

    if not client.collections.exists("KnowledgeBase"):
        client.collections.create(
            name="KnowledgeBase",
            vectorizer_config=Configure.Vectorizer.none(),
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="topic", data_type=DataType.TEXT),
                Property(name="source_file", data_type=DataType.TEXT),
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

    store.add_documents(chunks)
    return store,client