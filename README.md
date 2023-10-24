<h1 align="center">
        Simulatrex 🪄 
    </h1>
    <p align="center">
        <p align="center">Large Language Model (LLM) based simulation framework designed to run market research and social science simulations involving multi-agent structures and hierarchies
        <br>
        <br>
        <a href="https://cal.com/d42me/30min">Schedule Demo</a>
        ·
        <a href="https://github.com/simulatrex/simulatrex/issues/new?assignees=&labels=enhancement&projects=&title=%5BFeature%5D%3A+">Feature Request</a>
    </p>
<h4 align="center">
    <a href="https://pypi.org/project/simulatrex" target="_blank">
        <img src="https://img.shields.io/pypi/v/simulatrex.svg" alt="PyPI Version">
    </a>
    <a href="https://dominikscherm.substack.com/p/introducing-simulatrex">
        <img src="https://img.shields.io/badge/Documentation-Substack-orange" alt="Substack documentation">
    </a>
    <a href="https://discord.gg/THG27uRm">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
</h4>

<div align="center">
<img src="cover.png" alt="Simulatrex" width="300"/>
</div>
<br/>

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

## Simulation Examples

Simulatrex can be used for a variety of simulations. Here are a few examples:

### 1. Consumer Price Simulation

Simulate the impact of price changes on consumer behavior. This can help businesses understand how consumers might react to price increases or decreases, and make informed decisions about pricing strategies.

**Possible outcome**: 4 out of 10 agents stated that the price is too high.

### 2. Product Launch Simulation

Simulate the market response to a new product launch. By modeling different consumer personas and their potential reactions, businesses can get a sense of how a new product might be received and plan their marketing strategies accordingly.

**Possible outcome**: 7 out of 10 agents stated a positive buying intention.

### 3. Market Trend Simulation

Simulate broader market trends. This can help businesses anticipate changes in the market, identify opportunities for growth, and stay ahead of the competition.

**Possible outcome**: 6 out of 10 agents predicted a rising trend in the tech market due to increased interest in AI technologies.

---

Each simulation can be configured with specific metrics and targets. For example, in a product launch simulation, you might set the metric to "Buying intention among personas".

## Contributing
To contribute: Clone the repo locally -> Make a change -> Submit a PR with the change. 

Here's how to modify the repo locally: 
Step 1: Clone the repo 
```
git clone https://github.com/simulatrex/simulatrex
```

Step 2: Navigate into the project, setup a new virtual env (recommended) and install dependencies: 
```
cd simulatrex
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Step 3: Submit a PR with your changes! 🚀
- push your fork to your GitHub repo
- submit a PR from there 

# Support / talk with founders
- [Schedule Demo 👋](https://cal.com/d42me/30min)
- [Community Discord 💭](https://discord.gg/THG27uRm)
- Email ✉️ dom@simulatrex.com

# Why did we build this 
With Simulatrex we want to make rapid market simulations accessible to every professional out in the world. We aim for:

- Accessibility

    We allow everyone to run simulations, fast. That means the setup should be simple, intuitive, and explainable. As outlined social simulations following complex environments are currently hard to conduct. It takes days to outline the starting conditions. By fine-tuning our own models, we want to rapidly decrease the setup time.

- Performance

    By paralleling processes we aim for the maximum speed so that simulations take hours instead of days or weeks.


- Dynamic without limits

    Our world is constantly changing, so it’s a preliminary requirement for a social simulation framework to model dynamic environments. Simulatrex allows that by introducing a novel event engine, that releases an event at a certain time or follows natural language-described triggers.
