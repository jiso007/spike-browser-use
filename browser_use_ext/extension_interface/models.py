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