from enum import Enum
from typing import List, Optional

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1.error_wrappers import ValidationError

from assess.structures import prompts


class MissingApiKeyExcepetion(Exception):
    """To be raised if the API key environment variable hasn't been set"""

    pass


class AdvisorType(Enum):
    GPT_4 = "gpt-4"
    GPT_3_5 = "gpt-3.5-turbo"


class Advisor:
    """Interface class for advisors."""

    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    def ask(
        self,
        prompt: str,
        context: Optional[List[Document]] = None,
        search_results: Optional[str] = None,
    ) -> str:
        """Asks an arbitrary prompt and returns a string."""
        raise NotImplementedError

    def web_search(self, query: str) -> str:
        """Performs a web search and returns the results as a string."""
        return self.search.run(query)


class GPT4Advisor(Advisor):
    """An Advisor backed by GPT-4"""

    def __init__(self):
        super().__init__()
        self.model = ChatOpenAI(model=AdvisorType.GPT_4.value)
        self.engine = OpenAiEngine(self.model)

    def ask(
        self,
        s: str,
        context: Optional[List[Document]] = None,
        search_results: Optional[str] = None,
    ) -> str:
        return self.engine.ask(s, context)


class GPT3_5Advisor(Advisor):
    """An Advisor backed by GPT-3.5"""

    def __init__(self):
        super().__init__()
        self.model = ChatOpenAI(model=AdvisorType.GPT_3_5.value)
        self.engine = OpenAiEngine(self.model)

    def ask(
        self,
        s: str,
        context: Optional[List[Document]] = None,
        search_results: Optional[str] = None,
    ) -> str:
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

        self._context_and_search_prompt = ChatPromptTemplate.from_template(
            template=prompts.CONTEXT_AND_SEARCH_RESULTS
        )
        self._context_and_search_chain = create_stuff_documents_chain(
            self.model, prompt=self._context_and_search_prompt
        )

    def ask(
        self,
        s: str,
        context: Optional[List[Document]] = None,
        search_results: Optional[str] = None,
    ) -> str:
        if not context:
            return self._basic_chain.invoke({"question": s})
        elif context and not search_results:
            return self._context_chain.invoke({"question": s, "context": context})
        elif not context and search_results:
            return self._context_chain.invoke(
                {"question": s, "context": search_results}
            )
        else:
            return self._context_and_search_prompt(
                {"question": s, "context": context, "search_results": search_results}
            )


class AdvisorFactory:
    """Given a model identifier, instantiates the correct Advisor object."""

    def __init__(self, model_id: AdvisorType):
        self.advisor_type = model_id

    def _select_advisor(self) -> Advisor:
        if self.advisor_type == AdvisorType.GPT_4:
            return GPT4Advisor()
        elif self.advisor_type == AdvisorType.GPT_3_5:
            return GPT3_5Advisor()
        else:
            raise KeyError(
                f"Need to specify a valid advisor type (current: {self.advisor_type})"
            )

    def get_advisor(self) -> Advisor:
        try:
            return self._select_advisor()
        except ValidationError:
            raise MissingApiKeyExcepetion(
                "Make sure you provide an API key for the model you want to instantiate."
            )
