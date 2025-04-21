from typing import List
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common.config import settings
from common.logger import logger

class VectorStoreManager:
    """Creates / loads FAISS vector store with automatic chunking & embeddings."""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key)
        self.store: FAISS | None = None

    def _chunk_documents(self, docs: List[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
        chunked = splitter.split_documents(docs)
        logger.info(f"Chunked {len(docs)} docs into {len(chunked)} chunks")
        return chunked

    def build(self, docs: List[Document]) -> None:
        chunked_docs = self._chunk_documents(docs)
        logger.info("Building new FAISS index")
        self.store = FAISS.from_documents(chunked_docs, self.embeddings)
        self.save()

    def add(self, docs: List[Document]) -> None:
        if not self.store:
            self.build(docs)
            return
        chunked_docs = self._chunk_documents(docs)
        self.store.add_documents(chunked_docs)
        self.save()

    def save(self) -> None:
        if not self.store:
            raise RuntimeError("Vector store is empty, cannot save")
        self.store.save_local(str(settings.vector_path))
        logger.info(f"Saved vector store to {settings.vector_path}")

    def load(self) -> None:
        path: Path = settings.vector_path
        if not path.exists():
            raise FileNotFoundError(path)
        self.store = FAISS.load_local(str(path), self.embeddings, allow_dangerous_deserialization=True)
        logger.info(f"Loaded vector store from {path}")