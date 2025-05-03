import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test response'
                }
            }]
        }
        yield mock

@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a sample PDF file for testing."""
    pdf_path = temp_dir / "test.pdf"
    # Create a minimal PDF file
    with open(pdf_path, 'wb') as f:
        f.write(b'%PDF-1.4\n%EOF')
    return pdf_path

@pytest.fixture
def mock_arxiv_response():
    """Mock arXiv API response."""
    return {
        'entries': [
            {
                'title': 'Test Paper 1',
                'summary': 'Test summary 1',
                'authors': [{'name': 'Author 1'}],
                'published': '2024-01-01',
                'id': '1234.5678'
            }
        ]
    }

@pytest.fixture
def mock_vector_store():
    """Mock vector store for testing."""
    store = Mock()
    store.search.return_value = [
        {'content': 'Test document 1', 'metadata': {'source': 'test1'}},
        {'content': 'Test document 2', 'metadata': {'source': 'test2'}}
    ]
    return store

@pytest.fixture
def mock_graph_manager():
    """Mock graph manager for testing."""
    manager = Mock()
    manager.transform.return_value = [
        {'nodes': [{'id': '1', 'type': 'Paper'}], 'relationships': []}
    ]
    return manager 