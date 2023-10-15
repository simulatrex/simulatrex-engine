"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: memory.py
Description: Defines the memory class, which is used to define the memory of an agent

"""
import math
import uuid
from typing import List

from pydantic import BaseModel

from simulatrex.db import SqliteDB, MemoryUnitDB
from simulatrex.utils.logger_config import Logger
from simulatrex.utils.time_utils import TimeUtils
from simulatrex.vectordb import VectorDB

logger = Logger()


class MemoryUnitModel(BaseModel):
    type: str
    depth: float
    content: str
    keywords: str

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
            "keywords": self.keywords,
        }


class ShortTermMemory:
    def __init__(self, id: str, decay_factor: int):
        stm_id = "stm_" + id
        self.vector_db = VectorDB(stm_id)
        self.decay_factor = decay_factor

    def add_memory(self, memory_unit: MemoryUnitModel):
        logger.debug(f"Adding memory with id {memory_unit.id} to {self.id}")
        self.vector_db.add_memory(
            memory_unit.content,
            metadatas=[memory_unit.get_metadata()],
            ids=[memory_unit.id],
        )

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


class LongTermMemory:
    def __init__(self, id: str):
        ltm_id = "ltm_" + id
        self.db = SqliteDB(ltm_id)

    def add_memory(self, memory_unit: MemoryUnitModel):
        memory_unit_db = MemoryUnitDB(**memory_unit.model_dump())
        logger.debug(f"Adding memory with id {memory_unit_db.id}")
        self.db.insert_memory(memory_unit_db)

    def query_memory_by_type(self, type: str, n_results: int = 5):
        return self.db.query_memory_by_type(type, n_results)
