"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: agent.py
Description: Agent type defintions for the simulation

"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from collections import UserDict


class ActionSpec:
    """A specification of the action that agent is queried for.

    Attributes:
      call_to_action: fromated text that conditions agents response. {agent_id}
        and {timedelta} will be inserted by the agent.
      output_type: type of output - FREE, CHOICE or FLOAT
      options: if multiple choice, then provide possible answers here
      tag: a tag to add to the activity memory (e.g. action, speach, etc.)
    """

    call_to_action: str
    output_type: str
    options: Optional[List[str]] = None
    type: Optional[str] = None


OUTPUT_TYPES = ["FREE", "CHOICE", "FLOAT"]

DEFAULT_CALL_TO_SPEECH = (
    "Given the above, what is {agent_id} likely to say next? Respond in"
    ' the format `{agent_id} -- "..."` For example, '
    'Cristina -- "Hello! Mighty fine weather today, right?", '
    'Ichabod -- "I wonder if the alfalfa is ready to harvest", or '
    'Townsfolk -- "Good morning".\n'
)

DEFAULT_CALL_TO_ACTION = (
    "What would {agent_id} do for the next {timedelta}? "
    "Give a specific activity. Pick an activity that "
    "would normally take about {timedelta} to complete. "
    "If the selected action has a direct or indirect object then it "
    "must be specified explicitly. For example, it is valid to respond "
    'with "{agent_id} votes for Caroline because..." but not '
    'valid to respond with "{agent_id} votes because...".'
)


DEFAULT_ACTION_SPEC = ActionSpec(
    call_to_action=DEFAULT_CALL_TO_ACTION,
    output_type="FREE",
    options=None,
    type="action",
)


class Agent(BaseModel):
    identifier: str
    attributes: Dict[str, Union[str, int, float]]
    actions: List[str]
    instructions: str
    model_id: str
    memory: Optional[str]
    user_controlled: bool
    verbose: bool


class AgentRelationship(BaseModel):
    agent_id: str  # ID of the other agent in this relationship
    type: str  # E.g., "friend", "colleague"
    strength: float  # E.g., from 0 (acquaintance) to 1 (best friend)

    def summary(self) -> str:
        return f"{self.type.capitalize()} with {self.agent_id} at a strength level of {self.strength}"


class AgentGroup(BaseModel):
    id: str
    type: str  # E.g., "school", "company"
    member_agent_ids: List[str]
    metadata: Optional[Dict[str, Union[str, int, float]]]


class AgentsHierarchy(BaseModel):
    organizations: List[Dict[str, Union[str, List[str]]]]


class AgentResponse(UserDict):
    def __init__(self, *, question_name, answer, comment, prompts):
        super().__init__(
            {
                "question_name": question_name,
                "answer": answer,
                "comment": comment,
                "prompts": prompts,
            }
        )
