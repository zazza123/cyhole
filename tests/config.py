import json
import configparser
from pathlib import Path
from requests import Response
from typing import TypeVar, Type
from pydantic import BaseModel

ResponseModel = TypeVar('ResponseModel', bound = BaseModel)

class SolanaFMConfiguration(BaseModel):
    """
        Model in charge to manage the SolanaFM APIs.
    """
    mock_response: bool = True
    """Flag to enable/disable the mock responses."""
    mock_folder: str = "solana_fm"
    """Folder where the mock responses are stored."""
    api_key: str | None = None
    """API key to access the SolanaFM APIs."""

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
    jupiter: JupiterConfiguration = JupiterConfiguration()
    """Jupiter configuration."""
    solana_fm: SolanaFMConfiguration = SolanaFMConfiguration()
    """SolanaFM configuration."""

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

    # birdeye
    test_config.birdeye.mock_response_public = config.getboolean("birdeye", "mock_response_public", fallback = test_config.birdeye.mock_response_public)
    test_config.birdeye.mock_response_private = config.getboolean("birdeye", "mock_response_private", fallback = test_config.birdeye.mock_response_private)
    test_config.birdeye.mock_folder = config.get("birdeye", "mock_folder", fallback = test_config.birdeye.mock_folder)
    test_config.birdeye.api_key = config.get("birdeye", "api_key", fallback = test_config.birdeye.api_key)

    # jupiter
    test_config.jupiter.mock_response = config.getboolean("jupiter", "mock_response", fallback = test_config.jupiter.mock_response)
    test_config.jupiter.mock_folder = config.get("jupiter", "mock_folder", fallback = test_config.jupiter.mock_folder)

    # solana_fm
    test_config.solana_fm.mock_response = config.getboolean("solana_fm", "mock_response", fallback = test_config.solana_fm.mock_response)
    test_config.solana_fm.mock_folder = config.get("solana_fm", "mock_folder", fallback = test_config.solana_fm.mock_folder)
    test_config.solana_fm.api_key = config.get("solana_fm", "api_key", fallback = test_config.solana_fm.api_key)

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
            mock_response = response_model(**data)

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