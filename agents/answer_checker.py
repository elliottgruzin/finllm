import re

from utils.example import Example
import ast
from tqdm import tqdm
import numexpr

from .prompts.answer_checking import system_prompt, user_prompt
from .base import BaseAgent


class AnswerChecker(BaseAgent):
  def __init__(self, client, model, system_prompt: str = system_prompt, user_prompt: str = user_prompt):
    self.client = client
    self.model = model
    self.system_prompt = system_prompt
    self.user_prompt = user_prompt

  def predict(self, example: Example):
    filled_user_prompt = self.user_prompt.format(
        question=example.question,
        table=example.table,
        pre_table_context=example.pre_table_context,
        post_table_context=example.post_table_context,
        answer_a=example.answer,
        answer_b=example.predicted_answer
        )

    response = self._call_model(filled_user_prompt)
    example.preferred_answer_full_output = response

    extracted = self.extract_answer(response)
    if extracted is not None:
      example.preferred_answer = 'predicted' if extracted == 'B' else 'gold'

    return example

  def extract_answer(self, answer: str):
    try:
      return re.search(r"ANSWER: ([ABC])", answer).group(1)
    except Exception:
      return None