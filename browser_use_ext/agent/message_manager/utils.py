from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Optional, Type, List # Added List for type hints

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

logger = logging.getLogger(__name__)

MODELS_WITHOUT_TOOL_SUPPORT_PATTERNS = [
    'deepseek-reasoner',
    'deepseek-r1',
    '.*gemma.*-it',
]


def is_model_without_tool_support(model_name: str) -> bool:
    return any(re.match(pattern, model_name) for pattern in MODELS_WITHOUT_TOOL_SUPPORT_PATTERNS)


def extract_json_from_model_output(content: str) -> dict:
    """Extract JSON from model output, handling both plain JSON and code-block-wrapped JSON."""
    try:
        # If content is wrapped in code blocks, extract just the JSON part
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
        if match:
            json_str = match.group(1).strip()
        else:
            # If no triple backticks, assume the content might be a direct JSON string
            # or a JSON string with potential leading/trailing non-JSON text (e.g. explanations before/after JSON block)
            # Try to find the first '{' and last '}' to extract potential JSON object
            first_brace = content.find('{')
            last_brace = content.rfind('}')
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                json_str = content[first_brace : last_brace + 1]
            else: # Fallback to assuming the whole content is JSON (might fail if not)
                json_str = content.strip()
        
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.warning(f'Failed to parse JSON from model output: {content}. Error: {str(e)}')
        # Consider returning None or a more specific error structure if needed by caller
        raise ValueError(f'Could not parse JSON from response: {str(e)}') from e


def convert_input_messages(input_messages: List[BaseMessage], model_name: Optional[str]) -> List[BaseMessage]:
    """Convert input messages to a format that is compatible with models that don't fully support tool/function calling conventions."""
    if model_name is None or not is_model_without_tool_support(model_name):
        return input_messages

    converted_input_messages = _convert_messages_for_non_function_calling_models(input_messages)
    # Merging successive messages might be overly aggressive or model-specific.
    # Keep if specific models require it, otherwise, it might be safer to let models handle sequences.
    # merged_input_messages = _merge_successive_messages(converted_input_messages, HumanMessage)
    # merged_input_messages = _merge_successive_messages(merged_input_messages, AIMessage)
    # return merged_input_messages
    return converted_input_messages # Return without merging for now, can be re-enabled if needed


def _convert_messages_for_non_function_calling_models(input_messages: List[BaseMessage]) -> List[BaseMessage]:
    """Convert messages for non-function-calling models. Flattens tool calls and results into content."""
    output_messages = []
    for message in input_messages:
        if isinstance(message, (HumanMessage, SystemMessage)):
            output_messages.append(message)
        elif isinstance(message, ToolMessage):
            # Represent tool result as human message saying what the tool returned.
            output_messages.append(HumanMessage(content=f"Tool execution result for {getattr(message, 'name', 'unknown_tool')}:\n{message.content}"))
        elif isinstance(message, AIMessage):
            # If AI message has tool_calls, convert them to a string representation in content.
            if message.tool_calls:
                tool_calls_str = json.dumps(message.tool_calls) # Serialize tool_calls to string
                new_content = f"I need to use tools. Tool calls: {tool_calls_str}"
                if message.content: # Append to existing content if any
                    new_content = f"{message.content}\n{new_content}"
                output_messages.append(AIMessage(content=new_content))
            else:
                output_messages.append(message) # No tool_calls, keep as is
        else:
            logger.warning(f'Unknown message type encountered during conversion: {type(message)}')
            # Optionally, append a string representation or skip
            output_messages.append(HumanMessage(content=f"[Unsupported message type: {type(message).__name__}] {str(message.content)[:100]}"))
    return output_messages


