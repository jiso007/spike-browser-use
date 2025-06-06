from __future__ import annotations # Ensure this is at the top
from typing import Dict, Any, Optional, TypeVar, TYPE_CHECKING
import logging
# from browser.context import BrowserContext, BrowserContextConfig # Incorrect path
# from ..browser.context import BrowserContext, BrowserContextConfig # Corrected relative import path -> REMOVE THIS TOP-LEVEL IMPORT
# from .response_data import ResponseData # REMOVE THIS - will be imported from .models
# from .models import Message, ConnectionInfo # Old import, will be replaced
from .models import BaseMessage, Message, ResponseData, ConnectionInfo # REMOVED ServerMessage, StateData
# REMOVED: from ..browser.views import BrowserState
from ..browser.views import BrowserState # ADDED: Import BrowserState
import json
import os
from datetime import datetime
import asyncio
import inspect # ADDED FOR DEBUGGING
import re 
import uuid
from pydantic import ValidationError # Ensure ValidationError is imported
import websockets # type: ignore
from websockets.server import ServerConnection, serve
# from websockets.asyncio.server import ServerConnection # Old import for older versions
# from websockets import serve # Old import for serve
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from ..agent.views import ActionResult # CORRECTED IMPORT

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# Agent imports
try:
    from langchain_openai import ChatOpenAI
    from langchain_anthropic import ChatAnthropic
    from ..agent.service import Agent
    from ..agent.views import AgentSettings, AgentHistoryList
    AGENT_IMPORTS_AVAILABLE = True
except ImportError:
    AGENT_IMPORTS_AVAILABLE = False
    logger.warning("Agent imports not available. Agent functionality will be limited.")

# Maximum time (in seconds) to wait for a response from the extension
DEFAULT_REQUEST_TIMEOUT = 10  # seconds


