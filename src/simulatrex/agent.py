"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: agent.py
Description: Defines an agent, central unit in our simulation

"""
from typing import List
import uuid

from simulatrex.environment import BaseEnvironment
from simulatrex.config import (
    AgentIdentity,
    InitialConditions,
    AgentRelationship,
    AgentGroup,
    Objective,
)
from simulatrex.agent_utils.types import AgentType, AgentMemory, CognitiveModel
from simulatrex.agent_utils.perceive import perceive
from simulatrex.agent_utils.think import think
from simulatrex.event import Event
from simulatrex.utils.logger_config import Logger
from simulatrex.llm_utils.models import OpenAILanguageModel, LlamaLanguageModel
from simulatrex.llm_utils.prompts import PromptManager, TemplateType

logger = Logger()


class Message:
    def __init__(
        self,
        id: str,
        sender_id: str,
        receiver_id: str,
        content: str,
        group_id: str = None,
        metadata: any = {},
    ):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.group_id = group_id
        self.metadata = metadata


class BaseAgent:
    def __init__(
        self,
        id: str,
        type: AgentType,
        identity: AgentIdentity,
        initial_conditions: InitialConditions,
    ):
        self.id = "agent_" + id
        self.type = type

        self.identity = identity
        self.initial_conditions = initial_conditions

        self.relationships: List[AgentRelationship] = []
        self.groups: List[AgentGroup] = []

        self.memory = AgentMemory(
            self.id,
            decay_factor=initial_conditions["decay_factor"]
            if "decay_factor" in initial_conditions
            else 0.5,
        )


class LLMAgent(BaseAgent):
    def __init__(
        self,
        id: str,
        type: AgentType,
        identity: AgentIdentity,
        initial_conditions: InitialConditions,
        cognitive_model_id: str,
    ):
        super().__init__(id, type, identity, initial_conditions)

        self.cognitive_model_id = cognitive_model_id
        self.cognitive_model = None
        self.message_queue: List[Message] = []

        logger.debug(
            f"Agent {self.id} is using cognitive model {self.cognitive_model_id}"
        )
        self.init_cognition()

    def init_cognition(self):
        if self.cognitive_model_id == CognitiveModel.GPT_4.value:
            self.cognitive_model = OpenAILanguageModel(
                model_id=CognitiveModel.GPT_4, agent_id=self.id
            )
        elif self.cognitive_model_id == CognitiveModel.LLAMA_2_70b.value:
            self.cognitive_model = LlamaLanguageModel(
                model_id=CognitiveModel.LLAMA_2_70b, agent_id=self.id
            )
        else:
            raise NotImplementedError(
                f"Model {self.cognitive_model_id} not implemented yet"
            )

    async def perceive_event(self, event: Event, environment: BaseEnvironment):
        logger.debug(f"Agent {self.id} is processing event {event.id}")
        await perceive(
            self.cognitive_model,
            self.memory,
            self.identity,
            environment,
            event,
        )

    async def think(self, environment: BaseEnvironment):
        # Based on the provided envrioment make some thoughts
        await think(self.cognitive_model, self.memory, self.identity, environment)

    async def evaluate_outputs(
        self, environment: BaseEnvironment, objective: Objective
    ):
        logger.debug(f"Agent {self.id} is evaluating outputs")
        # Based on agent memory and environment, evaluate outputs
        prompt = PromptManager().get_filled_template(
            TemplateType.AGENT_EVALUATION,
            agent_name=self.identity.name,
            agent_output=self.memory.long_term_memory.retrieve_memory(
                environment.context, n_results=10
            ),
            environment=environment,
            objective=objective,
        )

        response = await self.cognitive_model.ask(prompt)
        return response

    def initiate_conversation(self):
        # Use the cognitive model to decide when to send a message and what the content should be
        if self.cognitive_model.should_send_message():  # You need to implement this
            content = self.cognitive_model.generate_message_content()  # And this
            receiver_id = self.choose_receiver()  # And this
            self.send_message(receiver_id, content)

    def send_message(self, receiver_id: str, content: str):
        message_id = str(uuid.uuid4())
        message = Message(message_id, self.id, receiver_id, content)
        return message

    async def process_messages(self):
        for message in self.message_queue:
            # Use the cognitive model to produce results
            converse_prompt = PromptManager().get_filled_template(
                TemplateType.AGENT_REPLY_TO_CONVERSATION,
                name=self.identity.name,
                age=self.identity.age,
                gender=self.identity.gender,
                persona=self.identity.persona,
                ethnicity=self.identity.ethnicity,
                language=self.identity.language,
                core_memories=", ".join(self.identity.core_memories),
                sender_identity=message.metadata,
                received_message=message.content,
            )

            response_content = await self.cognitive_model.ask(converse_prompt)

            # Send a reply message
            self.send_message(message.sender_id, response_content)

            # Remove current message object from queue
            self.message_queue = [
                msg for msg in self.message_queue if msg.id != message.id
            ]
