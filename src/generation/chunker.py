from typing import List
from langchainCore.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common.config import settings

__all__ = ["chunk_text"]

def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    docs = splitter.create_documents([text])
    return [d.page_content for d in docs]