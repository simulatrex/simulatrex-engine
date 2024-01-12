"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: target_group.py
Description: Target Group Class

"""
import asyncio
from typing import Any, List
from simulatrex.agent.agent import LLMAgent
from simulatrex.agent.actions.spawn import spawn_agent
from simulatrex.agent.utils.types import CognitiveModel
from simulatrex.llm_utils.models import OpenAILanguageModel


class TargetGroup:
    def __init__(
        self,
        id: str,
    ):
        self.id = id
        self.attributes = {}
        self.cognitive_model_id = "gpt-4-1106-preview"
        self.agents: List[LLMAgent] = []

    def age_range(self, min_age: int, max_age: int):
        self.attributes["age_range"] = (min_age, max_age)
        return self

    def location(self, location: str):
        self.attributes["location"] = location
        return self

    def income_range(self, min_income: float, max_income: float):
        self.attributes["income_range"] = (min_income, max_income)
        return self

    def education_level(self, education_level: str):
        self.attributes["education_level"] = education_level
        return self

    def ethnicity(self, ethnicity: str):
        self.attributes["ethnicity"] = ethnicity
        return self

    def gender(self, gender: str):
        self.attributes["gender"] = gender
        return self

    def occupation(self, occupation: str):
        self.attributes["occupation"] = occupation
        return self

    def add_trait(self, trait_name: str, trait_value: Any):
        self.attributes[trait_name] = trait_value
        return self

    def describe(self) -> str:
        description_lines = [f"Target Group ID: {self.id}"]
        for attribute, value in self.attributes.items():
            description_lines.append(f"{attribute.capitalize()}: {value}")
        return "\n".join(description_lines)

    async def spawn_agents(self, num_agents: int) -> List[any]:
        cognitive_model = OpenAILanguageModel(
            model_id=CognitiveModel.GPT_4_TURBO, agent_id=self.id
        )

        tasks = []
        for _ in range(num_agents):
            task = asyncio.create_task(
                spawn_agent(
                    cognitive_model,
                    self.cognitive_model_id,
                    list(self.attributes.items()),
                )
            )
            tasks.append(task)

        self.agents = await asyncio.gather(*tasks)

        return self.agents

    async def run_conversation_test(
        self, questions: List[str], iterations: int
    ) -> List[any]:
        spawn_task = None
        if len(self.agents) < iterations:
            spawn_task = asyncio.create_task(
                self.spawn_agents(iterations - len(self.agents))
            )

        # Wait for the spawn task if it was started
        if spawn_task:
            await spawn_task

        # Prepare and run ask tasks for all agents and questions
        responses = []
        for agent in self.agents:
            for question in questions:
                print(f"Agent {agent.id}: {question}")

                response = await agent.ask_based_on_personality(
                    question, self.attributes
                )
                print(f"Agent {agent.identity.name} responded: {response}")
                responses.append(response)

                yield response
