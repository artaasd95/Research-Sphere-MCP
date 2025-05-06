from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from loguru import logger
from ..core.config import settings

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        logger.info("DocumentProcessor initialized with chunk size {} and overlap {}", 
                   settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Process a list of documents by splitting them into chunks
        
        Args:
            documents (List[Document]): List of documents to process
            
        Returns:
            List[Document]: List of processed document chunks
        """
        try:
            logger.info(f"Processing {len(documents)} documents")
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
            return chunks
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            raise

    def add_metadata(self, documents: List[Document], metadata: Dict[str, Any]) -> List[Document]:
        """
        Add metadata to a list of documents
        
        Args:
            documents (List[Document]): List of documents to add metadata to
            metadata (Dict[str, Any]): Metadata to add to each document
            
        Returns:
            List[Document]: List of documents with added metadata
        """
        try:
            logger.info(f"Adding metadata to {len(documents)} documents")
            for doc in documents:
                doc.metadata.update(metadata)
            return documents
        except Exception as e:
            logger.error(f"Error adding metadata: {str(e)}")
            raise 