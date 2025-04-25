import asyncio
from loaders.pdf_loader import process_pdf_directory
from loaders.arxiv_loader import load_arxiv_documents
from storage.vector_store_manager import VectorStoreManager
from storage.graph_manager import GraphManager
from retrieval.retriever import KnowledgeRetriever
from generation.generator import LongAnswerGenerator
from common.logger import logger

async def ingest_corpus(vsm: VectorStoreManager, gm: GraphManager):
    # Example ingest: PDFs + arXiv
    pdf_docs = await process_pdf_directory(Path("./data/pdfs"))
    arxiv_docs = await load_arxiv_documents("retrieval augmented generation", max_docs=5)
    docs = pdf_docs + arxiv_docs

    vsm.build(docs)
    graph_docs = gm.transform(docs, allowed_nodes=["Paper"], allowed_relationships=[("Paper", "CITES", "Paper")])
    gm.ingest(graph_docs)

async def run_pipeline():
    vsm = VectorStoreManager()
    gm = GraphManager()

    # Ingest if no vector store present
    try:
        vsm.load()
        logger.info("Vector store loaded; skipping fresh ingest")
    except FileNotFoundError:
        logger.info("No vector store detected; ingesting corpus…")
        await ingest_corpus(vsm, gm)

    retriever = KnowledgeRetriever(vsm, gm)
    generator = LongAnswerGenerator()

    # ---- User query ----
    query = "What are the recent advancements in retrieval‑augmented generation?"
    hybrid = retriever.hybrid(query, k=8)
    docs = hybrid["vector"]  # list[Document]

    # Outline sections quickly with the LLM
    outline_llm = ChatOpenAI(model_name=settings.llm_model, temperature=0.3, api_key=settings.openai_api_key)
    outline_prompt = PromptTemplate.from_template("Create an outline of up to {n} sections for a technical report answering: {q}")
    outline_chain = LLMChain(llm=outline_llm, prompt=outline_prompt)
    outline = outline_chain.run(q=query, n=settings.max_sections)
    sections = [s.strip("• ") for s in outline.split("\n") if s.strip()][: settings.max_sections]

    answer = generator.generate(query, sections, docs)
    print("\n===== FINAL ANSWER =====\n")
    print(answer)

if __name__ == "__main__":
    asyncio.run(run_pipeline())