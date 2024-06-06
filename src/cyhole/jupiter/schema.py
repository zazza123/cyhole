from pydantic import BaseModel, Field

# classes used on GET "Price" endpoint
class GetPriceData(BaseModel):
    id: str
    mint_symbol: str = Field(alias = "mintSymbol")
    vs_token: str = Field(alias = "vsToken")
    vs_token_symbol: str = Field(alias = "vsTokenSymbol")
    price: float

class GetPriceResponse(BaseModel):
    """
        Model used to represent the **Price** endpoint from Jupiter API.
    """
    data: dict[str, GetPriceData]
    time_taken: float = Field(alias = "timeTaken")