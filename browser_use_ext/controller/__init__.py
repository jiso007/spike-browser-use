# This file makes the controller directory a Python package. 

from .service import Controller
# from .registry.views import ActionDefinition # If you want to expose it directly

__all__ = [
    "Controller",
] 