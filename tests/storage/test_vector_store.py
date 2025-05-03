import pytest
from unittest.mock import Mock, patch
from storage.vector_store_manager import VectorStoreManager

@pytest.fixture
def sample_documents():
    return [
        {'page_content': 'Test document 1', 'metadata': {'source': 'test1'}},
        {'page_content': 'Test document 2', 'metadata': {'source': 'test2'}}
    ]

def test_vector_store_build(sample_documents):
    """Test building the vector store."""
    with patch('storage.vector_store_manager.FAISS') as mock_faiss:
        vsm = VectorStoreManager()
        vsm.build(sample_documents)
        assert mock_faiss.from_documents.called
        assert len(mock_faiss.from_documents.call_args[0][0]) == 2

def test_vector_store_save_load(temp_dir, sample_documents):
    """Test saving and loading the vector store."""
    with patch('storage.vector_store_manager.FAISS') as mock_faiss:
        # Test save
        vsm = VectorStoreManager()
        vsm.build(sample_documents)
        vsm.save(temp_dir)
        assert mock_faiss.save_local.called
        
        # Test load
        vsm.load(temp_dir)
        assert mock_faiss.load_local.called

def test_vector_store_search(sample_documents):
    """Test searching the vector store."""
    with patch('storage.vector_store_manager.FAISS') as mock_faiss:
        mock_faiss_instance = Mock()
        mock_faiss_instance.similarity_search.return_value = sample_documents
        mock_faiss.from_documents.return_value = mock_faiss_instance
        
        vsm = VectorStoreManager()
        vsm.build(sample_documents)
        results = vsm.search("test query", k=2)
        
        assert len(results) == 2
        assert mock_faiss_instance.similarity_search.called
        assert mock_faiss_instance.similarity_search.call_args[1]['k'] == 2

def test_vector_store_error_handling():
    """Test error handling in vector store operations."""
    vsm = VectorStoreManager()
    with pytest.raises(Exception):
        vsm.load("nonexistent_path")
    
    with pytest.raises(Exception):
        vsm.search("test query") 