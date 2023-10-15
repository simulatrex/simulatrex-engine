# Simulatrex

Full description and examples can be found here: https://dominikscherm.substack.com/p/introducing-simulatrex.

Simulatrex is a Large Language Model (LLM) based simulation framework designed to run social science simulations involving multi-agent structures and hierarchies. It provides a robust and flexible platform for creating and running complex simulations, making it an ideal tool for researchers and developers in the field of social sciences, artificial intelligence, and more.

## Features

- Multi-Agent Simulations: Simulatrex allows you to create simulations with multiple agents, each with their own identities, initial conditions, and cognitive models.
- Dynamic Environments: Simulatrex supports both static and dynamic environments, allowing for a wide range of simulation scenarios.
- Event-Driven: Simulatrex simulations are event-driven, with a built-in event engine to process events and update the environment.
- Evaluation Engine: Simulatrex includes an evaluation engine to evaluate the outputs of the agents based on predefined objectives and metrics.
- Language Model Integration: Simulatrex integrates with language models like OpenAI's GPT-4, enabling agents to generate human-like responses.

## Installation

To install Simulatrex, you need to have Python 3.6 or higher. You can install it using pip:

```
pip install simulatrex
```

## Usage

Here is a basic example of how to use Simulatrex:

```
import asyncio
import dotenv
from simulatrex import SimulationEngine

dotenv.load_dotenv()

async def main():
    engine = SimulationEngine("./data/1_consumer_price_simulation_config.json")
    await engine.run()


if __name__ == "__main__":
    asyncio.run(main())
```

In this example, we're creating a new SimulationEngine with a configuration file and then running the simulation.
