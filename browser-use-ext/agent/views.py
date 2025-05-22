# Standard library imports
from typing import Optional, Dict, Any, List, Union
import logging

# Third-party imports
from pydantic import BaseModel, Field
from typing import Literal

# Local application/library specific imports
from browser_use.browser.views import BrowserState # For Agent to potentially receive or log
from .message_manager.service import Message

logger = logging.getLogger(__name__)

class AgentSettings(BaseModel):
    """
    Configuration settings for the Agent.
    This could include model preferences, persona definitions, tool configurations, etc.
    """
    name: str = Field(default="BrowserAgent", description="Name of the agent.")
    max_iterations: int = Field(default=10, description="Maximum number of iterations or steps the agent can take.")
    # Example: LLM model name to use for decision making
    language_model_name: Optional[str] = Field(default="gpt-4-turbo-preview", description="The language model to use.")
    # Example: Temperature for LLM generation, influencing creativity/randomness.
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="LLM generation temperature.")
    verbose: bool = Field(default=True, description="Enable verbose logging for agent activities.")
    allow_parallel_execution: bool = Field(default=False, description="Allow agent to execute multiple actions in parallel (not typically supported by simple controllers).")
    # Add other agent-specific settings here.
    # system_prompt: Optional[str] = Field(None, description="Default system prompt for the agent.")

    class Config:
        from_attributes = True

class AgentThought(BaseModel):
    """
    Represents a single thought or reasoning step of the agent.
    Useful for logging, debugging, and understanding the agent's decision process.
    """
    thought_process: str = Field(description="Textual description of the agent's reasoning.")
    tool_to_use: Optional[str] = Field(default=None, description="The name of the tool or action the agent decided to use.")
    tool_input: Optional[Dict[str, Any]] = Field(default_factory=dict, description="The parameters for the tool/action.")
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Agent's confidence in its decision (0.0 to 1.0).")
    raw_llm_response: Optional[str] = Field(default=None, description="Raw response from the LLM if applicable.")

    class Config:
        from_attributes = True

class AgentOutput(BaseModel):
    """
    Represents the final output or result of an agent's run or a significant step.
    """
    status: Literal["success", "failure", "max_iterations_reached"] = Field(description="Final status of the agent's execution.")
    output_message: str = Field(description="A summary message describing the outcome.")
    final_answer: Optional[Any] = Field(default=None, description="The final answer or result produced by the agent, if any.")
    iterations_taken: int = Field(description="Number of iterations the agent performed.")
    full_history: Optional[List[Message]] = Field(default_factory=list, description="Full conversation history if available.")
    thoughts_history: Optional[List[AgentThought]] = Field(default_factory=list, description="History of agent's thoughts and actions.")
    # Example: The browser state at the end of the agent's operation.
    final_browser_state: Optional[BrowserState] = Field(None, description="Browser state at the end of operation.")
    # Example: Any errors encountered during the agent's run.
    error: Optional[str] = Field(None, description="Error message if the agent run failed.")

    class Config:
        from_attributes = True
        json_encoders = {
            # Ensure Message objects within full_history are serialized correctly if they have datetimes
            Message: lambda v: v.model_dump(exclude_none=True) 
        }

# More Pydantic models can be added here as the agent's capabilities grow,
# for example, for specific task inputs, structured observations, etc. 

# Example:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    settings = AgentSettings(name="DemoAgent", max_iterations=5, verbose=True)
    logger.info(f"Agent Settings: {settings.model_dump_json(indent=2)}")

    thought = AgentThought(
        thought_process="The user wants to know the weather. I should use the get_weather tool.",
        tool_to_use="get_weather",
        tool_input={"city": "London"},
        confidence_score=0.9
    )
    logger.info(f"Agent Thought: {thought.model_dump_json(indent=2)}")

    output_success = AgentOutput(
        status="success",
        output_message="Successfully retrieved weather for London.",
        final_answer={"temperature": "15C", "condition": "Cloudy"},
        iterations_taken=3,
        thoughts_history=[thought]
    )
    logger.info(f"Agent Output (Success): {output_success.model_dump_json(indent=2)}")

    output_failure = AgentOutput(
        status="failure",
        output_message="Could not retrieve weather information after multiple attempts.",
        iterations_taken=5
    )
    logger.info(f"Agent Output (Failure): {output_failure.model_dump_json(indent=2)}") 