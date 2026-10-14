from ..core.exception import CyholeException


class GeckoException(CyholeException):
    """Base exception raised by the Gecko interaction."""
    pass


class GeckoAddressCountError(GeckoException):
    """Exception raised when a multi-address endpoint receives too few or too many addresses."""
    pass
