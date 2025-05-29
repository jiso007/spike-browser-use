import pytest
from unittest.mock import MagicMock, AsyncMock # Unused, can be removed if not needed for other tests here
from langchain_core.messages import AIMessage # type: ignore
from langchain_core.outputs import ChatResult, ChatGeneration # type: ignore

# Assuming MockLLM is now part of test_agent_e2e.py and can be imported from there
# If it's better placed in a shared testing utility, adjust the import accordingly.
from browser_use_ext.tests.utils.test_mocks import MockLLM
from browser_use_ext.agent.views import AgentLLMOutput, AgentBrain, ActionCommand # For fallback validation

class TestMockLLM:
    """Unit tests for the MockLLM class used in e2e testing."""
    
    @pytest.mark.asyncio
    async def test_mock_llm_returns_responses_in_order(self):
        """Test that MockLLM returns responses in the correct order and increments call count."""
        responses = ["response1_content", "response2_content", "response3_content"]
        mock_llm = MockLLM(responses=responses)
        
        assert mock_llm.call_count == 0, "Initial call count should be 0."

        # Test first response
        result1 = await mock_llm._agenerate(messages=[AIMessage(content="dummy_message_1")]) # Pass dummy messages
        assert isinstance(result1, ChatResult), "Result should be a ChatResult instance."
        assert len(result1.generations) == 1, "Should have one generation."
        assert result1.generations[0].message.content == "response1_content", "Incorrect first response content."
        assert mock_llm.call_count == 1, "Call count should be 1 after first call."
        assert mock_llm.current_response_index == 1, "Response index should be 1."
        
        # Test second response  
        result2 = await mock_llm._agenerate(messages=[AIMessage(content="dummy_message_2")])
        assert result2.generations[0].message.content == "response2_content", "Incorrect second response content."
        assert mock_llm.call_count == 2, "Call count should be 2 after second call."
        assert mock_llm.current_response_index == 2, "Response index should be 2."
        
        # Test third response
        result3 = await mock_llm._agenerate(messages=[AIMessage(content="dummy_message_3")])
        assert result3.generations[0].message.content == "response3_content", "Incorrect third response content."
        assert mock_llm.call_count == 3, "Call count should be 3 after third call."
        assert mock_llm.current_response_index == 3, "Response index should be 3."
    
    @pytest.mark.asyncio
    async def test_mock_llm_fallback_when_out_of_responses(self):
        """Test that MockLLM provides a valid fallback 'done' action when responses are exhausted."""
        responses = ["single_response_content"]
        mock_llm = MockLLM(responses=responses)
        
        # Use the one available response
        await mock_llm._agenerate(messages=[AIMessage(content="dummy_message_A")])
        assert mock_llm.call_count == 1, "Call count should be 1 after using the only response."
        assert mock_llm.current_response_index == 1, "Response index should be 1."
        
        # Request beyond available responses should trigger fallback
        fallback_result = await mock_llm._agenerate(messages=[AIMessage(content="dummy_message_B")])
        assert mock_llm.call_count == 2, "Call count should be 2 after fallback."
        assert mock_llm.current_response_index == 1, "Response index should remain at 1 (len of responses) after fallback."
        
        # Verify fallback content structure and parsability
        assert isinstance(fallback_result, ChatResult), "Fallback result should be a ChatResult."
        assert len(fallback_result.generations) == 1, "Fallback should have one generation."
        fallback_content_str = fallback_result.generations[0].message.content
        
        # Validate that the fallback content is a JSON representation of AgentLLMOutput
        # and that it represents a "done" action with success=False.
        try:
            parsed_output = AgentLLMOutput.model_validate_json(fallback_content_str)
            assert len(parsed_output.action) == 1, "Fallback should contain one action."
            action_command = parsed_output.action[0]
            assert action_command.action == "done", "Fallback action should be 'done'."
            assert action_command.params["success"] is False, "Fallback 'done' action should indicate failure."
            assert "Fallback: No more mock LLM responses" in action_command.params["message"], \
                "Fallback message not found in params."
        except Exception as e:
            pytest.fail(f"Fallback content could not be parsed as AgentLLMOutput or content is incorrect: {e}\nContent: {fallback_content_str}")
    
    def test_mock_llm_llm_type_property(self):
        """Test that MockLLM correctly returns its _llm_type property."""
        mock_llm = MockLLM(responses=["test_response"])
        assert mock_llm._llm_type == "mock_llm", "_llm_type property returned incorrect value."
    
    @pytest.mark.asyncio
    async def test_mock_llm_call_count_tracking_accuracy(self):
        """Test that MockLLM accurately tracks call count, including during fallback."""
        mock_llm = MockLLM(responses=["r1_content", "r2_content"])
        
        assert mock_llm.call_count == 0, "Initial call count should be 0."
        
        await mock_llm._agenerate(messages=[AIMessage(content="dummy_1")])
        assert mock_llm.call_count == 1, "Call count should be 1 after first call."
        
        await mock_llm._agenerate(messages=[AIMessage(content="dummy_2")])
        assert mock_llm.call_count == 2, "Call count should be 2 after second call."
        
        # Fallback call should also increment the count
        await mock_llm._agenerate(messages=[AIMessage(content="dummy_3")])
        assert mock_llm.call_count == 3, "Call count should be 3 after a fallback call."

    @pytest.mark.asyncio
    async def test_mock_llm_initialization_state(self):
        """Test the initial state of MockLLM upon instantiation."""
        responses_list = ["r1", "r2", "r3"]
        mock_llm = MockLLM(responses=responses_list)
        
        assert mock_llm.responses == responses_list, "Responses list not stored correctly."
        assert mock_llm.current_response_index == 0, "Initial current_response_index should be 0."
        assert mock_llm.call_count == 0, "Initial call_count should be 0." 