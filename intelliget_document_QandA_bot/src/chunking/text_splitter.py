from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from src.config import RETRIEVAL_CONFIG

# Split Markdown by header levels
headers_to_split_on = [
    ("#", "header_1"),
    ("##", "header_2"),
]


def load_markdown_file(file_path):
    """
    Load a markdown file and return its content as a string.

    Args:
        file_path (str): The path to the markdown file.
    Returns:
        str: The content of the markdown file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    return markdown_text


def split_markdown_into_chunks(file_path):
    """
    Split a markdown text into smaller, overlapping chunks based on header levels.

    Args:
        markdown_text (str): The input markdown text to be split.

    Returns:
        List[Document]: A list of text chunks.
    """

    markdown_text = load_markdown_file(file_path)


    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(markdown_text)

    # Further split the text into smaller, overlapping chunks
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=RETRIEVAL_CONFIG['splitting']['chunk_size'],
        chunk_overlap=RETRIEVAL_CONFIG['splitting']['chunk_overlap']
    )
    chunks = recursive_splitter.split_documents(md_header_splits)

    return chunks