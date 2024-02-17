"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: types.py
Description: QuestionType Enum

"""

from enum import Enum


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FREE_TEXT = "free_text"
