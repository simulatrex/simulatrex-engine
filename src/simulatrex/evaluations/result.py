"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: result.py
Description: Result class for the evaluation of an interview

"""

from __future__ import annotations
from collections import UserDict
from typing import Any, Type

from rich.table import Table

from simulatrex.agents import Agent
from simulatrex.base import Base
from simulatrex.experiments.scenarios.scenario import Scenario
from simulatrex.llms.llm_base import LanguageModel


class Result(Base, UserDict):
    """
    This class captures the result of one interview.
    """

    def __init__(
        self,
        agent: Agent,
        scenario: Scenario,
        model: Type[LanguageModel],
        iteration: int,
        answer: str,
        prompt: dict[str, str] = None,
    ):
        # initialize the UserDict
        data = {
            "agent": agent,
            "scenario": scenario,
            "model": model,
            "iteration": iteration,
            "answer": answer,
            "prompt": prompt or {},
        }
        super().__init__(**data)
        # but also store the data as attributes
        self.agent = agent
        self.scenario = scenario
        self.model = model
        self.iteration = iteration
        self.answer = answer
        self.prompt = prompt or {}

    @property
    def sub_dicts(self) -> dict[str, dict]:
        """Returns a dictionary where keys are strings for each of the main class attributes/objects (except for iteration) and values are dictionaries for the attributes and values for each of these objects."""
        return {
            "agent": self.agent.traits,
            "scenario": self.scenario,
            "model": self.model.parameters | {"model": self.model.model},
            "answer": self.answer,
            "prompt": self.prompt,
        }

    @property
    def combined_dict(self) -> dict[str, Any]:
        """Returns a dictionary that includes all sub_dicts, but also puts the key-value pairs in each sub_dict as a key_value pair in the combined dictionary."""
        combined = {}
        for key, sub_dict in self.sub_dicts.items():
            combined.update(sub_dict)
            combined.update({key: sub_dict})
        return combined

    def get_value(self, data_type: str, key: str) -> Any:
        """Returns the value for a given data type and key"""
        return self.sub_dicts[data_type][key]

    @property
    def key_to_data_type(self) -> dict[str, str]:
        """Returns a dictionary where keys are object attributes and values are the data type (object) that the attribute is associated with."""
        d = {}
        for data_type in ["agent", "scenario", "model", "answer", "prompt"]:
            for key in self.sub_dicts[data_type]:
                d[key] = data_type
        return d

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def to_dict(self) -> dict[str, Any]:
        """Returns a dictionary representation of the Result object."""
        return {
            k: v if not hasattr(v, "to_dict") else v.to_dict() for k, v in self.items()
        }

    def __repr__(self):
        return f"Result(agent={repr(self.agent)}, scenario={repr(self.scenario)}, model={repr(self.model)}, iteration={self.iteration}, answer={repr(self.answer)}, prompt={repr(self.prompt)}"
