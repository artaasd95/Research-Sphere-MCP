# Getting Started with MCP RAG System

This guide will help you get up and running with the MCP RAG System quickly.

## System Requirements

### Backend Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- OpenAI API key

### Frontend Requirements
- Node.js 16 or higher
- npm 7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation Guide

### Option 1: Standalone Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/mcp-rag.git
   cd mcp-rag
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Configure environment variables:
   ```bash
   # Backend (.env)
   OPENAI_API_KEY=your-api-key-here
   SECRET_KEY=your-secret-key-here
   
   # Frontend (env.example -> .env)
   VITE_API_URL=http://localhost:8000
   VITE_OPENAI_API_KEY=your-api-key-here
   ```

### Option 2: Docker Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/mcp-rag.git
   cd mcp-rag
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the system:
   ```bash
   docker-compose up -d
   ```

## Quick Start Guide

### Running the System

#### Standalone Mode
1. Start the backend:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the system:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

#### Docker Mode
1. Start all services:
   ```bash
   docker-compose up -d
   ```

2. Access the system:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### First Steps

1. Open the frontend in your browser
2. Navigate to Settings and configure your API key
3. Try the chat interface with a sample query
4. Check the response and adjust settings as needed

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Check if the backend is running
   - Verify the API URL in frontend settings
   - Check CORS configuration

2. **API Key Issues**
   - Ensure the API key is correctly set in both frontend and backend
   - Check if the API key has sufficient permissions
   - Verify the API key format

3. **Docker Issues**
   - Check if Docker is running
   - Verify port availability
   - Check Docker logs: `docker-compose logs`

### Getting Help

- Check the [User Guide](./user-guide.md) for detailed usage instructions
- Review the [Troubleshooting Guide](./troubleshooting.md) for common issues
- Open an issue on GitHub for bugs or feature requests
- Contact the development team for support 