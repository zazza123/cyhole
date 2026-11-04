from typing import Any

from ..core.exception import CyholeException


class HeliusException(CyholeException):
    """Base exception for Helius interaction."""
    pass


class HeliusAccountCountError(HeliusException):
    """
    The list of addresses given to `getMultipleAccounts` is empty or longer than the
    100 accounts the RPC method reads in one call.
    """
    pass


class HeliusRPCError(HeliusException):
    """
    A standard JSON-RPC call answered with an `error` object in place of a `result`.

    The HTTP status of such an answer is 200, so it reaches the library as a valid
    response. Reading it as the response model would fail on the missing `result` and
    hide the cause, so the error is raised first.

    Attributes:
        code: JSON-RPC error code, e.g. `-32602` for invalid params.
        message: error message of the RPC node.
        data: additional error data, when the node gives some.
    """
    def __init__(self, code: int, message: str, data: Any = None) -> None:
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"JSON-RPC error {code}: {message}")


class HeliusWebSocketError(HeliusException):
    """
    The WebSocket client failed: the connection could not be opened, a request got
    no answer in time, or the client stopped on an unexpected error.

    The message never contains the API key: the URL in aiohttp's errors is masked,
    and the aiohttp error is not chained to it.
    """
    pass


class HeliusWebSocketTimeout(HeliusWebSocketError):
    """
    A subscribe or unsubscribe request got no answer within the client's
    `request_timeout`. The connection may still be open.
    """
    pass


class HeliusWebSocketClosed(HeliusWebSocketError):
    """
    The WebSocket connection is closed: the client was closed, or the connection
    dropped and the client does not reconnect.

    Raised by a pending request when the connection drops before its answer, and
    by the iteration of a client built with `reconnect = False` when the connection
    drops.
    """
    pass
