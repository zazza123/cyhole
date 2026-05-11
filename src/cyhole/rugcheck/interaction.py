from typing import Any, Coroutine, overload, Literal

from ..core.param import RequestType
from ..core.interaction import Interaction
from ..rugcheck.client import RugcheckClient, RugcheckAsyncClient
from ..rugcheck.param import RugcheckAnalyticsWindow
from ..rugcheck.schema import (
    GetPingResponse,
    GetMaintenanceResponse,
    GetLeaderboardResponse,
    GetTokenReportResponse,
    GetTokenReportSummaryResponse,
    GetTokenMetadataResponse,
    GetTokenVotesResponse,
    GetTokenInsidersGraphResponse,
    GetTokenInsidersNetworksResponse,
    GetStatsNewTokensResponse,
    GetStatsRecentResponse,
    GetStatsTrendingResponse,
    GetStatsVerifiedResponse,
    GetStatsAnalyticsResponse,
    GetStatsRugsTickerResponse,
    GetCreatorResponse,
    GetDomainsResponse,
    GetDomainLookupResponse,
    PostTokenReportResponse,
    PostTokenVoteBody,
    PostTokenVoteResponse,
    GetTokenLockersResponse,
    GetTokenLockersFluxResponse,
    PostBulkTokensBody,
    PostBulkTokensReportResponse,
    PostBulkTokensSummaryResponse,
    PostTokensVerifyEligibleBody,
    PostTokensVerifyEligibleResponse,
    PostTokensVerifyBody,
    PostTokensVerifyResponse,
    PostTokensVerifyTransactionBody,
    PostTokensVerifyTransactionResponse,
)


