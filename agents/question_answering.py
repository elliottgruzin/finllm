import re

from utils.example import Example
import ast
from tqdm import tqdm
import numexpr

from .prompts.question_answering import default_system_prompt, default_user_prompt
from .base import BaseAgent



class QuestionAnswerer(BaseAgent):
  def __init__(self, client, model, system_prompt: str = default_system_prompt, user_prompt: str = default_user_prompt):
    self.client = client
    self.model = model
    self.system_prompt = system_prompt
    self.user_prompt = user_prompt

  def predict(self, example: Example):
    filled_user_prompt = self.user_prompt.format(
        question=example.question,
        table=example.table,
        pre_table_context=example.pre_table_context,
        post_table_context=example.post_table_context
        )
    response = self._call_model(filled_user_prompt)

    example.predicted_answer_full_output = response

    extracted = self.extract_answer(response)
    if extracted is not None:
      example.predicted_answer = extracted
    elif "CANNOT ANSWER" in example.predicted_answer_full_output:
      example.predicted_answer = "CANNOT ANSWER"

    return example

  def extract_answer(self, answer: str):
    try:
      expression = re.search(r"ANSWER: ([-\d\.\-\+\s\/\*\(\)]+)", answer).group(1)
      return float(numexpr.evaluate(expression).item())
    except Exception as e:
      return None