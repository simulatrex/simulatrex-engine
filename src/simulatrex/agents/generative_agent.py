"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: generative_agent.py
Description: Generative Agent class for the simulation

"""

from __future__ import annotations
import copy
import logging
from typing import Union

from simulatrex.associative_memory import associate_memory
from simulatrex.types.agent import AgentResponse

from simulatrex.base import Base
from simulatrex.experiments.questions.question import Question
from simulatrex.types.model import LanguageModelId
from simulatrex.utils.errors import AgentCombinationError


class GenerativeAgent(Base):
    """An agent represents a human in the simulation."""

    default_instruction = """Respond to each question by fully assuming a human persona. Maintain this character consistently and without deviation."""

    attributes = {}
    rules = {}
    instructions = {}

    def __init__(
        self,
        identifier: str,
        attributes: dict = None,
        instructions: str = None,
        model_id: LanguageModelId = LanguageModelId.GPT_4_TURBO,
        memory: associate_memory.AssociativeMemory = None,
        user_controlled: bool = False,
        logger=logging.getLogger("simulation_logger"),
        verbose: bool = False,
    ):
        self.identifier = identifier
        self.attributes = attributes or dict()
        self.instructions = instructions or self.default_instruction

        self._llm = LanguageModelId(model_id) if model_id else None
        self._memory = memory
        self._user_controlled = user_controlled
        self._logger = logger
        self_verbose = verbose

    @property
    def id(self) -> str:
        return self.identifier

    def copy(self) -> GenerativeAgent:
        """Creates a copy of the agent."""
        return copy.deepcopy(self)
    
    async def act(self, action_spec: Question) -> AgentResponse:
        """Generates a response to a question."""
        if self._llm:
            for action in self.actions:
                response = await self.llm.ask(f"Generate an action for: {action}.")
                self.logger.info(
                    f"Agent {self.identifier} action for {action}: {response}"
                )
        else:
            raise ValueError(f"Agent {self.identifier} has no LLM to generate action.")
    
    def __add__(self, other_agent: GenerativeAgent = None) -> GenerativeAgent:
        """
        Combines two agents by joining their traits
        """
        if other_agent is None:
            return self
        elif common_attributes := set(self.attributes.keys()) & set(other_agent.attributes.keys()):
            raise AgentCombinationError(
                f"The agents have overlapping traits: {
                    ', '.join(common_attributes)
                }."
            )
        else:
            new_agent = GenerativeAgent(attributes=copy.deepcopy(self.attributes))
            new_agent.attributes.update(other_agent.attributes)
            return new_agent

    def __eq__(self, other: GenerativeAgent) -> bool:
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

        return raw_data

    def to_dict(self) -> dict[str, Union[dict, bool]]:
        """Serializes to a dictionary."""
        return self.data

    @classmethod
    def from_dict(cls, agent_dict: dict[str, Union[dict, bool]]) -> GenerativeAgent:
        """Deserializes from a dictionary."""
        return cls(**agent_dict)
