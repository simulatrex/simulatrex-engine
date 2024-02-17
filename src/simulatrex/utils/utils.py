"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: utils.py
Description: Utility functions

"""

import json
import keyword
import random
import re
import string
from typing import Callable


def random_string() -> str:
    """Generate a random string of fixed length"""
    return "".join(random.choice(string.ascii_letters) for i in range(10))


def shortname_proposal(question, max_length=None):
    """Take a question text and generate a slug"""
    question = question.lower()
    tokens = question.split()
    stopwords = set(
        [
            "is",
            "your",
            "who",
            "the",
            "a",
            "an",
            "of",
            "could",
            "you",
            "what",
            "when",
            "where",
            "why",
            "in",
            "and",
            "to",
            "how",
            "are",
            "what",
        ]
    )
    filtered_tokens = [
        token.strip(string.punctuation) for token in tokens if token not in stopwords
    ]
    heading = "_".join(filtered_tokens)
    # Limit length if needed
    if max_length and len(heading) > max_length:
        heading = heading[:max_length]
    while heading.endswith("_"):  # trim any trailing _ characters
        heading = heading[:-1]
    return heading


def merge_dicts(dict_list):
    """Merges a list of dictionaries into a single dictionary."""
    result = {}
    all_keys = set()
    for d in dict_list:
        all_keys.update(d.keys())
    for key in all_keys:
        result[key] = [d.get(key, None) for d in dict_list]
    return result


def is_valid_variable_name(name):
    return name.isidentifier() and not keyword.iskeyword(name)


def create_valid_var_name(s, transform_func: Callable = lambda x: x.lower()) -> str:
    """Creates a valid variable name from a string."""
    if transform_func is None:
        transform_func = lambda x: x

    # Ensure the string is not empty
    if not s:
        raise ValueError("Input string cannot be empty.")

    if is_valid_variable_name(s):
        return transform_func(s)

    # Remove leading numbers if they exist since variable names can't start with a number
    s = re.sub("^[0-9]+", "", s)

    # Replace invalid characters (anything not a letter, number, or underscore) with an underscore
    s = re.sub("[^0-9a-zA-Z_]", "_", s)

    # Check if the first character is a number; if so, prepend an underscore
    if re.match("^[0-9]", s):
        s = "_" + s

    if s in keyword.kwlist:
        s += "_"

    # Ensure the string is not empty after the transformations
    if not s:
        raise ValueError(
            "Input string does not contain valid characters for a variable name."
        )

    return transform_func(s)


def shorten_string(s, max_length, placeholder="..."):
    if len(s) <= max_length:
        return s

    # Length to be removed
    remove_length = len(s) - max_length + len(placeholder)

    # Find the indices to start and end removal
    start_remove = (len(s) - remove_length) // 2
    end_remove = start_remove + remove_length

    # Adjust start and end to break at spaces (if possible)
    start_space = s.rfind(" ", 0, start_remove)
    end_space = s.find(" ", end_remove)

    if start_space != -1 and end_space != -1:
        start_remove = start_space
        end_remove = end_space
    elif start_space != -1:
        start_remove = start_space
    elif end_space != -1:
        end_remove = end_space

    return s[:start_remove] + placeholder + s[end_remove:]


def text_to_shortname(long_text, forbidden_names=[]):
    """Creates a slug for the question"""
    proposed_name = shortname_proposal(long_text)
    counter = 1
    # make sure the name is unique
    while proposed_name in forbidden_names:
        proposed_name += f"_{counter}"
        counter += 1
    return proposed_name


def extract_json_from_string(s):
    """Extracts a JSON string from a string."""
    # Find the first occurrence of '{'
    start_idx = s.find("{")
    # Find the last occurrence of '}'
    end_idx = s.rfind("}")
    # If both '{' and '}' are found in the string
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        # Extract the substring from start_idx to end_idx (inclusive)
        json_str = s[start_idx : end_idx + 1]
        return json_str
    else:
        raise ValueError("No JSON object found in string")


def valid_json(json_string):
    try:
        _ = json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False
