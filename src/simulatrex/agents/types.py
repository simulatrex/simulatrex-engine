"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: types.py
Description: AgentResponse Class

"""

from collections import UserDict


class AgentResponse(UserDict):
    def __init__(self, *, question_name, answer, comment, prompts):
        super().__init__(
            {
                "question_name": question_name,
                "answer": answer,
                "comment": comment,
                "prompts": prompts,
            }
        )
