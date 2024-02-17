"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: base.py
Description: Base class for all classes in the simulatrex package

"""

from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def to_dict(self):
        """This method should be implemented by subclasses."""
        raise NotImplementedError("This method is not implemented yet.")

    @abstractmethod
    def from_dict(cls, data):
        """This method should be implemented by subclasses."""
        raise NotImplementedError("This method is not implemented yet.")
