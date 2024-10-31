from pydantic import BaseModel

class CyholeToken(BaseModel):
    """
        Core model used to identify a token on `cyhole` library.
    """
    address: str
    """Hash code identifying the token on the chain."""
    decimals: int
    """Number of decimal places the token uses."""
    name: str
    """Name of the token."""
    symbol: str
    """Symbol of the token."""

    def __str__(self) -> str:
        return self.address

    def to_decimals(self, amount: int) -> float:
        """
            Convert the amount of token from integer to float according to its decimals.

            Parameters:
                amount: amount of token in integer.

            Returns:
                The amount of token in float.
        """
        return amount / 10 ** self.decimals