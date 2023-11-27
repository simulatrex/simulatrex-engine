"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: target_group.py
Description: Target Group Class

"""
from typing import List, Optional
from simulatrex.agent import LLMAgent
from simulatrex.agent_utils.spawn import spawn_agent
from simulatrex.agent_utils.types import CognitiveModel
from simulatrex.config import InitialConditions
from simulatrex.llm_utils.models import OpenAILanguageModel


class TargetGroupRelationship:
    def __init__(
        self,
        target_group_name: str,
        type: str,
        strength: float,
    ):
        self.target_group_name = target_group_name
        self.type = type
        self.strength = strength

    def summary(self) -> str:
        return f"Relationship to {self.target_group_name} of type {self.type} with strength {self.strength})"


class TargetGroup:
    def __init__(
        self,
        id: str,
        role: str,
        responsibilities: str,
        initial_conditions: Optional[InitialConditions] = None,
        relationships: List[TargetGroupRelationship] = [],
    ):
        self.id = id
        self.role = role
        self.responsibilities = responsibilities
        self.initial_conditions = initial_conditions
        self.agents = []
        self.cognitive_model_id = "gpt-4-1106-preview"
        self.relationships = relationships

    async def spawn_agents(self, num_agents: int) -> List[LLMAgent]:
        cognitive_model = OpenAILanguageModel(
            model_id=CognitiveModel.GPT_4, agent_id=self.id
        )
        for _ in range(num_agents):
            agent = await spawn_agent(
                cognitive_model,
                self.cognitive_model_id,
                self.role,
                self.responsibilities,
                self.initial_conditions,
                self.relationships,
            )
            self.agents.append(agent)

        return self.agents
