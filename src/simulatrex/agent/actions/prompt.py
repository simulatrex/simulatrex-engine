"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: prompt.py
Description: Agent prompt response

"""
from typing import Any, List
from simulatrex.agent.utils.types import AgentMemory
from simulatrex.experiments.possibleworlds.config import AgentIdentity
from simulatrex.llm_utils.models import BaseLanguageModel
from simulatrex.llm_utils.prompts import PromptManager, TemplateType


async def prompt_response(
    cognitive_model: BaseLanguageModel, question: str, attributes: dict
):
    prompt_manager = PromptManager()
    prompt = prompt_manager.get_filled_template(
        TemplateType.AGENT_BEHAVIORAL_RESPONSE,
        question=question,
        attributes=attributes,
    )
    response = await cognitive_model.ask(prompt)

    return response
