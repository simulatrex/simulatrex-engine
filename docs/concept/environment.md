# Environment

The environment is the surrounding of our simulation. There are two types of environments:

- Static: The environment does not change over the course of the simulation.
- Dynamic: The environment changes over the course of the simulation based on certain conditions or parameters.

## Required Parameters

 Parameter | Description |
-----------|-------------|
 `type` | The type of the environment (`STATIC` or `DYNAMIC`) |
 `context` | The context of the environment |
 `description` | A detailed description of the environment |
 `entities` | A list of entities present in the environment |
 `time_config` | The configuration for time in the environment |

## Time Config 

Simulations run in the realm of real time. However, with the `time_multiplier` parameter, you can define the speed of a simulation run. This parameter allows you to control how fast time passes in the simulation relative to real time. For example, a `time_multiplier` of 86400 would make one iteration in the simulation equivalent to one day in real time.

### Required Parameters

 Parameter | Description |
-----------|-------------|
 `start_time` | The start time of the simulation |
 `end_time` | The end time of the simulation |
 `time_multiplier` | The multiplier for time used in the simulation |


