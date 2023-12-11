# Target Group Relationship

> **Note:** This feature is first supported since config version 0.1.1 

A relationship in the context of a simulation represents the connection between two target groups. It defines how these target groups interact with each other within the simulation.

## Required Parameters

 Parameter | Description |
-----------|-------------|
 `target_group_id` | The id of the target group involved in the relationship |
 `type` | The type of relationship, can be chosen by the user (e.g., 'collaborate') |
 `strength` | The strength of the relationship, a number between 0 and 1 |
