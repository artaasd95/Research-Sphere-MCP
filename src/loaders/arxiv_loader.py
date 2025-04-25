from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import ArxivLoader
from common.logger import logger

__all__ = ["load_arxiv_documents"]

async def load_arxiv_documents(query: str, max_docs: int = 10, load_all_meta: bool = False) -> List[Document]:
    """Asynchronously fetch docs from arXiv."""
    logger.info(f"Querying arXiv for '{query}' (max {max_docs})")
    loader = ArxivLoader(query=query, load_max_docs=max_docs, load_all_available_meta=load_all_meta)
    docs = await loader.aload()
    logger.info(f"Fetched {len(docs)} arXiv docs")
    return docs