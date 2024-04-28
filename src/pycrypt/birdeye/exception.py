from ..core.exception import PycryptException

class BirdeyeException(PycryptException):
    pass

class TimeRangeError(BirdeyeException):
    pass

class BirdeyeAddressTypeUnknownError(BirdeyeException):
    pass