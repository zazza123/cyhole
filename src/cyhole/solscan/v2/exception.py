from ...core.exception import CyholeException

class SolscanException(CyholeException):
    """General Exception for Solscan API."""
    pass

class SolscanAccountTransferInvalidAmountRange(SolscanException):
    """Exception raised when the amount range is invalid."""
    pass

class SolscanAccountTransferInvalidTimeRange(SolscanException):
    """Exception raised when the time range is invalid."""
    pass