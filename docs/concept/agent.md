# Agent

An agent is the main entity in our simulation. 
Equipped with a cognitive model, an agent will have thoughts and interactions within the simulation environment.

## Required Parameters

 Parameter | Description |
-----------|-------------|
 `id` | The assigned id of the agent
 `type` | The type of the agent, at the moment only `LLM_AGENT` is supported |
 `cognitive_model` | The cognitive model assigned to the agent |
 `identity` | The identity attributes of an agent |
 `initial_conditions` | The initial conditions such as awareness |
 `relationships` | A list of relationship for the agent
 `group_affiliations` | A list of affiliated groups for the agent


## Available Cognitive Models

 Model | Name in config | Description |
-------|---------------------|-------------|
 `GPT_4` | `gpt-4` | A powerful language model developed by OpenAI |
 `GPT_4_TURBO` | `gpt-4-1106-preview` | A more efficient and cost-effective variant of GPT-4 |
 `LLAMA_2_70b` | `Llama2_70b` | A cognitive model developed for specific simulation tasks |


## Agent Identity

### Required Parameters

 Parameter | Description |
-----------|-------------|
 `name` | An illusive name for the agent |


### Optional Parameters

 Parameter | Description |
-----------|-------------|
 `age` | The age of the agent |
 `gender` | The gender of the agent |
 `ethnicity` | The ethnicity of the agent |
 `language` | The language the agent speaks |
 `persona` | The persona of the agent |
 `personality_description` | A brief description of the agent's personality |
 `traits` | The traits of the agent |
 `interests` | The interests of the agent |
 `knowledge_base` | The knowledge base of the agent |
 `skills` | The skills the agent possesses |
 `behaviour_patterns` | The behaviour patterns of the agent |
 `past_experiences` | The past experiences of the agent |
 `societal_role` | The societal role of the agent |
 `affiliations` | The affiliations of the agent |
 `current_state` | The current state of the agent |
 `core_memories` | The core memories of the agent |

