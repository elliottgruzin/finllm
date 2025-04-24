import math
from math import isclose
from typing import List, Tuple
from utils.example import Example

from tqdm import tqdm

class Evaluator:
    def _compare_to_rounded_number(self, long_decimal, short_decimal):
        long_decimal, short_decimal = float(long_decimal), float(short_decimal)
        try:
            return isclose(
                round(
                    long_decimal, len(str(short_decimal).split('.')[1])
                    ), 
                short_decimal, 
                rel_tol=1e-4
                )
        except Exception as e:
            return False

    def _check_is_fuzzily_correct(self, prediction: float, answer: float):
        if isinstance(prediction, str) or prediction == None:
            return True # assume its a fallback for now

        if self._compare_to_rounded_number(float(prediction), float(answer)): # numbers are equal
            return True
        elif self._compare_to_rounded_number(float(prediction), float(answer) * 100):
            return True
        elif self._compare_to_rounded_number(float(prediction), float(answer) / 100): # compensate for different ways of representing percentage
            return True
        elif self._compare_to_rounded_number(float(prediction), float(answer) * -1): # sometimes gold standard forgets to add a minus sign
            return True
        elif self.are_multiples_of_10(float(prediction), float(answer)):
            return True

        return False
    
    def _check_is_correct(self, prediction: float, answer: float):
        return self._compare_to_rounded_number(float(prediction), float(answer)) # numbers are equal

    def accuracy(self, examples: List[Example], fuzzy: bool = False):
        correct = 0
        for example in examples:
            if example.predicted_answer == "CANNOT ANSWER":
                continue
            if fuzzy:
                is_correct = self._check_is_fuzzily_correct(example.predicted_answer, example.answer)
            else:
                is_correct = self._check_is_correct(example.predicted_answer, example.answer)
            correct += is_correct
        return correct / len(examples)

    def return_incorrect(self, examples: List[Example], fuzzy: bool = False):
        incorrect = []
        for example in examples:
            if example.predicted_answer == "CANNOT ANSWER":
                continue
            if fuzzy:
                is_correct = self._check_is_fuzzily_correct(example.predicted_answer, example.answer)
            else:
                is_correct = self._check_is_correct(example.predicted_answer, example.answer)
            if not is_correct:
                incorrect.append(example)
        return incorrect

    def are_multiples_of_10(self, x: float, y: float, tolerance: float = 1e-9) -> bool:
        if x == 0 or y == 0:
            return False
        x, y = abs(x), abs(y)
        ratio = x / y if x > y else y / x
        log10_ratio = round(math.log10(ratio))
        
        # Check if ratio is approximately a power of 10
        return abs(ratio - 10 ** log10_ratio) < tolerance
