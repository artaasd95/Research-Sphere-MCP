import pytest
from unittest.mock import Mock, patch
from storage.graph_manager import GraphManager

@pytest.fixture
def sample_documents():
    return [
        {
            'title': 'Test Paper 1',
            'content': 'Test content 1',
            'citations': ['Test Paper 2']
        },
        {
            'title': 'Test Paper 2',
            'content': 'Test content 2',
            'citations': []
        }
    ]

def test_graph_manager_transform(sample_documents):
    """Test transforming documents into graph format."""
    gm = GraphManager()
    result = gm.transform(sample_documents, allowed_nodes=["Paper"], allowed_relationships=[("Paper", "CITES", "Paper")])
    
    assert len(result) == 2
    assert all('nodes' in doc for doc in result)
    assert all('relationships' in doc for doc in result)
    assert any(len(doc['relationships']) > 0 for doc in result)

def test_graph_manager_ingest(sample_documents):
    """Test ingesting documents into the graph database."""
    with patch('storage.graph_manager.Graph') as mock_graph:
        gm = GraphManager()
        graph_docs = gm.transform(sample_documents)
        gm.ingest(graph_docs)
        
        assert mock_graph.return_value.create.called
        assert mock_graph.return_value.create.call_count >= len(graph_docs)

def test_graph_manager_query():
    """Test querying the graph database."""
    with patch('storage.graph_manager.Graph') as mock_graph:
        mock_graph_instance = Mock()
        mock_graph_instance.run.return_value = [{'n': {'title': 'Test Paper'}}]
        mock_graph.return_value = mock_graph_instance
        
        gm = GraphManager()
        result = gm.query("MATCH (n) RETURN n")
        
        assert len(result) == 1
        assert result[0]['n']['title'] == 'Test Paper'
        assert mock_graph_instance.run.called

def test_graph_manager_error_handling():
    """Test error handling in graph operations."""
    gm = GraphManager()
    with pytest.raises(Exception):
        gm.query("INVALID QUERY")
    
    with pytest.raises(Exception):
        gm.ingest([{'invalid': 'format'}])

def test_graph_manager_allowed_nodes_relationships():
    """Test filtering of nodes and relationships."""
    gm = GraphManager()
    documents = [
        {
            'title': 'Test Paper',
            'content': 'Test content',
            'citations': ['Other Paper'],
            'invalid_node': 'Should be filtered'
        }
    ]
    
    result = gm.transform(
        documents,
        allowed_nodes=["Paper"],
        allowed_relationships=[("Paper", "CITES", "Paper")]
    )
    
    assert len(result) == 1
    assert all(node['type'] == 'Paper' for doc in result for node in doc['nodes'])
    assert all(rel['type'] == 'CITES' for doc in result for rel in doc['relationships']) 