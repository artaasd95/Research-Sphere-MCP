import pytest
from unittest.mock import Mock, patch
from generation.generator import LongAnswerGenerator

@pytest.fixture
def sample_documents():
    return [
        {'content': 'Test document 1', 'metadata': {'source': 'test1'}},
        {'content': 'Test document 2', 'metadata': {'source': 'test2'}}
    ]

@pytest.fixture
def sample_sections():
    return [
        "Introduction",
        "Background",
        "Methodology",
        "Results",
        "Conclusion"
    ]

def test_generate_answer(mock_openai, sample_documents, sample_sections):
    """Test answer generation with valid inputs."""
    generator = LongAnswerGenerator()
    query = "Test query"
    
    with patch('generation.generator.ChatOpenAI') as mock_llm:
        mock_llm.return_value = Mock()
        mock_llm.return_value.invoke.return_value.content = "Generated answer"
        
        result = generator.generate(query, sample_sections, sample_documents)
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        assert mock_llm.called

def test_generate_answer_empty_inputs(mock_openai):
    """Test answer generation with empty inputs."""
    generator = LongAnswerGenerator()
    query = "Test query"
    
    with patch('generation.generator.ChatOpenAI') as mock_llm:
        mock_llm.return_value = Mock()
        mock_llm.return_value.invoke.return_value.content = "Generated answer"
        
        result = generator.generate(query, [], [])
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

def test_generate_answer_error_handling(mock_openai, sample_documents, sample_sections):
    """Test error handling in answer generation."""
    generator = LongAnswerGenerator()
    query = "Test query"
    
    with patch('generation.generator.ChatOpenAI') as mock_llm:
        mock_llm.return_value = Mock()
        mock_llm.return_value.invoke.side_effect = Exception("LLM error")
        
        with pytest.raises(Exception):
            generator.generate(query, sample_sections, sample_documents)

def test_generate_answer_section_handling(mock_openai, sample_documents):
    """Test handling of different section configurations."""
    generator = LongAnswerGenerator()
    query = "Test query"
    
    with patch('generation.generator.ChatOpenAI') as mock_llm:
        mock_llm.return_value = Mock()
        mock_llm.return_value.invoke.return_value.content = "Generated answer"
        
        # Test with single section
        result1 = generator.generate(query, ["Single Section"], sample_documents)
        
        # Test with many sections
        result2 = generator.generate(query, ["Section"] * 10, sample_documents)
        
        assert result1 is not None
        assert result2 is not None
        assert len(result1) > 0
        assert len(result2) > 0

def test_generate_answer_document_handling(mock_openai, sample_sections):
    """Test handling of different document configurations."""
    generator = LongAnswerGenerator()
    query = "Test query"
    
    with patch('generation.generator.ChatOpenAI') as mock_llm:
        mock_llm.return_value = Mock()
        mock_llm.return_value.invoke.return_value.content = "Generated answer"
        
        # Test with single document
        result1 = generator.generate(query, sample_sections, [{'content': 'Single doc'}])
        
        # Test with many documents
        result2 = generator.generate(query, sample_sections, [{'content': f'Doc {i}'} for i in range(10)])
        
        assert result1 is not None
        assert result2 is not None
        assert len(result1) > 0
        assert len(result2) > 0 