from enum import Enum
from typing import List, Optional

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from assess.structures import prompts


class AdvisorType(Enum):
    GPT_4 = "gpt-4"
    GPT_3_5 = "gpt-3.5-turbo"


class Advisor:
    """Interface class for advisors."""

    def ask(self, prompt: str, context: Optional[List[Document]] = None) -> str:
        """Asks an arbitrary prompt and returns a string."""
        raise NotImplementedError


class GPT4Advisor(Advisor):
    """An Advisor backed by GPT-4"""

    def __init__(self):
        self.model = ChatOpenAI(model=AdvisorType.GPT_4.value)
        self.engine = OpenAiEngine(self.model)

    def ask(self, s: str, context: Optional[List[Document]] = None) -> str:
        return self.engine.ask(s, context)


class GPT3_5Advisor(Advisor):
    """An Advisor backed by GPT-3.5"""

    def __init__(self):
        self.model = ChatOpenAI(model=AdvisorType.GPT_3_5.value)
        self.engine = OpenAiEngine(self.model)

    def ask(self, s: str, context: Optional[List[Document]] = None) -> str:
        return self.engine.ask(s, context)


class OpenAiEngine:

    def __init__(self, model: ChatOpenAI):
        self.model = model
        self._basic_prompt = ChatPromptTemplate.from_template(
            template=prompts.BASIC_NO_CONTEXT
        )
        self._basic_chain = self._basic_prompt | self.model | StrOutputParser()

        self._context_prompt = ChatPromptTemplate.from_template(
            template=prompts.BASIC_CONTEXT
        )
        self._context_chain = create_stuff_documents_chain(
            self.model, prompt=self._context_prompt
        )

    def ask(self, s: str, context: Optional[List[Document]] = None) -> str:
        if not context:
            return self._basic_chain.invoke({"question": s})
        else:
            return self._context_chain.invoke({"question": s, "context": context})
