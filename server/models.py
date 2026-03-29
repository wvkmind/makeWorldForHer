"""Shared data models for World Server."""
from pydantic import BaseModel
from typing import Optional
import time


class WorldState(BaseModel):
    scene: str = "bedroom"
    action: str = "sleeping"
    expression: str = "sleepy"
    time_of_day: str = "night"
    outfit: str = "H05"
    engaged: bool = False
    last_interaction: float = 0
    last_ai_update: float = 0

    def to_dict(self):
        return self.model_dump()


class StateUpdate(BaseModel):
    scene: Optional[str] = None
    action: Optional[str] = None
    expression: Optional[str] = None
    time_of_day: Optional[str] = None
    outfit: Optional[str] = None
    engaged: Optional[bool] = None


class UserMessage(BaseModel):
    message: str


class AIResponse(BaseModel):
    reply: str
    state_update: Optional[StateUpdate] = None


class AIPush(BaseModel):
    """AI-initiated state change (heartbeat, schedule, etc.)"""
    message: Optional[str] = None
    state_update: StateUpdate
