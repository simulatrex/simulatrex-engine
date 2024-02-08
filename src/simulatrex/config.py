"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: config.py
Description: Configuration for required env vars

"""

import os
from dotenv import load_dotenv, find_dotenv
from simulatrex.utils.errors import (
    InvalidEnvironmentVariableError,
)

SETTINGS = {
    "OPENAI_API_KEY": {
        "default": None,
        "allowed": None,
        "user_message": "Please provide your OpenAI API key.",
    },
    "API_CALL_TIMEOUT_SEC": {
        "default": "60",
        "allowed": None,
        "user_message": "What is the maximum number of seconds to wait for an API call to return?",
    },
}


class Config:
    def __init__(self):
        self._load_dotenv()
        self._set_env_vars()
        self._validate_attributes()

    def _load_dotenv(self) -> None:
        """
        Loads environment variables from the .env file.
        """
        load_dotenv(dotenv_path=find_dotenv(usecwd=True), override=True)

    def _set_env_vars(self) -> None:
        """Sets env vars as Config class attributes."""
        for env_var, config in SETTINGS.items():
            if value := os.getenv(env_var):
                setattr(self, env_var, value)
            elif default_value := config.get("default"):
                setattr(self, env_var, default_value)
                os.environ[env_var] = default_value

    def _validate_attributes(self):
        """Validates that all attributes are allowed values."""
        for attr, value in self.__dict__.items():
            config = SETTINGS.get(attr)
            if config.get("allowed") and value not in config.get("allowed"):
                raise InvalidEnvironmentVariableError(
                    f"Variable {attr} has value {value}, which is not allowed.\n"
                    f"Allowed values are: {config.get('allowed')}. "
                )

    def get(self, env_var: str) -> str:
        """
        Returns the value of an environment variable.
        - If the environment variable is valid but not set, attempts to set it.
        """
        if env_var not in SETTINGS:
            raise InvalidEnvironmentVariableError(
                f"Variable {env_var} is not a valid environment variable. "
                f"Valid environment variables are: {set(SETTINGS.keys())}."
            )
        return self.__dict__.get(env_var)


# Export singleton
global_config = Config()
