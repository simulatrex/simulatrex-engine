from simulatrex.llms.models.models import OpenAILanguageModel


class Agent:
    def __init__(self, identifier, llm_id=None):
        self.identifier = identifier
        self.llm = OpenAILanguageModel(model_id=llm_id) if llm_id else None

    async def act(self):
        if self.llm:
            response = await self.llm.ask("Generate an action.")
            print(f"Agent {self.identifier} action: {response}")
        else:
            print(f"Agent {self.identifier} has no LLM to generate action.")


class Environment:
    def __init__(self, identifier):
        self.identifier = identifier

    async def interact(self, agents):
        print(
            f"Environment {self.identifier} is facilitating interaction among agents."
        )
        for agent in agents:
            # Example interaction: asking each agent to generate an action
            await agent.act()


class Simulation:
    def __init__(self, identifier, agents=None, environment=None):
        self.identifier = identifier
        self.agents = agents if agents is not None else []
        self.environment = environment

    async def run(self):
        print(f"Simulation {self.identifier} started.")
        if self.environment:
            await self.environment.interact(self.agents)
        print(f"Simulation {self.identifier} ended.")
