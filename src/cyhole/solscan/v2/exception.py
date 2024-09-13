from ...core.exception import CyholeException

class SolscanException(CyholeException):
    """General Exception for Solscan API."""
    pass

class SolscanInvalidAmountRange(SolscanException):
    """Exception raised when the amount range is invalid."""
    pass

class SolscanInvalidTimeRange(SolscanException):
    """Exception raised when the time range is invalid."""
    pass