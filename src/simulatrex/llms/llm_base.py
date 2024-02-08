"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: llm_base.py
Description: Language Model Base Class

"""

from __future__ import annotations
from functools import wraps
import json
from abc import ABC, abstractmethod

from typing import Any
from simulatrex.utils.errors import (
    LanguageModelResponseNotJSONError,
)


class LanguageModel(ABC):
    """ABC for LLM subclasses."""

    _model_ = None

    def __init__(self, **kwargs):
        self.model = getattr(self, "_model_", None)
        default_parameters = getattr(self, "_parameters_", None)
        parameters = self._overide_default_parameters(kwargs, default_parameters)
        self.parameters = parameters

        for key, value in parameters.items():
            setattr(self, key, value)

        for key, value in kwargs.items():
            if key not in parameters:
                setattr(self, key, value)

    @staticmethod
    def _overide_default_parameters(passed_parameter_dict, default_parameter_dict):
        """Returns a dictionary of parameters, with passed parameters taking precedence over defaults."""
        parameters = dict({})
        for parameter, default_value in default_parameter_dict.items():
            if parameter in passed_parameter_dict:
                parameters[parameter] = passed_parameter_dict[parameter]
            else:
                parameters[parameter] = default_value
        return parameters

    @abstractmethod
    async def async_execute_model_call():
        pass

    def _save_response_to_db(self, prompt, system_prompt, response):
        try:
            output = json.dumps(response)
        except json.JSONDecodeError:
            raise LanguageModelResponseNotJSONError
        self.crud.write_LLMOutputData(
            model=str(self.model),
            parameters=str(self.parameters),
            system_prompt=system_prompt,
            prompt=prompt,
            output=output,
        )

    def to_dict(self) -> dict[str, Any]:
        """Converts instance to a dictionary."""
        return {"model": self.model, "parameters": self.parameters}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model = '{self.model}', parameters={self.parameters})"
