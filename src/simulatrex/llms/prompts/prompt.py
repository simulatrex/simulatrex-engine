"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: prompt.py
Description: Prompt class for the LLM

"""

from simulatrex.base import Base


class Prompt(Base):
    def __init__(self, prompt_type, **attributes):
        self.prompt_type = prompt_type
        self.attributes = attributes

    def generate_prompt(self):
        raise NotImplementedError(
            "Subclasses should implement this method to generate the prompt text."
        )

    def validate_attributes(self):
        raise NotImplementedError(
            "Subclasses should implement this method to validate the attributes for the prompt."
        )
