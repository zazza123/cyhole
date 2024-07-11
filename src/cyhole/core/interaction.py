from typing import Any

from ..core.client import APIClient, AsyncAPIClient

class Interaction:
    """
        This class is the building block for a new integration of an external API in `cyhole` library, 
        and every new external API **must** be identified by a class that inherits from this class.

        Inside an `Interaction` there are two attributes identifying the clients responsable to 
        perform the API calls:

        - `client`: object used for **synchronous** logic.
        - `async_client`: object used for **asynchronous** logic.

        During the creation of the object is possible to specify some global configurations.

        Parameters:
            headers: headers used globally in all API requests.
    """
    def __init__(self, headers: Any | None = None) -> None:
        self.headers = headers

        # clients
        self.client = APIClient(self, headers = self.headers)
        self.async_client = AsyncAPIClient(self, headers = self.headers)

        return