from typing import List, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.docstore.document import Document
from loguru import logger
from .document_processor import DocumentProcessor
from .vector_store import VectorStoreManager
from ..core.config import settings

class RAGPipeline:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStoreManager()
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL_NAME,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        logger.info("RAGPipeline initialized")

    async def process_query(self, query: str, max_sections: int = settings.MAX_SECTIONS) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline
        
        Args:
            query (str): The user's query
            max_sections (int): Maximum number of sections in the response
            
        Returns:
            Dict[str, Any]: The generated response with answer and metadata
        """
        try:
            logger.info(f"Processing query: {query}")
            
            # 1. Retrieve relevant documents
            search_results = self.vector_store.hybrid_search(query)
            documents = search_results["similarity"]
            logger.info(f"Retrieved {len(documents)} relevant documents")
            
            # 2. Generate outline
            outline = await self._generate_outline(query, max_sections)
            logger.info(f"Generated outline with {len(outline)} sections")
            
            # 3. Generate detailed response
            response = await self._generate_response(query, outline, documents)
            logger.info("Generated detailed response")
            
            return {
                "answer": response,
                "sections": outline,
                "documents_used": len(documents)
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            raise

    async def _generate_outline(self, query: str, max_sections: int) -> List[str]:
        """Generate an outline for the response"""
        try:
            outline_prompt = ChatPromptTemplate.from_template(
                "Create a detailed outline with up to {max_sections} sections for answering: {query}"
            )
            outline_chain = LLMChain(llm=self.llm, prompt=outline_prompt)
            outline_text = await outline_chain.arun(query=query, max_sections=max_sections)
            return [section.strip() for section in outline_text.split("\n") if section.strip()]
        except Exception as e:
            logger.error(f"Error generating outline: {str(e)}")
            raise

    async def _generate_response(self, query: str, outline: List[str], documents: List[Document]) -> str:
        """Generate a detailed response based on the outline and documents"""
        try:
            # Combine document content
            context = "\n\n".join([doc.page_content for doc in documents])
            
            response_prompt = ChatPromptTemplate.from_template(
                """Based on the following context and outline, provide a detailed answer to the query.
                
                Query: {query}
                
                Outline:
                {outline}
                
                Context:
                {context}
                
                Provide a comprehensive answer following the outline structure."""
            )
            
            response_chain = LLMChain(llm=self.llm, prompt=response_prompt)
            response = await response_chain.arun(
                query=query,
                outline="\n".join(outline),
                context=context
            )
            
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise 