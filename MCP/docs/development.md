# Development Guide

This guide provides information for developers working on the MCP RAG System.

## Development Setup

### Prerequisites

1. Install development tools:
   ```bash
   # Backend
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   
   # Frontend
   npm install
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Development Environment

1. Backend Development:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn app.main:app --reload --port 8000
   ```

2. Frontend Development:
   ```bash
   cd frontend
   npm run dev
   ```

## Code Structure

### Backend Structure
```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── rag.py
│   ├── core/
│   │   ├── config.py
│   │   ├── auth.py
│   │   └── errors.py
│   ├── rag/
│   │   ├── document_processor.py
│   │   ├── pipeline.py
│   │   └── vector_store.py
│   └── main.py
├── tests/
│   ├── unit/
│   └── integration/
└── requirements.txt
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Chat.tsx
│   │   └── Settings.tsx
│   ├── hooks/
│   │   └── useTheme.ts
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   └── App.tsx
├── public/
└── package.json
```

## Development Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes:
   - Follow the coding style guide
   - Write tests for new features
   - Update documentation

3. Run tests:
   ```bash
   # Backend
   pytest
   
   # Frontend
   npm test
   ```

4. Submit a pull request:
   - Ensure CI passes
   - Get code review
   - Address feedback

## Best Practices

### Code Style

1. Backend (Python):
   - Follow PEP 8
   - Use type hints
   - Write docstrings
   - Keep functions small and focused

2. Frontend (TypeScript):
   - Follow ESLint rules
   - Use TypeScript types
   - Write component documentation
   - Follow React best practices

### Testing

1. Backend Tests:
   ```python
   # Example test
   def test_document_processor():
       processor = DocumentProcessor()
       result = processor.process_documents(documents)
       assert len(result) > 0
   ```

2. Frontend Tests:
   ```typescript
   // Example test
   test('renders chat interface', () => {
     render(<Chat />);
     expect(screen.getByPlaceholderText('Ask a question...')).toBeInTheDocument();
   });
   ```

### Documentation

1. Code Documentation:
   - Use docstrings for Python
   - Use JSDoc for TypeScript
   - Keep documentation up to date

2. API Documentation:
   - Document all endpoints
   - Include request/response examples
   - Update OpenAPI spec

## Debugging

### Backend Debugging

1. Enable debug logging:
   ```python
   logger.debug("Debug message")
   ```

2. Use debugger:
   ```python
   import pdb; pdb.set_trace()
   ```

### Frontend Debugging

1. Use React Developer Tools
2. Enable source maps
3. Use browser dev tools

## Performance Optimization

1. Backend:
   - Use async/await
   - Implement caching
   - Optimize database queries

2. Frontend:
   - Implement code splitting
   - Use React.memo
   - Optimize bundle size

## Security Considerations

1. API Security:
   - Validate input
   - Sanitize output
   - Use rate limiting

2. Frontend Security:
   - Sanitize user input
   - Use HTTPS
   - Implement CSP

## Deployment

1. Development:
   ```bash
   docker-compose up
   ```

2. Production:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [LangChain Documentation](https://python.langchain.com/) 