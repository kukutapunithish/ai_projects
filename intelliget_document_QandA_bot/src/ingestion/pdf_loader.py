import pymupdf4llm



def pdf_markdown_pipeline(file_path, output_file_path):
    """
    A pipeline function that converts a PDF file to markdown and saves it to a specified output file.

    Args:
        file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output file where the markdown will be saved.
    """
    markdown_content = pdf_to_markdown(file_path)
    save_markdown_to_file(markdown_content, output_file_path)



def save_markdown_to_file(markdown_content, output_file_path):
    """
    Save the markdown content to a file.

    Args:
        markdown_content (str): The markdown content to be saved.
        output_file_path (str): The path to the output file where the markdown will be saved.
    """
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)



def pdf_to_markdown(file_path):
    """
    Load a PDF file and extract its markdown content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted markdown content from the PDF file.
    """
    markdown_content = pymupdf4llm.to_markdown(file_path)

    return markdown_content