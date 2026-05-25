import json
import configparser
from pathlib import Path
from requests import Response
from typing import TypeVar, Type
from pydantic import BaseModel

ResponseModel = TypeVar('ResponseModel', bound = BaseModel)

class SolscanConfiguration(BaseModel):
    """
        Model in charge to manage the Solscan APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "solscan"
    """Folder where the mock responses are stored."""
    api_v1_key: str | None = None
    """API key to access the Solscan V1 APIs."""
    api_v2_key: str | None = None
    """API key to access the Solscan V2 APIs."""

class JupiterConfiguration(BaseModel):
    """
        Model in charge to manage the Jupiter APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "jupiter"
    """Folder where the mock responses are stored."""

class BirdeyeConfiguration(BaseModel):
    """
        Model in charge to manage the birdeye APIs.
    """
    mock_response_public: bool = True
    """Flag to enable/disable the mock responses for the public APIs."""
    mock_response_private: bool = True
    """Flag to enable/disable the mock responses for the private APIs."""
    mock_folder: str = "birdeye"
    """Folder where the mock responses are stored."""
    api_key: str = ""
    """API key to access the birdeye APIs."""

class DexScreenerConfiguration(BaseModel):
    """
        Model in charge to manage the DexScreener APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "dex_screener"
    """Folder where the mock responses are stored."""

class RugcheckConfiguration(BaseModel):
    """
        Model in charge to manage the Rugcheck APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "rugcheck"
    """Folder where the mock responses are stored."""
    api_key: str | None = None
    """Optional API key (Bearer token) for authenticated endpoints."""

class HeliusConfiguration(BaseModel):
    """
        Model in charge to manage the Helius APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "helius"
    """Folder where the mock responses are stored."""
    api_key: str | None = None
    """API key required for all Helius DAS API endpoints."""

class GeckoConfiguration(BaseModel):
    """
        Model in charge to manage the Gecko APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "gecko"
    """Folder where the mock responses are stored."""
    api_key: str | None = None
    """Optional CoinGecko Pro API key for the on-chain endpoints."""


