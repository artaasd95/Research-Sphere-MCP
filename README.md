# Research Sphere MCP 🚀

Welcome to Research Sphere MCP, an innovative project that combines the power of RAG (Retrieval-Augmented Generation) and MCP (Model Context Protocol) to revolutionize research and knowledge management! 🎯
## 📖 Introduction

Research Sphere is an advanced academic research assistant platform that combines two powerful standalone systems:

1. **RAG (Retrieval-Augmented Generation) System**
   - Intelligent article discovery and retrieval
   - Academic paper analysis and summarization
   - Context-aware research question answering
   - Semantic search across research papers

2. **MCP (Model Context Protocol) System**
   - Full-stack application with modern frontend and backend
   - Research workflow management
   - Interactive research exploration interface
   - API integration capabilities

Together, these systems create a comprehensive platform designed to:
- Streamline academic research processes
- Generate insightful responses to research queries
- Help researchers discover relevant academic papers
- Provide intelligent summarization of research content
- Enable semantic search across academic literature

The modular architecture allows each system to function independently while offering enhanced capabilities when used together.


## 🌟 Project Overview

Research Sphere MCP is a cutting-edge platform that integrates two powerful components:

1. **RAG System** 🔍
   - Advanced document processing and retrieval
   - Intelligent knowledge extraction
   - Context-aware response generation
   - Currently under active development

2. **MCP Framework** ⚡
   - Multi-component pipeline architecture
   - Scalable and modular design
   - Real-time processing capabilities
   - Currently under active development

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Compose
- Python 3.12 or higher
- Git

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/research-sphere-mcp.git
cd research-sphere-mcp
```

### 2. Environment Setup
Create a `.env` file in the root directory with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Running with Docker
```bash
docker-compose up --build
```

The application will be available at:
- Main Application: http://localhost:8000
- Neo4j Browser: http://localhost:7474

### 4. Running Locally
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install uv
uv pip install .
```

## 📚 Documentation

### RAG System Documentation
The RAG (Retrieval-Augmented Generation) system documentation is available in the `docs/rag` directory. It includes:
- System architecture
- API documentation
- Integration guidelines
- Best practices

### MCP Framework Documentation
The MCP (Multi-Component Pipeline) framework documentation is available in the `docs/mcp` directory. It includes:
- Framework architecture
- Component development guide
- Pipeline configuration
- Deployment guidelines

## 🧪 Testing

Run the test suite using:
```bash
pytest
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Issue Tracker](https://github.com/yourusername/research-sphere-mcp/issues)
- [Documentation](https://github.com/yourusername/research-sphere-mcp/docs)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for their invaluable tools and libraries

---

Made with ❤️ by the Research Sphere Team
