# Target Group

> **Note:** This feature is first supported since config version 0.1.1 

A target group is an abstraction of agents and consists of a defined number of agents. These agents are spawned with the help of an LLM.

## Required Parameters

 Parameter | Description |
-----------|-------------|
 `id` | The unique identifier of the target group |
 `role` | The role of the target group, defined by the user |
 `responsibilities` | The responsibilities of the target group, as a string |
 `num_agents` | The number of agents in the target group |
 `relationships` | The list of relationships to other target audiences |
