from typing import List, Dict, Any
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from loguru import logger
import os
from ..core.config import settings

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        self.vector_store = None
        self._initialize_vector_store()
        logger.info("VectorStoreManager initialized")

    def _initialize_vector_store(self):
        """Initialize or load the vector store"""
        try:
            if os.path.exists(settings.CHROMA_PERSIST_DIRECTORY):
                logger.info("Loading existing vector store")
                self.vector_store = Chroma(
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
            else:
                logger.info("Creating new vector store")
                self.vector_store = Chroma(
                    persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings
                )
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise

    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector store
        
        Args:
            documents (List[Document]): List of documents to add
        """
        try:
            logger.info(f"Adding {len(documents)} documents to vector store")
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            logger.info("Documents added and persisted successfully")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = settings.MAX_DOCS) -> List[Document]:
        """
        Perform similarity search on the vector store
        
        Args:
            query (str): Query string
            k (int): Number of results to return
            
        Returns:
            List[Document]: List of similar documents
        """
        try:
            logger.info(f"Performing similarity search for query: {query}")
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise

    def hybrid_search(self, query: str, k: int = settings.MAX_DOCS) -> Dict[str, List[Document]]:
        """
        Perform hybrid search combining similarity and keyword search
        
        Args:
            query (str): Query string
            k (int): Number of results to return
            
        Returns:
            Dict[str, List[Document]]: Dictionary containing both similarity and keyword search results
        """
        try:
            logger.info(f"Performing hybrid search for query: {query}")
            similarity_results = self.similarity_search(query, k=k)
            # Add keyword search results here if needed
            results = {
                "similarity": similarity_results,
                "keyword": []  # Implement keyword search if needed
            }
            logger.info(f"Hybrid search completed with {len(similarity_results)} results")
            return results
        except Exception as e:
            logger.error(f"Error performing hybrid search: {str(e)}")
            raise 