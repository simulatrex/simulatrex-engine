from simulatrex.llms.models.models import OpenAILanguageModel
from simulatrex.llms.types import LanguageModel


class Agent:
    def __init__(
        self,
        identifier,
        attributes=None,
        actions=None,
        llm_id=LanguageModel.GPT_4_TURBO,
    ):
        self.identifier = identifier
        self.attributes = attributes if attributes is not None else {}
        self.actions = actions if actions is not None else []
        self.llm = OpenAILanguageModel(model_id=llm_id) if llm_id else None

    async def act(self):
        if self.llm:
            for action in self.actions:
                response = await self.llm.ask(f"Generate an action for: {action}.")
                print(f"Agent {self.identifier} action for {action}: {response}")
        else:
            print(f"Agent {self.identifier} has no LLM to generate action.")


class Environment:
    def __init__(self, identifier, entities=None):
        self.identifier = identifier
        self.entities = entities if entities is not None else []

    async def interact(self, agents):
        print(
            f"Environment {self.identifier} is facilitating interaction among agents."
        )
        for agent in agents:
            # Example interaction: asking each agent to generate an action
            await agent.act()
        for entity in self.entities:
            print(f"Interacting with entity: {entity}")
            # Example entity interaction can be added here


class Simulation:
    def __init__(
        self, identifier, epochs=1, interactions=None, agents=None, environment=None
    ):
        self.identifier = identifier
        self.epochs = epochs
        self.interactions = interactions if interactions is not None else []
        self._agents = agents if agents is not None else []
        self._environment = environment

    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self, value):
        self._agents = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value

    async def run(self):
        print(f"Simulation {self.identifier} started.")
        for _ in range(self.epochs):
            if self.environment:
                await self.environment.interact(self.agents)
            for interaction in self.interactions:
                print(f"Executing interaction: {interaction}")
        print(f"Simulation {self.identifier} ended.")
