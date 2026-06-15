from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, json
from langchain_core.documents import Document
from src.config import RETRIEVAL_CONFIG
import json

# Split Markdown by header levels
headers_to_split_on = [
    ("#", "header_1"),
    ("##", "header_2"),
]


def load_json_file(file_path):
    """
    Load a JSON file and return its content as a list of dictionaries.

    Args:
        file_path (str): The path to the JSON file.
    Returns:
        list: The content of the JSON file as a list of Document objects.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        doc_list = json.load(f)
    documents = [
        Document(
            page_content=item["text"],
            metadata=item["metadata"]
        )
        for item in doc_list
    ]

    return documents


def split_markdown_into_chunks(file_path):
    """
    Split a markdown text into smaller, overlapping chunks based on header levels.

    Args:
        file_path (str): The path to the JSON file containing the markdown content.

    Returns:
        List[Document]: A list of text chunks.
    """

    doc_list = load_json_file(file_path)


    # markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    # md_header_splits = markdown_splitter.split_documents(doc_list)

    # Further split the text into smaller, overlapping chunks
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=RETRIEVAL_CONFIG['splitting']['chunk_size'],
        chunk_overlap=RETRIEVAL_CONFIG['splitting']['chunk_overlap']
    )
    chunks = recursive_splitter.split_documents(doc_list)

    return chunks