from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from loguru import logger
import sys
import os
from datetime import datetime

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/app_{time}.log",
    rotation="500 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)

class RAGRequest(BaseModel):
    query: str
    max_sections: int = 5
    max_docs: int = 8
    user_id: Optional[str] = None

class RAGResponse(BaseModel):
    answer: str
    sections: List[str]
    documents_used: int
    processing_time: float
    timestamp: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize components
    logger.info("Initializing RAG system components...")
    try:
        # Initialize your components here
        app.state.rag_graph = None  # Replace with actual initialization
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {str(e)}")
        raise
    yield
    # Cleanup
    logger.info("Shutting down RAG system")

app = FastAPI(
    title="MCP RAG API Service",
    description="Advanced Retrieval-Augmented Generation API with enhanced logging and monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/generate", response_model=RAGResponse)
async def process_query(request: RAGRequest):
    """
    Process a query through the RAG pipeline
    
    Args:
        request (RAGRequest): The query request containing the question and parameters
        
    Returns:
        RAGResponse: The generated response with answer, sections, and metadata
    """
    start_time = datetime.utcnow()
    logger.info(f"Processing query: {request.query}")
    
    try:
        # Execute the RAG pipeline
        # Replace with actual implementation
        result = {
            "answer": "Sample answer",
            "sections": ["Section 1", "Section 2"],
            "documents_used": 2
        }
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        response = RAGResponse(
            **result,
            processing_time=processing_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Query processed successfully in {processing_time:.2f} seconds")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 