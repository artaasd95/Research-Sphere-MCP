from langgraph.graph import StateGraph
from nodes import base_nodes, retrieval_nodes, generation_nodes
from typing import Dict, Any

def build_rag_graph() -> StateGraph:
    builder = StateGraph(state_schema=Dict[str, Any])
    
    # Add system initialization nodes
    builder.add_node("initialize_managers", base_nodes.initialize_managers)
    builder.add_node("check_vector_store", base_nodes.check_vector_store)
    
    # Add data processing nodes
    builder.add_node("ingest_corpus", base_nodes.ingest_corpus)
    builder.add_node("retrieve_documents", retrieval_nodes.retrieve_documents)
    
    # Add generation nodes
    builder.add_node("generate_outline", generation_nodes.generate_outline)
    builder.add_node("generate_answer", generation_nodes.generate_answer)

    # Define workflow
    builder.set_entry_point("initialize_managers")
    
    builder.add_edge("initialize_managers", "check_vector_store")
    builder.add_conditional_edges(
        "check_vector_store",
        base_nodes.decide_ingestion_path,
        {
            "ingest_corpus": "ingest_corpus",
            "retrieve_documents": "retrieve_documents"
        }
    )
    builder.add_edge("ingest_corpus", "retrieve_documents")
    builder.add_edge("retrieve_documents", "generate_outline")
    builder.add_edge("generate_outline", "generate_answer")

    return builder.compile()