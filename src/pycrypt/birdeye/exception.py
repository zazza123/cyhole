from ..core.exception import PycryptException

class BirdeyeException(PycryptException):
    pass

class BirdeyeAuthorisationError(BirdeyeException):
    def __init__(self, description: str = "The API Key is not authorised to use this endpoint."):
        super().__init__(description)

class BirdeyeTimeRangeError(BirdeyeException):
    pass

class BirdeyeAddressTypeUnknownError(BirdeyeException):
    pass