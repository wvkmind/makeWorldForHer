"""World state storage. Pure storage, no logic."""
import time
import json
import asyncio
from models import WorldState, StateUpdate
from typing import Callable, Awaitable

# In-memory state (single room for now)
_state = WorldState()
_listeners: list[Callable[[dict], Awaitable[None]]] = []


def get_state() -> WorldState:
    return _state


def update_state(update: StateUpdate) -> WorldState:
    """Apply partial update to world state. Returns new state."""
    changes = update.model_dump(exclude_none=True)
    for key, val in changes.items():
        setattr(_state, key, val)
    _state.last_ai_update = time.time()
    return _state


def set_engaged(engaged: bool):
    _state.engaged = engaged
    if engaged:
        _state.last_interaction = time.time()


def add_listener(fn: Callable[[dict], Awaitable[None]]):
    _listeners.append(fn)


def remove_listener(fn: Callable[[dict], Awaitable[None]]):
    if fn in _listeners:
        _listeners.remove(fn)


async def notify_listeners(event: dict):
    """Push event to all connected App clients."""
    for fn in _listeners[:]:
        try:
            await fn(event)
        except Exception:
            _listeners.remove(fn)
