import pymupdf4llm
import json


def pdf_markdown_pipeline(file_path, output_file_path):
    """
    A pipeline function that converts a PDF file to markdown and saves it to a specified output file.

    Args:
        file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output file where the markdown will be saved.
    """
    doc_list = pdf_to_markdown(file_path)
    save_markdown_to_json_file(doc_list, output_file_path)



def save_markdown_to_json_file(doc_list, output_file_path):
    """
    Save the markdown content and metadata to a JSON file.

    Args:
        doc_list (list[dict]): The list of dictionaries containing markdown content and metadata.
        output_file_path (str): The path to the output file where the JSON will be saved.
    """
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(doc_list, f, ensure_ascii=False, indent=2)



def pdf_to_markdown(file_path):
    """
    Load a PDF file and extract its markdown content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list[dict]: Extracted markdown content and metadata for each page chunk.
    """
    docs = pymupdf4llm.to_markdown(file_path, page_chunks=True)
    doc_list = []
    for doc in docs:
        doc_list.append(
            {
                "text": doc["text"],
                "metadata": {
                    "file_name": doc["metadata"]["file_path"].split("/")[-1],
                    "page_number": doc["metadata"]["page_number"],
                }
            }
        )

    return doc_list