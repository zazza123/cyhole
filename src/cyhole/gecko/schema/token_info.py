"""Schema for the standalone Token Info endpoint."""

from pydantic import BaseModel

from .common import TokenFullInfoAttributes


class TokenInfoData(BaseModel):
    """
    Single token resource returned by the Token Info endpoint.

    Attributes:
        id: GeckoTerminal token identifier.
        type: JSON:API resource type, always `"token"`.
        attributes: full token metadata block (image set, scores, holders, socials, ...).
    """
    id: str
    type: str
    attributes: TokenFullInfoAttributes


class GetTokenInfoResponse(BaseModel):
    """
    Response payload from the **Token Info** endpoint, returning the complete metadata block of a
    single token: image set, GeckoTerminal trust score breakdown, holders distribution, social
    links, description and authorities. Use this to enrich a token view without making multiple
    requests.

    Attributes:
        data: token info resource.
    """
    data: TokenInfoData
