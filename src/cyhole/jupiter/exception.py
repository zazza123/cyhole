from ..core.exception import CyholeException, CyholeRateLimitError

class JupiterException(CyholeException):
    """General Exception for Jupiter API."""

    status_code: int | None = None
    """HTTP status of the answer that raised it, when it came from one."""

class JupiterRateLimitError(JupiterException, CyholeRateLimitError):
    """Jupiter answered 429: the account's rate limit was hit. Jupiter gives no wait, so `retry_after` is `None`."""
    pass

class JupiterApiTierError(JupiterException):
    pass

class JupiterNoRouteFoundError(JupiterException):
    pass

class JupiterInvalidRequest(JupiterException):
    pass

class JupiterComputeAmountThresholdError(JupiterException):
    pass