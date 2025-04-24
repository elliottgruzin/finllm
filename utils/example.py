from typing import Optional, Union
from dataclasses import dataclass, field

@dataclass
class Example:
    question: str
    answer: str
    pre_table_context: str
    post_table_context: str
    table: str
    predicted_answer: Optional[Union[float, str]] = field(default=None)
    predicted_answer_full_output: Optional[str] = field(default=None)
    predicted_category: Optional[str] = field(default=None)
    preferred_answer: Optional[str] = field(default=None)
    preferred_answer_full_output: Optional[str] = field(default=None)
