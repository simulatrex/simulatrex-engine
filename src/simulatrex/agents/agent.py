"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: agent.py
Description: Agent class for the simulation

"""

from __future__ import annotations
import copy
import inspect
import types
from typing import Any, Callable, Optional, Union, Dict

from rich.table import Table
from simulatrex.agents.types import AgentResponse

from simulatrex.base import Base
from simulatrex.experiments.questions.question import Question
from simulatrex.llms.llm_base import LanguageModel
from simulatrex.utils.sync import sync_wrapper
from simulatrex.utils.errors import AgentCombinationError


class Agent(Base):
    """An agent represents a human in the simulation."""

    default_instruction = """Respond to each question by fully assuming a human persona. Maintain this character consistently and without deviation."""

    traits = {}
    rules = {}
    instructions = {}

    def __init__(
        self,
        traits: dict = None,
        rules: dict = None,
        instructions: str = None,
    ):
        self._traits = traits or dict()
        self.rules = rules or dict()
        self.instructions = instructions or self.default_instruction
        self.current_question = None

    def set_answer_method(self, method: Callable):
        """Adds a method to the agent that can answer a particular question type."""

        signature = inspect.signature(method)
        for argument in ["question", "scenario", "self"]:
            if argument not in signature.parameters:
                raise Exception(
                    f"The method {method} does not have a '{argument}' parameter."
                )
        bound_method = types.MethodType(method, self)
        setattr(self, "answer_question_directly", bound_method)

    def __add__(self, other_agent: Agent = None) -> Agent:
        """
        Combines two agents by joining their traits
        """
        if other_agent is None:
            return self
        elif common_traits := set(self.traits.keys()) & set(other_agent.traits.keys()):
            raise AgentCombinationError(
                f"The agents have overlapping traits: {common_traits}."
            )
        else:
            new_agent = Agent(traits=copy.deepcopy(self.traits))
            new_agent.traits.update(other_agent.traits)
            return new_agent

    def __eq__(self, other: Agent) -> bool:
        """Checks if two agents are equal. Only checks the traits."""
        return self.data == other.data

    def __repr__(self):
        class_name = self.__class__.__name__
        items = [
            f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}"
            for k, v in self.data.items()
            if k != "question_type"
        ]
        return f"{class_name}({', '.join(items)})"

    @property
    def data(self):
        raw_data = {
            k.replace("_", "", 1): v
            for k, v in self.__dict__.items()
            if k.startswith("_")
        }
        if self.rules == {}:
            raw_data.pop("instructions")
        return raw_data

    def to_dict(self) -> dict[str, Union[dict, bool]]:
        """Serializes to a dictionary."""
        return self.data

    @classmethod
    def from_dict(cls, agent_dict: dict[str, Union[dict, bool]]) -> Agent:
        """Deserializes from a dictionary."""
        return cls(**agent_dict)
