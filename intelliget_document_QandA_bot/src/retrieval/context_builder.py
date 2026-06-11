


def build_context_string(query,retrieved_docs):
    context_chunks = []
    for i, doc in enumerate(retrieved_docs, start=1):
        # 1. Pull the content and metadata fields cleanly
        text = doc.page_content
        topic = doc.metadata.get("topic", "Unknown Topic")
        source = doc.metadata.get("source_file", "Unknown Source")
        page = doc.metadata.get("page_number", "N/A")
        
        # 2. Format it into a highly legible block for the LLM
        chunk_string = (
            f"[Source {i}]: Topic: {topic} | File: {source} (Page {page})\n"
            f"Content: {text}\n"
            f"---"
        )
        context_chunks.append(chunk_string)
        
    # 3. Join all blocks together with double newlines
    return query + "\n\nContext: " + "\n\n".join(context_chunks)
