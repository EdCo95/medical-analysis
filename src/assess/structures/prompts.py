ASK_FOR_CPT_CODES = (
    "A CPT code is a sequence of numbers indicating medical procedures. "
    "What are the CPT codes for the procedures which the doctor has requested? "
    "DO NOT INCLUDE CODES FROM PREVIOUS TREATMENTS"
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
