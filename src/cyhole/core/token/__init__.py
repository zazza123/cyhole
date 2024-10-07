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

    def int_to_float(self, amount: int) -> float:
        """
            Convert the amount of token from integer to float according to decimals.

            Parameters:
                amount: amount of token in integer.
        """
        return amount / 10 ** self.decimals