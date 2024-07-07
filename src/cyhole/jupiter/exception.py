from ..core.exception import CyholeException

class JupiterException(CyholeException):
    """General Exception for Jupiter API."""
    pass

class JupiterNoRouteFoundError(JupiterException):
    pass

class JupiterInvalidRequest(JupiterException):
    pass