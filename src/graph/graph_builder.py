# graph_builder.py
from langgraph.graph import StateGraph
from nodes import (
    initialize_managers,
    check_vector_store,
    ingest_corpus,
    retrieve_documents,
    generate_outline,
    generate_answer
)
from typing import Dict, Any

def build_rag_graph() -> StateGraph:
    builder = StateGraph(state_schema=Dict[str, Any])
    
    # Add nodes
    builder.add_node("initialize_managers", initialize_managers)
    builder.add_node("check_vector_store", check_vector_store)
    builder.add_node("ingest_corpus", ingest_corpus)
    builder.add_node("retrieve_documents", retrieve_documents)
    builder.add_node("generate_outline", generate_outline)
    builder.add_node("generate_answer", generate_answer)

    # Set entry point
    builder.set_entry_point("initialize_managers")

    # Add edges
    builder.add_edge("initialize_managers", "check_vector_store")
    builder.add_conditional_edges(
        "check_vector_store",
        decide_ingestion_path,
        {
            "ingest_corpus": "ingest_corpus",
            "retrieve_documents": "retrieve_documents"
        }
    )
    builder.add_edge("ingest_corpus", "retrieve_documents")
    builder.add_edge("retrieve_documents", "generate_outline")
    builder.add_edge("generate_outline", "generate_answer")

    return builder.compile()

def decide_ingestion_path(state: Dict[str, Any]) -> str:
    return "ingest_corpus" if not state.get("vector_store_exists") else "retrieve_documents"