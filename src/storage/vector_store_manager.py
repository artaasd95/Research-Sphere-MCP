from typing import List, Optional
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common.config import settings
from common.logger import logger
from common.interfaces import VectorStore

class FAISSVectorStore(VectorStore):
    """Concrete implementation of VectorStore using FAISS."""
    
    def __init__(self, embeddings_model: Optional[str] = None):
        self.embeddings = OpenAIEmbeddings(model=embeddings_model)
        self.vector_store: Optional[FAISS] = None
    
    def build(self, documents: List[Document]) -> None:
        """Build the vector store from documents."""
        try:
            texts = [doc.content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            self.vector_store = FAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
            logger.info(f"Built vector store with {len(documents)} documents")
        except Exception as e:
            raise Exception(f"Error building vector store: {str(e)}")
    
    def save(self, path: Path) -> None:
        """Save the vector store to disk."""
        if not self.vector_store:
            raise Exception("Vector store not initialized")
        
        try:
            self.vector_store.save_local(str(path))
            logger.info(f"Saved vector store to {path}")
        except Exception as e:
            raise Exception(f"Error saving vector store: {str(e)}")
    
    def load(self, path: Path) -> None:
        """Load the vector store from disk."""
        try:
            self.vector_store = FAISS.load_local(
                str(path),
                embeddings=self.embeddings
            )
            logger.info(f"Loaded vector store from {path}")
        except Exception as e:
            raise Exception(f"Error loading vector store: {str(e)}")
    
    def search(self, query: str, k: int = 5) -> List[Document]:
        """Search the vector store."""
        if not self.vector_store:
            raise Exception("Vector store not initialized")
        
        try:
            results = self.vector_store.similarity_search_with_score(
                query,
                k=k
            )
            return results
        except Exception as e:
            raise Exception(f"Error searching vector store: {str(e)}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add new documents to the vector store."""
        if not self.vector_store:
            raise Exception("Vector store not initialized")
        
        try:
            texts = [doc.content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            raise Exception(f"Error adding documents to vector store: {str(e)}")

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