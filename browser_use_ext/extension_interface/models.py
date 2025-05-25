import asyncio
from typing import Optional, Dict, Any, List, TypeVar, Generic
from pydantic import BaseModel, Field

# For WebSocketServerProtocol type hint if needed, consult websockets library version
# For now, using 'Any' for simplicity if direct import is problematic or version specific.
# from websockets.server import WebSocketServerProtocol # Example, might be different path/type

T = TypeVar('T') # Generic TypeVar for Message data

class BaseMessage(BaseModel):
    """Base model for all WebSocket messages, providing common fields like id and type."""
    id: int = Field(description="Unique message identifier.")
    type: str = Field(description="Type of the WebSocket message.")

class Message(BaseMessage, Generic[T]):
    """
    Generic message model for communication.
    The 'data' field can hold different structures based on the message 'type'.
    """
    data: Optional[T] = Field(default=None, description="Payload of the message, type varies.")


# This specific RequestMessage isn't directly used by service.py's _process_message,
# which uses a generic Message[Dict[str, Any]].model_validate(raw_message).
# However, it's good for documentation and potential future typed request handling.
class RequestData_GetState(BaseModel):
    includeScreenshot: bool

class RequestData_ExecuteAction(BaseModel):
    action: str
    params: Dict[str, Any]

# If we wanted typed request messages:
# class GetStateRequestMessage(BaseMessage):
#     data: RequestData_GetState
#
# class ExecuteActionRequestMessage(BaseMessage):
#     data: RequestData_ExecuteAction


class RequestData(BaseModel):
    """General model for the 'data' field of various request messages sent to the extension."""
    # Common fields for different actions, all optional at this level.
    # Specific actions will expect certain fields to be present.

    # For "get_state"
    include_screenshot: Optional[bool] = None
    tab_id: Optional[int] = None

    # For actions like "click_element_by_index", "input_text", "scroll_page", "extract_content", "send_keys"
    highlight_index: Optional[int] = None
    
    # For "go_to_url", "open_tab"
    url: Optional[str] = None

    # For "input_text"
    text: Optional[str] = None

    # For "scroll_page"
    direction: Optional[str] = None # "up" or "down"

    # For "extract_content"
    content_type: Optional[str] = None # "text" or "html"

    # For "send_keys"
    keys: Optional[str] = None

    # For general execute_action if a more specific payload isn't used by RequestData directly
    # This allows execute_action(action_name="some_custom_action", params={"custom_param": val})
    # where params becomes the RequestData payload. 
    # Pydantic's `extra = "allow"` can handle this if we add it, or tests might need to adapt.
    # For now, let's keep it to explicitly defined fields that tests are using or imply.
    # The test `test_request_data_execute_action_scenario` has params={"highlight_index": 5, "text": "hello world"}
    # which are covered by highlight_index and text fields above.

    # The field `action_name` is NOT part of this model because in the Message structure,
    # `action_name` usually corresponds to Message.type (e.g., type="get_state", type="input_text").
    # The test `test_request_data_get_state_scenario` and `test_request_data_execute_action_scenario` in `test_models.py`
    # instantiate RequestData with an `action_name` field. This needs to be reconciled.
    # The tests seem to be using RequestData to represent the `params` argument of `controller.execute_action`
    # or the structured data for specific calls like `get_state`.

    # Let's adjust based on test_models.py's usage: it seems to expect `action_name` to be part of this model.
    # This means RequestData might be used to model the `params` dict sent to the extension OR a more general request structure.
    # Given test_models.py: 
    #   RequestData(action_name="get_state", include_screenshot=True, tab_id=123)
    #   RequestData(action_name="input_text", params={"highlight_index": 5, "text": "hello world"})
    # This implies `params` would be a nested dict if `action_name` is present.
    # This is getting confusing. Let's simplify: `RequestData` should model the `data` part of the Message.
    # The `action_name` is the `Message.type`. The tests need to reflect this. 

    # Re-evaluating: The test_models.py uses `RequestData(action_name=...)`. This is problematic if `RequestData` is just the `data` payload.
    # However, test_extension_interface.py does: 
    #   `expected_request_data = RequestData(include_screenshot=True, tab_id=1)` (for get_state)
    #   This `expected_request_data` is then model_dumped and becomes the `data` for `_send_request`.
    # This implies `RequestData` IS meant to be the `data` payload for `type="get_state"`.
    # For `execute_action(action_name, params)`, `params` itself becomes the `data` payload, and `action_name` is the `type`.

    # Let's define RequestData to cover the explicit fields used in tests for `get_state` data payload.
    # The `params: Dict[str, Any]` used in `execute_action` can remain a dictionary for flexibility, as the extension handles it.

    # This definition is for the data payload of a "get_state" request.
    # Fields that appear in `test_extension_interface.py`'s instantiation of `RequestData`:
    # include_screenshot: bool
    # tab_id: Optional[int]
    # Fields that appear in `test_models.py`'s instantiation of `RequestData` with action_name="get_state":
    # include_screenshot: True
    # tab_id: 123
    # (action_name is problematic here, should not be part of this model if this model represents Message.data)

    # Let's define RequestData to be specific for get_state's data payload first.
    # This is what `test_extension_interface.py` implies. We will then adjust `test_models.py`.
    include_screenshot: Optional[bool] = Field(default=False, description="Whether to include a screenshot in the state.")
    tab_id: Optional[int] = Field(default=None, description="Specific tab ID to get state from. None for active tab.")


class ResponseData(BaseModel):
    """Model for the 'data' field within a response message from the extension,
       or the structure of the data field in a 'response' type message from the server."""
    success: bool = Field(description="Indicates if the operation was successful.")
    error: Optional[str] = Field(default=None, description="Error message if an error occurred.")
    
    # Fields typically from get_state merged into BrowserStateModelData
    # These are what BrowserState.model_validate expects in the 'data' part of ResponseData
    url: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    html_content: Optional[str] = Field(default=None)
    tree: Optional[Dict[str, Any]] = Field(default=None) # Matches BrowserState.tree
    tabs: Optional[List[Dict[str, Any]]] = Field(default=None) # Matches BrowserState.tabs (list of TabInfo-like dicts)
    active_tab_id: Optional[int] = Field(default=None) # Matches BrowserState.active_tab_id
    viewport_size: Optional[Dict[str, int]] = Field(default=None) # Matches BrowserState.viewport_size
    scroll_position: Optional[Dict[str, int]] = Field(default=None) # Matches BrowserState.scroll_position
    pixels_below: Optional[int] = Field(default=None) # Matches BrowserState.pixels_below
    screenshot: Optional[str] = Field(default=None) # Matches BrowserState.screenshot
    
    # Other potential fields from various actions or events
    # content: Optional[str] = Field(default=None, description="Extracted content from the page.")
    # note: Optional[str] = Field(default=None, description="Additional note for the action's result.")
    # new_active_tab_id: Optional[int] = Field(default=None, description="ID of the new active tab.")
    # new_tab_id: Optional[int] = Field(default=None, description="ID of the newly created tab.")
    # closed_tab_id: Optional[int] = Field(default=None, description="ID of the closed tab.")

    class Config:
        extra = "allow" # Allow extra fields not strictly defined, useful for evolving APIs


class ConnectionInfo(BaseModel):
    """Stores information about an active WebSocket client connection."""
    client_id: str
    websocket: Any # Using Any for websockets.server.ServerConnection to avoid import version issues
    handler_task: Optional[asyncio.Task] = None

    class Config:
        arbitrary_types_allowed = True 