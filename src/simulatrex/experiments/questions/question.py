"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: question.py
Description: Question Class

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Type
from simulatrex.experiments.questions.types import QuestionType


class Question(
    ABC,
):
    question_name: str = ""
    question_text: str = ""
    question_type: QuestionType = QuestionType.FREE_TEXT
    short_names_dict: dict[str, str] = {}

    @property
    def data(self) -> dict:
        candidate_data = {
            k.replace("_", "", 1): v
            for k, v in self.__dict__.items()
            if k.startswith("_")
        }
        optional_attributes = {
            "set_instructions": "instructions",
        }
        for boolean_flag, attribute in optional_attributes.items():
            if hasattr(self, boolean_flag) and not getattr(self, boolean_flag):
                candidate_data.pop(attribute, None)

        return candidate_data

    def to_dict(self) -> dict[str, Any]:
        """Converts the question to a dictionary that includes the question type (used in deserialization)."""
        candidate_data = self.data.copy()
        candidate_data["question_type"] = self.question_type
        return candidate_data

    def __repr__(self) -> str:
        """Returns a string representation of the question. Should be able to be used to reconstruct the question."""
        class_name = self.__class__.__name__
        items = [
            f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}"
            for k, v in self.data.items()
            if k != "question_type"
        ]
        return f"{class_name}({', '.join(items)})"

    def __eq__(self, other: Type[Question]) -> bool:
        """Checks if two questions are equal. Equality is defined as having the .to_dict()"""
        if not isinstance(other, Question):
            return False
        return self.to_dict() == other.to_dict()

    def __add__(self, other_question):
        """
        Compose two questions into a single.
        """
        from simulatrex.experiments.questions import compose

        return compose(self, other_question)

    @abstractmethod
    def validate_answer(self, answer: dict[str, str]):
        pass

    def validate_response(self, response):
        """Validates the response from the LLM"""
        if "answer" not in response:
            raise Exception("Response from LLM does not have an answer")
        return response

    @abstractmethod
    def translate_answer_code_to_answer(self):  # pragma: no cover
        """Translates the answer code to the actual answer. Behavior depends on the question type."""
        pass

    @abstractmethod
    def simulate_answer(self, human_readable=True) -> dict:  # pragma: no cover
        """Simulates a valid answer for debugging purposes (what the validator expects)"""
        pass
