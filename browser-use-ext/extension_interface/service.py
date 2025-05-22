from __future__ import annotations

# Standard library imports
import asyncio
import json
import logging
import uuid
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

# Third-party imports
import websockets
from pydantic import BaseModel, Field, ValidationError
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from websockets.server import WebSocketServerProtocol

# Local application/library specific imports
from browser.views import BrowserState, TabInfo
from dom.views import DOMElementNode

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Generic TypeVar for async callback return types
T = TypeVar('T')

# --- Pydantic Models for WebSocket Communication ---

class BaseMessage(BaseModel):
    """Base model for all WebSocket messages, providing common fields like id and type."""
    # Unique identifier for the message, used to correlate requests and responses.
    id: int = Field(description="Unique message identifier.")
    # Type of the message, e.g., 'get_state', 'execute_action', 'response'.
    type: str = Field(description="Type of the WebSocket message.")

class RequestMessage(BaseMessage):
    """Model for request messages sent from Python to the Chrome extension."""
    # Action-specific data or parameters for the request.
    # For 'get_state': {"includeScreenshot": bool}
    # For 'execute_action': {"action": str, "params": Dict[str, Any]}
    data: Optional[Dict[str, Any]] = Field(None, description="Payload for the request.")

class ResponseData(BaseModel):
    """Model for the 'data' field within a response message from the extension."""
    # Indicates success or failure of the operation requested.
    success: Optional[bool] = Field(None, description="Indicates if the operation was successful.")
    # Error message if the operation failed.
    error: Optional[str] = Field(None, description="Error message if an error occurred.")
    # URL of the page, typically included in get_state responses.
    url: Optional[str] = Field(None, description="Current URL of the page.")
    # Title of the page, typically included in get_state responses.
    title: Optional[str] = Field(None, description="Title of the page.")
    # DOM structure, typically included in get_state responses.
    element_tree: Optional[Dict[str, Any]] = Field(None, description="Raw element tree from extension.")
    # Selector map, typically included in get_state responses.
    selector_map: Optional[Dict[str, Any]] = Field(None, description="Raw selector map from extension.")
    # List of tabs, typically included in get_state responses.
    tabs: Optional[List[Dict[str, Any]]] = Field(None, description="List of tabs from extension.")
    # Screenshot data (base64), if requested.
    screenshot: Optional[str] = Field(None, description="Base64 encoded screenshot data.")
    # Scroll position information.
    pixels_above: Optional[int] = Field(None, description="Pixels scrolled above the viewport.")
    pixels_below: Optional[int] = Field(None, description="Pixels scrollable below the viewport.")
    # Content extracted from the page, for 'extract_content' action.
    content: Optional[str] = Field(None, description="Extracted content from the page.")
    # Note for providing additional context for an action's result.
    note: Optional[str] = Field(None, description="Additional note for the action's result.")
    # ID of the newly activated tab after a switch_tab action.
    new_active_tab_id: Optional[int] = Field(None, description="ID of the new active tab.")
    # ID of a newly created tab.
    new_tab_id: Optional[int] = Field(None, description="ID of the newly created tab.")
    # ID of a closed tab.
    closed_tab_id: Optional[int] = Field(None, description="ID of the closed tab.")

    class Config:
        # Allows for extra fields in the response data that are not strictly defined
        # This is useful for flexibility as the extension might send additional info.
        extra = "allow"

class ResponseMessage(BaseMessage):
    """Model for response messages received from the Chrome extension."""
    # The actual payload of the response, structured according to ResponseData.
    data: ResponseData = Field(description="Payload of the response.")

# --- Connection Management ---

class ConnectionInfo(BaseModel):
    """Stores information about an active WebSocket client connection."""
    # Unique identifier assigned to the client by the server.
    client_id: str
    # The WebSocket connection object for this client.
    websocket: WebSocketServerProtocol
    # Task that handles message listening for this client.
    # Storing it allows for cancellation if needed.
    handler_task: Optional[asyncio.Task] = None

    class Config:
        # Allows Pydantic to handle non-standard types like WebSocketServerProtocol and asyncio.Task.
        arbitrary_types_allowed = True

# --- Main Extension Interface Class ---

