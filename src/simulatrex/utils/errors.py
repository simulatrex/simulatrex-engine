"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: errors.py
Description: Custom exceptions

"""


class AgentErrors(Exception):
    pass


class AgentCombinationError(AgentErrors):
    pass


class AgentLLMError(AgentErrors):
    pass


class AgentRespondedWithBadJSONError(AgentErrors):
    pass


class FailedTaskException(Exception):
    def __init__(self, message, agent_response_dict):
        super().__init__(message)
        self.agent_response_dict = agent_response_dict


class DatabaseErrors(Exception):
    pass


class DatabaseConnectionError(DatabaseErrors):
    pass


class ConfigurationError(Exception):
    """Base exception for errors."""

    pass


class InvalidEnvironmentVariableError(ConfigurationError):
    """Raised when an environment variable is invalid."""

    pass


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when an expected environment variable is missing."""

    pass


class LanguageModelExceptions(Exception):
    pass


class LanguageModelResponseNotJSONError(LanguageModelExceptions):
    pass


class PromptError(Exception):
    pass


class TemplateRenderError(PromptError):
    pass


class QuestionErrors(Exception):
    pass


class QuestionAnswerValidationError(QuestionErrors):
    pass


class QuestionAttributeMissing(QuestionErrors):
    pass


class QuestionSerializationError(QuestionErrors):
    pass


class QuestionScenarioRenderError(QuestionErrors):
    pass


class QuestionMissingTypeError(QuestionErrors):
    pass


class QuestionBadTypeError(QuestionErrors):
    pass


class ResultsErrors(Exception):
    pass


class ResultsBadMutationError(ResultsErrors):
    pass


class ResultsColumnNotFoundError(ResultsErrors):
    pass


class ResultsInvalidNameError(ResultsErrors):
    pass


class ResultsMutateError(ResultsErrors):
    pass
