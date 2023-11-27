"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: spawn.py
Description: Spawn Agent Utility

"""
from typing import Optional
import uuid
from simulatrex.agent import LLMAgent
from simulatrex.config import AgentIdentity, InitialConditions
from simulatrex.llm_utils.models import BaseLanguageModel
from simulatrex.llm_utils.prompts import PromptManager, TemplateType
from simulatrex.utils.log import SingletonLogger

_logger = SingletonLogger


async def spawn_agent(
    cognitive_model: BaseLanguageModel,
    cognitive_model_id: str,
    role: str,
    responsibilities: str,
    initial_conditions: Optional[InitialConditions] = None,
):
    """
    Spawn a new agent
    """
    prompt = PromptManager().get_filled_template(
        TemplateType.AGENT_IDENTITY_SPAWN,
        role=role,
        responsibilities=responsibilities,
    )

    try:
        agent_identity = await cognitive_model.generate_structured_output(
            prompt, AgentIdentity
        )
    except Exception as e:
        _logger.error(f"Error while asking LLM: {e}")

        # Try request again
        agent_identity = await cognitive_model.generate_structured_output(
            prompt, AgentIdentity
        )

    # Instantiate an LLMAgent
    agent = LLMAgent(
        id=str(uuid.uuid4()),
        type="LLM_AGENT",
        identity=agent_identity,
        initial_conditions=initial_conditions,
        cognitive_model_id=cognitive_model_id,
    )

    return agent
