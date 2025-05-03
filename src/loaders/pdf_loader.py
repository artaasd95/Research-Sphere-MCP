import asyncio
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders.parsers import PyMuPDFParser
from common.logger import logger
from langchain.document_loaders import PDFLoader
from common.interfaces import DocumentLoader
from common.models import PDFDocument

__all__ = ["process_pdf_directory"]

async def parse_pdf(
    file_path: Path,
    password: Optional[str] = None,
    mode: str = "single",
    pages_delimiter: str = "\n\n",
) -> List[Document]:
    """Parse a single PDF into a list of Documents (async)."""
    logger.info(f"Parsing PDF: {file_path}")

    def _blocking_parse():
        blob = Document.Blob.from_path(file_path)
        parser = PyMuPDFParser(password=password, mode=mode, pages_delimiter=pages_delimiter)
        return list(parser.lazy_parse(blob))

    return await asyncio.to_thread(_blocking_parse)

async def process_pdf_directory(directory: Path) -> List[Document]:
    pdf_files = list(directory.glob("*.pdf"))
    tasks = [parse_pdf(fp) for fp in pdf_files]
    results = await asyncio.gather(*tasks)
    return [d for sub in results for d in sub]

class PDFDocumentLoader(DocumentLoader):
    """Concrete implementation of DocumentLoader for PDF files."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    async def load(self, source: Path) -> List[PDFDocument]:
        """Load documents from a PDF file or directory."""
        if source.is_file():
            return await self._load_single_pdf(source)
        elif source.is_dir():
            return await self._load_pdf_directory(source)
        else:
            raise ValueError(f"Invalid source path: {source}")
    
    async def _load_single_pdf(self, pdf_path: Path) -> List[PDFDocument]:
        """Load a single PDF file."""
        try:
            loader = PDFLoader(str(pdf_path))
            raw_docs = loader.load()
            
            return [
                PDFDocument(
                    _content=doc.page_content,
                    _metadata={**doc.metadata, 'source': str(pdf_path)}
                )
                for doc in raw_docs
            ]
        except Exception as e:
            raise Exception(f"Error loading PDF {pdf_path}: {str(e)}")
    
    async def _load_pdf_directory(self, directory: Path) -> List[PDFDocument]:
        """Load all PDF files from a directory."""
        pdf_files = list(directory.glob("*.pdf"))
        all_docs = []
        
        for pdf_file in pdf_files:
            try:
                docs = await self._load_single_pdf(pdf_file)
                all_docs.extend(docs)
            except Exception as e:
                print(f"Warning: Skipping {pdf_file} due to error: {str(e)}")
                continue
        
        return all_docs