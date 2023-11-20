from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    avatar_url: Optional[str] = None


class SimulationBase(BaseModel):
    id: str
    name: str
    description: str
    author: str
