from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from loguru import logger
from ...rag.pipeline import RAGPipeline
from ...core.config import settings

router = APIRouter()
pipeline = RAGPipeline()

class QueryRequest(BaseModel):
    query: str
    max_sections: Optional[int] = settings.MAX_SECTIONS
    max_docs: Optional[int] = settings.MAX_DOCS

class QueryResponse(BaseModel):
    answer: str
    sections: List[str]
    documents_used: int
    processing_time: float
    timestamp: str

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query through the RAG pipeline
    
    Args:
        request (QueryRequest): The query request containing the question and parameters
        
    Returns:
        QueryResponse: The generated response with answer and metadata
    """
    start_time = datetime.utcnow()
    logger.info(f"Received query request: {request.query}")
    
    try:
        result = await pipeline.process_query(
            query=request.query,
            max_sections=request.max_sections
        )
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        response = QueryResponse(
            **result,
            processing_time=processing_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Query processed successfully in {processing_time:.2f} seconds")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    } 