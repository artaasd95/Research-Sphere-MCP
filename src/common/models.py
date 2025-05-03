from dataclasses import dataclass
from typing import Dict, Any, List
from .interfaces import Document

@dataclass
class PDFDocument(Document):
    """Concrete implementation of Document for PDF files."""
    _content: str
    _metadata: Dict[str, Any]
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

@dataclass
class ArxivDocument(Document):
    """Concrete implementation of Document for arXiv papers."""
    _content: str
    _metadata: Dict[str, Any]
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata
    
    @property
    def title(self) -> str:
        return self._metadata.get('title', '')
    
    @property
    def authors(self) -> List[str]:
        return self._metadata.get('authors', [])
    
    @property
    def published(self) -> str:
        return self._metadata.get('published', '')
    
    @property
    def arxiv_id(self) -> str:
        return self._metadata.get('id', '')

@dataclass
class GraphNode:
    """Model for graph nodes."""
    id: str
    type: str
    properties: Dict[str, Any]

@dataclass
class GraphRelationship:
    """Model for graph relationships."""
    source: str
    target: str
    type: str
    properties: Dict[str, Any]

@dataclass
class GraphDocument:
    """Model for graph documents."""
    nodes: List[GraphNode]
    relationships: List[GraphRelationship] 