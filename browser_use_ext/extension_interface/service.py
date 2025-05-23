from __future__ import annotations

import sys
import os
# print(f"Current working directory: {os.getcwd()}")
# print(f"sys.path: {sys.path}")

# Standard library imports
import asyncio
import inspect # ADDED FOR DEBUGGING
import json
import logging
import uuid
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, TYPE_CHECKING # ADDED TYPE_CHECKING

# Third-party imports
import websockets
from pydantic import BaseModel, Field, ValidationError
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK
from websockets.asyncio.server import ServerConnection
from websockets.protocol import State

# Local application/library specific imports
# REMOVED: from ..browser.views import TabInfo 
if TYPE_CHECKING:
    from ..browser.views import BrowserState, TabInfo # Keep for type hinting
    from ..dom.views import DOMElementNode, DOMDocumentNode # Keep for type hinting

# Initialize logger for this module
logger = logging.getLogger(__name__)
# ADDED: Ensure logger level is set for this module if not inherited
if not logger.hasHandlers(): # Basic check, or just set level directly
    logger.setLevel(logging.DEBUG) 
    # If no handlers, it might not output. This assumes root logger is configured.

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
    # Raw HTML content of the page, typically included in get_state responses.
    html_content: Optional[str] = Field(None, description="Raw HTML content of the page (optional).")
    # DOM structure, typically included in get_state responses.
    tree: Optional[Dict[str, Any]] = Field(None, description="Raw element tree from extension.")
    # Selector map, typically included in get_state responses.
    selector_map: Optional[Dict[str, Any]] = Field(None, description="Raw selector map from extension.")
    # List of tabs, typically included in get_state responses.
    tabs: Optional[List[Dict[str, Any]]] = Field(None, description="List of tabs from extension.")
    # Screenshot data (base64), if requested. Will be kept null.
    screenshot: Optional[str] = Field(None, description="Base64 encoded screenshot data (kept as null).")
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
    websocket: ServerConnection
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
    
    async def _handle_connection(self, websocket: ServerConnection, path: Optional[str] = None) -> None:
        """
        Manages a new WebSocket connection from a client (the Chrome extension).
        Each connection runs in its own instance of this coroutine.
        """
        # --- DEBUGGING LINES ADDED ---
        try:
            logger.critical(f"!!! EXECUTING _handle_connection from: {inspect.getfile(self.__class__)}")
            logger.critical(f"!!! Method signature: {inspect.signature(self._handle_connection)}")
        except Exception as e_inspect:
            logger.critical(f"!!! INSPECT FAILED: {e_inspect}")
        # --- END DEBUGGING LINES ---
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
        Processes a single message received from the WebSocket client.
        It parses the message, validates it, and then handles it based on its type.
        """
        # Log the raw message data for debugging purposes
        logger.info(f"Received message from {client_id}: {message_data}")

        try:
            # Parse the incoming JSON string into a dictionary
            raw_message = json.loads(message_data)
            # Validate the base structure first
            base_msg = BaseMessage.model_validate(raw_message)
            logger.debug(f"Received message from {client_id}: Type '{base_msg.type}', ID '{base_msg.id}'")

            if base_msg.type == "response":
                # Validate as a full ResponseMessage
                response_msg = ResponseMessage.model_validate(raw_message)
                future = self._pending_requests.pop(response_msg.id, None)
                if future and not future.done():
                    if response_msg.data.error:
                        # If there's an error in the response, encapsulate it and set it as the future's exception
                        error_message = f"Extension error for request ID {response_msg.id}: {response_msg.data.error}"
                        logger.error(error_message)
                        future.set_exception(RuntimeError(error_message))
                    else:
                        # Otherwise, set the successful result
                        future.set_result(response_msg.data)
                elif future and future.done():
                    logger.warning(f"Received response for already completed/cancelled future {response_msg.id}")
                else:
                    logger.warning(f"Received unsolicited response or response for unknown request ID: {response_msg.id}")
            
            elif base_msg.type == "error": # Assuming extension might send an 'error' type for unsolicited errors
                error_payload = raw_message.get("data", {})
                error_message = error_payload.get("message", "Unknown error from extension")
                logger.error(f"Received unsolicited error from {client_id}: {error_message} (Raw: {message_data})")

            elif base_msg.type == "extension_event": # For events like page load, tab switch, etc.
                event_payload = raw_message.get("data", {})
                event_name = event_payload.get("event_name", "unknown_event")
                logger.info(f"Received event '{event_name}' from {client_id}: {event_payload}")
                # Here you could dispatch these events to other parts of the application
                # For example, using asyncio.Queue or registered callbacks.

            else:
                logger.warning(f"Received message of unhandled type '{base_msg.type}' from {client_id}")

        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON message from {client_id}: {message_data[:200]}...") # Log snippet
        except ValidationError as e:
            logger.error(f"Message validation error from {client_id} for message '{message_data[:200]}...': {e}")
        except Exception as e: # Catch-all for other errors during message processing
            logger.error(f"Unexpected error processing message from {client_id}: {e}", exc_info=True)


    async def _send_request(self, request_type: str, data: Optional[Dict[str, Any]] = None, timeout: float = 30.0) -> ResponseData:
        active_conn_info = self.active_connection # Get it once
        
        # MODIFIED: Check connection state using websocket.state for version 15.0.1
        if not active_conn_info or active_conn_info.websocket.state != State.OPEN:
            logger.error(f"Attempted to send request but connection is not active or not in OPEN state.")
            active_client_id = active_conn_info.client_id if active_conn_info else "N/A"
            current_state = active_conn_info.websocket.state if active_conn_info else "N/A"
            logger.error(f"Connection details: ID={active_client_id}, Current State={current_state}")
            raise RuntimeError(f"Active connection {active_client_id} is not open (state: {current_state}).")

        async with self._lock: 
            self._message_id_counter += 1
            msg_id = self._message_id_counter
        
        request = RequestMessage(id=msg_id, type=request_type, data=data)
        future: asyncio.Future[ResponseData] = asyncio.Future()
        self._pending_requests[msg_id] = future

        try:
            await active_conn_info.websocket.send(request.model_dump_json())
            logger.debug(f"Sent {request_type} request (ID: {msg_id}) to {active_conn_info.client_id}")
            
            return await asyncio.wait_for(future, timeout=timeout)
        
        except asyncio.TimeoutError:
            logger.error(f"Timeout waiting for response to {request_type} request (ID: {msg_id})")
            self._pending_requests.pop(msg_id, None) 
            raise RuntimeError(f"Request {request_type} (ID: {msg_id}) timed out after {timeout}s.")
        except websockets.exceptions.ConnectionClosed: 
            logger.error(f"Connection closed while sending/waiting for {request_type} (ID: {msg_id})")
            self._pending_requests.pop(msg_id, None)
            raise RuntimeError(f"Connection closed during request {request_type} (ID: {msg_id}).")
        except Exception as e: 
            logger.error(f"Error sending/processing {request_type} request (ID: {msg_id}): {e}", exc_info=True)
            self._pending_requests.pop(msg_id, None)
            raise RuntimeError(f"Failed to process request {request_type} (ID: {msg_id}): {e}")


    async def get_state(self, include_screenshot: bool = False) -> 'BrowserState':
        """
        Requests the current browser state from the extension.
        """
        from ..browser.views import BrowserState, TabInfo
        from ..dom.views import DOMDocumentNode, DOMElementNode

        logger.info(f"Requesting browser state (screenshot: {include_screenshot})...")
        payload = {"includeScreenshot": include_screenshot}
        response_data = await self._send_request("get_state", payload)

        if response_data.url is None or \
           response_data.title is None or \
           response_data.tree is None or \
           response_data.selector_map is None or \
           response_data.tabs is None or \
           response_data.pixels_above is None or \
           response_data.pixels_below is None:
            error_msg = "Received incomplete state data from extension (missing one or more core fields)."
            logger.error(error_msg + f" Response: {response_data.model_dump_json(indent=2)}")
            raise RuntimeError(error_msg)
        
        try:
            raw_html_element_data = response_data.tree 
            if raw_html_element_data.get("type") != "element":
                err_msg = f"Expected root of tree from extension to be type 'element' (the html tag), but got '{raw_html_element_data.get('type')}'"
                logger.error(err_msg + f" Tree data: {json.dumps(raw_html_element_data, indent=2)}")
                raise ValueError(err_msg)

            parsed_html_element = self._parse_element_tree_data(raw_html_element_data)
            # logger.debug(f"[DEBUG] Type of parsed_html_element: {type(parsed_html_element)}") 

            parsed_document_tree = DOMDocumentNode(
                type="document", 
                children=[parsed_html_element]
            )
            # logger.debug(f"[DEBUG] Type of parsed_document_tree: {type(parsed_document_tree)}")
            
            DEBUG_TREE_FILENAME = os.path.join(os.getcwd(), "debug_parsed_document_tree.json")
            try:
                with open(DEBUG_TREE_FILENAME, "w", encoding="utf-8") as f_debug:
                    f_debug.write(parsed_document_tree.model_dump_json(indent=2))
                # MODIFIED: Use a standard print for high visibility
                print(f"\n\n>>>> SUCCESS: DEBUG TREE WRITTEN TO: {DEBUG_TREE_FILENAME} <<<<\n\n")
                logger.debug(f"[SERVICE_DEBUG] Parsed document tree structure saved to {DEBUG_TREE_FILENAME}") 
            except Exception as e_debug_write:
                # MODIFIED: Use a standard print for high visibility
                print(f"\n\n>>>> ERROR: FAILED TO WRITE DEBUG TREE TO FILE: {DEBUG_TREE_FILENAME} <<<<\nError: {e_debug_write}\n\n")
                logger.error(f"[SERVICE_DEBUG] Failed to write debug tree to file: {e_debug_write}", exc_info=True)
            
            # logger.debug(f"[DEBUG] parsed_document_tree content (before BrowserState): {parsed_document_tree.model_dump_json(indent=2)}") # Keep this commented for now
            
            parsed_tabs: List[TabInfo] = []
            for tab_data in response_data.tabs:
                if not all(k in tab_data for k in ("tabId", "url", "title", "isActive")):
                    logger.warning(f"Skipping tab with incomplete data: {tab_data}. Expected tabId, url, title, isActive.")
                    continue
                try:
                    parsed_tabs.append(TabInfo.model_validate(tab_data))
                except ValidationError as ve_tab:
                    logger.warning(f"Validation error parsing tab data: {ve_tab}. Data: {tab_data}")
                    continue            

            final_browser_state = BrowserState(
                url=response_data.url,
                title=response_data.title,
                html_content=response_data.html_content,
                tree=parsed_document_tree, 
                selector_map=response_data.selector_map,
                tabs=parsed_tabs,
                screenshot=None, 
                pixels_above=response_data.pixels_above,
                pixels_below=response_data.pixels_below
            )
            # logger.debug(f"[DEBUG] Type of final_browser_state.tree: {type(final_browser_state.tree)}")
            return final_browser_state
        except ValidationError as e: 
            logger.error(f"Pydantic validation error constructing BrowserState or its components: {e}", exc_info=True)
            logger.error(f"Data causing validation error: Relevant part of response_data: {response_data.model_dump_json(indent=2)}")
            raise RuntimeError(f"Failed to parse browser state from extension: {e}")
        except Exception as e:
            logger.error(f"Unexpected error constructing BrowserState: {e}", exc_info=True)
            tree_data_for_log = json.dumps(response_data.tree, indent=2) if response_data and response_data.tree else 'N/A'
            logger.error(f"Problematic tree data during BrowserState construction: {tree_data_for_log}")
            raise RuntimeError(f"Unexpected error constructing BrowserState: {e}")


    def _parse_element_tree_data(self, element_data: Dict[str, Any]) -> 'DOMElementNode':
        """
        Recursively parses the raw element tree data from the extension into DOMElementNode objects.
        Ensures that 'text' attribute is correctly handled.

        Args:
            element_data: A dictionary representing a node from the extension's element tree.

        Returns:
            A DOMElementNode object.
        """
        # Local import for instantiation
        from ..dom.views import DOMElementNode
        
        # Pre-validation of essential keys
        if not all(k in element_data for k in ("type", "xpath")):
            raise ValueError(f"Essential keys 'type' or 'xpath' missing in element data: {element_data}")

        # Create a copy to avoid modifying the original dict, especially for 'attributes'
        data_copy = element_data.copy()

        # Ensure 'attributes' is a dictionary, default to empty if not present or None
        attributes = data_copy.get("attributes")
        if not isinstance(attributes, dict):
            attributes = {}
        
        # Handle 'text' content: convert to string if present, otherwise it remains None via Pydantic default
        node_text: Optional[str] = None
        if data_copy.get("type") == "text": # For text nodes, 'text' is its content
            node_text = str(data_copy.get("text", "")) # Ensure it's a string, even if empty
        elif data_copy.get("type") == "element": # For element nodes, 'text' is direct text child
            if "text" in data_copy and data_copy["text"] is not None:
                node_text = str(data_copy["text"])
        
        # Recursively parse child nodes
        children_nodes = []
        if "children" in data_copy and isinstance(data_copy["children"], list):
            for child_data in data_copy["children"]:
                if isinstance(child_data, dict): # Ensure child_data is a dict before parsing
                    try:
                        children_nodes.append(self._parse_element_tree_data(child_data))
                    except ValueError as ve: # Catch parsing errors from children
                        logger.warning(f"Skipping child due to parsing error: {ve}. Child data: {child_data}")
                else:
                    logger.warning(f"Skipping non-dictionary child item: {child_data}")
        
        # Prepare fields for DOMElementNode, ensuring all required fields are present or have defaults
        node_fields = {
            "type": data_copy["type"],
            "xpath": data_copy["xpath"],
            "highlight_id": data_copy.get("highlight_id"), # Will be None if not present
            "tag_name": data_copy.get("tag_name"), # Will be None for non-element types
            "attributes": attributes,
            "text": node_text, # Assign the processed text
            "children": children_nodes,
            "is_interactive": data_copy.get("is_interactive", False), # Default to False
            "is_visible": data_copy.get("is_visible", False), # Default to False
            "value": data_copy.get("value"), # For input elements
            "raw_html_outer": data_copy.get("raw_html_outer"),
            "raw_html_inner": data_copy.get("raw_html_inner"),
        }
        
        # Validate and create the DOMElementNode
        try:
            return DOMElementNode.model_validate(node_fields)
        except ValidationError as e:
            logger.error(f"Validation error creating DOMElementNode for {data_copy.get('xpath')}: {e}\nData: {node_fields}", exc_info=True)
            # Instead of raising here and potentially stopping a large tree parse,
            # one might consider returning a "failed_parse" node or logging and skipping.
            # For now, re-raise to indicate the issue.
            raise ValueError(f"Failed to validate DOMElementNode: {e}. Data: {node_fields}") from e


    async def execute_action(self, action: str, params: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        """
        Executes an action in the browser via the extension.

        Args:
            action: The name of the action to execute (e.g., "click", "input_text").
            params: A dictionary of parameters for the action.
            timeout: Timeout for the action in seconds.

        Returns:
            A dictionary containing the result of the action from the extension.
        """
        logger.info(f"Executing action '{action}' with params: {params}")
        payload = {"action": action, "params": params}
        response_data = await self._send_request("execute_action", payload, timeout=timeout)
        
        # The response_data itself is a Pydantic model. We return its dictionary representation.
        # Exclude None values for cleaner output.
        action_result = response_data.model_dump(exclude_none=True)
        logger.info(f"Action '{action}' executed. Result: {action_result}")
        return action_result

    @property
    def active_connection(self) -> Optional[ConnectionInfo]:
        """Returns the currently active ConnectionInfo, or None if no connection is active."""
        if self._active_connection_id and self._active_connection_id in self._connections:
            return self._connections[self._active_connection_id]
        return None

    @property
    def is_server_running(self) -> bool:
        """Checks if the WebSocket server is currently running."""
        return self._server is not None and self._server.is_serving()

    @property
    def has_active_connection(self) -> bool:
        """Checks if there is an active and open WebSocket connection using state for v15.0.1."""
        conn_info = self.active_connection
        if conn_info is None:
            return False
        # MODIFIED: Use .state == State.OPEN for checking connection status as per websockets v15.0.1 docs
        return conn_info.websocket.state == State.OPEN

# --- Main Execution Block (for standalone server operation) ---

async def main():
    """Main function to run the WebSocket server."""
    # Configure basic logging
    logging.basicConfig(
        level=logging.DEBUG, # Changed to DEBUG for more verbose output
        format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Define server host and port
    host = "localhost"
    port = 8765
    
    # Create an instance of the interface
    interface = ExtensionInterface(host=host, port=port)
    
    # Log sys.path for debugging import issues
    logger.debug(f"Current sys.path: {sys.path}")
    import os # Ensure os is imported for getcwd
    logger.debug(f"Current working directory: {os.getcwd()}")

    try:
        # Start the server
        await interface.start_server()
        
        # Keep the server running until interrupted (e.g., Ctrl+C)
        # This loop also allows for periodic checks or tasks if needed.
        while interface.is_server_running:
            await asyncio.sleep(1) # Sleep for a short duration to prevent busy-waiting
            
    except KeyboardInterrupt:
        logger.info("Server shutting down due to KeyboardInterrupt...")
    except Exception as e:
        logger.error(f"An unhandled error occurred in main: {e}", exc_info=True)
    finally:
        logger.info("Initiating server stop sequence...")
        await interface.stop_server()
        logger.info("Server has been stopped.")

if __name__ == "__main__":
    # Entry point when the script is executed directly.
    # This sets up and runs the asyncio event loop.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # This is just to make the exit cleaner on Ctrl+C if asyncio.run() itself is interrupted
        # before main() handles it.
        logger.info("Asyncio event loop interrupted. Exiting.")
    except Exception as e:
        # Catch-all for any other exceptions during asyncio.run, e.g., if main() raises something
        # that isn't caught internally.
        logger.critical(f"Fatal error during asyncio.run: {e}", exc_info=True) 