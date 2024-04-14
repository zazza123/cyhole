from enum import Enum

class RequestType(Enum):
    """
        Enum class for RequestType
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"