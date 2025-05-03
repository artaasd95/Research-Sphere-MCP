import pytest
from unittest.mock import Mock, patch
from retrieval.retriever import KnowledgeRetriever

@pytest.fixture
def mock_retriever_components():
    """Create mock components for the retriever."""
    vector_store = Mock()
    vector_store.search.return_value = [
        {'content': 'Vector result 1', 'metadata': {'source': 'test1'}},
        {'content': 'Vector result 2', 'metadata': {'source': 'test2'}}
    ]
    
    graph_manager = Mock()
    graph_manager.query.return_value = [
        {'n': {'title': 'Graph result 1', 'content': 'Graph content 1'}},
        {'n': {'title': 'Graph result 2', 'content': 'Graph content 2'}}
    ]
    
    return vector_store, graph_manager

def test_hybrid_retrieval(mock_retriever_components):
    """Test hybrid retrieval combining vector and graph results."""
    vector_store, graph_manager = mock_retriever_components
    retriever = KnowledgeRetriever(vector_store, graph_manager)
    
    result = retriever.hybrid("test query", k=2)
    
    assert 'vector' in result
    assert 'graph' in result
    assert len(result['vector']) == 2
    assert len(result['graph']) == 2
    assert vector_store.search.called
    assert graph_manager.query.called

def test_hybrid_retrieval_empty_results(mock_retriever_components):
    """Test hybrid retrieval with empty results."""
    vector_store, graph_manager = mock_retriever_components
    vector_store.search.return_value = []
    graph_manager.query.return_value = []
    
    retriever = KnowledgeRetriever(vector_store, graph_manager)
    result = retriever.hybrid("test query", k=2)
    
    assert len(result['vector']) == 0
    assert len(result['graph']) == 0

def test_hybrid_retrieval_partial_results(mock_retriever_components):
    """Test hybrid retrieval with partial results."""
    vector_store, graph_manager = mock_retriever_components
    vector_store.search.return_value = []
    graph_manager.query.return_value = [
        {'n': {'title': 'Graph result', 'content': 'Graph content'}}
    ]
    
    retriever = KnowledgeRetriever(vector_store, graph_manager)
    result = retriever.hybrid("test query", k=2)
    
    assert len(result['vector']) == 0
    assert len(result['graph']) == 1

def test_hybrid_retrieval_error_handling(mock_retriever_components):
    """Test error handling in hybrid retrieval."""
    vector_store, graph_manager = mock_retriever_components
    vector_store.search.side_effect = Exception("Vector store error")
    
    retriever = KnowledgeRetriever(vector_store, graph_manager)
    with pytest.raises(Exception):
        retriever.hybrid("test query", k=2)

def test_hybrid_retrieval_ranking(mock_retriever_components):
    """Test ranking of hybrid retrieval results."""
    vector_store, graph_manager = mock_retriever_components
    vector_store.search.return_value = [
        {'content': 'Relevant result', 'metadata': {'source': 'test1', 'score': 0.9}},
        {'content': 'Less relevant', 'metadata': {'source': 'test2', 'score': 0.5}}
    ]
    
    retriever = KnowledgeRetriever(vector_store, graph_manager)
    result = retriever.hybrid("test query", k=2)
    
    assert result['vector'][0]['metadata']['score'] > result['vector'][1]['metadata']['score'] 