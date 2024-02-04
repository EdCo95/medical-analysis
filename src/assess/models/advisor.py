from enum import Enum
from typing import Dict, List, Optional

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
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

    def assess_against_criteria(
        self, to_be_assessed: List[Document], criteria: str
    ) -> str:
        """Assesses the given item against the given criteria."""
        raise NotImplementedError

    def extract_json(
        self,
        prompt: str,
        json_structure: BaseModel,
        context: Optional[List[Document]] = None,
    ) -> Dict:
        """Extracts JSON data"""
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

    def extract_json(
        self,
        prompt: str,
        json_structure: BaseModel,
        context: Optional[List[Document]] = None,
    ) -> Dict:
        return self.engine.extract_json(prompt, json_structure, context)

    def assess_against_criteria(
        self, to_be_assessed: List[Document], criteria: str
    ) -> str:
        return self.engine.assess_against_criteria(to_be_assessed, criteria)


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

    def extract_json(
        self,
        prompt: str,
        json_structure: BaseModel,
        context: Optional[List[Document]] = None,
    ) -> Dict:
        return self.engine.extract_json(prompt, json_structure, context)

    def assess_against_criteria(
        self, to_be_assessed: List[Document], criteria: str
    ) -> str:
        return self.engine.assess_against_criteria(to_be_assessed, criteria)


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

        self._assessment_prompt = ChatPromptTemplate.from_template(
            template=prompts.ASSESS_AGAINST_CRITERIA
        )
        self._assessment_chain = create_stuff_documents_chain(
            self.model, self._assessment_prompt
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

    def extract_json(
        self,
        prompt: str,
        json_structure: BaseModel,
        context: Optional[List[Document]] = None,
    ) -> Dict:
        parser = JsonOutputParser(pydantic_object=json_structure)
        prompt = PromptTemplate(
            template=prompts.JSON_EXTRACTION_PROMPT,
            input_variables=["prompt", "context"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = create_stuff_documents_chain(self.model, prompt) | parser
        result = chain.invoke({"prompt": prompt, "context": context})
        return result

    def assess_against_criteria(
        self, to_be_assessed: List[Document], criteria: str
    ) -> str:
        result = self._assessment_chain.invoke(
            {"context": to_be_assessed, "criteria": criteria}
        )
        return result


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
