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
    state["retriever"] = KnowledgeRetriever(state["vsm"], state["gm"])
    state["generator"] = LongAnswerGenerator()
    return state

async def check_vector_store(state: Dict[str, Any]) -> Dict[str, Any]:
    try:
        state["vsm"].load()
        logger.info("Vector store loaded")
        state["vector_store_exists"] = True
    except FileNotFoundError:
        logger.info("Vector store not found")
        state["vector_store_exists"] = False
    return state

async def ingest_corpus(state: Dict[str, Any]) -> Dict[str, Any]:
    pdf_docs = await process_pdf_directory(Path("./data/pdfs"))
    arxiv_docs = await load_arxiv_documents("retrieval augmented generation", max_docs=5)
    docs = pdf_docs + arxiv_docs
    
    state["vsm"].build(docs)
    graph_docs = state["gm"].transform(
        docs,
        allowed_nodes=["Paper"],
        allowed_relationships=[("Paper", "CITES", "Paper")]
    )
    state["gm"].ingest(graph_docs)
    return state

async def retrieve_documents(state: Dict[str, Any]) -> Dict[str, Any]:
    hybrid_results = state["retriever"].hybrid(state["query"], k=8)
    state["docs"] = hybrid_results["vector"]
    return state

async def generate_outline(state: Dict[str, Any]) -> Dict[str, Any]:
    llm = ChatOpenAI(
        model_name=settings.llm_model,
        temperature=0.3,
        api_key=settings.openai_api_key
    )
    prompt = PromptTemplate.from_template(
        "Create an outline of up to {n} sections for a technical report answering: {q}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    outline = await chain.arun(q=state["query"], n=settings.max_sections)
    state["sections"] = [
        s.strip("• ") for s in outline.split("\n") 
        if s.strip()
    ][:settings.max_sections]
    return state

async def generate_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    answer = await state["generator"].agenerate(
        state["query"],
        state["sections"],
        state["docs"]
    )
    state["answer"] = answer
    return state