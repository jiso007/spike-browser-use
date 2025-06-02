"""
Unit tests for LLM initialization in ExtensionInterface.
Tests different API key configurations and model selections.
"""

import pytest
from unittest.mock import patch, Mock
import os

from browser_use_ext.extension_interface.service import ExtensionInterface


class TestLLMInitialization:
    """Test LLM initialization with various configurations."""
    
    @pytest.fixture
    def clean_env(self, monkeypatch):
        """Ensure clean environment without API keys."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    
    def test_initialize_llm_with_openai_gpt4(self, monkeypatch):
        """Test initialization with OpenAI GPT-4."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            mock_llm = Mock()
            mock_openai.return_value = mock_llm
            
            interface = ExtensionInterface(llm_model="gpt-4o")
            
            assert interface._llm == mock_llm
            mock_openai.assert_called_once_with(
                model="gpt-4o",
                temperature=0.0,
                api_key="test-openai-key"
            )
    
    def test_initialize_llm_with_openai_gpt35(self, monkeypatch):
        """Test initialization with OpenAI GPT-3.5."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            interface = ExtensionInterface(
                llm_model="gpt-3.5-turbo",
                llm_temperature=0.5
            )
            
            mock_openai.assert_called_once_with(
                model="gpt-3.5-turbo",
                temperature=0.5,
                api_key="test-openai-key"
            )
    
    def test_initialize_llm_with_anthropic_claude(self, monkeypatch):
        """Test initialization with Anthropic Claude."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatAnthropic') as mock_anthropic:
            mock_llm = Mock()
            mock_anthropic.return_value = mock_llm
            
            interface = ExtensionInterface(llm_model="claude-3-opus-20240229")
            
            assert interface._llm == mock_llm
            mock_anthropic.assert_called_once_with(
                model="claude-3-opus-20240229",
                temperature=0.0,
                api_key="test-anthropic-key"
            )
    
    def test_initialize_llm_with_both_keys_prefers_model_match(self, monkeypatch):
        """Test that when both keys exist, it prefers the one matching the model."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
        
        # Test Claude model uses Anthropic
        with patch('browser_use_ext.extension_interface.service.ChatAnthropic') as mock_anthropic:
            with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
                interface = ExtensionInterface(llm_model="claude-3-sonnet")
                
                mock_anthropic.assert_called_once()
                mock_openai.assert_not_called()
        
        # Test GPT model uses OpenAI
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            with patch('browser_use_ext.extension_interface.service.ChatAnthropic') as mock_anthropic:
                interface = ExtensionInterface(llm_model="gpt-4-turbo")
                
                mock_openai.assert_called_once()
                mock_anthropic.assert_not_called()
    
    def test_initialize_llm_fallback_to_openai(self, monkeypatch):
        """Test fallback to OpenAI when unknown model is specified."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            interface = ExtensionInterface(llm_model="unknown-model-xyz")
            
            # Should fall back to gpt-4o
            mock_openai.assert_called_once_with(
                model="gpt-4o",
                temperature=0.0,
                api_key="test-openai-key"
            )
    
    def test_initialize_llm_no_api_keys(self, clean_env):
        """Test initialization without any API keys."""
        with patch('browser_use_ext.extension_interface.service.logger') as mock_logger:
            interface = ExtensionInterface()
            
            assert interface._llm is None
            mock_logger.warning.assert_called_with(
                "No LLM API keys found in environment. Agent functionality will be limited."
            )
    
    def test_initialize_llm_only_anthropic_key(self, monkeypatch):
        """Test with only Anthropic key but requesting GPT model."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatAnthropic'):
            with patch('browser_use_ext.extension_interface.service.ChatOpenAI'):
                interface = ExtensionInterface(llm_model="gpt-4o")
                
                # Should result in no LLM since no OpenAI key
                assert interface._llm is None
    
    def test_temperature_configuration(self, monkeypatch):
        """Test that temperature is properly configured."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        
        temperatures = [0.0, 0.5, 1.0, 1.5]
        
        for temp in temperatures:
            with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
                interface = ExtensionInterface(llm_temperature=temp)
                
                call_args = mock_openai.call_args
                assert call_args.kwargs['temperature'] == temp
    
    def test_model_name_variations(self, monkeypatch):
        """Test various model name formats."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
        
        # GPT variations
        gpt_models = ["gpt-4", "gpt-4o", "gpt-3.5-turbo", "gpt-4-32k"]
        for model in gpt_models:
            with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
                interface = ExtensionInterface(llm_model=model)
                mock_openai.assert_called_once()
        
        # Claude variations
        claude_models = ["claude-3-opus", "claude-3-sonnet", "claude-2", "claude-instant"]
        for model in claude_models:
            with patch('browser_use_ext.extension_interface.service.ChatAnthropic') as mock_anthropic:
                interface = ExtensionInterface(llm_model=model)
                mock_anthropic.assert_called_once()


class TestLLMIntegrationEdgeCases:
    """Test edge cases in LLM integration."""
    
    def test_initialize_with_empty_api_key(self, monkeypatch):
        """Test with empty string API key."""
        monkeypatch.setenv("OPENAI_API_KEY", "")
        
        interface = ExtensionInterface()
        # Empty string is falsy, so should result in no LLM
        assert interface._llm is None
    
    def test_initialize_with_whitespace_api_key(self, monkeypatch):
        """Test with whitespace API key."""
        monkeypatch.setenv("OPENAI_API_KEY", "   ")
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            interface = ExtensionInterface()
            # Whitespace is truthy, so it will try to create LLM
            mock_openai.assert_called_once()
    
    def test_llm_initialization_exception_handling(self, monkeypatch):
        """Test handling of exceptions during LLM initialization."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI') as mock_openai:
            mock_openai.side_effect = Exception("API key invalid")
            
            # Should not crash, just set LLM to None (exception is caught internally)
            interface = ExtensionInterface()
            assert interface._llm is None
    
    def test_interface_attributes_after_init(self, monkeypatch):
        """Test that all LLM-related attributes are properly set."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        
        with patch('browser_use_ext.extension_interface.service.ChatOpenAI'):
            interface = ExtensionInterface(
                llm_model="gpt-4-turbo",
                llm_temperature=0.7
            )
            
            assert interface._llm_model == "gpt-4-turbo"
            assert interface._llm_temperature == 0.7
            assert hasattr(interface, '_active_agents')
            assert isinstance(interface._active_agents, dict)
            assert len(interface._active_agents) == 0