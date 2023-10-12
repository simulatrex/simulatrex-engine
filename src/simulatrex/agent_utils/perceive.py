"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: perceive.py
Description: Perceive the current enviroment and what is happening

"""
from simulatrex.environment import BaseEnvironment
from simulatrex.config import AgentIdentity
from simulatrex.llm_utils.prompts import PromptManager, TemplateType
from simulatrex.llm_utils.models import BaseLanguageModel
from simulatrex.utils.logger_config import Logger
from simulatrex.event import Event
from .types import AgentMemory

logger = Logger()


async def perceive(
    cognitive_model: BaseLanguageModel,
    memory: AgentMemory,
    identity: AgentIdentity,
    environment: BaseEnvironment,
    event: Event,
):
    """
    Perceive the current event and what is happening
    """
    recent_memories = memory.short_term_memory.retrieve_memory(
        event.content, n_results=5
    )

    logger.debug("Recent memories: %s", recent_memories)

    # Based on event content make a decision and request model
    prompt = PromptManager().get_filled_template(
        TemplateType.AGENT_PERCEPTION,
        name=identity.name,
        age=identity.age,
        gender=identity.gender,
        persona=identity.persona,
        ethnicity=identity.ethnicity,
        language=identity.language,
        core_memories=", ".join(identity.core_memories),
        recent_memories=", ".join(recent_memories),
        environment_description=environment.description,
        environment_context=environment.context,
        environment_entities=", ".join(environment.entities),
        event=event,
    )

    response = await cognitive_model.ask(prompt)

    logger.debug(response)

    return response
