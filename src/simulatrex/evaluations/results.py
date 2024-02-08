"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: results.py
Description: Results class for the simulatrex package

"""

from __future__ import annotations
from collections import UserList, defaultdict
from typing import Any, Type, Union

from simulatrex.agents.agent import Agent
from simpleeval import EvalWithCompoundTypes

from simulatrex.base import Base
from simulatrex.evaluations.result import Result
from simulatrex.experiments.scenarios.scenario import Scenario
from simulatrex.experiments.surveys.survey import Survey
from simulatrex.llms.llm_base import LanguageModel
from simulatrex.utils.errors import (
    ResultsBadMutationError,
    ResultsColumnNotFoundError,
    ResultsInvalidNameError,
    ResultsMutateError,
)
from simulatrex.utils.utils import is_valid_variable_name, shorten_string
from simulatrex.evaluations.dataset import Dataset


class Results(UserList, Base):
    """
    This class is a UserList of Result objects.
    """

    def __init__(
        self,
        survey: Survey = None,
        data: list[Result] = None,
        created_columns: list = None,
        total_results: int = None,
    ):
        super().__init__(data)
        self.survey = survey
        self.created_columns = created_columns or []
        self._total_results = total_results

    def __getitem__(self, i):
        if isinstance(i, slice):
            # Return a sliced view of the list
            return self.__class__(survey=self.survey, data=self.data[i])
        else:
            # Return a single item
            return self.data[i]

    def __repr__(self) -> str:
        return f"Results(data = {self.data}, survey = {repr(self.survey)}, created_columns = {self.created_columns})"

    def to_dict(self) -> dict[str, Any]:
        """Converts the Results object to a dictionary"""
        return {
            "data": [result.to_dict() for result in self.data],
            "survey": self.survey.to_dict(),
            "created_columns": self.created_columns,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Results:
        """Converts a dictionary to a Results object"""
        results = cls(
            survey=Survey.from_dict(data["survey"]),
            data=[Result.from_dict(r) for r in data["data"]],
            created_columns=data.get("created_columns", None),
        )
        return results

    @property
    def _key_to_data_type(self) -> dict[str, str]:
        """
        Returns a mapping of keys (how_feeling, status, etc.) to strings representing data types (objects such as Agent, Answer, Model, Scenario, etc.)
        """
        d = {}
        for result in self.data:
            d.update(result.key_to_data_type)
        for column in self.created_columns:
            d[column] = "answer"
        return d

    @property
    def _data_type_to_keys(self) -> dict[str, str]:
        """
        Returns a mapping of strings representing data types (objects such as Agent, Answer, Model, Scenario, etc.) to keys (how_feeling, status, etc.)
        """
        d = defaultdict(set)
        for result in self.data:
            for key, value in result.key_to_data_type.items():
                d[value] = d[value].union(set({key}))
        for column in self.created_columns:
            d["answer"] = d["answer"].union(set({column}))
        return d

    @property
    def answer_keys(self) -> dict[str, str]:
        """Returns a mapping of answer keys to question text"""
        answer_keys = self._data_type_to_keys["answer"]
        answer_keys = {k for k in answer_keys if "_comment" not in k}
        questions_text = [
            self.survey.get_question(k).question_text for k in answer_keys
        ]
        short_question_text = [shorten_string(q, 80) for q in questions_text]
        return dict(zip(answer_keys, short_question_text))

    @property
    def agents(self) -> list[Agent]:
        return [r.agent for r in self.data]

    @property
    def models(self) -> list[Type[LanguageModel]]:
        return [r.model for r in self.data]

    @property
    def scenarios(self) -> list[Scenario]:
        return [r.scenario for r in self.data]

    @property
    def agent_keys(self) -> set[str]:
        """Returns a set of all of the keys that are in the Agent data"""
        return self._data_type_to_keys["agent"]

    @property
    def model_keys(self) -> set[str]:
        """Returns a set of all of the keys that are in the LanguageModel data"""
        return self._data_type_to_keys["model"]

    @property
    def scenario_keys(self) -> set[str]:
        """Returns a set of all of the keys that are in the Scenario data"""
        return self._data_type_to_keys["scenario"]

    @property
    def question_names(self) -> list[str]:
        """Returns a list of all of the question names"""
        if self.survey is None:
            return []
        return list(self.survey.question_names)

    @property
    def all_keys(self) -> set[str]:
        """Returns a set of all of the keys that are in the Results"""
        answer_keys = set(self.answer_keys)
        return (
            answer_keys.union(self.agent_keys)
            .union(self.scenario_keys)
            .union(self.model_keys)
        )

    def relevant_columns(self) -> set[str]:
        """Returns all of the columns that are in the results."""
        return set().union(
            *(observation.combined_dict.keys() for observation in self.data)
        )

    def _parse_column(self, column: str) -> tuple[str, str]:
        """
        Parses a column name into a tuple containing a data type and a key.
        """
        if "." in column:
            data_type, key = column.split(".")
        else:
            try:
                data_type, key = self._key_to_data_type[column], column
            except KeyError:
                raise ResultsColumnNotFoundError(f"Column {column} not found in data")
        return data_type, key

    def first(self) -> Result:
        """Returns the first observation in the results."""
        return self.data[0]

    def mutate(self, new_var_string: str, functions_dict: dict = None) -> Results:
        """
        Creates a value in the Results object as if has been asked as part of the survey.
        """
        # extract the variable name and the expression
        if "=" not in new_var_string:
            raise ResultsBadMutationError(
                f"Mutate requires an '=' in the string, but '{new_var_string}' doesn't have one."
            )
        raw_var_name, expression = new_var_string.split("=", 1)
        var_name = raw_var_name.strip()
        if not is_valid_variable_name(var_name):
            raise ResultsInvalidNameError(f"{var_name} is not a valid variable name.")

        # create the evaluator
        functions_dict = functions_dict or {}

        def create_evaluator(result: Result) -> EvalWithCompoundTypes:
            return EvalWithCompoundTypes(
                names=result.combined_dict, functions=functions_dict
            )

        def new_result(old_result: Result, var_name: str) -> Result:
            evaluator = create_evaluator(old_result)
            value = evaluator.eval(expression)
            new_result = old_result.copy()
            new_result["answer"][var_name] = value
            return new_result

        try:
            new_data = [new_result(result, var_name) for result in self.data]
        except Exception as e:
            raise ResultsMutateError(f"Error in mutate. Exception:{e}")

        return Results(
            survey=self.survey,
            data=new_data,
            created_columns=self.created_columns + [var_name],
        )

    def select(self, *columns: Union[str, list[str]]) -> Dataset:
        """
        This selects data from the results and turns it into a format
        """

        if not columns or columns == ("*",) or columns == (None,):
            columns = ("*.*",)

        if isinstance(columns[0], list):
            columns = tuple(columns[0])

        known_data_types = ["answer", "scenario", "agent", "model", "prompt"]

        def get_data_types_to_return(parsed_data_type):
            if parsed_data_type == "*":  # they want all of the columns
                return known_data_types
            else:
                if parsed_data_type not in known_data_types:
                    raise Exception(
                        f"Data type {parsed_data_type} not found in data. Did you mean one of {known_data_types}"
                    )
                return [parsed_data_type]

        # we're doing to populate this with the data we want to fetch
        to_fetch = defaultdict(list)

        new_data = []
        items_in_order = []
        # iterate through the passed columns
        for column in columns:
            # a user could pass 'result.how_feeling' or just 'how_feeling'
            parsed_data_type, parsed_key = self._parse_column(column)
            data_types = get_data_types_to_return(parsed_data_type)
            found_once = False  # we need to track this to make sure we found the key at least once

            for data_type in data_types:
                # the keys for that data_type e.g.,# if data_type is 'answer', then the keys are 'how_feeling', 'how_feeling_comment', etc.
                relevant_keys = self._data_type_to_keys[data_type]

                for key in relevant_keys:
                    if key == parsed_key or parsed_key == "*":
                        found_once = True
                        to_fetch[data_type].append(key)
                        items_in_order.append(data_type + "." + key)

            if not found_once:
                raise Exception(f"Key {parsed_key} not found in data.")

        for data_type in to_fetch:
            for key in to_fetch[data_type]:
                entries = self._fetch_list(data_type, key)
                new_data.append({data_type + "." + key: entries})

        def sort_by_key_order(dictionary):
            # Extract the single key from the dictionary
            single_key = next(iter(dictionary))
            # Return the index of this key in the list_of_keys
            return items_in_order.index(single_key)

        sorted(new_data, key=sort_by_key_order)

        return Dataset(new_data)

    def sort_by(self, column, reverse=True) -> Results:
        "Sorts the results by a column"

        data_type, key = self._parse_column(column)

        def to_numeric_if_possible(v):
            try:
                return float(v)
            except:
                return v

        new_data = sorted(
            self.data,
            key=lambda x: to_numeric_if_possible(x.get_value(data_type, key)),
            reverse=reverse,
        )
        return Results(survey=self.survey, data=new_data, created_columns=None)

    def filter(self, expression) -> Results:
        """
        This filters a result based on the expression that is passed in.
        """

        def create_evaluator(result):
            return EvalWithCompoundTypes(names=result.combined_dict)

        try:
            new_data = [
                result
                for result in self.data
                if create_evaluator(result).eval(expression)
            ]
        except Exception as e:
            print(f"Exception:{e}")

        return Results(survey=self.survey, data=new_data, created_columns=None)

    def __str__(self):
        return self.rich_print()