class ExtensionInterface:
    """
    Manages WebSocket communication with the Chrome extension.
    It handles starting/stopping the server, sending requests to the extension,
    and processing responses.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        """
        Initializes the ExtensionInterface.

        Args:
            host: The hostname for the WebSocket server.
            port: The port number for the WebSocket server.
        """
        self.host = host
        self.port = port
        self._server: Optional[websockets.server.WebSocketServer] = None
        self._connections: Dict[str, ConnectionInfo] = {}
        self._active_connection_id: Optional[str] = None
        self._message_id_counter: int = 0
        self._pending_requests: Dict[int, asyncio.Future[ResponseData]] = {}
        self._server_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock() # Lock for managing shared resources like _message_id_counter
    
    async def start_server(self) -> None:
        """Starts the WebSocket server to listen for connections from the extension."""
        if self._server is not None:
            logger.warning("WebSocket server is already running.")
            return
        
        try:
            # `websockets.serve` creates and starts the server.
            # `self._handle_connection` will be called for each new client.
            self._server = await websockets.serve(
                self._handle_connection, 
                self.host, 
                self.port
            )
            logger.info(f"WebSocket server started successfully on ws://{self.host}:{self.port}")
            # Create a task to monitor the server's status. `wait_closed` will complete when the server stops.
            self._server_task = asyncio.create_task(self._server.wait_closed(), name=f"WebSocketServerMonitor-{self.port}")
        except Exception as e:
            logger.error(f"Failed to start WebSocket server on ws://{self.host}:{self.port}: {e}", exc_info=True)
            self._server = None # Ensure server is None if start failed
            raise # Re-raise the exception to signal failure to the caller
    
    async def stop_server(self) -> None:
        """Stops the WebSocket server and cleans up connections."""
        if self._server is None:
            logger.warning("WebSocket server is not running.")
            return
        
        logger.info("Attempting to stop WebSocket server...")
        self._server.close() # Initiates the server shutdown
        
        # Wait for the server to close fully and for its monitoring task to complete.
        if self._server_task:
            try:
                await asyncio.wait_for(self._server_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Timeout waiting for server task to complete during shutdown.")
            except Exception as e:
                logger.error(f"Error during server task completion: {e}", exc_info=True)

        # Cancel any pending client handler tasks
        for conn_id, conn_info in list(self._connections.items()): # Iterate over a copy
            if conn_info.handler_task and not conn_info.handler_task.done():
                conn_info.handler_task.cancel()
                try:
                    await conn_info.handler_task # Wait for cancellation to complete
                except asyncio.CancelledError:
                    logger.debug(f"Handler task for {conn_id} cancelled successfully.")
                except Exception as e:
                    logger.error(f"Error cancelling handler task for {conn_id}: {e}", exc_info=True)
            # Close the individual websocket connection if it's still open
            if not conn_info.websocket.closed:
                await conn_info.websocket.close(code=1001, reason="Server shutting down")

        # Clear pending requests
        for req_id, future in self._pending_requests.items():
            if not future.done():
                future.cancel(f"Request {req_id} cancelled due to server shutdown.")
        self._pending_requests.clear()
        
        # Reset server state
        self._server = None
        self._server_task = None
        self._connections.clear()
        self._active_connection_id = None
        logger.info("WebSocket server stopped successfully.")
    
    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """
        Manages a new WebSocket connection from a client (the Chrome extension).
        Each connection runs in its own instance of this coroutine.
        """
        client_id = f"client_{websocket.id}" # Use a unique ID from the websocket object
        handler_task = asyncio.current_task()
        if handler_task:
             handler_task.set_name(f"WSClientHandler-{client_id}")

        conn_info = ConnectionInfo(client_id=client_id, websocket=websocket, handler_task=handler_task)
        self._connections[client_id] = conn_info
        logger.info(f"New WebSocket connection established from {websocket.remote_address}: {client_id}") 

        # If no active connection, set this new one as active.
        if self._active_connection_id is None:
            self._active_connection_id = client_id
            logger.info(f"Set {client_id} as the active connection.")

        try:
            # Loop indefinitely to process messages from this client.
            async for message_data in websocket:
                if isinstance(message_data, str):
                    await self._process_message(client_id, message_data)
                else:
                    logger.warning(f"Received non-text message from {client_id}, ignoring.")
        except ConnectionClosedOK:
            logger.info(f"Connection {client_id} closed gracefully (OK). Path: {path}")
        except ConnectionClosed as e:
            logger.warning(f"Connection {client_id} closed with code {e.code}, reason: {e.reason}. Path: {path}")
        except Exception as e:
            logger.error(f"Error during message handling for {client_id} on path {path}: {e}", exc_info=True)
        finally:
            # Cleanup when the connection is closed or an error occurs.
            logger.info(f"Cleaning up connection {client_id}.")
            if client_id in self._connections:
                del self._connections[client_id]
            
            # If this was the active connection, try to set a new active one.
            if self._active_connection_id == client_id:
                if self._connections:
                    self._active_connection_id = next(iter(self._connections.keys()))
                    logger.info(f"Switched active connection to {self._active_connection_id}.")
                else:
                    self._active_connection_id = None
                    logger.info("No remaining connections, active connection set to None.")
            logger.info(f"Connection {client_id} fully cleaned up.")

    async def _process_message(self, client_id: str, message_data: str) -> None:
        """
        Processes an incoming WebSocket message string from a specific client.
        """
        try:
            raw_message = json.loads(message_data)
            # Validate the base structure first
            base_msg = BaseMessage.model_validate(raw_message)
            logger.debug(f"Received message from {client_id}: Type '{base_msg.type}', ID '{base_msg.id}'")

            if base_msg.type == "response":
                # If it's a response, validate against ResponseMessage and handle it.
                response_msg = ResponseMessage.model_validate(raw_message)
                future = self._pending_requests.pop(response_msg.id, None)
                if future and not future.done():
                    if response_msg.data.error:
                        logger.warning(f"Response for ID {response_msg.id} contained an error: {response_msg.data.error}")
                        future.set_exception(RuntimeError(f"Extension Error: {response_msg.data.error}"))
                    else:
                        future.set_result(response_msg.data)
                elif future and future.done():
                    logger.warning(f"Received response for already completed future ID {response_msg.id}")
                else:
                    logger.warning(f"Received response for unknown or already handled request ID: {response_msg.id}")
            # TODO: Handle other message types if the extension can send requests to Python.
            # Example: if base_msg.type == "event_from_extension":
            #            logger.info(f"Received event from extension: {raw_message.get('data')}")
            else:
                logger.warning(f"Unhandled message type '{base_msg.type}' from {client_id}. Content: {message_data}")
        
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message received from {client_id}: {message_data}", exc_info=True)
        except Exception as e:
            logger.error(f"Error processing message from {client_id}: {e}. Original message: {message_data}", exc_info=True)
    
    async def _send_request(self, request_type: str, data: Dict[str, Any], timeout: float = 30.0) -> ResponseData:
        """
        Sends a request to the currently active Chrome extension and awaits a response.

        Args:
            request_type: The type of request (e.g., "get_state", "execute_action").
            data: The payload for the request.
            timeout: Maximum time in seconds to wait for a response.

        Returns:
            The data part of the response message from the extension.

        Raises:
            RuntimeError: If no active connection is available or if the connection is lost.
            TimeoutError: If the extension does not respond within the specified timeout.
        """
        async with self._lock: # Ensure thread-safe access to shared message counter
            if not self._active_connection_id or self._active_connection_id not in self._connections:
                logger.error("Cannot send request: No active extension connection or connection info missing.")
                raise RuntimeError("No active extension connection available.")
            
            connection_info = self._connections[self._active_connection_id]
            websocket = connection_info.websocket

            if websocket.closed:
                logger.error(f"Cannot send request: WebSocket for active connection {self._active_connection_id} is closed.")
                # Attempt to clean up this connection as it's unexpectedly closed.
                del self._connections[self._active_connection_id]
                self._active_connection_id = next(iter(self._connections.keys())) if self._connections else None
                raise RuntimeError(f"WebSocket connection {connection_info.client_id} is closed.")

            request_id = self._message_id_counter
            self._message_id_counter += 1
        
        future: asyncio.Future[ResponseData] = asyncio.Future()
        self._pending_requests[request_id] = future
        
        message_payload = {"id": request_id, "type": request_type}
        if data: # Add 'data' field only if it's provided for the specific request type
            message_payload["data"] = data
        
        # Validate the outgoing message structure with Pydantic (optional but good practice)
        try:
            request_msg = RequestMessage.model_validate(message_payload)
            serialized_message = request_msg.model_dump_json()
        except Exception as e:
            logger.error(f"Failed to validate or serialize outgoing request: {e}", exc_info=True)
            if request_id in self._pending_requests: # Clean up future if serialization failed
                 del self._pending_requests[request_id]
            raise ValueError(f"Internal error: Failed to create valid request message: {e}")

        logger.debug(f"Sending request to {self._active_connection_id}: ID {request_id}, Type {request_type}, Data {data}")
        try:
            await websocket.send(serialized_message)
        except ConnectionClosed as e:
            logger.error(f"Connection closed while trying to send request {request_id}: {e}")
            self._pending_requests.pop(request_id, None) # Clean up future
            raise RuntimeError(f"Connection lost while sending request: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending request {request_id}: {e}", exc_info=True)
            self._pending_requests.pop(request_id, None) # Clean up future
            raise
        
        # Wait for the response with the specified timeout.
        try:
            response_data = await asyncio.wait_for(future, timeout=timeout)
            return response_data
        except asyncio.TimeoutError:
            logger.error(f"Request ID {request_id} (Type: {request_type}) to extension timed out after {timeout}s.")
            self._pending_requests.pop(request_id, None) # Clean up future on timeout
            raise TimeoutError(f"Request {request_type} (ID: {request_id}) to extension timed out.")
        except asyncio.CancelledError:
            logger.info(f"Request ID {request_id} (Type: {request_type}) was cancelled.")
            self._pending_requests.pop(request_id, None)
            raise # Re-raise CancelledError
        except Exception as e:
            logger.error(f"Exception waiting for response for request ID {request_id}: {e}", exc_info=True)
            self._pending_requests.pop(request_id, None)
            raise # Re-raise other exceptions

    async def get_state(self, include_screenshot: bool = False) -> BrowserState:
        """
        Retrieves the current browser state from the Chrome extension.

        Args:
            include_screenshot: Whether to request a screenshot from the extension.

        Returns:
            A BrowserState object representing the current state of the browser.

        Raises:
            RuntimeError: If there's an error communicating with the extension or parsing the response.
            TimeoutError: If the request to the extension times out.
        """
        logger.info(f"Requesting browser state from extension (screenshot: {include_screenshot})...")
        request_data = {"includeScreenshot": include_screenshot}
        response_payload = await self._send_request("get_state", request_data)

        if response_payload.error:
            logger.error(f"Extension returned an error when getting state: {response_payload.error}")
            raise RuntimeError(f"Error from extension getting browser state: {response_payload.error}")
        
        # Parse the element tree from the raw dictionary into DOMElementNode objects
        parsed_element_tree = self._parse_element_tree_data(response_payload.element_tree or {})

        # Parse tab information
        parsed_tabs = []
        if response_payload.tabs:
            for tab_data in response_payload.tabs:
                try:
                    # The extension sends page_id, url, title. We map it to TabInfo.
                    # The extension might also send its internal `id` (Chrome's tabId).
                    parsed_tabs.append(TabInfo(
                        page_id=tab_data.get("page_id", -1), # Default to -1 if missing
                        url=tab_data.get("url", ""),
                        title=tab_data.get("title", "")
                        # We can store tab_data.get("id") if needed later for direct tab manipulation.
                    ))
                except Exception as e:
                    logger.warning(f"Failed to parse tab data: {tab_data}. Error: {e}", exc_info=True)
        
        # Construct and return the BrowserState object
        try:
            state = BrowserState(
                url=response_payload.url or "",
                title=response_payload.title or "",
                element_tree=parsed_element_tree,
                # The selector_map from extension is Dict[str, Dict[str, Any]] where key is highlight_index as string
                # BrowserState expects Dict[int, Any]. We need to convert keys to int.
                selector_map={int(k): v for k, v in response_payload.selector_map.items()} if response_payload.selector_map else {},
                tabs=parsed_tabs,
                screenshot=response_payload.screenshot,
                pixels_above=response_payload.pixels_above or 0,
                pixels_below=response_payload.pixels_below or 0
            )
            logger.info("Successfully received and parsed browser state from extension.")
            return state
        except Exception as e:
            logger.error(f"Failed to create BrowserState from extension response: {e}", exc_info=True)
            logger.debug(f"Raw response data that caused parsing error: {response_payload.model_dump_json(indent=2)}")
            raise RuntimeError(f"Could not parse browser state from extension: {e}")

    def _parse_element_tree_data(self, element_data: Dict[str, Any]) -> DOMElementNode:
        """
        Recursively parses the raw element tree data (JSON-like dict)
        received from the extension into a structured DOMElementNode object.

        Args:
            element_data: A dictionary representing a node in the DOM tree from the extension.

        Returns:
            A DOMElementNode object representing the parsed element and its children.
            Returns a default/empty DOMElementNode if input is invalid or empty.
        """
        if not element_data or not element_data.get("type"): # Basic validation
            logger.warning(f"Attempted to parse empty or invalid element data: {element_data}")
            # Return a default, empty, but valid DOMElementNode to prevent crashes upstream.
            return DOMElementNode(tag_name="unknown", xpath="", children=[], attributes={}, is_visible=False, type="element")

        node_type = element_data.get("type", "element")
        
        # Handle text nodes specifically
        if node_type == "text":
            return DOMElementNode(
                tag_name="#text", # Conventional name for text nodes
                text=element_data.get("text", ""),
                type="text",
                is_visible=element_data.get("is_visible", False),
                # Text nodes don't have attributes, children, xpath in the same way elements do
                attributes={},
                xpath="", # XPath is not typically used for text nodes in this context
                children=[]
            )

        # Handle element nodes
        # Recursively parse child nodes
        children_nodes = []
        raw_children = element_data.get("children", [])
        if raw_children:
            for child_data in raw_children:
                if isinstance(child_data, dict):
                    parsed_child = self._parse_element_tree_data(child_data)
                    children_nodes.append(parsed_child)
                else:
                    logger.warning(f"Child data is not a dictionary, skipping: {child_data}")
        
        # Create the DOMElementNode for the current element
        try:
            node = DOMElementNode(
                tag_name=element_data.get("tag_name", "unknown"),
                attributes=element_data.get("attributes", {}),
                highlight_index=element_data.get("highlight_index"), # Can be None
                is_visible=element_data.get("is_visible", False),
                xpath=element_data.get("xpath", ""),
                children=children_nodes,
                type="element" # Explicitly set type for element nodes
                # Parent references are typically set in a separate pass if needed by walking the tree.
            )
            # Explicitly assign text if type is element and text is in element_data, 
            # as Pydantic might only map it if DOMElementNode.text wasn't None by default or if type was 'text'.
            # This ensures that if the extension sends a "text" field for an element, it's captured.
            if node.type == "element" and "text" in element_data and element_data["text"] is not None:
                node.text = str(element_data["text"])
            return node
        except Exception as e:
            logger.error(f"Error parsing element data into DOMElementNode: {e}. Data: {element_data}", exc_info=True)
            # Return a fallback node to avoid crashing
            return DOMElementNode(tag_name="parse_error", xpath="", children=[], attributes={}, is_visible=False, type="element")
    
    async def execute_action(self, action: str, params: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        """
        Executes a specific action in the browser extension (e.g., click, type, scroll).
        Args:
            action: The name of the action to execute.
            params: A dictionary of parameters for the action.
            timeout: Timeout in seconds for awaiting the response.
        Returns:
            A dictionary containing the result of the action.
        """
        payload = {"action": action, "params": params}
        logger.debug(f"Executing action: '{action}' with params: {params}")
        # Call _send_request with keyword arguments for clarity and robustness
        response_data = await self._send_request(request_type="execute_action", data=payload, timeout=timeout)
        
        # response_data is a ResponseData model instance. Convert to dict for return.
        # model_dump will include fields from model_extra if ResponseData allows them.
        return response_data.model_dump(exclude_none=True)

    # --- Helper properties and methods ---
    @property
    def active_connection(self) -> Optional[ConnectionInfo]:
        """Returns the active ConnectionInfo object, or None if no connection is active."""
        if self._active_connection_id and self._active_connection_id in self._connections:
            return self._connections[self._active_connection_id]
        return None

    @property
    def is_server_running(self) -> bool:
        """Checks if the WebSocket server is currently running."""
        return self._server is not None and self._server.is_serving()
    
    @property
    def has_active_connection(self) -> bool:
        """Checks if there is an active and open WebSocket connection to an extension."""
        conn = self.active_connection
        return conn is not None and conn.websocket is not None and conn.websocket.open


# Example usage (for testing purposes if run directly)
async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    interface = ExtensionInterface()
    await interface.start_server()
    
    try:
        # Keep the server running until interrupted
        while True:
            if interface.has_active_connection:
                logger.info("Extension interface is running and has an active connection.")
                # Example: Periodically request state if an extension is connected
                # try:
                #     state = await interface.get_state(include_screenshot=False)
                #     logger.info(f"Got state: URL: {state.url}, Title: {state.title}")
                #     if state.tabs:
                #        logger.info(f"Open tabs: {[(t.page_id, t.title) for t in state.tabs]}")
                # except Exception as e:
                #     logger.error(f"Error getting state in main loop: {e}")
            else:
                logger.info("Extension interface is running, waiting for connection...")
            await asyncio.sleep(10) # Check status every 10 seconds
            
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"An unexpected error occurred in main loop: {e}", exc_info=True)
    finally:
        logger.info("Shutting down server...")
        await interface.stop_server()
        logger.info("Server shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Main programmatically interrupted.") 