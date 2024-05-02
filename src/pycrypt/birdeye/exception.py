from typing import Any

from ..core.exception import PycryptException, ParamUnknownError
from ..birdeye.param import (
    BirdeyeChain,
    BirdeyeOrder,
    BirdeyeSort,
    BirdeyeTimeFrame,
    BirdeyeTradeType,
    BirdeyeAddressType
)

class BirdeyeException(PycryptException):
    pass

class BirdeyeAuthorisationError(BirdeyeException):
    def __init__(self, description: str = "The API Key is not authorised to use this endpoint."):
        super().__init__(description)

class BirdeyeTimeRangeError(BirdeyeException):
    pass

class BirdeyeParamUnknownError(ParamUnknownError):
    pass

class BirdeyeChainUnknownError(BirdeyeParamUnknownError):
    def __init__(self, param_value: Any, param_enum = BirdeyeChain):
        super().__init__(param_value, param_enum)

class BirdeyeOrderUnknownError(BirdeyeParamUnknownError):
    def __init__(self, param_value: Any, param_enum = BirdeyeOrder):
        super().__init__(param_value, param_enum)

class BirdeyeSortUnknownError(BirdeyeParamUnknownError):
    def __init__(self, param_value: Any, param_enum = BirdeyeSort):
        super().__init__(param_value, param_enum)

class BirdeyeTimeFrameUnknownError(BirdeyeParamUnknownError):
    def __init__(self, param_value: Any, param_enum = BirdeyeTimeFrame):
        super().__init__(param_value, param_enum)

class BirdeyeTradeTypeUnknownError(BirdeyeParamUnknownError):
    def __init__(self, param_value: Any, param_enum = BirdeyeTradeType):
        super().__init__(param_value, param_enum)

class BirdeyeAddressTypeUnknownError(BirdeyeParamUnknownError):
    def __init__(self, param_value: Any, param_enum = BirdeyeAddressType):
        super().__init__(param_value, param_enum)