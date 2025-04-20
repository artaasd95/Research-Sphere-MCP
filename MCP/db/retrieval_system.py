import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.graphs import Neo4jGraph
from langchain_openai import OpenAIEmbeddings

class KnowledgeRetriever:
    def __init__(
        self,
        vector_store_path: str = "./vector_store",
        neo4j_uri: str = "neo4j://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password",
        embedding_model: str = "text-embedding-3-small"
    ):
        """
        Initialize the knowledge retriever with connections to both storage systems.
        
        Args:
            vector_store_path: Path to saved FAISS vector store
            neo4j_uri: Neo4j connection URI
            neo4j_user: Database username
            neo4j_password: Database password
            embedding_model: Name of embedding model
        """
        # Initialize vector store
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = self._load_vector_store(vector_store_path)
        
        # Initialize graph connection
        self.graph_db = Neo4jGraph(
            uri=neo4j_uri,
            username=neo4j_user,
            password=neo4j_password
        )
    
    def _load_vector_store(self, path: str) -> FAISS:
        """Load existing vector store from disk"""
        if os.path.exists(path):
            return FAISS.load_local(
                folder_path=path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )
        raise FileNotFoundError(f"No vector store found at {path}")

    def vector_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict] = None
    ) -> List[Document]:
        """
        Retrieve documents from vector store using semantic search.
        
        Args:
            query: Search query text
            k: Number of results to return
            filter: Metadata filters
            
        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter
        )

    def graph_query(
        self,
        cypher_query: str,
        params: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query on the graph database.
        
        Args:
            cypher_query: Query to execute
            params: Query parameters
            
        Returns:
            List of query results as dictionaries
        """
        return self.graph_db.query(
            cypher_query,
            params=params
        )

    def hybrid_search(
        self,
        query: str,
        graph_pattern: str,
        k: int = 3
    ) -> Dict:
        """
        Combine vector and graph search results.
        
        Args:
            query: Semantic search query
            graph_pattern: Cypher MATCH pattern
            k: Number of vector results
            
        Returns:
            Combined results from both stores
        """
        # Vector search for documents
        vector_results = self.vector_search(query, k=k)
        
        # Graph search for related entities
        graph_results = self.graph_query(
            f"MATCH {graph_pattern} RETURN nodes, relationships LIMIT 10"
        )
        
        return {
            "vector_results": vector_results,
            "graph_results": graph_results
        }

    def get_document_context(
        self,
        entity_name: str,
        entity_type: str
    ) -> Dict:
        """
        Retrieve both document context and graph relationships for an entity.
        
        Args:
            entity_name: Name of the entity to search
            entity_type: Type of entity (Person, Organization, etc.)
            
        Returns:
            Combined document and graph information
        """
        # Find documents mentioning the entity
        docs = self.vector_search(entity_name, k=3)
        
        # Find graph relationships
        relationships = self.graph_query(
            """
            MATCH (e:{type})-[r]->(related)
            WHERE e.name = $name
            RETURN type(r) as relationship, related.name as entity
            """.format(type=entity_type),
            {"name": entity_name}
        )
        
        return {
            "documents": docs,
            "relationships": relationships
        }

# Example usage
if __name__ == "__main__":
    # Initialize retriever
    retriever = KnowledgeRetriever(
        vector_store_path="./vector_store",
        neo4j_uri="neo4j://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )
    
    # Example 1: Simple vector search
    vector_results = retriever.vector_search("quantum physics discoveries", k=2)
    print("Vector search results:")
    for doc in vector_results:
        print(f"- {doc.page_content[:100]}...")
    
    # Example 2: Graph query
    graph_results = retriever.graph_query("""
        MATCH (s:Scientist)-[r:DISCOVERED]->(d:Discovery)
        RETURN s.name, d.name, r.year
        LIMIT 5
    """)
    print("\nGraph relationships:")
    for result in graph_results:
        print(f"- {result['s.name']} discovered {result['d.name']} in {result['r.year']}")
    
    # Example 3: Hybrid search
    hybrid_results = retriever.hybrid_search(
        query="Marie Curie's contributions",
        graph_pattern="(s:Scientist {name: 'Marie Curie'})-[r]->(related)"
    )
    print("\nHybrid search documents:")
    for doc in hybrid_results['vector_results']:
        print(f"- {doc.page_content[:100]}...")
    
    print("\nHybrid search graph relationships:")
    for rel in hybrid_results['graph_results']:
        print(f"- {rel['nodes']} connected via {rel['relationships']}")
    
    # Example 4: Entity context retrieval
    context = retriever.get_document_context(
        entity_name="Albert Einstein",
        entity_type="Scientist"
    )
    print("\nEinstein context:")
    print("Documents mentioning Einstein:")
    for doc in context['documents']:
        print(f"- {doc.page_content[:100]}...")
    
    print("\nEinstein's relationships:")
    for rel in context['relationships']:
        print(f"- {rel['relationship']} with {rel['entity']}")