# API Documentation

This document provides detailed information about the MCP RAG System API endpoints.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.your-domain.com`

## Authentication

The API uses API key authentication. Include your API key in the request header:

```http
X-API-Key: your-api-key
```

## Endpoints

### RAG Query

Process a query using the RAG system.

```http
POST /api/v1/rag/query
```

#### Request Body

```json
{
  "query": "string",
  "max_documents": 5,
  "temperature": 0.7
}
```

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| query | string | The question to process | Required |
| max_documents | integer | Maximum number of documents to retrieve | 5 |
| temperature | float | Response temperature (0.0 to 1.0) | 0.7 |

#### Response

```json
{
  "response": "string",
  "documents": [
    {
      "content": "string",
      "metadata": {
        "source": "string",
        "page": "integer"
      }
    }
  ],
  "processing_time": "float",
  "token_usage": {
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "total_tokens": "integer"
  }
}
```

### Health Check

Check the API health status.

```http
GET /api/v1/health
```

#### Response

```json
{
  "status": "healthy",
  "version": "string",
  "timestamp": "string"
}
```

### Document Management

#### Upload Document

Upload a new document to the system.

```http
POST /api/v1/documents
```

##### Request Body (multipart/form-data)

| Parameter | Type | Description |
|-----------|------|-------------|
| file | file | Document file (PDF, TXT, DOCX) |
| metadata | string | JSON string with document metadata |

##### Response

```json
{
  "document_id": "string",
  "status": "success",
  "message": "string"
}
```

#### List Documents

Get a list of all documents.

```http
GET /api/v1/documents
```

##### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| page | integer | Page number | 1 |
| limit | integer | Items per page | 10 |
| search | string | Search query | null |

##### Response

```json
{
  "documents": [
    {
      "id": "string",
      "filename": "string",
      "upload_date": "string",
      "metadata": {
        "source": "string",
        "page_count": "integer"
      }
    }
  ],
  "total": "integer",
  "page": "integer",
  "pages": "integer"
}
```

#### Delete Document

Delete a document from the system.

```http
DELETE /api/v1/documents/{document_id}
```

##### Response

```json
{
  "status": "success",
  "message": "string"
}
```

## Error Handling

The API uses standard HTTP status codes and returns error responses in the following format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- 100 requests per minute for authenticated users
- 10 requests per minute for unauthenticated users

Rate limit headers are included in the response:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1620000000
```

## WebSocket API

The system also provides a WebSocket API for real-time communication.

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

### Events

#### Query Event

```javascript
ws.send(JSON.stringify({
  type: 'query',
  data: {
    query: 'string',
    max_documents: 5
  }
}));
```

#### Response Event

```javascript
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  // Handle response
};
```

## SDK Examples

### Python

```python
import requests

API_KEY = 'your-api-key'
BASE_URL = 'http://localhost:8000'

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Query endpoint
response = requests.post(
    f'{BASE_URL}/api/v1/rag/query',
    headers=headers,
    json={
        'query': 'What is RAG?',
        'max_documents': 5
    }
)

print(response.json())
```

### JavaScript

```javascript
const API_KEY = 'your-api-key';
const BASE_URL = 'http://localhost:8000';

async function queryRAG(query) {
  const response = await fetch(`${BASE_URL}/api/v1/rag/query`, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query,
      max_documents: 5
    })
  });

  return response.json();
}
```

## Versioning

The API uses semantic versioning. The current version is v1.

To specify a version, include it in the URL:

```http
/api/v1/rag/query
```

## Changelog

### v1.0.0 (2024-03-20)
- Initial release
- Basic RAG functionality
- Document management
- WebSocket support 