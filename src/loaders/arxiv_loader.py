from typing import List, Optional
import arxiv
from common.interfaces import DocumentLoader
from common.models import ArxivDocument
from common.logger import logger

__all__ = ["load_arxiv_documents"]

class ArxivDocumentLoader(DocumentLoader):
    """Concrete implementation of DocumentLoader for arXiv papers."""
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self.client = arxiv.Client()
    
    async def load(self, source: str) -> List[ArxivDocument]:
        """Load documents from arXiv based on a search query."""
        try:
            search = arxiv.Search(
                query=source,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = self.client.results(search)
            documents = []
            
            for result in results:
                doc = ArxivDocument(
                    _content=result.summary,
                    _metadata={
                        'title': result.title,
                        'authors': [author.name for author in result.authors],
                        'published': result.published.strftime('%Y-%m-%d'),
                        'id': result.entry_id,
                        'pdf_url': result.pdf_url,
                        'primary_category': result.primary_category,
                        'categories': result.categories
                    }
                )
                documents.append(doc)
            
            return documents
            
        except Exception as e:
            raise Exception(f"Error loading arXiv documents: {str(e)}")
    
    def set_max_results(self, max_results: int) -> None:
        """Update the maximum number of results to fetch."""
        self.max_results = max_results

async def load_arxiv_documents(query: str, max_docs: int = 10, load_all_meta: bool = False) -> List[ArxivDocument]:
    """Asynchronously fetch docs from arXiv."""
    logger.info(f"Querying arXiv for '{query}' (max {max_docs})")
    loader = ArxivDocumentLoader(max_results=max_docs)
    docs = await loader.load(query)
    logger.info(f"Fetched {len(docs)} arXiv docs")
    return docs