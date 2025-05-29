class LLMException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f'Error {status_code}: {message}') 

class AgentException(Exception):
    """Base class for agent-related exceptions."""
    pass

class InvalidActionError(AgentException):
    """Raised when an invalid action is specified or parsed."""
    pass

class ActionFailedException(AgentException):
    """Raised when an action fails to execute as expected."""
    pass 