# Contributing Guide

This guide provides information for contributors to the MCP RAG System.

## Getting Started

### Prerequisites

1. Development Tools
   - Git
   - Python 3.8+
   - Node.js 16+
   - Docker (optional)

2. Accounts
   - GitHub account
   - OpenAI API key

### Development Setup

1. Fork the Repository
   ```bash
   # Clone your fork
   git clone https://github.com/your-username/mcp-rag.git
   cd mcp-rag
   ```

2. Set up Backend
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Set up Frontend
   ```bash
   cd frontend
   npm install
   ```

## Development Workflow

### Branch Strategy

1. Main Branches
   - `main`: Production-ready code
   - `develop`: Development branch

2. Feature Branches
   ```bash
   # Create feature branch
   git checkout -b feature/your-feature-name
   ```

3. Bug Fix Branches
   ```bash
   # Create bug fix branch
   git checkout -b fix/your-bug-fix
   ```

### Code Style

1. Python Style
   - Follow PEP 8
   - Use type hints
   - Write docstrings
   ```python
   def process_document(document: Document) -> ProcessedDocument:
       """
       Process a document for the RAG system.

       Args:
           document: The document to process

       Returns:
           The processed document
       """
       # Implementation
   ```

2. TypeScript Style
   - Follow ESLint rules
   - Use TypeScript types
   - Write component documentation
   ```typescript
   interface ChatProps {
     /** The initial message to display */
     initialMessage?: string;
     /** Callback when a message is sent */
     onMessageSent?: (message: string) => void;
   }
   ```

### Testing

1. Backend Tests
   ```bash
   # Run all tests
   pytest

   # Run specific test
   pytest tests/test_document_processor.py

   # Run with coverage
   pytest --cov=app tests/
   ```

2. Frontend Tests
   ```bash
   # Run all tests
   npm test

   # Run specific test
   npm test -- -t "Chat component"

   # Run with coverage
   npm test -- --coverage
   ```

### Documentation

1. Code Documentation
   - Use docstrings for Python
   - Use JSDoc for TypeScript
   - Keep documentation up to date

2. API Documentation
   - Document all endpoints
   - Include request/response examples
   - Update OpenAPI spec

## Pull Request Process

### Creating a Pull Request

1. Update Documentation
   - Update README if needed
   - Add/update API documentation
   - Update changelog

2. Write Tests
   - Add unit tests
   - Add integration tests
   - Update existing tests

3. Submit PR
   - Use PR template
   - Link related issues
   - Request reviews

### PR Review Process

1. Code Review
   - Check code style
   - Verify tests
   - Review documentation

2. CI Checks
   - Run tests
   - Check linting
   - Verify builds

3. Merge Process
   - Squash commits
   - Update changelog
   - Merge to develop

## Development Guidelines

### Backend Development

1. API Design
   ```python
   @router.post("/query")
   async def process_query(
       query: QueryRequest,
       background_tasks: BackgroundTasks
   ) -> QueryResponse:
       """
       Process a query using the RAG system.

       Args:
           query: The query request
           background_tasks: Background tasks

       Returns:
           The query response
       """
       # Implementation
   ```

2. Error Handling
   ```python
   class RAGError(Exception):
       """Base exception for RAG system errors."""
       pass

   class DocumentProcessingError(RAGError):
       """Error during document processing."""
       pass
   ```

### Frontend Development

1. Component Design
   ```typescript
   const Chat: React.FC<ChatProps> = ({
     initialMessage,
     onMessageSent
   }) => {
     // Implementation
   };
   ```

2. State Management
   ```typescript
   const useChat = () => {
     const [messages, setMessages] = useState<Message[]>([]);
     const [loading, setLoading] = useState(false);

     // Implementation
   };
   ```

## Code Review Guidelines

### Review Checklist

1. Code Quality
   - [ ] Follows style guide
   - [ ] Has tests
   - [ ] Documentation complete

2. Functionality
   - [ ] Works as expected
   - [ ] Handles errors
   - [ ] Performance acceptable

3. Security
   - [ ] No sensitive data
   - [ ] Input validation
   - [ ] Error handling

### Review Process

1. Initial Review
   - Check PR description
   - Review changes
   - Run tests locally

2. Feedback
   - Provide constructive feedback
   - Suggest improvements
   - Request changes if needed

3. Approval
   - All checks pass
   - Documentation complete
   - Tests passing

## Release Process

### Versioning

1. Semantic Versioning
   - MAJOR: Breaking changes
   - MINOR: New features
   - PATCH: Bug fixes

2. Changelog
   ```markdown
   ## [1.1.0] - 2024-03-20
   ### Added
   - New feature X
   ### Changed
   - Updated feature Y
   ### Fixed
   - Bug fix Z
   ```

### Release Steps

1. Prepare Release
   ```bash
   # Update version
   npm version 1.1.0
   git tag v1.1.0
   ```

2. Create Release
   - Create GitHub release
   - Add release notes
   - Upload artifacts

3. Deploy
   - Deploy to staging
   - Run tests
   - Deploy to production

## Community Guidelines

### Communication

1. Issues
   - Use issue templates
   - Provide reproduction steps
   - Include error messages

2. Discussions
   - Be respectful
   - Provide context
   - Follow guidelines

### Code of Conduct

1. Behavior
   - Be respectful
   - Be inclusive
   - Be constructive

2. Enforcement
   - Report violations
   - Follow process
   - Respect decisions

## Development Tools

### Recommended Tools

1. IDE/Editor
   - VS Code
   - PyCharm
   - WebStorm

2. Extensions
   - Python
   - TypeScript
   - ESLint
   - Prettier

### Development Environment

1. Local Setup
   ```bash
   # Start backend
   cd backend
   uvicorn app.main:app --reload

   # Start frontend
   cd frontend
   npm run dev
   ```

2. Docker Setup
   ```bash
   # Start all services
   docker-compose up -d
   ```

## Troubleshooting

### Common Issues

1. Build Issues
   ```bash
   # Clean and rebuild
   npm clean-install
   pip install -r requirements.txt
   ```

2. Test Issues
   ```bash
   # Clear test cache
   pytest --cache-clear
   npm test -- --clearCache
   ```

### Getting Help

1. Documentation
   - Read the docs
   - Check examples
   - Search issues

2. Community
   - Ask in discussions
   - Join chat
   - Contact maintainers 