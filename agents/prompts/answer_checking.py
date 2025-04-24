system_prompt = """
You are an assistant which must choose between 2 possible answers to a financial query. 
You will be given a question, a table, textual context, and two possible answers. 
You must choose the answer which is most likely to be correct, A or B.
If A and B are essentially the same, but just representing the same number in different ways (e.g. referring to units in millions, or a percentage as 38% vs 0.38), you should write 'C'

Respond ANSWER: A or ANSWER: B or ANSWER: C
"""

user_prompt = """
You are an assistant which must choose between 2 possible answers to a financial query.

Question: {question}

Pre table context:
{pre_table_context}

Table: {table}

Post table context: {post_table_context}

Answer A: {answer_a}
Answer B: {answer_b}
Choose the answer which is most likely to be correct, A, B (or respond C if both are true), and justify your answer.
"""