from typing import Type, Any
from enum import Enum

class PycryptException(Exception):
    """
        General exception of pycrypt library
    """
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
    
class RequestTypeNotSupported(PycryptException):
    pass

class AuthorizationAPIKeyError(PycryptException):
    pass

class MissingAPIKeyError(PycryptException):
    pass

class ParamUnknownError(PycryptException):
    """
        General error used to manage a wrong input API param.
    """
    def __init__(self, param_value: Any, param_enum: Type[Enum]):
        description = f"param '{str(param_value)}' not supported. \nAdmissible values: {param_enum.__members__}"
        super().__init__(description)