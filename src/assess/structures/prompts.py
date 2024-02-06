from enum import Enum


class PromptConstant(Enum):
    YES = "YES"
    NO = "NO"


ASK_FOR_CPT_CODES = (
    "A CPT code is a sequence of numbers indicating medical procedures. "
    "What are the CPT codes for the procedures which the doctor has requested? "
    "DO NOT INCLUDE CODES FROM PREVIOUS TREATMENTS "
    "Give JUST THE CODES in your answer and no other text at all"
)

CPT_WEB_SEARCH = "What procedures do the following CPT codes correspond to: {codes}"

SUMMARISE_DOCTORS_ORDERS = "Summarise the treatment the doctor has recommended."

SUMMARISE_CODE_MEANINGS = (
    "Summarise what the CPT codes {codes} mean based on the context."
)

DETERMINE_MATCH = (
    "The doctor's recommended treatment is {summary}. The medical record requests "
    "procedures {codes}, and the meaning of these codes is {code_meaning}. "
    "Does the meaning of the codes match the doctor's recommended treatment, "
    "or has there been a mistake? Show your reasoning. If there has been a mistake,"
    ' start your response with the indicator "[ERROR]"'
)

SUMMARY_OF_TREATMENT_SO_FAR = (
    "For the patient's CURRENT CONDITION, answer the questions below. "
    "Provide detail and reasoning, all based on evidence from the context."
    "\n1. Have any treatments already been attempted? If so, what was their outcome?"
    "\n2. Is there anything which has improved the patient's current condition?"
)


YES_NO_DID_ANYTHING_HELP = (
    f"Read the summary, then output either '{PromptConstant.YES.value}' or '{PromptConstant.NO.value}' indicating "
    "WHETHER ANYTHING HAS HELPED THE PATIENT'S CURRENT CONDITION."
)


BASIC_NO_CONTEXT = """Provide an appropriate, concise answer to the user's question.

Question: {question}
"""

BASIC_CONTEXT = """Answer the question based only on the provided context and nothing else.

<context>
{context}
</context>

Question: {question}
"""

CONTEXT_AND_SEARCH_RESULTS = """Read the context and the search results, then answer the question:

<context>
{context}
</context>

<search-results>
{search_result}
</search-results>

Question: {input}"""


JSON_EXTRACTION_PROMPT = """Read the context then extract the JSON data as described in the prompt.

<prompt>
{prompt}
</prompt>

<context>
{context}
</context>

<json-format-instructions>
{format_instructions}
</json-format-instructions>
"""


ASSESS_AGAINST_INDIVIDUAL_CRITERIA = (
    "Below is a patient profile, an assessment criteria, and the raw medical record. "
    "It is your task to assess whether the patient meets the assessment criteria "
    "for the recommended procedure. "
    "IT IS ESSENTIAL THAT YOU QUOTE YOUR EVIDENCE FOR EACH DEDUCTION VERBATIM "
    "FROM THE PATIENT PROFILE OR MEDICAL RECORD. "
    "UNDER NO CIRCUMSTANCES SHOULD YOU MAKE AN INFERENCE, "
    "ALL OF YOUR CONCLUSIONS MUST BE DIRECTLY SUPPORTED BY EVIDENCE. "
    "Show your reasoning in detail. "
    'START YOUR RESPONSE WITH EITHER "[YES]" OR "[NO]" INDICATING IF THEY MEET THAT CRITERIA.\n\n'
    "<patient-profile>\n"
    "{profile}\n"
    "</patient-profile>\n\n"
    "<criteria>\n"
    "{criteria}\n"
    "</criteria>\n\n"
    "<medical-record>\n"
    "{context}\n"
    "</medical-record>\n\n"
)

FINAL_ASSESSMENT = (
    "Your task is to determine whether a patient meets the criteria for the stated medical procedure. "
    "You have access to a list of assessments already given for each sub-point of the criteria. "
    "Your job is to provide the final, overall assessment of whether the patient meets the criteria. "
    "YOU MUST QUOTE YOUR EVIDENCE FOR YOUR DECISION VERBATIM. "
    'Begin your answer with "[YES]" if they do meet the criteria, and "[NO]" otherwise.\n\n'
    "<instructions>\n"
    "{instructions}\n"
    "</instructions>\n\n"
    "<assessments>\n\n"
    "{assessments}\n"
    "</assessments>\n\n"
)
