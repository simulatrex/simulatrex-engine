"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: log_config.py
Description: Log helper

"""
import logging
import json

from termcolor import colored


class Logger:
    def __init__(
        self,
        name="simulatrex-agents",
        log_file="run.log",
        response_log_file="response.log",
    ):
        # Create logger
        self.logger = logging.getLogger(name)
        self.agent_logger = logging.getLogger("agent_logger")
        if not self.logger.handlers:  # Check if logger already has handlers
            self.logger.setLevel(logging.DEBUG)  # Set default logging level

            # Create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # Create file handler and set level to debug
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)

            # Create file handler for response log
            rh = logging.FileHandler(response_log_file)
            rh.setLevel(logging.INFO)

            # Create formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # Add formatter to handlers
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            rh.setFormatter(formatter)

            # Add handlers to logger
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

            self.agent_logger.addHandler(rh)

    def debug(self, msg):
        self.logger.debug(colored(msg, "blue"))

    def info(self, msg):
        self.logger.info(colored(msg, "green"))

    def warning(self, msg):
        self.logger.warning(colored(msg, "yellow"))

    def error(self, msg):
        self.logger.error(colored(msg, "red"))

    def log_agent_response(self, agent_id: str, response: str):
        response_dict = {"agent_id": agent_id, "response": response}
        self.agent_logger.info(json.dumps(response_dict), extra={"handler": "rh"})
