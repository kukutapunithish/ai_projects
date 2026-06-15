import os
from src.utils.logger import logger
from src.ingestion.document_loader import load_document


def docs_ingestion(dir_path):
    """Ingest documents from the specified directory."""
    # Placeholder for document ingestion logic
    # This could involve reading files, extracting text, and storing it in a vector database
    logger.info(f"Ingesting documents from: {dir_path}")
    processed_dir = os.path.join(dir_path, "processed_docs")
    os.makedirs(processed_dir, exist_ok=True)
    output_file_paths = []

    # get all the files in the dir_path
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            output_file_path = os.path.join(processed_dir, f"{os.path.splitext(file_name)[0]}.json")
            load_document(file_path, output_file_path)
            output_file_paths.append(output_file_path)
    return output_file_paths