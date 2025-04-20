import asyncio
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.document_loaders import ArxivLoader

async def load_arxiv_documents(
    query: str,
    max_docs: int = 10,
    load_all_meta: bool = False
) -> List[Document]:
    """
    Asynchronously load documents from arXiv based on a search query.
    
    Args:
        query: Search query for arXiv articles
        max_docs: Maximum number of documents to load (default: 10)
        load_all_meta: Whether to load all available metadata (default: False)
    
    Returns:
        List of loaded documents with content and metadata
    """
    loader = ArxivLoader(
        query=query,
        load_max_docs=max_docs,
        load_all_available_meta=load_all_meta
    )
    return await loader.aload()
