"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: behavioral_test.py
Description: Behavioral Test

"""
from simulatrex import TargetGroup
from simulatrex.utils.log import SingletonLogger

_logger = SingletonLogger


class BehavioralTest:
    def __init__(self, audience: TargetGroup):
        self.audience = audience
        self.tests = []

    def add_conversational_test(self, title: str, questions: list, iterations: int):
        self.tests.append(
            {"title": title, "questions": questions, "iterations": iterations}
        )

    async def run(self):
        # Placeholder for running the test
        results = {"test_results": []}
        agent_responses = []

        async for agent_response in self.audience.run_conversation_test(
            self.tests[0]["questions"], self.tests[0]["iterations"]
        ):
            agent_responses.append(agent_response)
            _logger.info(f"Agent response: {agent_response}")
            yield agent_response

    def summarize(self):
        return "Behavioral Test Results: " + str(self.run())