class TestConfiguration(BaseModel):
    """
        Model in charge to manage the tests' configuration.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "tests/resources/mock"
    """Folder where the mock responses are stored."""
    mock_file_overwrite: bool = False
    """Flag to enable/disable the overwrite of the mock files."""

    birdeye: BirdeyeConfiguration = BirdeyeConfiguration()
    """Birdeye configuration."""
    dex_screener: DexScreenerConfiguration = DexScreenerConfiguration()
    """DexScreener configuration."""
    rugcheck: RugcheckConfiguration = RugcheckConfiguration()
    """Rugcheck configuration."""
    jupiter: JupiterConfiguration = JupiterConfiguration()
    """Jupiter configuration."""
    solscan: SolscanConfiguration = SolscanConfiguration()
    """Solscan configuration."""
    helius: HeliusConfiguration = HeliusConfiguration()
    """Helius configuration."""
    gecko: GeckoConfiguration = GeckoConfiguration()
    """Gecko configuration."""

def load_config(path: str = "tests", file: str = "test.ini") -> TestConfiguration:
    """
        This function is used to load the test configuration file.

        It is **strongly suggested** to leave the default `path` and `file` 
        name for the test configuration file. However, if a dedicated file 
        is used, then is possible to load another file by providing the 
        necessary information in the input variables.

        Parameters:
            path: path of the configuration file.
            file: name of the configuration file (with extension).

        Returns:
            pydantic model of the test's configuration.
    """
    config_path_file = f"{path}/{file}"
    config = configparser.ConfigParser()

    # load config
    config.read(config_path_file)
    test_config = TestConfiguration()
    
    # global
    test_config.mock_response = config.getboolean("global", "mock_response", fallback = test_config.mock_response)
    test_config.mock_folder = config.get("global", "mock_folder", fallback = test_config.mock_folder)
    test_config.mock_file_overwrite = config.getboolean("global", "mock_file_overwrite", fallback = test_config.mock_file_overwrite)

    # dex_screener
    test_config.dex_screener.mock_response = config.getboolean("dex_screener", "mock_response", fallback = test_config.dex_screener.mock_response)
    test_config.dex_screener.mock_folder = config.get("dex_screener", "mock_folder", fallback = test_config.dex_screener.mock_folder)

    # rugcheck
    test_config.rugcheck.mock_response = config.getboolean("rugcheck", "mock_response", fallback = test_config.rugcheck.mock_response)
    test_config.rugcheck.mock_folder = config.get("rugcheck", "mock_folder", fallback = test_config.rugcheck.mock_folder)
    test_config.rugcheck.api_key = config.get("rugcheck", "api_key", fallback = test_config.rugcheck.api_key)

    # birdeye
    test_config.birdeye.mock_response_public = config.getboolean("birdeye", "mock_response_public", fallback = test_config.birdeye.mock_response_public)
    test_config.birdeye.mock_response_private = config.getboolean("birdeye", "mock_response_private", fallback = test_config.birdeye.mock_response_private)
    test_config.birdeye.mock_folder = config.get("birdeye", "mock_folder", fallback = test_config.birdeye.mock_folder)
    test_config.birdeye.api_key = config.get("birdeye", "api_key", fallback = test_config.birdeye.api_key)

    # jupiter
    test_config.jupiter.mock_response = config.getboolean("jupiter", "mock_response", fallback = test_config.jupiter.mock_response)
    test_config.jupiter.mock_folder = config.get("jupiter", "mock_folder", fallback = test_config.jupiter.mock_folder)

    # solscan
    test_config.solscan.mock_response = config.getboolean("solscan", "mock_response", fallback = test_config.solscan.mock_response)
    test_config.solscan.mock_folder = config.get("solscan", "mock_folder", fallback = test_config.solscan.mock_folder)
    test_config.solscan.api_v1_key = config.get("solscan", "api_v1_key", fallback = test_config.solscan.api_v1_key)
    test_config.solscan.api_v2_key = config.get("solscan", "api_v2_key", fallback = test_config.solscan.api_v2_key)

    # helius
    test_config.helius.mock_response = config.getboolean("helius", "mock_response", fallback = test_config.helius.mock_response)
    test_config.helius.mock_folder = config.get("helius", "mock_folder", fallback = test_config.helius.mock_folder)
    test_config.helius.api_key = config.get("helius", "api_key", fallback = test_config.helius.api_key)

    # gecko
    test_config.gecko.mock_response = config.getboolean("gecko", "mock_response", fallback = test_config.gecko.mock_response)
    test_config.gecko.mock_folder = config.get("gecko", "mock_folder", fallback = test_config.gecko.mock_folder)
    test_config.gecko.api_key = config.get("gecko", "api_key", fallback = test_config.gecko.api_key)

    return test_config

class MockerManager:
    """
        Class used to manage the mock responses.
    """

    def __init__(self, mock_path: Path) -> None:
        # set/create resources folder
        self.mock_path = mock_path
        mock_path.mkdir(parents = True, exist_ok = True)
    
    def load_mock_model(self, file_name: str, response_model: Type[ResponseModel]) -> ResponseModel:
        """
            Use this function to load mock response model from a file.

            Parameters:
                file_name: file name containing the response to load.
                    By assumption, the file must be a JSON file and the file name should not contain the extension.
                response_model: objects that inherit from `pydantic.BaseModel` and describe the response object element.
        """
        mock_file = f"{file_name}.json"
        mock_path_file = self.mock_path / mock_file

        if not mock_path_file.exists():
            raise Exception(f"mock file '{mock_file}' does not exist in '{self.mock_path}'.")

        with open(mock_path_file, "r") as file:
            data = json.loads(file.read())
            mock_response = response_model.model_validate(data)

        return mock_response

    def store_mock_model(self, file_name: str, response: BaseModel) -> None:
        """
            Use this function to store the mock response model into a file.

            Parameters:
                file_name: file name containing the response to load.
                    By assumption, the file must be a JSON file and the file name should not contain the extension.
                response: objects that inherit from `pydantic.BaseModel` and describe the response object element.
        """
        mock_file = f"{file_name}.json"
        mock_path_file = self.mock_path / mock_file

        with open(mock_path_file, "w") as file:
            file.write(response.model_dump_json(indent = 4, by_alias = True))

        return

    def load_mock_response(self, file_name: str, response_model: Type[ResponseModel]) -> Response:
        """
            Use this function to load mock response model from a file and return a dummy `Response` object.

            Parameters:
                file_name: file name containing the response to load.
                    By assumption, the file must be a JSON file and the file name should not contain the extension.
                response_model: objects that inherit from `pydantic.BaseModel` and describe the response object element.
        """
        mock_model = self.load_mock_model(file_name, response_model)

        # create dummy response
        mock_response = Response()
        mock_response._content = mock_model.model_dump_json(by_alias = True, exclude_none = True).encode()
        mock_response.status_code = 200
        mock_response.encoding = "utf-8"

        return mock_response

    def adjust_content_json(self, content: str) -> bytes:
        """
            Use this function to adjust an input string to ensure that 
            can be used as content for a `Response` object and paresed 
            as a JSON object.

            Parameters:
                content: string to adjust.
        """
        # adjustemts
        content = content.replace("'", '"')
        content = content.replace("False", "false")
        content = content.replace("True", "true")
        content = content.replace("None", "null")

        return content.encode()