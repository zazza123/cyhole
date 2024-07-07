"""
    This file is used to load and manage all the tests' configurations.

    The 'cyhole' library interacts with many external API that requires 
    an API Key in order to extract data. Since the usage of these API Keys 
    is subjected to costs, a proper configuration for the tests was required.

    The configuration is managed by a 'test.ini' file loaded during the 
    execution of the tests. By using this file will be possible to:
        - manage API Keys externally
        - enable/disable mock responses

    Check the default 'test.ini' file for a complete list of available configurations.

    Mock Responses
    If the mock response functionality is enabled, then the tests try to load a JSON file 
    with the response stored from a previous extration from the API.
    Moreover, every time the tests are executed with the mock response functionality 
    disabled, the process automatically stores the response in a JSON file into the 
    proper resources folder.

"""
import json
import configparser
from pathlib import Path
from requests import Response
from typing import TypeVar, Type
from pydantic import BaseModel

ResponseModel = TypeVar('ResponseModel', bound = BaseModel)

class JupiterConfiguration(BaseModel):
    """
        Model in charge to manage the Jupiter APIs.
    """
    mock_response: bool = True
    mock_folder: str = "jupiter"

class BirdeyeConfiguration(BaseModel):
    """
        Model in charge to manage the birdeye APIs.
    """
    mock_response_public: bool = False
    mock_response_private: bool = True
    mock_folder: str = "birdeye"
    api_key: str = ""

class TestConfiguration(BaseModel):
    """
        Model in charge to manage the tests' configuration.
    """
    mock_response: bool = True
    mock_folder: str = "tests/resources/mock"
    mock_file_overwrite: bool = False
    birdeye: BirdeyeConfiguration = BirdeyeConfiguration()
    jupiter: JupiterConfiguration = JupiterConfiguration()

def load_config(path: str = "tests", file: str = "test.ini") -> TestConfiguration:
    """
        This function is used to load the test configuration file.

        It is strongly suggested to leave the default 'path' and 'file' 
        name for the test configuration file. However, if a dedicated file 
        is used, then is possible to load another file by providing the 
        necesary information in the input variables.

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