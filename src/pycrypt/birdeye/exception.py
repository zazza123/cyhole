from ..core.exception import PycryptException

from ..birdeye.param import (
    BirdeyeAddressType
)

class BirdeyeException(PycryptException):
    pass

class BirdeyeAuthorisationError(BirdeyeException):
    def __init__(self, description: str = "The API Key is not authorised to use this endpoint."):
        super().__init__(description)

class BirdeyeTimeRangeError(BirdeyeException):
    pass

class BirdeyeAddressTypeUnknownError(BirdeyeException):
    def __init__(self, address_type: str):
        description = f"address type '{address_type}' not supported. \nAdmissible values: {BirdeyeAddressType.__members__}"
        super().__init__(description)