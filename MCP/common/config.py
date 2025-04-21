from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # Vector store
    vector_path: Path = Path("./vector_store")
    vector_rebuild: bool = False

    # Neo4j
    neo4j_uri: str = "neo4j://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    # Chunking
    chunk_size: int = 2000
    chunk_overlap: int = 200

    # Generation
    max_sections: int = 10  # fallback
    temperature: float = 0.0

    class Config:
        env_file = ".env"

settings = Settings()  # singleton style