from typing import List, Dict, Any
from langchain_core.documents import Document
from storage.vector_store_manager import VectorStoreManager
from storage.graph_manager import GraphManager
from common.logger import logger
from common.interfaces import Retriever, VectorStore, GraphStore

class HybridRetriever(Retriever):
    """Concrete implementation of Retriever using hybrid vector and graph search."""
    
    def __init__(self, vector_store: VectorStore, graph_store: GraphStore):
        self.vector_store = vector_store
        self.graph_store = graph_store
    
    def retrieve(self, query: str, k: int = 5) -> Dict[str, List[Document]]:
        """Retrieve relevant documents using hybrid search."""
        try:
            # Vector search
            vector_results = self.vector_store.search(query, k=k)
            
            # Graph search
            graph_query = self._build_graph_query(query)
            graph_results = self.graph_store.query(graph_query)
            
            return {
                'vector': vector_results,
                'graph': self._convert_graph_results(graph_results)
            }
        except Exception as e:
            raise Exception(f"Error in hybrid retrieval: {str(e)}")
    
    def _build_graph_query(self, query: str) -> str:
        """Build a Cypher query for graph search."""
        return f"""
        MATCH (n:Node)
        WHERE n.properties.title CONTAINS '{query}'
           OR n.properties.content CONTAINS '{query}'
        RETURN n
        LIMIT 5
        """
    
    def _convert_graph_results(self, results: List[Dict[str, Any]]) -> List[Document]:
        """Convert graph results to Document format."""
        documents = []
        for result in results:
            node = result.get('n', {})
            if node:
                doc = Document(
                    content=node.get('properties', {}).get('content', ''),
                    metadata={
                        'title': node.get('properties', {}).get('title', ''),
                        'type': node.get('type', ''),
                        'id': node.get('id', '')
                    }
                )
                documents.append(doc)
        return documents
    
    def set_vector_store(self, vector_store: VectorStore) -> None:
        """Update the vector store."""
        self.vector_store = vector_store
    
    def set_graph_store(self, graph_store: GraphStore) -> None:
        """Update the graph store."""
        self.graph_store = graph_store

class KnowledgeRetriever:
    def __init__(self, vsm: VectorStoreManager, gm: GraphManager):
        self.vsm = vsm
        self.gm = gm

    # --- Vector ---
    def vector_search(self, query: str, k: int = 5) -> List[Document]:
        logger.info(f"Vector search: '{query}' (k={k})")
        return self.vsm.store.similarity_search(query, k=k)

    # --- Graph ---
    def related_papers(self, title: str) -> List[Dict[str, Any]]:
        query = (
            "MATCH (p:Paper {title: $title})-[:CITES|:RELATED_TO*1..2]-(r:Paper) "
            "RETURN r.title as title, r.year as year LIMIT 10"
        )
        return self.gm.cypher(query, {"title": title})

    # --- Hybrid ---
    def hybrid(self, query: str, k: int = 5) -> Dict[str, Any]:
        vector_docs = self.vector_search(query, k=k)
        related = []
        if vector_docs:
            related = self.related_papers(vector_docs[0].metadata.get("title", ""))
        return {"vector": vector_docs, "graph": related}