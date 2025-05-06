# MCP RAG System

A modern, scalable Retrieval-Augmented Generation (RAG) system with a beautiful frontend interface. This system provides advanced document processing, semantic search, and AI-powered response generation capabilities.

## Features

- **Advanced RAG Pipeline**
  - Document processing and chunking
  - Vector-based semantic search
  - Hybrid search capabilities
  - Structured response generation with outlines

- **Modern Frontend**
  - React-based user interface
  - Light and dark mode support
  - Real-time response streaming
  - Interactive document visualization

- **Robust Backend**
  - FastAPI-based REST API
  - Comprehensive logging and monitoring
  - Scalable architecture
  - Async processing support

## Project Structure

```
MCP/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   ├── core/
│   │   ├── rag/
│   │   ├── utils/
│   │   └── models/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── docs/
```

## Setup and Installation

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## API Documentation

The API documentation is available at `/docs` when running the backend server. Key endpoints include:

- `POST /api/v1/rag/query`: Process a query through the RAG pipeline
- `GET /api/v1/rag/health`: Health check endpoint

## Logging and Monitoring

The system includes comprehensive logging:

- Console logging with colored output
- File-based logging with rotation
- Performance metrics tracking
- Error tracking and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- LangChain for the RAG framework
- FastAPI for the backend framework
- React for the frontend framework
- OpenAI for the language models 