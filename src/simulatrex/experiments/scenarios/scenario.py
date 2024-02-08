"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: scenario.py
Description: Scenario class

"""

import copy
from collections import UserDict
from rich.table import Table

from simulatrex.base import Base


class Scenario(Base, UserDict):
    """A Scenario is a dictionary of key/values that describe some situation."""

    def __add__(self, other_scenario):
        """Combine two scenarios. If the other scenario is None, then just return self."""
        if other_scenario is None:
            return self
        else:
            new_scenario = Scenario()
            new_scenario.data = copy.deepcopy(self.data)
            new_scenario.update(copy.deepcopy(other_scenario))
            return Scenario(new_scenario)

    def to(self, question_or_survey):
        """Run a question/survey with this particular scenario.
        Useful if you want to reverse the typical chain of operations.
        """
        return question_or_survey.by(self)

    def rename(self, replacement_dict: dict) -> "Scenario":
        """Rename the keys of a scenario. Useful for changing the names of keys."""
        new_scenario = Scenario()
        for key, value in self.items():
            if key in replacement_dict:
                new_scenario[replacement_dict[key]] = value
            else:
                new_scenario[key] = value
        return new_scenario

    def run_question(self, question_class: type):
        """Make a question from this scenario. Note it takes a QuestionClass (not a question)
        as an input.
        """
        return question_class(**self)

    def to_dict(self):
        """Convert a scenario to a dictionary."""
        return self.data

    @classmethod
    def from_dict(cls, d):
        """Convert a dictionary to a scenario."""
        return cls(d)
