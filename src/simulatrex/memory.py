"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: memory.py
Description: Defines the memory class, which is used to define the memory of an agent

"""
import math
import uuid
from typing import List

from pydantic import BaseModel

from simulatrex.utils.time_utils import TimeUtils
from simulatrex.vectordb import VectorDB


class MemoryUnit(BaseModel):
    type: str
    depth: float
    content: str
    keywords: List[str]

    id: str = str(uuid.uuid4())
    created: int = 0
    last_accessed: int = 0

    def get_metadata(self):
        return {
            "id": self.id,
            "type": self.type,
            "depth": self.depth,
            "created": self.created,
            "last_accessed": self.last_accessed,
            "keywords": ",".join(self.keywords),
        }


class BaseMemory:
    def __init__(self, id: str):
        self.id = id
        self.vector_db = VectorDB(collection_name=id)

    def add_memory(self, memory_unit: MemoryUnit):
        self.vector_db.add_memory(
            memory_unit.content, metadatas=[memory_unit.get_metadata()]
        )

    def retrieve_memory(self, content: str, n_results: int):
        results = self.vector_db.query_memory(content, n_results=n_results)
        return results


class ShortTermMemory(BaseMemory):
    def __init__(self, id: str, decay_factor: int):
        stm_id = "stm_" + id
        super().__init__(stm_id)
        self.decay_factor = decay_factor

    def retrieve_memory(self, content: str, n_results: int, current_timestamp: int):
        results = self.vector_db.query_memory(content, n_results=n_results)

        # Apply decay factor to the results based on the 'created' date
        for memory in results:
            time_diff = current_timestamp - TimeUtils.to_timestamp(
                memory["last_accessed"]
            )
            memory["score"] *= math.exp(-self.decay_factor * time_diff)

        # Sort the results by score in descending order
        results.sort(key=lambda x: x["score"], reverse=True)
        return results


class LongTermMemory(BaseMemory):
    def __init__(self, id: str):
        ltm_id = "ltm_" + id
        super().__init__(ltm_id)
