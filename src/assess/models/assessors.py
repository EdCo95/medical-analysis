import tomlkit
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger

from assess.models.llms import LlmType
from assess.structures import prompts
from assess.structures.criteria import AssessmentCriteria
from assess.structures.medical_record import MedicalRecord


class Assessor:
    """Interface for an object which can assess a medical record against a criteria."""

    def assess_criteria(
        self, criteria: AssessmentCriteria, record: MedicalRecord
    ) -> str:
        """Performs the assessment"""
        raise NotImplementedError


class GPT4Assessor(Assessor):
    """Assesses using GPT4"""

    def __init__(self):
        self.model = ChatOpenAI(model=LlmType.GPT_4.value)
        self.engine = OpenAiAssessmentEngine(self.model)

    def assess_criteria(
        self, criteria: AssessmentCriteria, record: MedicalRecord
    ) -> str:
        return self.engine.assess_criteria(criteria, record)


class OpenAiAssessmentEngine:
    """Engine class to call OpenAI models."""

    def __init__(self, model: ChatOpenAI):
        self.model = model
        self._individual_criteria_prompt = ChatPromptTemplate.from_template(
            template=prompts.ASSESS_AGAINST_INDIVIDUAL_CRITERIA
        )
        self._individual_criteria_chain = create_stuff_documents_chain(
            self.model, self._individual_criteria_prompt
        )

        self._final_assessment = ChatPromptTemplate.from_template(
            template=prompts.FINAL_ASSESSMENT
        )
        self._final_assessment_chain = (
            self._final_assessment | self.model | StrOutputParser()
        )

    def assess_criteria(
        self, criteria: AssessmentCriteria, record: MedicalRecord
    ) -> str:
        patient_profile = record.extract_patient_profile()
        logger.info(f"The patient's profile: {tomlkit.dumps(patient_profile)}")
        assessements_of_each_criteria = []
        for criteria_name, description in criteria.get_sections():
            logger.info(f"Assessing criteria '{criteria_name}'...")
            criteria_string = f"{criteria_name}:\n{description}"
            result = self._individual_criteria_chain.invoke(
                {
                    "profile": tomlkit.dumps(patient_profile),
                    "criteria": criteria_string,
                    "context": record.pages,
                }
            )
            logger.info(f"Assessment response: {result}")
            result = f'Assessment for criteria "{criteria_name}":\n{result}\n\n'
            assessements_of_each_criteria.append(result)

        logger.info("Performing final assessment...")
        assessments = "\n".join(assessements_of_each_criteria)
        result = self._final_assessment_chain.invoke(
            {"instructions": criteria.get_description(), "assessments": assessments}
        )
        logger.info(f"Final assessment: {result}")
        return result
