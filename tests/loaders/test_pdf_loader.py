import pytest
from pathlib import Path
from unittest.mock import patch
from loaders.pdf_loader import process_pdf_directory

@pytest.mark.asyncio
async def test_process_pdf_directory_empty(temp_dir):
    """Test processing an empty directory."""
    result = await process_pdf_directory(temp_dir)
    assert len(result) == 0

@pytest.mark.asyncio
async def test_process_pdf_directory_with_pdf(sample_pdf_path):
    """Test processing a directory with a PDF file."""
    pdf_dir = sample_pdf_path.parent
    with patch('loaders.pdf_loader.PDFLoader') as mock_loader:
        mock_loader.return_value.load.return_value = [
            {'page_content': 'Test content', 'metadata': {'source': str(sample_pdf_path)}}
        ]
        result = await process_pdf_directory(pdf_dir)
        assert len(result) == 1
        assert result[0]['page_content'] == 'Test content'
        assert result[0]['metadata']['source'] == str(sample_pdf_path)

@pytest.mark.asyncio
async def test_process_pdf_directory_invalid_pdf(temp_dir):
    """Test processing a directory with an invalid PDF file."""
    invalid_pdf = temp_dir / "invalid.pdf"
    with open(invalid_pdf, 'w') as f:
        f.write("Not a PDF file")
    
    with pytest.raises(Exception):
        await process_pdf_directory(temp_dir)

@pytest.mark.asyncio
async def test_process_pdf_directory_multiple_files(temp_dir, sample_pdf_path):
    """Test processing a directory with multiple PDF files."""
    # Create another PDF file
    another_pdf = temp_dir / "another.pdf"
    with open(another_pdf, 'wb') as f:
        f.write(b'%PDF-1.4\n%EOF')
    
    with patch('loaders.pdf_loader.PDFLoader') as mock_loader:
        mock_loader.return_value.load.return_value = [
            {'page_content': 'Test content 1', 'metadata': {'source': str(sample_pdf_path)}},
            {'page_content': 'Test content 2', 'metadata': {'source': str(another_pdf)}}
        ]
        result = await process_pdf_directory(temp_dir)
        assert len(result) == 2
        assert all(doc['page_content'].startswith('Test content') for doc in result) 