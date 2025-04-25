from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RefineDocumentsChain, ReduceDocumentsChain, AnalyzeDocumentChain
from langchain_core.documents import Document
from common.config import settings
from common.logger import logger

class LongAnswerGenerator:
    """Generates long answers via sequential section refinement."""
    def __init__(self):
        self.llm = ChatOpenAI(model_name=settings.llm_model, temperature=settings.temperature, api_key=settings.openai_api_key)

        self.section_prompt = PromptTemplate(
            template=(
                "You are writing a comprehensive report responding to the question:\n"
                "{question}\n\n"
                "Current draft:\n{draft}\n\n"
                "Relevant sources:\n{sources}\n\n"
                "Write the next section titled '{section_title}'."
            ),
            input_variables=["question", "draft", "sources", "section_title"],
        )
        self.section_chain = LLMChain(llm=self.llm, prompt=self.section_prompt)

    def generate(self, question: str, sections: List[str], docs: List[Document]) -> str:
        sources_text = "\n\n".join(d.page_content[:1500] for d in docs)  # truncate per source
        draft = ""  # grows over time
        for title in sections:
            logger.info(f"Generating section: {title}")
            output = self.section_chain.run(question=question, draft=draft, sources=sources_text, section_title=title)
            draft += f"\n\n### {title}\n\n" + output
        return draft.strip()