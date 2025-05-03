import pytest
from unittest.mock import patch
from loaders.arxiv_loader import load_arxiv_documents

@pytest.mark.asyncio
async def test_load_arxiv_documents_success(mock_arxiv_response):
    """Test successful loading of arXiv documents."""
    with patch('arxiv.Client.results') as mock_results:
        mock_results.return_value = mock_arxiv_response
        result = await load_arxiv_documents("test query", max_docs=1)
        
        assert len(result) == 1
        assert result[0]['title'] == 'Test Paper 1'
        assert result[0]['summary'] == 'Test summary 1'
        assert result[0]['authors'] == ['Author 1']
        assert result[0]['published'] == '2024-01-01'
        assert result[0]['id'] == '1234.5678'

@pytest.mark.asyncio
async def test_load_arxiv_documents_empty_response():
    """Test handling of empty arXiv response."""
    with patch('arxiv.Client.results') as mock_results:
        mock_results.return_value = {'entries': []}
        result = await load_arxiv_documents("test query", max_docs=1)
        assert len(result) == 0

@pytest.mark.asyncio
async def test_load_arxiv_documents_error():
    """Test handling of arXiv API errors."""
    with patch('arxiv.Client.results') as mock_results:
        mock_results.side_effect = Exception("API Error")
        with pytest.raises(Exception):
            await load_arxiv_documents("test query", max_docs=1)

@pytest.mark.asyncio
async def test_load_arxiv_documents_max_docs():
    """Test limiting the number of documents returned."""
    with patch('arxiv.Client.results') as mock_results:
        mock_results.return_value = {
            'entries': [
                {'title': f'Test Paper {i}', 'summary': f'Test summary {i}'}
                for i in range(10)
            ]
        }
        result = await load_arxiv_documents("test query", max_docs=3)
        assert len(result) == 3 