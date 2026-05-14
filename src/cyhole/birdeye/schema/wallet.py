from pydantic import BaseModel

# classes used on GET "Wallet - Supported Networks" endpoint
class GetWalletSupportedNetworksResponse(BaseModel):
    """
        Model used to represent the **Wallet - Supported Networks** endpoint from birdeye API.
    """
    data: list[str]
    success: bool
