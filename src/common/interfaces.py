from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path

class Document(ABC):
    """Abstract base class for documents."""
    @property
    @abstractmethod
    def content(self) -> str:
        pass
    
    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        pass

class DocumentLoader(ABC):
    """Interface for document loaders."""
    @abstractmethod
    async def load(self, source: Any) -> List[Document]:
        pass

class VectorStore(ABC):
    """Interface for vector stores."""
    @abstractmethod
    def build(self, documents: List[Document]) -> None:
        pass
    
    @abstractmethod
    def save(self, path: Path) -> None:
        pass
    
    @abstractmethod
    def load(self, path: Path) -> None:
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Document]:
        pass

class GraphStore(ABC):
    """Interface for graph stores."""
    @abstractmethod
    def transform(self, documents: List[Document], 
                 allowed_nodes: List[str],
                 allowed_relationships: List[tuple]) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def ingest(self, graph_docs: List[Dict[str, Any]]) -> None:
        pass
    
    @abstractmethod
    def query(self, query: str) -> List[Dict[str, Any]]:
        pass

class Retriever(ABC):
    """Interface for retrievers."""
    @abstractmethod
    def retrieve(self, query: str, k: int = 5) -> Dict[str, List[Document]]:
        pass

class AnswerGenerator(ABC):
    """Interface for answer generators."""
    @abstractmethod
    def generate(self, query: str, 
                sections: List[str],
                documents: List[Document]) -> str:
        pass

class Pipeline(ABC):
    """Interface for the main pipeline."""
    @abstractmethod
    async def run(self, query: str) -> str:
        pass 