from src.ingestion.pdf_loader import pdf_markdown_pipeline
from src.utils.common import get_file_extension


def load_document(file_path, output_file_path):
    """
    Load a document from a specified file path, convert it to markdown, and save it to an output file.

    Args:
        file_path (str): The path to the input document file.
        output_file_path (str): The path to the output file where the markdown will be saved.
    """
    ext = get_file_extension(file_path)
    if ext == 'pdf': 
        pdf_markdown_pipeline(file_path, output_file_path)
    elif ext == 'docx':
        pass
    elif ext in ['ppt', 'pptx']:
        pass
    else:
        raise ValueError(f"Unsupported file extension: {ext}")



