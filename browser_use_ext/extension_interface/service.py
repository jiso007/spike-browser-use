from typing import Dict, Any, Optional, TypeVar
import logging
# from browser.context import BrowserContext, BrowserContextConfig # Incorrect path
from ..browser.context import BrowserContext, BrowserContextConfig # Corrected relative import path
# from .response_data import ResponseData # REMOVE THIS - will be imported from .models
# from .models import Message, ConnectionInfo # Old import, will be replaced
from .models import BaseMessage, Message, ResponseData, ConnectionInfo # CORRECTED consolidated import
import json
import os
from datetime import datetime
import asyncio
import inspect # ADDED FOR DEBUGGING
import re 
import uuid
from pydantic import ValidationError # Ensure ValidationError is imported
import websockets # type: ignore
from websockets.asyncio.server import ServerConnection # CORRECTED WEBSOCKET TYPE IMPORT

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# Maximum time (in seconds) to wait for a response from the extension
DEFAULT_REQUEST_TIMEOUT = 10  # seconds


class ExtensionInterface:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self._server: Optional[websockets.server.WebSocketServer] = None
        self._connections: Dict[str, ConnectionInfo] = {}
        self._active_connection_id: Optional[str] = None
        self._message_id_counter: int = 0
        self._pending_requests: Dict[int, asyncio.Future] = {}
        # self._initial_state_fetched_for_event = False # Flag seems unused, can be removed if truly so
        self._filename_sanitize_re = re.compile(r'[^a-zA-Z0-9_.-]+')

    def _sanitize_filename_component(self, component: str) -> str:
        """Sanitizes a string component to be safe for use in a filename."""
        component = component.replace("http://", "").replace("https://", "").replace("www.", "")
        sanitized = self._filename_sanitize_re.sub('_', component)
        return sanitized[:50]

    async def _fetch_and_save_initial_state(self, client_id: str, event_data: Dict[str, Any]) -> None:
        """Fetches the browser state and saves it to a JSON file, triggered by an event."""
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

    async def get_state(self, include_screenshot: bool = False, tab_id: Optional[int] = None) -> ResponseData:
        """
        Requests the current browser state from the connected Chrome extension.

        Args:
            include_screenshot: Whether to include a screenshot in the state.
            tab_id: Optional specific tab ID to target for page-specific data.

        Returns:
            A ResponseData object containing the success status, data (BrowserStateModelData),
            or an error message.
        """
        logger.info(f"Requesting browser state (screenshot: {include_screenshot}, target_tab_id: {tab_id})...")
        payload_data = {"includeScreenshot": include_screenshot}
        if tab_id is not None:
            payload_data["tabId"] = tab_id
        response_dict = await self._send_request(
            action="get_state",
            data=payload_data,
            timeout=45 
        )
        return ResponseData.model_validate(response_dict)

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
                ping_timeout=20
            )
            logger.info(f"WebSocket server listening on ws://{self.host}:{self.port}")
            await self._server.wait_closed()
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
        client_id = str(uuid.uuid4())
        connection_info = ConnectionInfo(client_id=client_id, websocket=websocket, handler_task=asyncio.current_task())
        self._connections[client_id] = connection_info
        logger.info(f"Client {client_id} connected from {websocket.remote_address}. Path: {path if path else 'N/A'}")
        if self._active_connection_id is None:
            self._active_connection_id = client_id
            logger.info(f"Set {client_id} as the active connection.")
        try:
            async for message_str in websocket:
                if isinstance(message_str, str):
                    try:
                        raw_message = json.loads(message_str)
                        await self._process_message(client_id, raw_message)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to decode JSON from {client_id}: {message_str}")
                    except Exception as e:
                        logger.error(f"Error processing message from {client_id}: {e}", exc_info=True)
                else:
                    logger.warning(f"Received non-text message from {client_id}, ignoring.")
        except websockets.exceptions.ConnectionClosedOK:
            logger.info(f"Client {client_id} disconnected gracefully.")
        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"Client {client_id} connection closed with error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in connection handler for {client_id}: {e}", exc_info=True)
        finally:
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

    async def _process_message(self, client_id: str, raw_message: Dict[str, Any]) -> None:
        """Processes a deserialized message received from a client."""
        try:
            base_msg = Message[Dict[str, Any]].model_validate(raw_message)
        except ValidationError as e:
            logger.error(f"Invalid message structure from {client_id}: {e}. Message: {raw_message}")
            return
        if base_msg.type == "response":
            request_id = base_msg.id
            if request_id in self._pending_requests:
                future = self._pending_requests.pop(request_id)
                try:
                    response_data = ResponseData.model_validate(raw_message.get("data", {}))
                    if not response_data.success:
                        logger.error(f"Extension error for request ID {request_id}: {response_data.error}")
                        future.set_exception(RuntimeError(f"Extension error for request ID {request_id}: {response_data.error}"))
                    else:
                        future.set_result(response_data) 
                except ValidationError as e:
                    logger.error(f"Response data validation error for request ID {request_id}: {e}. Data: {raw_message.get('data')}")
                    future.set_exception(RuntimeError(f"Response data validation error: {e}"))
                except Exception as e: 
                    logger.error(f"Unexpected error processing response for request ID {request_id}: {e}", exc_info=True)
                    future.set_exception(RuntimeError(f"Unexpected error processing response: {e}"))
            else:
                logger.warning(f"Received response for unknown or timed-out request ID {request_id} from {client_id}.")
        elif base_msg.type == "extension_event": 
            event_payload = raw_message.get("data", {})
            event_name = event_payload.get("event_name", "unknown_event")
            logger.info(f"Received event '{event_name}' from {client_id}: {event_payload}")
            if event_name == "page_fully_loaded_and_ready":
                logger.info(f"'{event_name}' event received from {client_id}. Triggering state fetch.")
                asyncio.create_task(self._fetch_and_save_initial_state(client_id, event_payload))
            elif event_name == "content_script_ready_ack": 
                logger.info(f"Received content_script_ready_ack: {event_payload}")
        else:
            logger.warning(f"Received unhandled message type '{base_msg.type}' from {client_id}.")

    def _get_next_message_id(self) -> int:
        """Generates a unique, incrementing message ID."""
        self._message_id_counter += 1
        return self._message_id_counter

    async def _send_request(self, action: str, data: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None) -> Dict[str, Any]:
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
        request_id = self._get_next_message_id()
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
            return response_data_obj.model_dump()
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
        """Closes the WebSocket server and all active connections."""
        logger.info("Closing WebSocket server and all connections...")
        if self._server:
            self._server.close()
            logger.info("WebSocket server has been closed.")
            self._server = None
        active_connections = list(self._connections.values())
        for conn_info in active_connections:
            try:
                logger.info(f"Closing connection to client {conn_info.client_id}...")
                await conn_info.websocket.close(code=1000, reason="Server shutting down")
                if conn_info.handler_task and not conn_info.handler_task.done():
                    conn_info.handler_task.cancel()
                    try:
                        await conn_info.handler_task 
                    except asyncio.CancelledError:
                        logger.info(f"Message handler task for {conn_info.client_id} cancelled.")
            except websockets.exceptions.ConnectionClosed:
                logger.info(f"Connection to {conn_info.client_id} was already closed.")
            except Exception as e:
                logger.error(f"Error closing connection to {conn_info.client_id}: {e}", exc_info=True)
        self._connections.clear()
        self._active_connection_id = None
        for request_id, future in self._pending_requests.items():
            if not future.done():
                future.cancel(f"Server shutting down; request {request_id} cancelled.")
        self._pending_requests.clear()
        logger.info("All client connections closed and server resources released.")

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