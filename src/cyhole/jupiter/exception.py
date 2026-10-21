from ..core.exception import CyholeException

class JupiterException(CyholeException):
    """General Exception for Jupiter API."""

    status_code: int | None = None
    """HTTP status of the answer that raised it, when it came from one."""

class JupiterRateLimitError(JupiterException):
    """Jupiter answered 429: the account's rate limit was hit."""
    pass

class JupiterApiTierError(JupiterException):
    pass

class JupiterNoRouteFoundError(JupiterException):
    pass

class JupiterInvalidRequest(JupiterException):
    pass

class JupiterComputeAmountThresholdError(JupiterException):
    pass