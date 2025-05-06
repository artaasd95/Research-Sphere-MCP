# Architecture Documentation

This document outlines the architecture of the MCP RAG System.

## System Overview

The MCP RAG System is a modern, scalable Retrieval-Augmented Generation system that combines document processing, vector storage, and language models to provide intelligent responses to user queries.

### High-Level Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │     │   Backend   │     │  Vector DB  │
│  (React)    │◄────┤  (FastAPI)  │◄────┤  (Chroma)   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  OpenAI API │
                    └─────────────┘
```

## Component Architecture

### Frontend Components

1. User Interface
   ```
   frontend/
   ├── src/
   │   ├── components/
   │   │   ├── Layout.tsx
   │   │   ├── Chat.tsx
   │   │   └── DocumentViewer.tsx
   │   ├── pages/
   │   │   ├── Home.tsx
   │   │   ├── Chat.tsx
   │   │   └── Settings.tsx
   │   ├── hooks/
   │   │   ├── useTheme.ts
   │   │   └── useChat.ts
   │   └── services/
   │       └── api.ts
   ```

2. State Management
   - React Query for server state
   - Context API for theme
   - Local storage for settings

### Backend Components

1. API Layer
   ```
   backend/
   ├── app/
   │   ├── api/
   │   │   └── endpoints/
   │   │       └── rag.py
   │   ├── core/
   │   │   ├── config.py
   │   │   └── security.py
   │   └── rag/
   │       ├── pipeline.py
   │       └── vector_store.py
   ```

2. RAG Pipeline
   - Document processing
   - Vector storage
   - Query processing
   - Response generation

## Data Flow

### Query Processing

1. User Query Flow
   ```
   User Query
      │
      ▼
   Frontend Validation
      │
      ▼
   API Request
      │
      ▼
   Backend Processing
      │
      ▼
   Vector Search
      │
      ▼
   LLM Generation
      │
      ▼
   Response
   ```

2. Document Processing Flow
   ```
   Document Upload
      │
      ▼
   File Validation
      │
      ▼
   Text Extraction
      │
      ▼
   Chunking
      │
      ▼
   Embedding
      │
      ▼
   Vector Storage
   ```

## Technical Stack

### Frontend

1. Core Technologies
   - React 18
   - TypeScript
   - Vite
   - Material-UI

2. State Management
   - React Query
   - Context API
   - Local Storage

3. Styling
   - Material-UI
   - CSS Modules
   - Theme Provider

### Backend

1. Core Technologies
   - Python 3.8+
   - FastAPI
   - Uvicorn
   - Pydantic

2. RAG Components
   - LangChain
   - OpenAI
   - Chroma DB

3. Utilities
   - Loguru
   - Python-dotenv
   - Pytest

## Database Schema

### Vector Store

1. Document Collection
   ```python
   class Document:
       id: str
       content: str
       metadata: Dict
       embedding: List[float]
   ```

2. Query Collection
   ```python
   class Query:
       id: str
       query: str
       response: str
       documents: List[str]
       timestamp: datetime
   ```

## API Design

### REST Endpoints

1. RAG Endpoints
   ```python
   @router.post("/query")
   async def process_query(query: QueryRequest):
       # Process query
       return response

   @router.post("/documents")
   async def upload_document(file: UploadFile):
       # Process document
       return document_id
   ```

2. Management Endpoints
   ```python
   @router.get("/health")
   async def health_check():
       # Check system health
       return status

   @router.get("/documents")
   async def list_documents():
       # List documents
       return documents
   ```

### WebSocket Endpoints

1. Real-time Communication
   ```python
   @app.websocket("/ws")
   async def websocket_endpoint(websocket: WebSocket):
       # Handle real-time updates
       await websocket.accept()
   ```

## Security Architecture

### Authentication

1. API Key Authentication
   ```python
   @app.middleware("http")
   async def verify_api_key(request: Request, call_next):
       # Verify API key
       return await call_next(request)
   ```

2. JWT Authentication
   ```python
   @app.middleware("http")
   async def verify_jwt(request: Request, call_next):
       # Verify JWT token
       return await call_next(request)
   ```

### Authorization

1. Role-Based Access
   ```python
   def check_permission(user: User, resource: str):
       # Check user permissions
       return has_permission
   ```

2. Resource Access
   ```python
   def check_resource_access(user: User, document: Document):
       # Check document access
       return has_access
   ```

## Monitoring and Logging

### Logging Architecture

1. Application Logs
   ```python
   logger = logging.getLogger("app")
   logger.info("Application started")
   ```

2. Access Logs
   ```python
   logger = logging.getLogger("access")
   logger.info(f"API access: {request}")
   ```

### Monitoring Architecture

1. Health Checks
   ```python
   @app.get("/health")
   async def health_check():
       return {
           "status": "healthy",
           "version": VERSION,
           "timestamp": datetime.now()
       }
   ```

2. Metrics
   ```python
   @app.get("/metrics")
   async def get_metrics():
       return {
           "requests": request_count,
           "errors": error_count,
           "latency": average_latency
       }
   ```

## Deployment Architecture

### Container Architecture

1. Docker Services
   ```yaml
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
   ```

2. Volume Management
   ```yaml
   volumes:
     data:
       driver: local
     logs:
       driver: local
   ```

### Scaling Architecture

1. Horizontal Scaling
   ```yaml
   services:
     backend:
       deploy:
         replicas: 3
   ```

2. Load Balancing
   ```nginx
   upstream backend {
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   ```

## Development Architecture

### Development Environment

1. Local Development
   ```bash
   # Backend
   uvicorn app.main:app --reload

   # Frontend
   npm run dev
   ```

2. Testing Environment
   ```bash
   # Backend tests
   pytest

   # Frontend tests
   npm test
   ```

### CI/CD Pipeline

1. Build Pipeline
   ```yaml
   stages:
     - build
     - test
     - deploy
   ```

2. Deployment Pipeline
   ```yaml
   deploy:
     stage: deploy
     script:
       - docker-compose up -d
   ```

## Performance Architecture

### Caching Strategy

1. Response Caching
   ```python
   @app.middleware("http")
   async def cache_middleware(request: Request, call_next):
       # Check cache
       return cached_response or await call_next(request)
   ```

2. Vector Cache
   ```python
   class VectorCache:
       def get(self, key: str) -> List[float]:
           # Get from cache
           return cached_vector
   ```

### Optimization Strategy

1. Query Optimization
   ```python
   def optimize_query(query: str) -> str:
       # Optimize query
       return optimized_query
   ```

2. Response Optimization
   ```python
   def optimize_response(response: str) -> str:
       # Optimize response
       return optimized_response
   ```

## Future Architecture

### Planned Improvements

1. Architecture Enhancements
   - Microservices architecture
   - Event-driven design
   - Real-time processing

2. Feature Additions
   - Multi-model support
   - Advanced analytics
   - Custom embeddings

### Scalability Roadmap

1. Infrastructure
   - Kubernetes deployment
   - Service mesh
   - Cloud-native design

2. Performance
   - Distributed processing
   - Advanced caching
   - Load balancing
``` 