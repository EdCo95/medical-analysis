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


ASSESS_AGAINST_CRITERIA = (
    "Read the document then make an assessment against the criteria to decide whether the context "
    "meets the criteria. YOU MUST SHOW YOUR REASONING IN DETAIL. When justifying your decision, "
    "QUOTE EVIDENCE VERBATIM from the criteria and the document.\n\n"
    "<age>"
    "{age}"
    "</age>"
    "<document>\n"
    "{context}\n"
    "</document>\n\n"
    "<criteria>\n"
    "{criteria}\n"
    "</criteria>"
)
