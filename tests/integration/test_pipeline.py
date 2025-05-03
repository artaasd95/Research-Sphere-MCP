import pytest
import asyncio
from unittest.mock import Mock, patch
from pathlib import Path
from storage.vector_store_manager import VectorStoreManager
from storage.graph_manager import GraphManager
from retrieval.retriever import KnowledgeRetriever
from generation.generator import LongAnswerGenerator

@pytest.fixture
def mock_components():
    """Create mock components for the pipeline."""
    vector_store = Mock()
    vector_store.search.return_value = [
        {'content': 'Test document 1', 'metadata': {'source': 'test1'}},
        {'content': 'Test document 2', 'metadata': {'source': 'test2'}}
    ]
    
    graph_manager = Mock()
    graph_manager.query.return_value = [
        {'n': {'title': 'Graph result 1', 'content': 'Graph content 1'}},
        {'n': {'title': 'Graph result 2', 'content': 'Graph content 2'}}
    ]
    
    generator = Mock()
    generator.generate.return_value = "Generated answer"
    
    return vector_store, graph_manager, generator

@pytest.mark.asyncio
async def test_complete_pipeline(mock_components):
    """Test the complete pipeline from ingestion to answer generation."""
    vector_store, graph_manager, generator = mock_components
    
    # Mock the ingest_corpus function
    async def mock_ingest_corpus(vsm, gm):
        return
    
    # Mock the document loaders
    with patch('loaders.pdf_loader.process_pdf_directory') as mock_pdf_loader, \
         patch('loaders.arxiv_loader.load_arxiv_documents') as mock_arxiv_loader:
        
        mock_pdf_loader.return_value = []
        mock_arxiv_loader.return_value = []
        
        # Create the pipeline components
        vsm = VectorStoreManager()
        vsm.vector_store = vector_store
        
        gm = GraphManager()
        gm.graph = graph_manager
        
        retriever = KnowledgeRetriever(vsm, gm)
        generator = LongAnswerGenerator()
        
        # Run the pipeline
        query = "Test query"
        hybrid = retriever.hybrid(query, k=2)
        docs = hybrid["vector"]
        
        # Generate sections
        sections = ["Introduction", "Background", "Conclusion"]
        
        # Generate answer
        answer = generator.generate(query, sections, docs)
        
        # Verify the results
        assert answer is not None
        assert isinstance(answer, str)
        assert len(answer) > 0
        
        # Verify component interactions
        assert vector_store.search.called
        assert graph_manager.query.called
        assert mock_pdf_loader.called
        assert mock_arxiv_loader.called

@pytest.mark.asyncio
async def test_pipeline_error_handling(mock_components):
    """Test error handling in the complete pipeline."""
    vector_store, graph_manager, generator = mock_components
    vector_store.search.side_effect = Exception("Vector store error")
    
    with pytest.raises(Exception):
        vsm = VectorStoreManager()
        vsm.vector_store = vector_store
        
        gm = GraphManager()
        gm.graph = graph_manager
        
        retriever = KnowledgeRetriever(vsm, gm)
        retriever.hybrid("test query", k=2)

@pytest.mark.asyncio
async def test_pipeline_with_empty_results(mock_components):
    """Test the pipeline with empty results from components."""
    vector_store, graph_manager, generator = mock_components
    vector_store.search.return_value = []
    graph_manager.query.return_value = []
    
    vsm = VectorStoreManager()
    vsm.vector_store = vector_store
    
    gm = GraphManager()
    gm.graph = graph_manager
    
    retriever = KnowledgeRetriever(vsm, gm)
    hybrid = retriever.hybrid("test query", k=2)
    
    assert len(hybrid["vector"]) == 0
    assert len(hybrid["graph"]) == 0

@pytest.mark.asyncio
async def test_pipeline_with_partial_results(mock_components):
    """Test the pipeline with partial results from components."""
    vector_store, graph_manager, generator = mock_components
    vector_store.search.return_value = []
    graph_manager.query.return_value = [
        {'n': {'title': 'Graph result', 'content': 'Graph content'}}
    ]
    
    vsm = VectorStoreManager()
    vsm.vector_store = vector_store
    
    gm = GraphManager()
    gm.graph = graph_manager
    
    retriever = KnowledgeRetriever(vsm, gm)
    hybrid = retriever.hybrid("test query", k=2)
    
    assert len(hybrid["vector"]) == 0
    assert len(hybrid["graph"]) == 1 