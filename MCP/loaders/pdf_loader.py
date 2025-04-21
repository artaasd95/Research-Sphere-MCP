import asyncio
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders.parsers import PyMuPDFParser
from common.logger import logger

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