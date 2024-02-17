"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: survey.py
Description: Survey class

"""

from __future__ import annotations

from simulatrex.base import Base
from simulatrex.experiments.questions.question import Question


class Survey(Base):
    questions = []

    """
    A collection of questions that supports skip logic.
    """

    def __init__(
        self,
        questions: list[Question] = None,
    ):
        """Creates a new survey."""
        self.questions = questions or []
