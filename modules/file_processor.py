# modules/file_processor.py

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

def load_and_split_pdf(pdf_doc):
    """
    Loads a PDF, extracts its content, and splits it into chunks.
    """
    # PyPDFLoader requires a file path, so we create a temporary file
    # to store the uploaded PDF's content.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_doc.getvalue())
        tmp_file_path = tmp_file.name

    # Load the document from the temporary file path
    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load()
    
    # Clean up the temporary file after loading
    os.remove(tmp_file_path)
    
    # Initialize the splitter to break the document into smaller, semantically related chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    # Split the loaded documents into chunks
    chunks = text_splitter.split_documents(documents)
    return chunks
