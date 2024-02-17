import logging
from simulatrex.llms.models.models import OpenAILanguageModel
from simulatrex.llms.types import LanguageModel


class Agent:
    def __init__(
        self,
        identifier,
        attributes=None,
        actions=None,
        llm_id=LanguageModel.GPT_4_TURBO,
        logger=logging.getLogger("simulation_logger"),
    ):
        self.identifier = identifier
        self.attributes = attributes if attributes is not None else {}
        self.actions = actions if actions is not None else []
        self.llm = OpenAILanguageModel(model_id=llm_id) if llm_id else None
        self.logger = logger

    async def act(self):
        if self.llm:
            for action in self.actions:
                response = await self.llm.ask(f"Generate an action for: {action}.")
                self.logger.info(
                    f"Agent {self.identifier} action for {action}: {response}"
                )  # Use logger
        else:
            self.logger.warning(
                f"Agent {self.identifier} has no LLM to generate action."
            )  # Use logger

    def to_dict(self):
        return {
            "id": self.identifier,
            "attributes": self.attributes,
            "actions": self.actions,
        }


class Environment:
    def __init__(
        self, identifier, entities=None, logger=logging.getLogger("simulation_logger")
    ):
        self.identifier = identifier
        self.entities = entities if entities is not None else []
        self.logger = logger  # Store logger

    async def interact(self, agents):
        self.logger.info(  # Use logger
            f"Environment {self.identifier} is facilitating interaction among agents."
        )
        for agent in agents:
            await agent.act()
        for entity in self.entities:
            self.logger.debug(f"Interacting with entity: {entity}")

    def to_dict(self):
        return {
            "id": self.identifier,
            "entities": self.entities,
        }


class Simulation:
    def __init__(
        self,
        identifier,
        epochs=1,
        interactions=None,
        agents=None,
        environment=None,
        logger=None,
    ):
        self.identifier = identifier
        self.epochs = epochs
        self.interactions = interactions if interactions is not None else []
        self._agents = agents if agents is not None else []
        self._environment = environment
        self.logger = (
            logger if logger is not None else logging.getLogger("simulation_logger")
        )

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
        self.logger.info(f"Simulation {self.identifier} started.")
        for _ in range(self.epochs):
            if self.environment:
                await self.environment.interact(self.agents)
            for interaction in self.interactions:
                self.logger.info(f"Executing interaction: {interaction}")
        self.logger.info(f"Simulation {self.identifier} ended.")

    def to_dict(self):
        return {
            "id": self.identifier,
            "epochs": self.epochs,
            "interactions": self.interactions,
        }
