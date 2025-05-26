# This file makes the agent directory a Python package. 

# You might want to expose key classes from the agent submodules here, for example:
# from .views import AgentSettings, AgentOutput
# from .message_manager.service import MessageManager
# from .memory.service import AgentMemory
# from .prompts import SystemPrompt

# For now, keeping it simple. Can be expanded as the agent develops.

# flake8: noqa
# Export AgentSettings and AgentOutput from views.py
from .views import (
    AgentSettings,
    AgentThought,
    AgentOutput,
    # ActionResult, # Not defined in views.py
    # AgentHistory, # Not defined in views.py
    # AgentState,   # Not defined in views.py
    # StepMetadata, # Not defined in views.py
)
# Export prompts
# Only SystemPrompt is defined in prompts.py currently
from .prompts import SystemPrompt #, UserPrompt, AgentMessagePrompt, PlannerPrompt

# NEW: Export Agent and ActionCommand from agent_core.py
from .agent_core import Agent, ActionCommand, InvalidActionError

__all__ = [
    "AgentSettings",
    "AgentThought",
    "AgentOutput",
    # "ActionResult",
    # "AgentHistory",
    # "AgentState",
    # "StepMetadata",
    "SystemPrompt",
    # "UserPrompt", 
    # "AgentMessagePrompt",
    # "PlannerPrompt",
    # Add new exports to __all__
    "Agent",
    "ActionCommand",
    "InvalidActionError",
] 