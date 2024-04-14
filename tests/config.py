"""
    This file is used to load and manage all the tests' configurations.

    The 'pycrypt' library interacts with many external API that requires 
    an API Key in order to extract data. Since the usage of these API Keys 
    is subjected to costs, a proper configuration for the tests was required.

    The configuration is managed by a 'test.ini' file loaded during the 
    execution of the tests. By usin this file will be possible to:
        - manage API Keys externally
        - enable/disable mock responses

    Check the default 'test.ini' file for a complete list of available configurations.
"""
import configparser
from pydantic import BaseModel

class TestConfiguration(BaseModel):
    """
        Model in charge to manage the tests' configuration.
    """
    mock_response: bool = True
    mock_folder: str = "tests/resources/mock"

def load_config(path: str = "tests", file: str = "test.ini") -> TestConfiguration:
    """
        This function is used to load the test configuration file.

        It is strongly suggested to leave the default 'path' and 'file' 
        name for the test configuration file. However, if a dedicated file 
        is used, then is possible to load another file by providing the 
        necesary information in the input variables.

        Args:

        - path (str) [optional] : path of the configuration file. \\
            By default is the same test folder 'tests'.

        - file (str) [optional] : name of the configuration file (with extension). \\
            By default is 'test.ini'.
    """
    config_path_file = f"{path}/{file}"
    config = configparser.ConfigParser()

    # load config
    config.read(config_path_file)
    test_config = TestConfiguration()
    
    # global
    test_config.mock_response = config.getboolean("global", "mock_response", fallback = test_config.mock_response)
    test_config.mock_folder = config.get("global", "mock_folder", fallback = test_config.mock_folder)

    return test_config