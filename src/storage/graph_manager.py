from typing import List, Tuple, Union
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.graphs import Neo4jGraph
from common.config import settings
from common.logger import logger

class GraphManager:
    def __init__(self):
        self.graph_db = Neo4jGraph(uri=settings.neo4j_uri, username=settings.neo4j_user, password=settings.neo4j_password)
        self.llm = ChatOpenAI(model_name=settings.llm_model, temperature=settings.temperature, api_key=settings.openai_api_key)

    def transform(self, docs: List[Document], allowed_nodes: List[str] | None = None, allowed_relationships: List[Union[str, Tuple]] | None = None, node_properties: List[str] | None = None) -> List[Document]:
        transformer = LLMGraphTransformer(
            llm=self.llm,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships,
            node_properties=node_properties,
        )
        return transformer.convert_to_graph_documents(docs)

    def ingest(self, graph_docs: List[Document]):
        logger.info(f"Ingesting {len(graph_docs)} graph docs into Neo4j")
        self.graph_db.add_graph_documents(graph_docs)

    def cypher(self, query: str, params: dict | None = None):
        return self.graph_db.query(query, params=params)