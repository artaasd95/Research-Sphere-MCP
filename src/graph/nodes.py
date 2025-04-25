# nodes.py
import asyncio
from pathlib import Path
from typing import Dict, Any
from loaders.pdf_loader import process_pdf_directory
from loaders.arxiv_loader import load_arxiv_documents
from storage.vector_store_manager import VectorStoreManager
from storage.graph_manager import GraphManager
from retrieval.retriever import KnowledgeRetriever
from generation.generator import LongAnswerGenerator
from common.logger import logger
from common.config import settings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

async def initialize_managers(state: Dict[str, Any]) -> Dict[str, Any]:
    state["vsm"] = VectorStoreManager()
    state["gm"] = GraphManager()
    return state

async def check_vector_store(state: Dict[str, Any]) -> Dict[str, Any]:
    try:
        state["vsm"].load()
        state["vector_store_exists"] = True
    except FileNotFoundError:
        state["vector_store_exists"] = False
    return state

def decide_ingestion_path(state: Dict[str, Any]) -> str:
    return "ingest_corpus" if not state.get("vector_store_exists") else "retrieve_documents"

# nodes/retrieval_nodes.py
async def ingest_corpus(state: Dict[str, Any]) -> Dict[str, Any]:
    pdf_docs = await process_pdf_directory(Path("./data/pdfs"))
    arxiv_docs = await load_arxiv_documents(state["query"], max_docs=5)
    docs = pdf_docs + arxiv_docs
    # ... rest of ingestion logic ...
    return state

async def retrieve_documents(state: Dict[str, Any]) -> Dict[str, Any]:
    retriever = KnowledgeRetriever(state["vsm"], state["gm"])
    hybrid = retriever.hybrid(state["query"], k=8)
    state["docs"] = hybrid["vector"]
    return state

# nodes/generation_nodes.py
async def generate_outline(state: Dict[str, Any]) -> Dict[str, Any]:
    prompt_template = """Generate a comprehensive outline for a technical report on: {query}
    Requirements:
    - Maximum {max_sections} sections
    - Include both theoretical and practical aspects
    - Prioritize recent developments (last 2-3 years)
    - Format sections as markdown headers (## Section Title)
    
    Output format:
    1. Section 1 Title
    2. Section 2 Title
    ..."""
    
    prompt = PromptTemplate.from_template(prompt_template)
    chain = LLMChain(
        llm=ChatOpenAI(model_name=settings.llm_model, temperature=0.3),
        prompt=prompt
    )
    outline = await chain.arun(
        query=state["query"],
        max_sections=state.get("max_sections", 5)
    )
    state["sections"] = [s.strip() for s in outline.split("\n") if s.strip()]
    return state

async def generate_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    generator = LongAnswerGenerator()
    answer = await generator.agenerate(
        state["query"],
        state["sections"],
        state["docs"]
    )
    state["answer"] = answer
    return state