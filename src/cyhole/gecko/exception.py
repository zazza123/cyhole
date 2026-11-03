import math

from requests import HTTPError, Response

from ..core.exception import CyholeException, CyholeRateLimitError

GECKO_PUBLIC_RATE_WINDOW_S = 60.0
"""
Seconds a client blocked by the public API waits before its calls are let through again.

The public API counts each client's successful calls over a rolling minute; a client over
the limit is answered 429 with `Retry-After: 0` until its last minute of calls has passed.
"""


class GeckoException(CyholeException):
    """Base exception raised by the Gecko interaction."""
    pass


class GeckoAddressCountError(GeckoException):
    """Exception raised when a multi-address endpoint receives too few or too many addresses."""
    pass


class GeckoRateLimitError(GeckoException, CyholeRateLimitError, HTTPError):
    """
        GeckoTerminal answered 429: the client's rate limit was hit.

        It is also a `requests.HTTPError` carrying the answer, so code that catches the
        HTTP error keeps working, and a
        [`CyholeRateLimitError`][cyhole.core.exception.CyholeRateLimitError].

        Attributes:
            status_code: the HTTP status of the answer, always 429.
            retry_after: seconds to wait before calling again. It is the answer's
                `Retry-After` when that is a positive finite number of seconds; otherwise
                (the public API always sends 0, which is not true; an HTTP date is not
                read) it is [`GECKO_PUBLIC_RATE_WINDOW_S`][cyhole.gecko.exception.GECKO_PUBLIC_RATE_WINDOW_S].
    """

    status_code: int = 429

    def __init__(self, message: str, response: Response | None = None, retry_after: float = GECKO_PUBLIC_RATE_WINDOW_S) -> None:
        """
            Parameters:
                message: the error message, as the HTTP error's.
                response: the 429 answer, when there is one.
                retry_after: seconds to wait before calling again.
        """
        # the two bases take different arguments: set each one up explicitly
        HTTPError.__init__(self, message, response = response)
        self.description = message
        self.retry_after = retry_after

    @classmethod
    def from_http_error(cls, error: HTTPError) -> "GeckoRateLimitError":
        """
            Build the exception from the HTTP error of a 429 answer.

            Parameters:
                error: the HTTP error raised for the 429 answer.

            Returns:
                The rate limit error, with the answer and the time to wait.
        """
        response = error.response
        retry_after = GECKO_PUBLIC_RATE_WINDOW_S
        if response is not None:
            try:
                header = float(response.headers.get("Retry-After", "0"))
            except ValueError:
                header = 0.0
            if math.isfinite(header) and header > 0:
                retry_after = header
        return cls(str(error), response = response, retry_after = retry_after)
