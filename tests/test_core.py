import pytest

from cyhole.core import APICaller
from cyhole.core.param import CyholeParam
from cyhole.core.exception import RequestTypeNotSupported, ParamUnknownError

client = APICaller()

def test_api_request_type_not_supported() -> None:
    """
        Unit Test for `APICaller.api` function with Request Type not supported.
    """
    with pytest.raises(RequestTypeNotSupported):
        client.api(type = "XXX", url = "")

def test_api_with_header() -> None:
    """
        Unit Test for `APICaller.api` function with `headers`.
    """
    with pytest.raises(RequestTypeNotSupported):
        client.api(type = "XXX", url = "", headers = {"test": "test"})

def test_param_unknown() -> None:
    """
        Unit Test for `ParamUnknownError` exception.
    """
    class ParamTest(CyholeParam):
        TEST: str = "test"

    with pytest.raises(ParamUnknownError):
        ParamTest.check("xxx")