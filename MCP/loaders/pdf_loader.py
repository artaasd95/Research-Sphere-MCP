import asyncio
from pathlib import Path
from typing import List, Optional, Generator
from langchain_core.documents import Document
from langchain_core.documents.base import Blob
from langchain_community.document_loaders.parsers import PyMuPDFParser

async def parse_pdf(
    file_path: str | Path,
    password: Optional[str] = None,
    mode: str = "single",
    pages_delimiter: str = "\n\n"
) -> List[Document]:
    """
    Asynchronously parse a PDF file using PyMuPDF parser.
    
    Args:
        file_path: Path to PDF file
        password: PDF decryption password (optional)
        mode: Parsing mode ('single' or 'multi')
        pages_delimiter: Delimiter between pages
    
    Returns:
        List of parsed documents with metadata
    """
    def _parse():
        blob = Blob.from_path(file_path)
        parser = PyMuPDFParser(
            password=password,
            mode=mode,
            pages_delimiter=pages_delimiter
        )
        return list(parser.lazy_parse(blob))
    
    return await asyncio.to_thread(_parse)

async def process_pdf_directory(
    directory_path: str | Path,
    password: Optional[str] = None,
    mode: str = "single",
    pages_delimiter: str = "\n\n"
) -> List[Document]:
    """
    Asynchronously process all PDF files in a directory.
    
    Args:
        directory_path: Path to directory containing PDFs
        password: PDF decryption password (optional)
        mode: Parsing mode ('single' or 'multi')
        pages_delimiter: Delimiter between pages
    
    Returns:
        Combined list of documents from all PDFs
    """
    path = Path(directory_path)
    pdf_files = path.glob("*.pdf")
    
    tasks = [
        parse_pdf(pdf_file, password, mode, pages_delimiter)
        for pdf_file in pdf_files
    ]
    
    results = await asyncio.gather(*tasks)
    return [doc for sublist in results for doc in sublist]

