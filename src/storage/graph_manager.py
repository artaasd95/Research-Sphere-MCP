from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from common.interfaces import GraphStore, Document
from common.models import GraphNode, GraphRelationship, GraphDocument
from common.logger import logger

class Neo4jGraphStore(GraphStore):
    """Concrete implementation of GraphStore using Neo4j."""
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._verify_connection()
    
    def _verify_connection(self) -> None:
        """Verify the connection to the Neo4j database."""
        try:
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            raise Exception(f"Failed to connect to Neo4j: {str(e)}")
    
    def transform(self, documents: List[Document],
                 allowed_nodes: List[str],
                 allowed_relationships: List[tuple]) -> List[GraphDocument]:
        """Transform documents into graph format."""
        graph_docs = []
        
        for doc in documents:
            nodes = []
            relationships = []
            
            # Create paper node
            paper_node = GraphNode(
                id=doc.metadata.get('id', str(hash(doc.content))),
                type='Paper',
                properties={
                    'title': doc.metadata.get('title', ''),
                    'content': doc.content,
                    'source': doc.metadata.get('source', '')
                }
            )
            nodes.append(paper_node)
            
            # Create author nodes and relationships
            if 'authors' in doc.metadata:
                for author in doc.metadata['authors']:
                    author_node = GraphNode(
                        id=f"author_{hash(author)}",
                        type='Author',
                        properties={'name': author}
                    )
                    nodes.append(author_node)
                    
                    relationship = GraphRelationship(
                        source=paper_node.id,
                        target=author_node.id,
                        type='WRITTEN_BY',
                        properties={}
                    )
                    relationships.append(relationship)
            
            # Create citation relationships
            if 'citations' in doc.metadata:
                for citation in doc.metadata['citations']:
                    relationship = GraphRelationship(
                        source=paper_node.id,
                        target=citation,
                        type='CITES',
                        properties={}
                    )
                    relationships.append(relationship)
            
            graph_docs.append(GraphDocument(nodes=nodes, relationships=relationships))
        
        return graph_docs
    
    def ingest(self, graph_docs: List[GraphDocument]) -> None:
        """Ingest graph documents into the database."""
        with self.driver.session() as session:
            for doc in graph_docs:
                # Create nodes
                for node in doc.nodes:
                    session.run(
                        """
                        MERGE (n:Node {id: $id})
                        SET n.type = $type,
                            n.properties = $properties
                        """,
                        id=node.id,
                        type=node.type,
                        properties=node.properties
                    )
                
                # Create relationships
                for rel in doc.relationships:
                    session.run(
                        """
                        MATCH (source:Node {id: $source_id})
                        MATCH (target:Node {id: $target_id})
                        MERGE (source)-[r:RELATIONSHIP {type: $rel_type}]->(target)
                        SET r.properties = $properties
                        """,
                        source_id=rel.source,
                        target_id=rel.target,
                        rel_type=rel.type,
                        properties=rel.properties
                    )
        
        logger.info(f"Ingested {len(graph_docs)} graph documents")
    
    def query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a Cypher query."""
        try:
            with self.driver.session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")
    
    def close(self) -> None:
        """Close the database connection."""
        self.driver.close()
        logger.info("Closed Neo4j connection")