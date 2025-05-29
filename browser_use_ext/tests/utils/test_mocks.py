from typing import List, Any, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from browser_use_ext.agent.views import AgentLLMOutput, AgentBrain, ActionCommand
import logging

logger = logging.getLogger(__name__)

class MockLLM(BaseChatModel):
    """A mock LLM that returns predefined responses."""
    responses: List[str]
    current_response_index: int = 0
    call_count: int = 0

    def _generate(
        self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any
    ) -> ChatResult:
        self.call_count += 1
        logger.info(f"MockLLM (_generate call #{self.call_count}): Current index: {self.current_response_index}, Total responses: {len(self.responses)}")
        if self.current_response_index >= len(self.responses):
            logger.error(f"MockLLM (_generate): Ran out of responses. Requested index: {self.current_response_index}.")
            raise ValueError("MockLLM ran out of responses in _generate.")
        
        response_content = self.responses[self.current_response_index]
        logger.info(f"MockLLM (_generate call #{self.call_count}): Providing response index {self.current_response_index}: {response_content[:100]}...")
        self.current_response_index += 1
        
        generation = ChatGeneration(message=AIMessage(content=response_content))
        return ChatResult(generations=[generation])

    async def _agenerate(
        self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any
    ) -> ChatResult:
        self.call_count += 1
        logger.info(f"MockLLM (_agenerate call #{self.call_count}): Current index: {self.current_response_index}, Total responses: {len(self.responses)}")
        if self.current_response_index >= len(self.responses):
            logger.error(f"MockLLM (_agenerate call #{self.call_count}): Ran out of responses. Requested index: {self.current_response_index}. Returning fallback 'done' action.")
            fallback_brain = AgentBrain(evaluation_previous_goal="Fallback due to no more LLM responses", memory="N/A", next_goal="Finish task")
            fallback_action = ActionCommand(
                action="done", 
                params={"success": False, "message": "Fallback: No more mock LLM responses"}
            )
            fallback_output = AgentLLMOutput(current_state=fallback_brain, action=[fallback_action])
            response_content = fallback_output.model_dump_json()
        else:
            response_content = self.responses[self.current_response_index]
            logger.info(f"MockLLM (_agenerate call #{self.call_count}): Providing response index {self.current_response_index}: {response_content[:100]}...")
            self.current_response_index += 1
        
        generation = ChatGeneration(message=AIMessage(content=response_content))
        return ChatResult(generations=[generation])
    
    @property
    def _llm_type(self) -> str:
        return "mock_llm" 