class ExtensionInterface:
    def __init__(self, host: str = "localhost", port: int = 8765, 
                 llm_model: str = "gpt-4o", llm_temperature: float = 0.0):
        self.host = host
        self.port = port
        self._server: Optional[websockets.server.WebSocketServer] = None
        self._connections: Dict[str, ConnectionInfo] = {}
        self._active_connection_id: Optional[str] = None
        self._message_id_counter: int = 0
        self._pending_requests: Dict[int, asyncio.Future] = {}
        self._active_tab_id: Optional[int] = None
        # self._initial_state_fetched_for_event = False # Flag seems unused, can be removed if truly so
        self._filename_sanitize_re = re.compile(r'[^a-zA-Z0-9_.-]+')
        self._content_script_ready_tabs: Dict[int, float] = {}
        
        # Agent-related attributes
        self._llm_model = llm_model
        self._llm_temperature = llm_temperature
        self._llm = None
        self._active_agents: Dict[str, Any] = {}  # session_id -> Agent instance
        
        # Initialize LLM for agent functionality
        self._initialize_llm()
    
    def _initialize_llm(self) -> None:
        """Initialize the LLM for agent functionality based on available API keys."""
        if not AGENT_IMPORTS_AVAILABLE:
            logger.warning("LLM imports not available. Agent functionality disabled.")
            return
            
        # Check for API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Determine which LLM to use based on model and available keys
        if self._llm_model.startswith("claude") and anthropic_key:
            try:
                self._llm = ChatAnthropic(
                    model=self._llm_model,
                    temperature=self._llm_temperature,
                    api_key=anthropic_key
                )
                logger.info(f"Initialized Anthropic LLM with model: {self._llm_model}")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic LLM: {e}")
                self._llm = None
        elif (self._llm_model.startswith("gpt") or not self._llm_model.startswith("claude")) and openai_key:
            try:
                # Default to gpt-4o if unknown model
                model_to_use = self._llm_model if self._llm_model.startswith("gpt") else "gpt-4o"
                self._llm = ChatOpenAI(
                    model=model_to_use,
                    temperature=self._llm_temperature,
                    api_key=openai_key
                )
                logger.info(f"Initialized OpenAI LLM with model: {model_to_use}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI LLM: {e}")
                self._llm = None
        else:
            logger.warning("No LLM API keys found in environment. Agent functionality will be limited.")
            self._llm = None

    @property
    def has_active_connection(self) -> bool:
        """Returns True if there is an active client connection, False otherwise."""
        return self._active_connection_id is not None

    @property
    def active_connection_object(self) -> Optional[ConnectionInfo]:
        """Returns the ConnectionInfo object for the active connection, or None."""
        if self._active_connection_id:
            return self._connections.get(self._active_connection_id)
        return None

    @property
    def is_server_running(self) -> bool:
        """Returns True if the WebSocket server is running, False otherwise."""
        return self._server is not None

    def _sanitize_filename_component(self, component: str) -> str:
        """Sanitizes a string component to be safe for use in a filename."""
        component = component.replace("http://", "").replace("https://", "").replace("www.", "")
        sanitized = self._filename_sanitize_re.sub('_', component)
        return sanitized[:50]

    async def _fetch_and_save_initial_state(self, client_id: str, event_data: Dict[str, Any]) -> None:
        """Fetches the browser state and saves it to a JSON file, triggered by an event."""
        # Import moved here to break circular dependency
        from ..browser.context import BrowserContext, BrowserContextConfig

        tab_id = event_data.get('tabId') 
        page_url = event_data.get('url', 'unknown_url')

        logger.info(f"Attempting to fetch browser state for client_{client_id} (Tab ID: {tab_id}, URL: {page_url})")
        try:
            config = BrowserContextConfig() 
            browser_context = BrowserContext(config=config, extension_interface=self)
            current_tab_id = tab_id if isinstance(tab_id, int) else None
            current_state = await browser_context.get_state(tab_id=current_tab_id) 
            logger.info(f"Browser state successfully fetched for client_{client_id} (Tab ID: {tab_id}):")
            state_json_str = json.dumps(current_state.model_dump(), indent=2)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            sanitized_url_component = self._sanitize_filename_component(page_url)
            filename_tab_id_part = str(tab_id) if tab_id is not None else "unknown_tab"
            filename = f"browser_state_tab{filename_tab_id_part}_{sanitized_url_component}_{timestamp}.json"
            output_subdirectory = "browser_states_json_logs"
            base_dir = os.getcwd() 
            full_dir_path = os.path.join(base_dir, output_subdirectory)
            if not os.path.exists(full_dir_path):
                os.makedirs(full_dir_path)
                logger.info(f"Created directory: {full_dir_path}")
            file_path = os.path.join(full_dir_path, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(state_json_str)
            logger.info(f"Successfully saved browser state to {file_path}")
        except Exception as e:
            logger.error(f"Error fetching/saving state for client_{client_id} (Tab ID: {tab_id}) triggered by event: {e}", exc_info=True)

    async def get_state(self, for_vision: bool = False, tab_id: Optional[int] = None) -> Optional[BrowserState]:
        """
        Requests the current browser state from the best available tab.
        """
        # Smart tab selection: use explicit tab_id, or find best ready tab, or fallback to active tab
        target_tab_id = tab_id if tab_id is not None else self._get_best_ready_tab_id()
        if target_tab_id is None:
            logger.warning("get_state called but no suitable tab ID found (no active tab or ready tabs).")
            return None

        logger.debug(f"Sending 'get_state' request for tab ID: {target_tab_id}")

        # Wait for content script ready before sending request
        try:
            await self._wait_for_content_script_ready(target_tab_id, timeout_seconds=DEFAULT_REQUEST_TIMEOUT)
        except asyncio.TimeoutError as e:
            logger.error(f"Content script in tab {target_tab_id} not ready before sending get_state: {e}")
            raise RuntimeError(f"Content script in tab {target_tab_id} not ready: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error while waiting for content script ready for tab {target_tab_id}: {e}", exc_info=True)
            raise RuntimeError(f"Unexpected error waiting for content script ready for tab {target_tab_id}: {e}") from e

        # Use _send_request to handle the request properly
        try:
            response_data_model = await self._send_request(
                action="get_state",
                data={
                    "action": "get_state",
                    "params": {"for_vision": for_vision},
                    "tabId": target_tab_id  # FIXED: Send the target tab ID to background.js
                },
                timeout=DEFAULT_REQUEST_TIMEOUT
            )

            if not response_data_model:
                logger.warning("get_state received None response from _send_request")
                return None

            # Parse the received data into a BrowserState model
            # response_data_model is already a ResponseData instance
            browser_state = BrowserState.model_validate(response_data_model.model_dump())
            logger.debug(f"Successfully parsed BrowserState")
            return browser_state

        except RuntimeError as e:
             # Catch the RuntimeError raised for extension errors and add context
             logger.error(f"RuntimeError during get_state for tab {target_tab_id}: {e}")
             raise RuntimeError(f"Error getting browser state for tab {target_tab_id}: {e}") from e # Chain the exception
        except Exception as e:
            logger.error(f"Unexpected error processing get_state request for tab {target_tab_id}: {e}", exc_info=True)
            raise RuntimeError(f"Unexpected error getting browser state for tab {target_tab_id}: {e}") from e # Chain the exception

    async def execute_action(self, action_name: str, params: Dict[str, Any], tab_id: Optional[int] = None, timeout: Optional[float] = None) -> Dict[str, Any]:
        """Sends an action to the extension and waits for a result."""
        request_id = self._get_request_id()
        logger.info(f"ExtensionInterface (Agent request {request_id}): execute_action called. Action: {action_name}, Params: {params}, Target Tab ID: {tab_id if tab_id is not None else 'current active'}, Timeout: {timeout if timeout is not None else 'default'}")
        current_active_connection = self.active_connection_object
        if not current_active_connection or not current_active_connection.websocket:
            logger.error(f"Execute_action ({action_name}): No active WebSocket connection.")
            return {"success": False, "error": "No active WebSocket connection to send action."}
        logger.info(f"Requesting execution of action '{action_name}' with params: {params}")
        
        target_tab_id = tab_id if tab_id is not None else self._active_tab_id

        if target_tab_id is None:
            # Decide behavior: raise error, return failure, or attempt on active tab
            logger.error(f"execute_action called for '{action_name}' but no target_tab_id or active tab ID is set.")
            return {"success": False, "error": "No target or active tab ID specified for action."}

        # --- Call the waiting method before sending the request ---
        # Skip content script check for navigate actions - the extension will handle blank tabs directly
        if action_name != "navigate":
            try:
                # Use a reasonable timeout, potentially action-specific or default
                wait_timeout = timeout if timeout is not None else DEFAULT_REQUEST_TIMEOUT # Use same timeout for wait? Or separate?
                await self._wait_for_content_script_ready(target_tab_id, timeout_seconds=wait_timeout)
            except asyncio.TimeoutError as e:
                logger.error(f"Content script in tab {target_tab_id} not ready before sending action '{action_name}': {e}")
                return {"success": False, "error": f"Content script in tab {target_tab_id} not ready before action: {e}"}
            except Exception as e:
                logger.error(f"Unexpected error while waiting for content script ready for tab {target_tab_id} before action '{action_name}': {e}", exc_info=True)
                return {"success": False, "error": f"Unexpected error waiting for content script ready: {e}"}

        request_payload = {
            "action_name": action_name,
            "params": params
        }

        try:
            response_data_model = await self._send_request(
                action="execute_action", # This is the 'type' of message for the extension router
                data=request_payload,
                timeout=timeout if timeout is not None else DEFAULT_REQUEST_TIMEOUT
            )

            if response_data_model:
                # The response_data_model is an instance of ResponseData
                # It has fields like .success, .error, .url, .title directly.
                # It does NOT have a nested .data field.
                if response_data_model.success:
                    logger.info(f"Action '{action_name}' executed successfully by extension for client {self.active_connection_object.client_id}. Response success: {response_data_model.success}")
                    # For 'navigate', 'extract_content', etc., the primary result info is in success/error and potentially other direct fields.
                    # We want to pass back any relevant data fields from ResponseData, excluding 'success' and 'error' which are handled separately.
                    # Also exclude 'id' and 'type' as those are part of the outer message, not the action result itself.
                    action_result_data = response_data_model.model_dump(exclude={"success", "error", "id", "type"}, exclude_unset=True)

                    # RETURN A DICTIONARY, NOT AN ACTIONRESULT MODEL INSTANCE
                    return {
                        "success": True,
                        "data": action_result_data if action_result_data else {}, # Ensure 'data' key exists
                        "error": None
                    }
                else:
                    error_msg_from_ext = response_data_model.error or f"Action '{action_name}' failed in extension (no specific error message)."
                    logger.error(f"Action '{action_name}' failed for client {self.active_connection_object.client_id}: {error_msg_from_ext}")
                    # RETURN A DICTIONARY
                    return {
                        "success": False,
                        "data": None,
                        "error": error_msg_from_ext
                    }
            else:
                # _send_request itself might return None on timeout or critical failure before parsing ResponseData
                logger.error(f"No response from extension for action '{action_name}'.")
                return {"success": False, "data": None, "error": f"No response from extension for action '{action_name}'."}
        except RuntimeError as e_runtime: # From _send_request if future.set_exception by extension error
            logger.error(f"RuntimeError during execute_action '{action_name}': {e_runtime}")
            return {"success": False, "data": None, "error": str(e_runtime)}
        except Exception as e_main:
            logger.error(f"Unexpected error in execute_action '{action_name}': {e_main}", exc_info=True)
            return {"success": False, "data": None, "error": f"Unexpected error: {str(e_main)}"}

    async def start_server(self) -> None:
        """Starts the WebSocket server and listens for incoming connections."""
        if self._server is not None:
            logger.warning("Server is already running.")
            return
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}...")
        try:
            self._server = await websockets.serve( 
                self._handle_connection, 
                self.host, 
                self.port,
                max_size=2**24,  
                ping_interval=20,
                ping_timeout=20,
                reuse_address=True  # Explicitly enable SO_REUSEADDR
            )
            logger.info(f"WebSocket server listening on ws://{self.host}:{self.port}")
        except OSError as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred with the WebSocket server: {e}", exc_info=True)
            raise

    async def _handle_connection(self, websocket: ServerConnection, path: Optional[str] = None) -> None:
        """
        Handles a new client connection, including message processing and cleanup.
        The 'path' argument is provided by 'websockets.serve' but not used here.
        """
        logger.info(f"_handle_connection: Attempting to accept new connection from {websocket.remote_address}. Path: {path if path else 'N/A'}") # ENTRY LOG
        client_id = str(uuid.uuid4())
        
        # Log when the handler task itself starts
        logger.critical(f"!!! _handle_connection TASK STARTED for client: {client_id}. Websocket state: {websocket.state.name} !!!")

        # Store connection information
        # Critical to store the task so it can be cancelled if needed.
        # Make sure ConnectionInfo is defined and handles asyncio.Task correctly.
        connection_info = ConnectionInfo(client_id=client_id, websocket=websocket, handler_task=asyncio.current_task())
        
        self._connections[client_id] = connection_info
        logger.info(f"Client {client_id} (from {websocket.remote_address}) added to self._connections. Total connections: {len(self._connections)}")
        
        if self._active_connection_id is None:
            self._active_connection_id = client_id
            logger.info(f"Set {client_id} as the active connection. self._active_connection_id = {self._active_connection_id}")
        else:
            logger.info(f"A connection is already active ({self._active_connection_id}). New client {client_id} is connected but not primary.")

        logger.critical(f"!!! _handle_connection: Client {client_id} connected. Active_connection_id: {self._active_connection_id}. About to enter message loop. Websocket state: {websocket.state.name}. !!!")

        try:
            # Log before entering the message processing loop
            logger.critical(f"!!! _handle_connection: Client {client_id} processed initial setup. ABOUT TO ENTER explicit 'await websocket.recv()' message loop. Websocket state: {websocket.state.name}. !!!")
            while True: # Explicit loop
                try:
                    await asyncio.sleep(0.05) # ADDED: Small yield in each iteration before recv()
                    message_json_str = await websocket.recv() 
                    if message_json_str is None: # Should not happen unless connection closed abruptly without error
                        logger.warning(f"Received None from websocket.recv() for client {client_id}. Breaking message loop.")
                        break
                    # _process_message expects client_id and the raw message_json (which should be a string here)
                    await self._process_message(client_id, message_json_str) 
                except websockets.exceptions.ConnectionClosedOK:
                    # Re-raise to be handled by outer exception handler for proper "graceful disconnect" logging
                    raise
                except websockets.exceptions.ConnectionClosedError as e: # Catch specific closure errors here
                    logger.info(f"Connection closed for client {client_id} during recv: {e.code} {e.reason}")
                    break # Exit the while True loop
                except Exception as e_recv: # Catch other potential errors during recv or _process_message
                    logger.error(f"Error during websocket.recv() or _process_message for client {client_id}: {e_recv}", exc_info=True)
                    # Decide if to break or continue based on error type, for now, let's break on most errors
                    break
        except websockets.exceptions.ConnectionClosedOK:
            logger.info(f"Client {client_id} disconnected gracefully.")
        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"Client {client_id} connection closed with error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in connection handler for {client_id}: {e}", exc_info=True)
        finally:
            await self._remove_client(client_id)

    async def _remove_client(self, client_id: str) -> None:
        """Remove a client and update active connection state."""
        if client_id in self._connections:
            del self._connections[client_id]
            logger.info(f"Removed client {client_id} from active connections.")
        
        if self._active_connection_id == client_id:
            self._active_connection_id = None
            logger.info(f"Cleared active connection (was {client_id}).")
            if self._connections:
                new_active_id = next(iter(self._connections.keys()))
                self._active_connection_id = new_active_id
                logger.info(f"Set new active connection to: {new_active_id}")

    async def _process_message(self, client_id: str, message_json_str: str) -> None:
        """Processes a deserialized message received from a client."""
        logger.critical(f"!!! _process_message RAW from {client_id}: {message_json_str} !!!")

        try:
            # Ensure message_json_str is parsed from JSON string to dict first
            parsed_message_dict = json.loads(message_json_str)
            message = Message[Dict[str, Any]].model_validate(parsed_message_dict)
        except ValidationError as e:
            logger.error(f"Invalid message structure from {client_id}: {e}. Message: {message_json_str}")
            return # Or send an error response to the client
        
        logger.info(f"_process_message PARSED from {client_id} - Type: {message.type}, ID: {message.id}")

        if message.type == "response":
            request_id = message.id
            if request_id in self._pending_requests:
                future = self._pending_requests.pop(request_id)
                try:
                    response_data = ResponseData.model_validate(message.data)
                    if not response_data.success:
                        logger.error(f"Extension error for request ID {request_id}: {response_data.error}")
                        future.set_exception(RuntimeError(f"Extension error for request ID {request_id}: {response_data.error}"))
                    else:
                        future.set_result(response_data) 
                except ValidationError as e:
                    logger.error(f"Response data validation error for request ID {request_id}: {e}. Data: {message.data}")
                    future.set_exception(RuntimeError(f"Response data validation error: {e}"))
                except Exception as e: 
                    logger.error(f"Unexpected error processing response for request ID {request_id}: {e}", exc_info=True)
                    future.set_exception(RuntimeError(f"Unexpected error processing response: {e}"))
            else:
                logger.warning(f"Received response for unknown or timed-out request ID {request_id} from {client_id}.")
        elif message.type == "extension_event": 
            event_payload = message.data
            event_name = event_payload.get("event_name", "unknown_event")
            logger.info(f"Received event '{event_name}' from {client_id}: {event_payload}")
            if event_name == "page_fully_loaded_and_ready":
                logger.info(f"'{event_name}' event received from {client_id}. Triggering state fetch.")
                # Update active tab ID when a page is fully loaded
                if "tabId" in event_payload and isinstance(event_payload["tabId"], int):
                    self._active_tab_id = event_payload["tabId"]
                    logger.info(f"Active tab ID updated to: {self._active_tab_id} from '{event_name}' event.")
                    await self._set_active_tab_id(self._active_tab_id, event_payload.get("url"))
                asyncio.create_task(self._fetch_and_save_initial_state(client_id, event_payload))
            elif event_name == "tab_activated": # Example of another event that could update active_tab_id
                if "tabId" in event_payload and isinstance(event_payload["tabId"], int):
                    await self._set_active_tab_id(event_payload["tabId"], event_payload.get("url"))
            elif event_name == "tab_activated_on_query":
                logger.info(f"'{event_name}' event received from {client_id}. Setting active tab.")
                if "tabId" in event_payload and isinstance(event_payload["tabId"], int):
                    await self._set_active_tab_id(event_payload["tabId"], event_payload.get("url"))
            elif event_name == "content_script_ready_ack": 
                logger.info(f"Received content_script_ready_ack: {event_payload}")
            elif event_name == "content_script_ready": # Handle the content_script_ready event
                tab_id = event_payload.get("tabId")
                if isinstance(tab_id, int):
                    timestamp = asyncio.get_event_loop().time()
                    self._content_script_ready_tabs[tab_id] = timestamp
                    logger.critical(f"!!! CONTENT SCRIPT READY: Tab {tab_id} marked as ready at {timestamp} !!!")
                    logger.critical(f"!!! READY TABS NOW: {list(self._content_script_ready_tabs.keys())} !!!")
                    # If we had pending futures waiting for this tab, we could potentially notify them here,
                    # but the _wait_for_content_script_ready method will handle the waiting logic.
                else:
                    logger.warning(f"Received content_script_ready event with invalid or missing tabId: {event_payload}.")
            elif event_name == "tab_removed": # Handle the tab_removed event for cleanup
                tab_id = event_payload.get("tabId")
                if isinstance(tab_id, int) and tab_id in self._content_script_ready_tabs:
                    del self._content_script_ready_tabs[tab_id]
                    logger.info(f"Removed tab {tab_id} from ready tracking due to tab_removed event.")
            elif event_name == "user_task_submitted": # Handle user task submission from popup
                task = event_payload.get("task")
                context = event_payload.get("context", {})
                tab_id = event_payload.get("tabId")
                logger.info(f"User submitted task from extension popup: '{task}' (Tab ID: {tab_id})")
                
                # Update active tab if provided
                if isinstance(tab_id, int):
                    self._active_tab_id = tab_id
                    logger.info(f"Updated active tab ID to {tab_id} from user task submission")
                
                # Trigger agent processing of the task
                if self._llm and AGENT_IMPORTS_AVAILABLE:
                    logger.info(f"Task details - Task: {task}, Context: {context}, Tab: {tab_id}")
                    # Create async task for agent processing
                    asyncio.create_task(self.process_user_task(task, context, tab_id))
                else:
                    logger.warning("Cannot process task - agent functionality not available")
            # Add other event handling as needed
        else:
            logger.warning(f"Received unhandled message type '{message.type}' from {client_id}.")

    def _get_request_id(self) -> int:
        """Generates a unique, incrementing message ID for requests."""
        self._message_id_counter += 1
        return self._message_id_counter

    async def _send_request(self, action: str, data: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None) -> Optional[ResponseData]:
        """
        Sends a request to the active Chrome extension and waits for a response.

        Args:
            action: The action to be performed by the extension.
            data: Optional data payload for the action.
            timeout: Optional timeout in seconds. Uses DEFAULT_REQUEST_TIMEOUT if None.

        Returns:
            The 'data' part of the response from the extension as a dictionary.
        
        Raises:
            RuntimeError: If no active connection, timed out, or an extension error occurred.
        """
        if self._active_connection_id is None or self._active_connection_id not in self._connections:
            logger.error(f"Cannot send request '{action}': No active and valid connection.")
            raise RuntimeError("No active extension connection.")
        conn_info = self._connections[self._active_connection_id]
        request_id = self._get_request_id()
        message_payload = {
            "id": request_id,
            "type": action, 
            "data": data if data is not None else {}
        }
        future: asyncio.Future[ResponseData] = asyncio.Future()
        self._pending_requests[request_id] = future
        try:
            logger.debug(f"Sending {action} request (ID: {request_id}) to {self._active_connection_id} with payload: {message_payload}")
            await conn_info.websocket.send(json.dumps(message_payload))
            actual_timeout = timeout if timeout is not None else DEFAULT_REQUEST_TIMEOUT
            response_data_obj = await asyncio.wait_for(future, timeout=actual_timeout)
            return response_data_obj
        except asyncio.TimeoutError:
            logger.error(f"Request {action} (ID: {request_id}) to {self._active_connection_id} timed out after {actual_timeout}s.")
            if request_id in self._pending_requests: 
                self._pending_requests.pop(request_id)
            raise RuntimeError(f"Request '{action}' (ID: {request_id}) timed out.")
        except websockets.exceptions.ConnectionClosed:
            logger.error(f"Connection to {self._active_connection_id} closed while sending request {action} (ID: {request_id}).")
            if request_id in self._pending_requests:
                self._pending_requests.pop(request_id)
            raise RuntimeError(f"Connection closed during request '{action}' (ID: {request_id}).")
        except RuntimeError as e: 
            logger.error(f"Error sending/processing {action} request (ID: {request_id}): {e}")
            if request_id in self._pending_requests and not self._pending_requests[request_id].done():
                 self._pending_requests.pop(request_id).cancel()
            raise 
        except Exception as e:
            logger.error(f"Unexpected error during _send_request for {action} (ID: {request_id}): {e}", exc_info=True)
            if request_id in self._pending_requests:
                self._pending_requests.pop(request_id)
            raise RuntimeError(f"Unexpected error during request '{action}' (ID: {request_id}): {e}")

    async def close(self) -> None:
        """Closes all client connections and shuts down the WebSocket server."""
        logger.info(f"Closing ExtensionInterface. Number of active connections: {len(self._connections)}")
        
        # Close all active client connections
        # Create a list of connection objects to iterate over, as closing them modifies the dictionary
        active_connections_to_close = list(self._connections.values())
        for conn_info in active_connections_to_close:
            try:
                logger.info(f"Closing client connection: {conn_info.client_id}")
                await conn_info.websocket.close(code=1000, reason="Server shutting down")
                logger.info(f"Successfully sent close frame to client: {conn_info.client_id}")
                if conn_info.handler_task and not conn_info.handler_task.done():
                    conn_info.handler_task.cancel()
                    try:
                        await conn_info.handler_task
                    except asyncio.CancelledError:
                        logger.info(f"Handler task for {conn_info.client_id} cancelled as expected.")
                    except Exception as e_task_close:
                        logger.error(f"Error awaiting cancelled handler task for {conn_info.client_id}: {e_task_close}")

            except websockets.exceptions.ConnectionClosed:
                logger.info(f"Client connection {conn_info.client_id} already closed when attempting to send close frame.")
            except Exception as e:
                logger.error(f"Error closing client connection {conn_info.client_id}: {e}", exc_info=True)
        
        self._connections.clear()
        self._active_connection_id = None
        logger.info("All client connections processed and cleared.")

        if self._server:
            logger.info("Shutting down WebSocket server...")
            try:
                self._server.close() # Request the server to close
                logger.info("Server close() called. Waiting for it to shut down...")
                # Wait for the server to close, but with a timeout to prevent indefinite hanging
                await asyncio.wait_for(self._server.wait_closed(), timeout=5.0)
                logger.info("WebSocket server successfully shut down.")
            except asyncio.TimeoutError:
                logger.warning("Timeout waiting for WebSocket server to shut down. It might not have closed cleanly.")
            except Exception as e:
                logger.error(f"Error shutting down WebSocket server: {e}", exc_info=True)
            finally:
                self._server = None # Ensure server attribute is reset
        else:
            logger.info("No active WebSocket server to shut down.")
        logger.info("ExtensionInterface close() method finished.")

    async def get_active_tab_id(self) -> Optional[int]:
        """Returns the currently known active tab ID."""
        # This method provides immediate access without waiting.
        # For waiting, use wait_for_active_tab.
        if self._active_tab_id is None:
            logger.warning("Active tab ID is not yet known. Has an extension event (e.g., page_fully_loaded_and_ready or tab_activated) been received?")
        return self._active_tab_id

    async def wait_for_active_tab(self, timeout_seconds: float = 5.0) -> int:
        """
        Waits until _active_tab_id is set by an incoming extension event.

        Args:
            timeout_seconds: Maximum time to wait.

        Returns:
            The active tab ID.

        Raises:
            RuntimeError: If the active tab ID is not set within the timeout.
        """
        start_time = asyncio.get_event_loop().time()
        logger.info(f"Waiting for active tab ID to be set (timeout: {timeout_seconds}s). Current value: {self._active_tab_id}")
        loop_count = 0
        while True:
            loop_count += 1
            logger.debug(f"wait_for_active_tab loop {loop_count}: Checking self._active_tab_id (current: {self._active_tab_id})")
            if self._active_tab_id is not None:
                logger.info(f"Active tab ID is set: {self._active_tab_id} (found in loop {loop_count})")
                return self._active_tab_id

            if (asyncio.get_event_loop().time() - start_time) >= timeout_seconds:
                logger.error(f"Timeout waiting for active tab ID after {timeout_seconds}s. self._active_tab_id is still {self._active_tab_id} after {loop_count} loops.")
                raise RuntimeError(f"Timeout waiting for active tab ID after {timeout_seconds}s. Extension did not report an active tab.")
            
            await asyncio.sleep(0.1) # Yield control

    async def _set_active_tab_id(self, tab_id: int, url: Optional[str] = None) -> None:
        """Sets the active tab ID and logs the change."""
        logger.critical(f"!!! _set_active_tab_id CALLED with tab_id: {tab_id}, url: {url} !!!")
        self._active_tab_id = tab_id
        logger.critical(f"!!! _set_active_tab_id: self._active_tab_id is NOW {self._active_tab_id} !!!")
        # Create an event if one doesn't exist or clear the existing one
        # This event can be used by other parts of the system to wait for tab info.
        # logger.info(f"Active tab changed/set to ID: {tab_id}, URL: {url if url else 'N/A'}")
        # logger.info(f"Active tab reaffirmed: {tab_id}, URL: {url if url else 'N/A'}") # Can be noisy
        # pass # No need to log if not changing, the critical log above is enough

    def _get_best_ready_tab_id(self) -> Optional[int]:
        """
        Returns the best tab ID to use for get_state, prioritizing ready tabs over active tab.
        """
        current_time = asyncio.get_event_loop().time()
        logger.critical(f"!!! _get_best_ready_tab_id CALLED at {current_time} !!!")
        logger.critical(f"!!! CURRENT READY TABS: {dict(self._content_script_ready_tabs)} !!!")
        logger.critical(f"!!! CURRENT ACTIVE TAB: {self._active_tab_id} !!!")
        
        # If we have ready tabs, prefer the most recently ready one
        if self._content_script_ready_tabs:
            # Find the most recently ready tab (highest timestamp)
            best_tab_id = max(self._content_script_ready_tabs.keys(), 
                             key=lambda tid: self._content_script_ready_tabs[tid])
            ready_time = self._content_script_ready_tabs[best_tab_id]
            logger.critical(f"!!! USING READY TAB {best_tab_id} for get_state (ready at {ready_time}, {current_time - ready_time:.1f}s ago) !!!")
            logger.critical(f"!!! ALL READY TABS: {list(self._content_script_ready_tabs.keys())} !!!")
            return best_tab_id
        
        # Fallback to active tab if no ready tabs
        if self._active_tab_id is not None:
            logger.critical(f"!!! NO READY TABS - FALLING BACK to active tab {self._active_tab_id} for get_state !!!")
            return self._active_tab_id
        
        # No tabs available
        logger.critical("!!! NO READY TABS OR ACTIVE TAB available for get_state !!!")
        return None

    async def _wait_for_content_script_ready(self, tab_id: int, timeout_seconds: float) -> None:
        """
        Waits until the content script for the specified tab ID is marked as ready.

        Args:
            tab_id: The ID of the tab to wait for.
            timeout_seconds: Maximum time to wait.

        Raises:
            asyncio.TimeoutError: If the tab does not become ready within the timeout.
        """
        start_wait_time = asyncio.get_event_loop().time()
        logger.debug(f"_wait_for_content_script_ready CALLED for tabId: {tab_id}, timeout: {timeout_seconds}s.")

        # SIMPLIFIED: If tab is already ready, return immediately (no timestamp checking needed)
        if tab_id in self._content_script_ready_tabs:
            ready_timestamp = self._content_script_ready_tabs[tab_id]
            logger.debug(f"Content script for tab {tab_id} already marked ready at {ready_timestamp}. Returning immediately.")
            return

        # If not immediately ready, start polling
        polling_interval = 0.1 # Poll every 100ms
        elapsed_time = 0

        while elapsed_time < timeout_seconds:
            # Check again inside the loop - simple check
            if tab_id in self._content_script_ready_tabs:
                ready_timestamp = self._content_script_ready_tabs[tab_id]
                logger.debug(f"Content script for tab {tab_id} became ready during wait at {ready_timestamp}.")
                return

            await asyncio.sleep(polling_interval)
            elapsed_time += polling_interval

        # If loop finishes without returning, it timed out
        logger.error(f"Timeout waiting for content script in tab {tab_id} to signal ready after {timeout_seconds}s.")
        raise asyncio.TimeoutError(f"Timeout waiting for content script in tab {tab_id} to signal ready.")

    async def process_user_task(self, task: str, context: dict, tab_id: int) -> None:
        """
        Process a user task through the agent system.
        
        Args:
            task: The task description from the user
            context: Additional context (URL, title, etc.)
            tab_id: The tab ID where the task should be executed
        """
        if not self._llm:
            logger.error("Cannot process task - no LLM configured")
            return
            
        if not AGENT_IMPORTS_AVAILABLE:
            logger.error("Cannot process task - agent imports not available")
            return
        
        session_id = f"tab_{tab_id}_{uuid.uuid4().hex[:8]}"
        
        try:
            logger.info(f"Starting agent session {session_id} for task: {task}")
            
            # Create agent with the configured LLM
            agent = Agent(
                task=task,
                llm=self._llm,
                extension_interface=self,
                settings=AgentSettings(
                    max_steps_per_run=15,
                    max_failures=3
                )
            )
            
            # Store agent in active sessions
            self._active_agents[session_id] = agent
            
            # Run the agent
            history = await agent.run()
            
            # Log results
            if history and len(history.history) > 0:
                logger.info(f"Agent session {session_id} completed with {len(history.history)} steps")
                # TODO: Send results back to extension popup
            else:
                logger.warning(f"Agent session {session_id} completed with no history")
                
        except Exception as e:
            logger.error(f"Error during agent task processing in session {session_id}: {e}", exc_info=True)
        finally:
            # Clean up session
            if session_id in self._active_agents:
                del self._active_agents[session_id]
                logger.info(f"Cleaned up agent session {session_id}")

async def main():
    """Main function to run the WebSocket server."""
    # Configure basic logging if no handlers are configured
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s'
        )
    
    extension_interface = ExtensionInterface(host="localhost", port=8765)
    try:
        await extension_interface.start_server()
    except KeyboardInterrupt:
        logger.info("Server shutting down due to KeyboardInterrupt...")
    except Exception as e:
        logger.error(f"Server failed to run: {e}", exc_info=True)
    finally:
        logger.info("Performing final cleanup...")
        await extension_interface.close()
        logger.info("Server shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user (KeyboardInterrupt in asyncio.run).")
    except Exception as e:
        logger.critical(f"Unhandled exception in __main__: {e}", exc_info=True) 