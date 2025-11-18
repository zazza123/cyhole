from ..core.exception import CyholeException

class JupiterException(CyholeException):
    """General Exception for Jupiter API."""
    pass

class JupiterApiTierError(JupiterException):
    pass

class JupiterNoRouteFoundError(JupiterException):
    pass

class JupiterInvalidRequest(JupiterException):
    pass

class JupiterComputeAmountThresholdError(JupiterException):
    pass