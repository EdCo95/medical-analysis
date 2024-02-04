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