def _merge_successive_messages(messages: List[BaseMessage], class_to_merge: Type[BaseMessage]) -> List[BaseMessage]:
    """Some models (e.g., older versions or specific APIs) don't allow multiple messages of the same role in a row. This function merges them."""
    if not messages:
        return []

    merged_messages: List[BaseMessage] = []
    current_message_content_parts: List[str] = []

    for i, message in enumerate(messages):
        is_last_message = (i == len(messages) - 1)
        is_mergeable_type = isinstance(message, class_to_merge)

        if is_mergeable_type:
            if isinstance(message.content, str):
                current_message_content_parts.append(message.content)
            elif isinstance(message.content, list): # For HumanMessage with image and text
                for part in message.content:
                    if isinstance(part, dict) and part.get('type') == 'text':
                        current_message_content_parts.append(part['text'])
                    # Note: This simplistic merge won't handle merging image parts from multiple messages.
                    # If merging HumanMessages with images, this part needs more sophisticated handling.
                    # For now, assume we merge text content primarily.
        
        # If the next message is different, or this is the last message, finalize the current merged message.
        if not is_last_message and not isinstance(messages[i+1], class_to_merge) and current_message_content_parts:
            merged_content = "\n\n".join(current_message_content_parts)
            # Create a new message of the original type with the merged content
            # This requires knowing how to reconstruct the message (e.g. AIMessage(content=...))
            # For simplicity, this example assumes class_to_merge has a constructor like Class(content=str)
            # This might need adjustment based on actual BaseMessage subclasses
            if merged_messages and isinstance(merged_messages[-1], class_to_merge) and class_to_merge != SystemMessage:
                 # if last message in merged_messages is of same type, append to its content
                 if isinstance(merged_messages[-1].content, str):
                    merged_messages[-1].content += "\n\n" + merged_content
                 # Cannot easily merge if content is not a simple string (e.g. list with images)
            elif current_message_content_parts: # only add if there's content
                merged_messages.append(class_to_merge(content=merged_content))
            current_message_content_parts = [] # Reset for the next streak
        
        if not is_mergeable_type:
            # Before adding a non-mergeable message, ensure any pending mergeable content is flushed.
            if current_message_content_parts:
                merged_content = "\n\n".join(current_message_content_parts)
                if merged_messages and isinstance(merged_messages[-1], class_to_merge) and class_to_merge != SystemMessage:
                    if isinstance(merged_messages[-1].content, str):
                        merged_messages[-1].content += "\n\n" + merged_content
                elif current_message_content_parts:
                    merged_messages.append(class_to_merge(content=merged_content))
                current_message_content_parts = []
            merged_messages.append(message) # Add the non-mergeable message itself

    # After the loop, if there's any remaining content in current_message_content_parts, add it.
    if current_message_content_parts:
        merged_content = "\n\n".join(current_message_content_parts)
        if merged_messages and isinstance(merged_messages[-1], class_to_merge) and class_to_merge != SystemMessage:
            if isinstance(merged_messages[-1].content, str):
                merged_messages[-1].content += "\n\n" + merged_content
        else: # Handles case where ALL messages were of class_to_merge
            merged_messages.append(class_to_merge(content=merged_content))
            
    return merged_messages


def save_conversation(input_messages: List[BaseMessage], response_model_obj: Any, target: str, encoding: Optional[str] = None) -> None:
    """Save conversation history to file. Takes a Pydantic model for response."""
    if dirname := os.path.dirname(target):
        os.makedirs(dirname, exist_ok=True)

    with open(target, 'w', encoding=encoding if encoding else 'utf-8') as f:
        _write_messages_to_file(f, input_messages)
        if hasattr(response_model_obj, 'model_dump_json'):
            f.write('\nRESPONSE (AgentLLMOutput Model Dump):\n')
            f.write(response_model_obj.model_dump_json(indent=2, exclude_unset=True))
        elif isinstance(response_model_obj, str): # If it's a raw string (e.g. error)
            f.write('\nRESPONSE (Raw String):\n')
            f.write(response_model_obj)
        else: # Fallback for other types
            f.write('\nRESPONSE (Fallback - str representation):\n')
            f.write(str(response_model_obj))

def _write_messages_to_file(f: Any, messages: List[BaseMessage]) -> None:
    """Write messages to conversation file"""
    for message in messages:
        f.write(f'\n--- {message.__class__.__name__} ---\n')
        if isinstance(message.content, list): # For HumanMessage with vision
            for item in message.content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        f.write(item['text'].strip() + '\n')
                    elif item.get('type') == 'image_url':
                        f.write(f"[Image URL: {item['image_url'].get('url', 'N/A')[:100]}...]\n")
        elif isinstance(message.content, str):
            try:
                # Attempt to pretty-print if it's a JSON string in content (e.g. AIMessage from older version)
                content_json = json.loads(message.content)
                f.write(json.dumps(content_json, indent=2) + '\n')
            except json.JSONDecodeError:
                f.write(message.content.strip() + '\n')
        
        if message.tool_calls: # Langchain AIMessage specific
            f.write("Tool Calls:\n")
            f.write(json.dumps(message.tool_calls, indent=2) + '\n')
        if hasattr(message, 'tool_call_id') and message.tool_call_id: # Langchain ToolMessage specific
             f.write(f"Tool Call ID: {message.tool_call_id}\n")

# _write_response_to_file is effectively merged into save_conversation's handling of response_model_obj 