import os
from typing import List, Optional, Tuple, Union
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import FAISS

class KnowledgePipeline:
    def __init__(
        self,
        llm_model: str = "gpt-4-turbo",
        embedding_model: str = "text-embedding-3-small",
        temperature: float = 0.0,
        api_key: Optional[str] = None
    ):
        """
        Initialize the knowledge processing pipeline with graph and vector storage.
        
        Args:
            llm_model: LLM for graph transformation
            embedding_model: Embedding model for vector storage
            temperature: Model creativity control
            api_key: API key for services
        """
        self.llm = ChatOpenAI(
            temperature=temperature,
            model_name=llm_model,
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        
        self.vector_store: Optional[FAISS] = None
        self.graph_db: Optional[Neo4jGraph] = None

    def init_vector_store(self, documents: List[Document]) -> None:
        """Initialize or update the vector store with documents"""
        if self.vector_store:
            self.vector_store.add_documents(documents)
        else:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)

    def init_graph_db(self, uri: str, username: str, password: str) -> None:
        """Initialize graph database connection"""
        self.graph_db = Neo4jGraph(
            uri=uri,
            username=username,
            password=password
        )

    def create_graph_transformer(
        self,
        allowed_nodes: Optional[List[str]] = None,
        allowed_relationships: Optional[List[Union[str, Tuple]]] = None,
        node_properties: Optional[List[str]] = None
    ) -> LLMGraphTransformer:
        """Create a configured graph transformer"""
        return LLMGraphTransformer(
            llm=self.llm,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships,
            node_properties=node_properties
        )

    def process_to_graph(
        self,
        transformer: LLMGraphTransformer,
        documents: List[Document]
    ) -> List[Document]:
        """Convert documents to graph format"""
        return transformer.convert_to_graph_documents(documents)

    def save_to_graph(self, graph_documents: List[Document]) -> None:
        """Save graph documents to connected graph DB"""
        if not self.graph_db:
            raise ValueError("Graph database not initialized")
        self.graph_db.add_graph_documents(graph_documents)

    def vector_search(self, query: str, k: int = 5) -> List[Document]:
        """Search in vector store"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        return self.vector_store.similarity_search(query, k=k)

    async def full_pipeline(
        self,
        documents: List[Document],
        graph_config: dict
    ) -> None:
        """Complete processing pipeline: vector storage + graph transformation"""
        # Store original documents in vector DB
        self.init_vector_store(documents)
        
        # Create and configure graph transformer
        transformer = self.create_graph_transformer(**graph_config)
        
        # Process to graph format
        graph_docs = self.process_to_graph(transformer, documents)
        
        # Save to graph database
        if self.graph_db:
            self.save_to_graph(graph_docs)

# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = KnowledgePipeline()
    
    # Load documents from any source
    documents = [Document(page_content="""
        Albert Einstein (1879-1955) was a German-born theoretical physicist
        who developed the theory of relativity. He worked at the Swiss Patent Office
        and later became a professor at the University of Berlin. Awarded the 1921
        Nobel Prize in Physics for his explanation of the photoelectric effect.
    """)]
    
    # Configure graph transformation
    graph_config = {
        "allowed_nodes": ["Scientist", "Institution", "Discovery"],
        "allowed_relationships": [
            ("Scientist", "WORKED_AT", "Institution"),
            ("Scientist", "DISCOVERED", "Discovery")
        ],
        "node_properties": ["birth_year", "award_year"]
    }
    
    # Initialize graph database connection
    pipeline.init_graph_db(
        uri="neo4j://localhost:7687",
        username="neo4j",
        password="password"
    )
    
    # Run complete processing pipeline
    import asyncio
    asyncio.run(pipeline.full_pipeline(documents, graph_config))
    
    # Search in vector store
    results = pipeline.vector_search("German physicist relativity theory")
    print(f"Vector search results: {results[0].page_content[:100]}...")
    
    # Retrieve from graph DB (example)
    if pipeline.graph_db:
        query = """
        MATCH (s:Scientist)-[r:DISCOVERED]->(d:Discovery)
        RETURN s.name, r.type, d.name
        """
        graph_results = pipeline.graph_db.query(query)
        print("Graph relationships:", graph_results)