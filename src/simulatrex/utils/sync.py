"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: sync.py
Description: Synchronous wrapper for asynchronous functions

"""

import functools
import asyncio
import nest_asyncio

nest_asyncio.apply()


def sync_wrapper(async_func):
    """Decorator to create a synchronous wrapper for an asynchronous function."""

    @functools.wraps(async_func)
    def wrapper(*args, **kwargs):
        return asyncio.run(async_func(*args, **kwargs))

    return wrapper
