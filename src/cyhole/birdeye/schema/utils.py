from pydantic import BaseModel

# classes used on GET "Utils v1 Credits" endpoint
class GetUtilsV1CreditsBreakdown(BaseModel):
    """
        Credit breakdown by channel for one of the usage, remaining, overage_usage or
        overage_cost sub-objects in the Utils v1 Credits response.

        Attributes:
            api: value attributed to REST API calls; `None` when not reported.
            ws: value attributed to WebSocket connections; `None` when not reported.
            total: combined value across all channels; `None` when not reported.
    """
    api: float | None = None
    ws: float | None = None
    total: float | None = None


class GetUtilsV1CreditsData(BaseModel):
    """
        Credit usage payload returned by the Birdeye Utils v1 Credits endpoint.

        Attributes:
            start_time: unix-second timestamp of the start of the reported period; `None`
                when not provided.
            end_time: unix-second timestamp of the end of the reported period; `None`
                when not provided.
            usage: credits consumed during the period, broken down by channel; `None` when
                not reported.
            remaining: credits still available, broken down by channel; `None` when not
                reported.
            overage_usage: credits consumed beyond the plan limit during the period,
                broken down by channel; `None` when not reported.
            overage_cost: monetary cost incurred by overage usage, broken down by channel;
                `None` when not reported.
    """
    start_time: int | None = None
    end_time: int | None = None
    usage: GetUtilsV1CreditsBreakdown | None = None
    remaining: GetUtilsV1CreditsBreakdown | None = None
    overage_usage: GetUtilsV1CreditsBreakdown | None = None
    overage_cost: GetUtilsV1CreditsBreakdown | None = None


class GetUtilsV1CreditsResponse(BaseModel):
    """
        Model used to represent the **Utils v1 Credits** endpoint from the Birdeye API.

        Attributes:
            data: credit usage statistics for the current account.
            success: `True` when the API processed the request successfully.
    """
    data: GetUtilsV1CreditsData
    success: bool
