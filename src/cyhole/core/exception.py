from typing import Type, Any
from enum import Enum

class CyholeException(Exception):
    """
        General exception of Cyhole library
    """
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description

class RequestTypeNotSupported(CyholeException):
    pass

class AuthorizationAPIKeyError(CyholeException):
    pass

class MissingAPIKeyError(CyholeException):
    pass

class ParamUnknownError(CyholeException):
    """
        General error used to manage a wrong input API param.
    """
    def __init__(self, param_value: Any, param_enum: Type[Enum]):
        description = f"param '{str(param_value)}' not supported in {param_enum.__name__} enum class. \nAdmissible values: {[(param.name, param.value) for param in param_enum]}"
        super().__init__(description)