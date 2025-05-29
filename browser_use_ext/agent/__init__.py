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
# from .agent_core import Agent, ActionCommand, InvalidActionError

# Core agent components
from .prompts import (
    DEFAULT_SYSTEM_PROMPT,
    DEFAULT_PLANNER_PROMPT,
    SystemPrompt,
    PromptVariable,
    generate_actions_text_description,
    get_agent_llm_output_json_schema,
)
from .actions import *
from .views import (
    AgentSettings,
    AgentState,
    AgentHistoryList,
    AgentHistory,
    AgentLLMOutput,
    ActionCommand, # ActionCommand is here
    InvalidActionError, # InvalidActionError is here
    ActionResult,
    StepMetadata,
    AgentError,
    AgentBrain,
    AgentOutput,
    AgentThought
)
from .message_manager import MessageManager
from .service import Agent # Import Agent from .service

__all__ = [
    # Prompts
    "DEFAULT_SYSTEM_PROMPT",
    "DEFAULT_PLANNER_PROMPT",
    "SystemPrompt",
    "PromptVariable",
    "generate_actions_text_description",
    "get_agent_llm_output_json_schema",
    # Actions (assuming you want to export all from .actions using *)
    # If not, list them explicitly similar to how views are handled.
    # For now, let's assume * export is fine for .actions if it contains only Pydantic models.

    # Views
    "AgentSettings",
    "AgentState",
    "AgentHistoryList",
    "AgentHistory",
    "AgentLLMOutput",
    "ActionCommand",
    "InvalidActionError",
    "ActionResult",
    "StepMetadata",
    "AgentError",
    "AgentBrain",
    "AgentOutput",
    "AgentThought",

    # Message Manager
    "MessageManager",

    # Agent Service
    "Agent",
] 