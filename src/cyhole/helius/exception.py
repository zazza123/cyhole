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
