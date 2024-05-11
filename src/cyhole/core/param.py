from typing import Any
from enum import Enum

from ..core.exception import ParamUnknownError

class CyholeParam(Enum):
    """
        Generic Enum representing a param for an API endpoint
    """
    @classmethod
    def check(cls, value: Any) -> None:
        """
            Function used to check the consistency of an input API 
            parameter (param) belonging to the value list (enum.Enum).

            The function will raise a ParamUnknownError if the value
            does not belong to the Enum.

            Parameters:
                value: value to check.
        """
        if value not in cls:
            raise ParamUnknownError(value, cls)
        return

class RequestType(CyholeParam):
    """
        Enum class for RequestType
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"