class Rugcheck(Interaction):
    """
    Class used to connect [Rugcheck](https://rugcheck.xyz) API.

    Rugcheck provides rug-pull risk analysis for Solana tokens, including
    liquidity analysis, insider detection, and community voting.

    Public endpoints require no API key. Authenticated endpoints require a
    Bearer token passed as `api_key`.

    **Example**

    ```python
    from cyhole.rugcheck import Rugcheck

    rugcheck = Rugcheck()
    report = rugcheck.client.get_token_report("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
    ```
    """

    def __init__(self, api_key: str | None = None, headers: Any | None = None) -> None:
        super().__init__(headers)
        if api_key:
            auth_header = {"Authorization": f"Bearer {api_key}"}
            self.headers = {**(self.headers or {}), **auth_header}
        self.client = RugcheckClient(self)
        self.async_client = RugcheckAsyncClient(self)
        self.url_api = "https://api.rugcheck.xyz"

    # -------------------------------------------------------------------------
    # Ping
    # -------------------------------------------------------------------------

    @overload
    def _get_ping(self, sync: Literal[True]) -> GetPingResponse: ...
    @overload
    def _get_ping(self, sync: Literal[False]) -> Coroutine[None, None, GetPingResponse]: ...
    def _get_ping(self, sync: bool) -> GetPingResponse | Coroutine[None, None, GetPingResponse]:
        """
        This function refers to the **Ping** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetPingResponse: ping response with a `message` field.
        """
        url = self.url_api + "/ping"
        return self.api_return_model(sync, RequestType.GET.value, url, GetPingResponse)

    # -------------------------------------------------------------------------
    # Maintenance
    # -------------------------------------------------------------------------

    @overload
    def _get_maintenance(self, sync: Literal[True]) -> GetMaintenanceResponse: ...
    @overload
    def _get_maintenance(self, sync: Literal[False]) -> Coroutine[None, None, GetMaintenanceResponse]: ...
    def _get_maintenance(self, sync: bool) -> GetMaintenanceResponse | Coroutine[None, None, GetMaintenanceResponse]:
        """
        This function refers to the **Maintenance** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetMaintenanceResponse: maintenance status message.
        """
        url = self.url_api + "/v1/maintenance"
        return self.api_return_model(sync, RequestType.GET.value, url, GetMaintenanceResponse)

    # -------------------------------------------------------------------------
    # Leaderboard
    # -------------------------------------------------------------------------

    @overload
    def _get_leaderboard(self, sync: Literal[True], page: int = 0, limit: int = 50) -> GetLeaderboardResponse: ...
    @overload
    def _get_leaderboard(self, sync: Literal[False], page: int = 0, limit: int = 50) -> Coroutine[None, None, GetLeaderboardResponse]: ...
    def _get_leaderboard(self, sync: bool, page: int = 0, limit: int = 50) -> GetLeaderboardResponse | Coroutine[None, None, GetLeaderboardResponse]:
        """
        This function refers to the **Leaderboard** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            page: page number (default 0).
            limit: number of entries per page, max 100 (default 50).

        Returns:
            GetLeaderboardResponse: ordered list of top voters.
        """
        url = self.url_api + "/v1/leaderboard"
        params = {"page": page, "limit": limit}
        return self.api_return_model(sync, RequestType.GET.value, url, GetLeaderboardResponse, params=params)

    # -------------------------------------------------------------------------
    # Token report (full)
    # -------------------------------------------------------------------------

    @overload
    def _get_token_report(self, sync: Literal[True], mint: str, refresh: bool | None = None) -> GetTokenReportResponse: ...
    @overload
    def _get_token_report(self, sync: Literal[False], mint: str, refresh: bool | None = None) -> Coroutine[None, None, GetTokenReportResponse]: ...
    def _get_token_report(self, sync: bool, mint: str, refresh: bool | None = None) -> GetTokenReportResponse | Coroutine[None, None, GetTokenReportResponse]:
        """
        This function refers to the **Get Token Report** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.
            refresh: if True, force a fresh report generation.

        Returns:
            GetTokenReportResponse: full rug-check report for the token.
        """
        url = self.url_api + f"/v1/tokens/{mint}/report"
        params = {"refresh": refresh}
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenReportResponse, params=params)

    # -------------------------------------------------------------------------
    # Token report summary
    # -------------------------------------------------------------------------

    @overload
    def _get_token_report_summary(self, sync: Literal[True], mint: str, cache_only: str | None = None, refresh: bool | None = None) -> GetTokenReportSummaryResponse: ...
    @overload
    def _get_token_report_summary(self, sync: Literal[False], mint: str, cache_only: str | None = None, refresh: bool | None = None) -> Coroutine[None, None, GetTokenReportSummaryResponse]: ...
    def _get_token_report_summary(self, sync: bool, mint: str, cache_only: str | None = None, refresh: bool | None = None) -> GetTokenReportSummaryResponse | Coroutine[None, None, GetTokenReportSummaryResponse]:
        """
        This function refers to the **Get Token Report Summary** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.
            cache_only: if set, only return cached results.
            refresh: if True, force a fresh report generation.

        Returns:
            GetTokenReportSummaryResponse: lightweight summary of the token report.
        """
        url = self.url_api + f"/v1/tokens/{mint}/report/summary"
        params = {"cacheOnly": cache_only, "refresh": refresh}
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenReportSummaryResponse, params=params)

    # -------------------------------------------------------------------------
    # Token metadata
    # -------------------------------------------------------------------------

    @overload
    def _get_token_metadata(self, sync: Literal[True], mint: str) -> GetTokenMetadataResponse: ...
    @overload
    def _get_token_metadata(self, sync: Literal[False], mint: str) -> Coroutine[None, None, GetTokenMetadataResponse]: ...
    def _get_token_metadata(self, sync: bool, mint: str) -> GetTokenMetadataResponse | Coroutine[None, None, GetTokenMetadataResponse]:
        """
        This function refers to the **Get Token Metadata** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.

        Returns:
            GetTokenMetadataResponse: token metadata including image URI.
        """
        url = self.url_api + f"/v1/tokens/{mint}/metadata"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenMetadataResponse)

    # -------------------------------------------------------------------------
    # Token votes
    # -------------------------------------------------------------------------

    @overload
    def _get_token_votes(self, sync: Literal[True], mint: str) -> GetTokenVotesResponse: ...
    @overload
    def _get_token_votes(self, sync: Literal[False], mint: str) -> Coroutine[None, None, GetTokenVotesResponse]: ...
    def _get_token_votes(self, sync: bool, mint: str) -> GetTokenVotesResponse | Coroutine[None, None, GetTokenVotesResponse]:
        """
        This function refers to the **Get Token Votes** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.

        Returns:
            GetTokenVotesResponse: up/down vote counts for the token.
        """
        url = self.url_api + f"/v1/tokens/{mint}/votes"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenVotesResponse)

    # -------------------------------------------------------------------------
    # Token insiders graph
    # -------------------------------------------------------------------------

    @overload
    def _get_token_insiders_graph(self, sync: Literal[True], mint: str) -> GetTokenInsidersGraphResponse: ...
    @overload
    def _get_token_insiders_graph(self, sync: Literal[False], mint: str) -> Coroutine[None, None, GetTokenInsidersGraphResponse]: ...
    def _get_token_insiders_graph(self, sync: bool, mint: str) -> GetTokenInsidersGraphResponse | Coroutine[None, None, GetTokenInsidersGraphResponse]:
        """
        This function refers to the **Get Token Insiders Graph** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.

        Returns:
            GetTokenInsidersGraphResponse: list of insider networks with full node graphs.
        """
        url = self.url_api + f"/v1/tokens/{mint}/insiders/graph"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenInsidersGraphResponse)

    # -------------------------------------------------------------------------
    # Token insiders networks
    # -------------------------------------------------------------------------

    @overload
    def _get_token_insiders_networks(self, sync: Literal[True], mint: str) -> GetTokenInsidersNetworksResponse: ...
    @overload
    def _get_token_insiders_networks(self, sync: Literal[False], mint: str) -> Coroutine[None, None, GetTokenInsidersNetworksResponse]: ...
    def _get_token_insiders_networks(self, sync: bool, mint: str) -> GetTokenInsidersNetworksResponse | Coroutine[None, None, GetTokenInsidersNetworksResponse]:
        """
        This function refers to the **Get Token Insiders Networks** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.

        Returns:
            GetTokenInsidersNetworksResponse: summarised list of insider network metadata.
        """
        url = self.url_api + f"/v1/tokens/{mint}/insiders/networks"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenInsidersNetworksResponse)

    # -------------------------------------------------------------------------
    # Stats: new tokens
    # -------------------------------------------------------------------------

    @overload
    def _get_stats_new_tokens(self, sync: Literal[True]) -> GetStatsNewTokensResponse: ...
    @overload
    def _get_stats_new_tokens(self, sync: Literal[False]) -> Coroutine[None, None, GetStatsNewTokensResponse]: ...
    def _get_stats_new_tokens(self, sync: bool) -> GetStatsNewTokensResponse | Coroutine[None, None, GetStatsNewTokensResponse]:
        """
        This function refers to the **Get Stats New Tokens** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetStatsNewTokensResponse: list of recently created tokens.
        """
        url = self.url_api + "/v1/stats/new_tokens"
        return self.api_return_model(sync, RequestType.GET.value, url, GetStatsNewTokensResponse)

    # -------------------------------------------------------------------------
    # Stats: recent
    # -------------------------------------------------------------------------

    @overload
    def _get_stats_recent(self, sync: Literal[True]) -> GetStatsRecentResponse: ...
    @overload
    def _get_stats_recent(self, sync: Literal[False]) -> Coroutine[None, None, GetStatsRecentResponse]: ...
    def _get_stats_recent(self, sync: bool) -> GetStatsRecentResponse | Coroutine[None, None, GetStatsRecentResponse]:
        """
        This function refers to the **Get Stats Recent** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetStatsRecentResponse: list of recently visited/checked tokens.
        """
        url = self.url_api + "/v1/stats/recent"
        return self.api_return_model(sync, RequestType.GET.value, url, GetStatsRecentResponse)

    # -------------------------------------------------------------------------
    # Stats: trending
    # -------------------------------------------------------------------------

    @overload
    def _get_stats_trending(self, sync: Literal[True]) -> GetStatsTrendingResponse: ...
    @overload
    def _get_stats_trending(self, sync: Literal[False]) -> Coroutine[None, None, GetStatsTrendingResponse]: ...
    def _get_stats_trending(self, sync: bool) -> GetStatsTrendingResponse | Coroutine[None, None, GetStatsTrendingResponse]:
        """
        This function refers to the **Get Stats Trending** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetStatsTrendingResponse: trending tokens by vote activity (may be null).
        """
        url = self.url_api + "/v1/stats/trending"
        return self.api_return_model(sync, RequestType.GET.value, url, GetStatsTrendingResponse)

    # -------------------------------------------------------------------------
    # Stats: verified
    # -------------------------------------------------------------------------

    @overload
    def _get_stats_verified(self, sync: Literal[True]) -> GetStatsVerifiedResponse: ...
    @overload
    def _get_stats_verified(self, sync: Literal[False]) -> Coroutine[None, None, GetStatsVerifiedResponse]: ...
    def _get_stats_verified(self, sync: bool) -> GetStatsVerifiedResponse | Coroutine[None, None, GetStatsVerifiedResponse]:
        """
        This function refers to the **Get Stats Verified** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.

        Returns:
            GetStatsVerifiedResponse: list of verified tokens with project metadata.
        """
        url = self.url_api + "/v1/stats/verified"
        return self.api_return_model(sync, RequestType.GET.value, url, GetStatsVerifiedResponse)

    # -------------------------------------------------------------------------
    # Stats: analytics
    # -------------------------------------------------------------------------

    @overload
    def _get_stats_analytics(self, sync: Literal[True], window: RugcheckAnalyticsWindow = RugcheckAnalyticsWindow.D7) -> GetStatsAnalyticsResponse: ...
    @overload
    def _get_stats_analytics(self, sync: Literal[False], window: RugcheckAnalyticsWindow = RugcheckAnalyticsWindow.D7) -> Coroutine[None, None, GetStatsAnalyticsResponse]: ...
    def _get_stats_analytics(self, sync: bool, window: RugcheckAnalyticsWindow = RugcheckAnalyticsWindow.D7) -> GetStatsAnalyticsResponse | Coroutine[None, None, GetStatsAnalyticsResponse]:
        """
        This function refers to the **Get Stats Analytics** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            window: time window for the analytics data (default: 7d).

        Returns:
            GetStatsAnalyticsResponse: aggregate analytics statistics.
        """
        url = self.url_api + "/v1/stats/analytics"
        params = {"window": window.value}
        return self.api_return_model(sync, RequestType.GET.value, url, GetStatsAnalyticsResponse, params=params)

    # -------------------------------------------------------------------------
    # Stats: rugs ticker
    # -------------------------------------------------------------------------

    @overload
    def _get_stats_rugs_ticker(self, sync: Literal[True], limit: int = 10) -> GetStatsRugsTickerResponse: ...
    @overload
    def _get_stats_rugs_ticker(self, sync: Literal[False], limit: int = 10) -> Coroutine[None, None, GetStatsRugsTickerResponse]: ...
    def _get_stats_rugs_ticker(self, sync: bool, limit: int = 10) -> GetStatsRugsTickerResponse | Coroutine[None, None, GetStatsRugsTickerResponse]:
        """
        This function refers to the **Get Stats Rugs Ticker** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            limit: maximum number of items to return, max 50 (default 10).

        Returns:
            GetStatsRugsTickerResponse: recent rug-pull ticker items.
        """
        url = self.url_api + "/v1/stats/rugs/ticker"
        params = {"limit": limit}
        return self.api_return_model(sync, RequestType.GET.value, url, GetStatsRugsTickerResponse, params=params)

    # -------------------------------------------------------------------------
    # Creator
    # -------------------------------------------------------------------------

    @overload
    def _get_creator(self, sync: Literal[True], wallet: str) -> GetCreatorResponse: ...
    @overload
    def _get_creator(self, sync: Literal[False], wallet: str) -> Coroutine[None, None, GetCreatorResponse]: ...
    def _get_creator(self, sync: bool, wallet: str) -> GetCreatorResponse | Coroutine[None, None, GetCreatorResponse]:
        """
        This function refers to the **Get Creator** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            wallet: creator wallet address.

        Returns:
            GetCreatorResponse: creator statistics including rug history.
        """
        url = self.url_api + f"/v1/creators/{wallet}"
        return self.api_return_model(sync, RequestType.GET.value, url, GetCreatorResponse)

    # -------------------------------------------------------------------------
    # Domains
    # -------------------------------------------------------------------------

    @overload
    def _get_domains(self, sync: Literal[True], page: int | None = None, limit: int | None = None, verified: bool | None = None) -> GetDomainsResponse: ...
    @overload
    def _get_domains(self, sync: Literal[False], page: int | None = None, limit: int | None = None, verified: bool | None = None) -> Coroutine[None, None, GetDomainsResponse]: ...
    def _get_domains(self, sync: bool, page: int | None = None, limit: int | None = None, verified: bool | None = None) -> GetDomainsResponse | Coroutine[None, None, GetDomainsResponse]:
        """
        This function refers to the **Get Domains** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            page: page number for pagination.
            limit: number of results per page.
            verified: if True, return only verified domain tokens.

        Returns:
            GetDomainsResponse: list of domain-mapped tokens.
        """
        url = self.url_api + "/v1/domains"
        params = {"page": page, "limit": limit, "verified": verified}
        return self.api_return_model(sync, RequestType.GET.value, url, GetDomainsResponse, params=params)

    # -------------------------------------------------------------------------
    # Domain lookup
    # -------------------------------------------------------------------------

    @overload
    def _get_domain_lookup(self, sync: Literal[True], domain_id: str) -> GetDomainLookupResponse: ...
    @overload
    def _get_domain_lookup(self, sync: Literal[False], domain_id: str) -> Coroutine[None, None, GetDomainLookupResponse]: ...
    def _get_domain_lookup(self, sync: bool, domain_id: str) -> GetDomainLookupResponse | Coroutine[None, None, GetDomainLookupResponse]:
        """
        This function refers to the **Get Domain Lookup** API endpoint.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            domain_id: domain identifier to resolve.

        Returns:
            GetDomainLookupResponse: resolved mint address for the domain.
        """
        url = self.url_api + f"/v1/domains/lookup/{domain_id}"
        return self.api_return_model(sync, RequestType.GET.value, url, GetDomainLookupResponse)

    # -------------------------------------------------------------------------
    # Post token report (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_token_report(self, sync: Literal[True], mint: str) -> PostTokenReportResponse: ...
    @overload
    def _post_token_report(self, sync: Literal[False], mint: str) -> Coroutine[None, None, PostTokenReportResponse]: ...
    def _post_token_report(self, sync: bool, mint: str) -> PostTokenReportResponse | Coroutine[None, None, PostTokenReportResponse]:
        """
        This function refers to the **Post Token Report** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address to trigger report generation for.

        Returns:
            PostTokenReportResponse: confirmation that report generation was queued.
        """
        url = self.url_api + f"/v1/tokens/{mint}/report"
        return self.api_return_model(sync, RequestType.POST.value, url, PostTokenReportResponse)

    # -------------------------------------------------------------------------
    # Post token vote (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_token_vote(self, sync: Literal[True], body: PostTokenVoteBody) -> PostTokenVoteResponse: ...
    @overload
    def _post_token_vote(self, sync: Literal[False], body: PostTokenVoteBody) -> Coroutine[None, None, PostTokenVoteResponse]: ...
    def _post_token_vote(self, sync: bool, body: PostTokenVoteBody) -> PostTokenVoteResponse | Coroutine[None, None, PostTokenVoteResponse]:
        """
        This function refers to the **Post Token Vote** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            body: vote body containing mint address and vote direction.

        Returns:
            PostTokenVoteResponse: updated vote counts after casting the vote.
        """
        url = self.url_api + f"/v1/tokens/{body.mint}/vote"
        return self.api_return_model(sync, RequestType.POST.value, url, PostTokenVoteResponse, json=body.model_dump())

    # -------------------------------------------------------------------------
    # Get token lockers (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _get_token_lockers(self, sync: Literal[True], mint: str) -> GetTokenLockersResponse: ...
    @overload
    def _get_token_lockers(self, sync: Literal[False], mint: str) -> Coroutine[None, None, GetTokenLockersResponse]: ...
    def _get_token_lockers(self, sync: bool, mint: str) -> GetTokenLockersResponse | Coroutine[None, None, GetTokenLockersResponse]:
        """
        This function refers to the **Get Token Lockers** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.

        Returns:
            GetTokenLockersResponse: locker details and aggregate vault totals.
        """
        url = self.url_api + f"/v1/tokens/{mint}/lockers"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenLockersResponse)

    # -------------------------------------------------------------------------
    # Get token lockers flux (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _get_token_lockers_flux(self, sync: Literal[True], mint: str) -> GetTokenLockersFluxResponse: ...
    @overload
    def _get_token_lockers_flux(self, sync: Literal[False], mint: str) -> Coroutine[None, None, GetTokenLockersFluxResponse]: ...
    def _get_token_lockers_flux(self, sync: bool, mint: str) -> GetTokenLockersFluxResponse | Coroutine[None, None, GetTokenLockersFluxResponse]:
        """
        This function refers to the **Get Token Lockers Flux** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            mint: token mint address.

        Returns:
            GetTokenLockersFluxResponse: flux vault locker details and aggregate totals.
        """
        url = self.url_api + f"/v1/tokens/{mint}/lockers/flux"
        return self.api_return_model(sync, RequestType.GET.value, url, GetTokenLockersFluxResponse)

    # -------------------------------------------------------------------------
    # Post bulk tokens report (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_bulk_tokens_report(self, sync: Literal[True], body: PostBulkTokensBody) -> PostBulkTokensReportResponse: ...
    @overload
    def _post_bulk_tokens_report(self, sync: Literal[False], body: PostBulkTokensBody) -> Coroutine[None, None, PostBulkTokensReportResponse]: ...
    def _post_bulk_tokens_report(self, sync: bool, body: PostBulkTokensBody) -> PostBulkTokensReportResponse | Coroutine[None, None, PostBulkTokensReportResponse]:
        """
        This function refers to the **Post Bulk Tokens Report** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            body: bulk request body with list of token mint addresses.

        Returns:
            PostBulkTokensReportResponse: detailed reports for all requested tokens.
        """
        url = self.url_api + "/v1/bulk/tokens/report"
        return self.api_return_model(sync, RequestType.POST.value, url, PostBulkTokensReportResponse, json=body.model_dump(by_alias=True))

    # -------------------------------------------------------------------------
    # Post bulk tokens summary (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_bulk_tokens_summary(self, sync: Literal[True], body: PostBulkTokensBody) -> PostBulkTokensSummaryResponse: ...
    @overload
    def _post_bulk_tokens_summary(self, sync: Literal[False], body: PostBulkTokensBody) -> Coroutine[None, None, PostBulkTokensSummaryResponse]: ...
    def _post_bulk_tokens_summary(self, sync: bool, body: PostBulkTokensBody) -> PostBulkTokensSummaryResponse | Coroutine[None, None, PostBulkTokensSummaryResponse]:
        """
        This function refers to the **Post Bulk Tokens Summary** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            body: bulk request body with list of token mint addresses.

        Returns:
            PostBulkTokensSummaryResponse: summary reports for all requested tokens.
        """
        url = self.url_api + "/v1/bulk/tokens/summary"
        return self.api_return_model(sync, RequestType.POST.value, url, PostBulkTokensSummaryResponse, json=body.model_dump(by_alias=True))

    # -------------------------------------------------------------------------
    # Post tokens verify eligible (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_tokens_verify_eligible(self, sync: Literal[True], body: PostTokensVerifyEligibleBody) -> PostTokensVerifyEligibleResponse: ...
    @overload
    def _post_tokens_verify_eligible(self, sync: Literal[False], body: PostTokensVerifyEligibleBody) -> Coroutine[None, None, PostTokensVerifyEligibleResponse]: ...
    def _post_tokens_verify_eligible(self, sync: bool, body: PostTokensVerifyEligibleBody) -> PostTokensVerifyEligibleResponse | Coroutine[None, None, PostTokensVerifyEligibleResponse]:
        """
        This function refers to the **Post Tokens Verify Eligible** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            body: body containing the mint address to evaluate.

        Returns:
            PostTokensVerifyEligibleResponse: eligibility check result with detailed criteria.
        """
        url = self.url_api + "/v1/tokens/verify/eligible"
        return self.api_return_model(sync, RequestType.POST.value, url, PostTokensVerifyEligibleResponse, json=body.model_dump())

    # -------------------------------------------------------------------------
    # Post tokens verify (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_tokens_verify(self, sync: Literal[True], body: PostTokensVerifyBody) -> PostTokensVerifyResponse: ...
    @overload
    def _post_tokens_verify(self, sync: Literal[False], body: PostTokensVerifyBody) -> Coroutine[None, None, PostTokensVerifyResponse]: ...
    def _post_tokens_verify(self, sync: bool, body: PostTokensVerifyBody) -> PostTokensVerifyResponse | Coroutine[None, None, PostTokensVerifyResponse]:
        """
        This function refers to the **Post Tokens Verify** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            body: verification submission body with mint, payer, signature, and metadata.

        Returns:
            PostTokensVerifyResponse: confirmation that the verification was submitted.
        """
        url = self.url_api + "/v1/tokens/verify"
        return self.api_return_model(sync, RequestType.POST.value, url, PostTokensVerifyResponse, json=body.model_dump(by_alias=True))

    # -------------------------------------------------------------------------
    # Post tokens verify transaction (auth required)
    # -------------------------------------------------------------------------

    @overload
    def _post_tokens_verify_transaction(self, sync: Literal[True], body: PostTokensVerifyTransactionBody) -> PostTokensVerifyTransactionResponse: ...
    @overload
    def _post_tokens_verify_transaction(self, sync: Literal[False], body: PostTokensVerifyTransactionBody) -> Coroutine[None, None, PostTokensVerifyTransactionResponse]: ...
    def _post_tokens_verify_transaction(self, sync: bool, body: PostTokensVerifyTransactionBody) -> PostTokensVerifyTransactionResponse | Coroutine[None, None, PostTokensVerifyTransactionResponse]:
        """
        This function refers to the **Post Tokens Verify Transaction** API endpoint.

        Requires authentication.

        Parameters:
            sync: if True run synchronously, else return a coroutine.
            body: body containing mint, payer, data payload, and priority fee.

        Returns:
            PostTokensVerifyTransactionResponse: serialised transaction for on-chain submission.
        """
        url = self.url_api + "/v1/tokens/verify/transaction"
        return self.api_return_model(sync, RequestType.POST.value, url, PostTokensVerifyTransactionResponse, json=body.model_dump())
