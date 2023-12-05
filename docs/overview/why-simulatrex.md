# Why LLM-based simulations?

Simulations are already widely used in social sciences to apply theories and to understand underlying implications. Currently, if you speak about simulations for example in sociology or economics, you are referring to one of these techniques:

- **Agent-Based Modeling (ABM):** Uses autonomous agents that follow specified rules and interact with one another or with their environment. The interactions can lead to emergent phenomena at the system level.

- **System Dynamics:** Focuses on the feedback loops and time delays to model the behavior of complex systems over time. It uses stocks (accumulations) and flows (transitions) for representation.

- **Cellular Automata:** Spatially explicit models where grid cells evolve based on a set of rules and states of neighboring cells.

- **Monte Carlo Simulation:** Uses randomness to solve problems that might be deterministic. It repeatedly runs simulations using random inputs within predefined constraints and then analyzes the distribution of results.

If you apply for example ABM you need to define the behavior of each agent and decisions are made by a statistical model, which is defined by the same group that defined the in- and outputs. So simulations that involve human behavior still lack accuracy.

There is a pressing need for more accurate and real-world-like simulations that are more capable of mimicking human behavior.

In a recent paper “Turning large language models into cognitive models“ by Binz et al., 2023 researchers demonstrated that large language models can be turned into cognitive models by finetuning their final layer. This implies that we can use adjusted LLMs to mimic human behavior.

Following this research, Park et al. conducted a large-scale simulation with agents using GPT 3.5-turbo as their cognitive model referring to their infamous paper “Generative Agents: Interactive Simulacra of Human Behavior”. The agents are equipped with different personality traits and act in a virtual environment (a virtual town). The agents can perceive, plan, act, and reflect on their actions. They can even dialogue with other agents.

After running the simulation with 25 agents for two days, the agent showed emergent behavior. For evaluation purposes, each memory, action, and conversation of an agent was recorded to evaluate and understand their decision-making. They also started interviewing the agents with a panel of participants and found out that their system produces realistic actions. They believe that generative agents can be used in many interactive tools, from design software to social platforms to virtual settings.
