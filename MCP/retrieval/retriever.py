from typing import List, Dict, Any
from langchain_core.documents import Document
from storage.vector_store_manager import VectorStoreManager
from storage.graph_manager import GraphManager
from common.logger import logger

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