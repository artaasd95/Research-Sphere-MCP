from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from ..graph.graph_builder import build_rag_graph
from ..common.logger import logger
import uvicorn

class RAGRequest(BaseModel):
    query: str
    max_sections: int = 5
    max_docs: int = 8

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize graph once at startup
    app.state.rag_graph = build_rag_graph()
    logger.info("RAG graph initialized")
    yield
    # Cleanup resources
    logger.info("Shutting down RAG system")

app = FastAPI(
    title="RAG API Service",
    description="Advanced Retrieval-Augmented Generation API",
    lifespan=lifespan
)

@app.post("/generate")
async def process_query(request: RAGRequest):
    try:
        state = {
            "query": request.query,
            "max_sections": request.max_sections,
            "max_docs": request.max_docs
        }
        
        # Execute the LangGraph pipeline
        async for step in app.state.rag_graph.astream(state):
            logger.debug(f"Processing step: {step['node']}")
            
            # Handle intermediate errors
            if "error" in step["state"]:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error in {step['node']}: {step['state']['error']}"
                )
        
        return {
            "answer": state["answer"],
            "sections": state["sections"],
            "documents_used": len(state["docs"])
        }
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug_mode
    )