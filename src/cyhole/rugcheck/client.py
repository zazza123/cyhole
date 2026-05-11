from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ..core.client import APIClient, AsyncAPIClient
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

if TYPE_CHECKING:
    from ..rugcheck.interaction import Rugcheck


class RugcheckClient(APIClient):
    """Client for synchronous API calls for `Rugcheck` interaction."""

    def __init__(self, interaction: Rugcheck, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Rugcheck = self._interaction

    def get_ping(self) -> GetPingResponse:
        """
        Call the Rugcheck's GET **[Ping](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_ping`][cyhole.rugcheck.interaction.Rugcheck._get_ping].
        """
        return self._interaction._get_ping(True)

    def get_maintenance(self) -> GetMaintenanceResponse:
        """
        Call the Rugcheck's GET **[Maintenance](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_maintenance`][cyhole.rugcheck.interaction.Rugcheck._get_maintenance].
        """
        return self._interaction._get_maintenance(True)

    def get_leaderboard(self, page: int = 0, limit: int = 50) -> GetLeaderboardResponse:
        """
        Call the Rugcheck's GET **[Leaderboard](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_leaderboard`][cyhole.rugcheck.interaction.Rugcheck._get_leaderboard].
        """
        return self._interaction._get_leaderboard(True, page=page, limit=limit)

    def get_token_report(self, mint: str, refresh: bool | None = None) -> GetTokenReportResponse:
        """
        Call the Rugcheck's GET **[Get Token Report](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_report`][cyhole.rugcheck.interaction.Rugcheck._get_token_report].
        """
        return self._interaction._get_token_report(True, mint=mint, refresh=refresh)

    def get_token_report_summary(self, mint: str, cache_only: str | None = None, refresh: bool | None = None) -> GetTokenReportSummaryResponse:
        """
        Call the Rugcheck's GET **[Get Token Report Summary](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_report_summary`][cyhole.rugcheck.interaction.Rugcheck._get_token_report_summary].
        """
        return self._interaction._get_token_report_summary(True, mint=mint, cache_only=cache_only, refresh=refresh)

    def get_token_metadata(self, mint: str) -> GetTokenMetadataResponse:
        """
        Call the Rugcheck's GET **[Get Token Metadata](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_metadata`][cyhole.rugcheck.interaction.Rugcheck._get_token_metadata].
        """
        return self._interaction._get_token_metadata(True, mint=mint)

    def get_token_votes(self, mint: str) -> GetTokenVotesResponse:
        """
        Call the Rugcheck's GET **[Get Token Votes](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_votes`][cyhole.rugcheck.interaction.Rugcheck._get_token_votes].
        """
        return self._interaction._get_token_votes(True, mint=mint)

    def get_token_insiders_graph(self, mint: str) -> GetTokenInsidersGraphResponse:
        """
        Call the Rugcheck's GET **[Get Token Insiders Graph](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_insiders_graph`][cyhole.rugcheck.interaction.Rugcheck._get_token_insiders_graph].
        """
        return self._interaction._get_token_insiders_graph(True, mint=mint)

    def get_token_insiders_networks(self, mint: str) -> GetTokenInsidersNetworksResponse:
        """
        Call the Rugcheck's GET **[Get Token Insiders Networks](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_insiders_networks`][cyhole.rugcheck.interaction.Rugcheck._get_token_insiders_networks].
        """
        return self._interaction._get_token_insiders_networks(True, mint=mint)

    def get_stats_new_tokens(self) -> GetStatsNewTokensResponse:
        """
        Call the Rugcheck's GET **[Get Stats New Tokens](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_new_tokens`][cyhole.rugcheck.interaction.Rugcheck._get_stats_new_tokens].
        """
        return self._interaction._get_stats_new_tokens(True)

    def get_stats_recent(self) -> GetStatsRecentResponse:
        """
        Call the Rugcheck's GET **[Get Stats Recent](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_recent`][cyhole.rugcheck.interaction.Rugcheck._get_stats_recent].
        """
        return self._interaction._get_stats_recent(True)

    def get_stats_trending(self) -> GetStatsTrendingResponse:
        """
        Call the Rugcheck's GET **[Get Stats Trending](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_trending`][cyhole.rugcheck.interaction.Rugcheck._get_stats_trending].
        """
        return self._interaction._get_stats_trending(True)

    def get_stats_verified(self) -> GetStatsVerifiedResponse:
        """
        Call the Rugcheck's GET **[Get Stats Verified](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_verified`][cyhole.rugcheck.interaction.Rugcheck._get_stats_verified].
        """
        return self._interaction._get_stats_verified(True)

    def get_stats_analytics(self, window: RugcheckAnalyticsWindow = RugcheckAnalyticsWindow.D7) -> GetStatsAnalyticsResponse:
        """
        Call the Rugcheck's GET **[Get Stats Analytics](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_analytics`][cyhole.rugcheck.interaction.Rugcheck._get_stats_analytics].
        """
        return self._interaction._get_stats_analytics(True, window=window)

    def get_stats_rugs_ticker(self, limit: int = 10) -> GetStatsRugsTickerResponse:
        """
        Call the Rugcheck's GET **[Get Stats Rugs Ticker](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_rugs_ticker`][cyhole.rugcheck.interaction.Rugcheck._get_stats_rugs_ticker].
        """
        return self._interaction._get_stats_rugs_ticker(True, limit=limit)

    def get_creator(self, wallet: str) -> GetCreatorResponse:
        """
        Call the Rugcheck's GET **[Get Creator](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_creator`][cyhole.rugcheck.interaction.Rugcheck._get_creator].
        """
        return self._interaction._get_creator(True, wallet=wallet)

    def get_domains(self, page: int | None = None, limit: int | None = None, verified: bool | None = None) -> GetDomainsResponse:
        """
        Call the Rugcheck's GET **[Get Domains](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_domains`][cyhole.rugcheck.interaction.Rugcheck._get_domains].
        """
        return self._interaction._get_domains(True, page=page, limit=limit, verified=verified)

    def get_domain_lookup(self, domain_id: str) -> GetDomainLookupResponse:
        """
        Call the Rugcheck's GET **[Get Domain Lookup](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_domain_lookup`][cyhole.rugcheck.interaction.Rugcheck._get_domain_lookup].
        """
        return self._interaction._get_domain_lookup(True, domain_id=domain_id)

    def post_token_report(self, mint: str) -> PostTokenReportResponse:
        """
        Call the Rugcheck's POST **[Post Token Report](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_token_report`][cyhole.rugcheck.interaction.Rugcheck._post_token_report].
        """
        return self._interaction._post_token_report(True, mint=mint)

    def post_token_vote(self, body: PostTokenVoteBody) -> PostTokenVoteResponse:
        """
        Call the Rugcheck's POST **[Post Token Vote](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_token_vote`][cyhole.rugcheck.interaction.Rugcheck._post_token_vote].
        """
        return self._interaction._post_token_vote(True, body=body)

    def get_token_lockers(self, mint: str) -> GetTokenLockersResponse:
        """
        Call the Rugcheck's GET **[Get Token Lockers](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_lockers`][cyhole.rugcheck.interaction.Rugcheck._get_token_lockers].
        """
        return self._interaction._get_token_lockers(True, mint=mint)

    def get_token_lockers_flux(self, mint: str) -> GetTokenLockersFluxResponse:
        """
        Call the Rugcheck's GET **[Get Token Lockers Flux](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_lockers_flux`][cyhole.rugcheck.interaction.Rugcheck._get_token_lockers_flux].
        """
        return self._interaction._get_token_lockers_flux(True, mint=mint)

    def post_bulk_tokens_report(self, body: PostBulkTokensBody) -> PostBulkTokensReportResponse:
        """
        Call the Rugcheck's POST **[Post Bulk Tokens Report](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_bulk_tokens_report`][cyhole.rugcheck.interaction.Rugcheck._post_bulk_tokens_report].
        """
        return self._interaction._post_bulk_tokens_report(True, body=body)

    def post_bulk_tokens_summary(self, body: PostBulkTokensBody) -> PostBulkTokensSummaryResponse:
        """
        Call the Rugcheck's POST **[Post Bulk Tokens Summary](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_bulk_tokens_summary`][cyhole.rugcheck.interaction.Rugcheck._post_bulk_tokens_summary].
        """
        return self._interaction._post_bulk_tokens_summary(True, body=body)

    def post_tokens_verify_eligible(self, body: PostTokensVerifyEligibleBody) -> PostTokensVerifyEligibleResponse:
        """
        Call the Rugcheck's POST **[Post Tokens Verify Eligible](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_tokens_verify_eligible`][cyhole.rugcheck.interaction.Rugcheck._post_tokens_verify_eligible].
        """
        return self._interaction._post_tokens_verify_eligible(True, body=body)

    def post_tokens_verify(self, body: PostTokensVerifyBody) -> PostTokensVerifyResponse:
        """
        Call the Rugcheck's POST **[Post Tokens Verify](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_tokens_verify`][cyhole.rugcheck.interaction.Rugcheck._post_tokens_verify].
        """
        return self._interaction._post_tokens_verify(True, body=body)

    def post_tokens_verify_transaction(self, body: PostTokensVerifyTransactionBody) -> PostTokensVerifyTransactionResponse:
        """
        Call the Rugcheck's POST **[Post Tokens Verify Transaction](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for synchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_tokens_verify_transaction`][cyhole.rugcheck.interaction.Rugcheck._post_tokens_verify_transaction].
        """
        return self._interaction._post_tokens_verify_transaction(True, body=body)


class RugcheckAsyncClient(AsyncAPIClient):
    """Client for asynchronous API calls for `Rugcheck` interaction."""

    def __init__(self, interaction: Rugcheck, headers: Any | None = None) -> None:
        super().__init__(interaction, headers)
        self._interaction: Rugcheck = self._interaction

    async def get_ping(self) -> GetPingResponse:
        """
        Call the Rugcheck's GET **[Ping](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_ping`][cyhole.rugcheck.interaction.Rugcheck._get_ping].
        """
        return await self._interaction._get_ping(False)

    async def get_maintenance(self) -> GetMaintenanceResponse:
        """
        Call the Rugcheck's GET **[Maintenance](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_maintenance`][cyhole.rugcheck.interaction.Rugcheck._get_maintenance].
        """
        return await self._interaction._get_maintenance(False)

    async def get_leaderboard(self, page: int = 0, limit: int = 50) -> GetLeaderboardResponse:
        """
        Call the Rugcheck's GET **[Leaderboard](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_leaderboard`][cyhole.rugcheck.interaction.Rugcheck._get_leaderboard].
        """
        return await self._interaction._get_leaderboard(False, page=page, limit=limit)

    async def get_token_report(self, mint: str, refresh: bool | None = None) -> GetTokenReportResponse:
        """
        Call the Rugcheck's GET **[Get Token Report](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_report`][cyhole.rugcheck.interaction.Rugcheck._get_token_report].
        """
        return await self._interaction._get_token_report(False, mint=mint, refresh=refresh)

    async def get_token_report_summary(self, mint: str, cache_only: str | None = None, refresh: bool | None = None) -> GetTokenReportSummaryResponse:
        """
        Call the Rugcheck's GET **[Get Token Report Summary](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_report_summary`][cyhole.rugcheck.interaction.Rugcheck._get_token_report_summary].
        """
        return await self._interaction._get_token_report_summary(False, mint=mint, cache_only=cache_only, refresh=refresh)

    async def get_token_metadata(self, mint: str) -> GetTokenMetadataResponse:
        """
        Call the Rugcheck's GET **[Get Token Metadata](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_metadata`][cyhole.rugcheck.interaction.Rugcheck._get_token_metadata].
        """
        return await self._interaction._get_token_metadata(False, mint=mint)

    async def get_token_votes(self, mint: str) -> GetTokenVotesResponse:
        """
        Call the Rugcheck's GET **[Get Token Votes](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_votes`][cyhole.rugcheck.interaction.Rugcheck._get_token_votes].
        """
        return await self._interaction._get_token_votes(False, mint=mint)

    async def get_token_insiders_graph(self, mint: str) -> GetTokenInsidersGraphResponse:
        """
        Call the Rugcheck's GET **[Get Token Insiders Graph](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_insiders_graph`][cyhole.rugcheck.interaction.Rugcheck._get_token_insiders_graph].
        """
        return await self._interaction._get_token_insiders_graph(False, mint=mint)

    async def get_token_insiders_networks(self, mint: str) -> GetTokenInsidersNetworksResponse:
        """
        Call the Rugcheck's GET **[Get Token Insiders Networks](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_insiders_networks`][cyhole.rugcheck.interaction.Rugcheck._get_token_insiders_networks].
        """
        return await self._interaction._get_token_insiders_networks(False, mint=mint)

    async def get_stats_new_tokens(self) -> GetStatsNewTokensResponse:
        """
        Call the Rugcheck's GET **[Get Stats New Tokens](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_new_tokens`][cyhole.rugcheck.interaction.Rugcheck._get_stats_new_tokens].
        """
        return await self._interaction._get_stats_new_tokens(False)

    async def get_stats_recent(self) -> GetStatsRecentResponse:
        """
        Call the Rugcheck's GET **[Get Stats Recent](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_recent`][cyhole.rugcheck.interaction.Rugcheck._get_stats_recent].
        """
        return await self._interaction._get_stats_recent(False)

    async def get_stats_trending(self) -> GetStatsTrendingResponse:
        """
        Call the Rugcheck's GET **[Get Stats Trending](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_trending`][cyhole.rugcheck.interaction.Rugcheck._get_stats_trending].
        """
        return await self._interaction._get_stats_trending(False)

    async def get_stats_verified(self) -> GetStatsVerifiedResponse:
        """
        Call the Rugcheck's GET **[Get Stats Verified](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_verified`][cyhole.rugcheck.interaction.Rugcheck._get_stats_verified].
        """
        return await self._interaction._get_stats_verified(False)

    async def get_stats_analytics(self, window: RugcheckAnalyticsWindow = RugcheckAnalyticsWindow.D7) -> GetStatsAnalyticsResponse:
        """
        Call the Rugcheck's GET **[Get Stats Analytics](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_analytics`][cyhole.rugcheck.interaction.Rugcheck._get_stats_analytics].
        """
        return await self._interaction._get_stats_analytics(False, window=window)

    async def get_stats_rugs_ticker(self, limit: int = 10) -> GetStatsRugsTickerResponse:
        """
        Call the Rugcheck's GET **[Get Stats Rugs Ticker](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_stats_rugs_ticker`][cyhole.rugcheck.interaction.Rugcheck._get_stats_rugs_ticker].
        """
        return await self._interaction._get_stats_rugs_ticker(False, limit=limit)

    async def get_creator(self, wallet: str) -> GetCreatorResponse:
        """
        Call the Rugcheck's GET **[Get Creator](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_creator`][cyhole.rugcheck.interaction.Rugcheck._get_creator].
        """
        return await self._interaction._get_creator(False, wallet=wallet)

    async def get_domains(self, page: int | None = None, limit: int | None = None, verified: bool | None = None) -> GetDomainsResponse:
        """
        Call the Rugcheck's GET **[Get Domains](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_domains`][cyhole.rugcheck.interaction.Rugcheck._get_domains].
        """
        return await self._interaction._get_domains(False, page=page, limit=limit, verified=verified)

    async def get_domain_lookup(self, domain_id: str) -> GetDomainLookupResponse:
        """
        Call the Rugcheck's GET **[Get Domain Lookup](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_domain_lookup`][cyhole.rugcheck.interaction.Rugcheck._get_domain_lookup].
        """
        return await self._interaction._get_domain_lookup(False, domain_id=domain_id)

    async def post_token_report(self, mint: str) -> PostTokenReportResponse:
        """
        Call the Rugcheck's POST **[Post Token Report](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_token_report`][cyhole.rugcheck.interaction.Rugcheck._post_token_report].
        """
        return await self._interaction._post_token_report(False, mint=mint)

    async def post_token_vote(self, body: PostTokenVoteBody) -> PostTokenVoteResponse:
        """
        Call the Rugcheck's POST **[Post Token Vote](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_token_vote`][cyhole.rugcheck.interaction.Rugcheck._post_token_vote].
        """
        return await self._interaction._post_token_vote(False, body=body)

    async def get_token_lockers(self, mint: str) -> GetTokenLockersResponse:
        """
        Call the Rugcheck's GET **[Get Token Lockers](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_lockers`][cyhole.rugcheck.interaction.Rugcheck._get_token_lockers].
        """
        return await self._interaction._get_token_lockers(False, mint=mint)

    async def get_token_lockers_flux(self, mint: str) -> GetTokenLockersFluxResponse:
        """
        Call the Rugcheck's GET **[Get Token Lockers Flux](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._get_token_lockers_flux`][cyhole.rugcheck.interaction.Rugcheck._get_token_lockers_flux].
        """
        return await self._interaction._get_token_lockers_flux(False, mint=mint)

    async def post_bulk_tokens_report(self, body: PostBulkTokensBody) -> PostBulkTokensReportResponse:
        """
        Call the Rugcheck's POST **[Post Bulk Tokens Report](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_bulk_tokens_report`][cyhole.rugcheck.interaction.Rugcheck._post_bulk_tokens_report].
        """
        return await self._interaction._post_bulk_tokens_report(False, body=body)

    async def post_bulk_tokens_summary(self, body: PostBulkTokensBody) -> PostBulkTokensSummaryResponse:
        """
        Call the Rugcheck's POST **[Post Bulk Tokens Summary](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_bulk_tokens_summary`][cyhole.rugcheck.interaction.Rugcheck._post_bulk_tokens_summary].
        """
        return await self._interaction._post_bulk_tokens_summary(False, body=body)

    async def post_tokens_verify_eligible(self, body: PostTokensVerifyEligibleBody) -> PostTokensVerifyEligibleResponse:
        """
        Call the Rugcheck's POST **[Post Tokens Verify Eligible](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_tokens_verify_eligible`][cyhole.rugcheck.interaction.Rugcheck._post_tokens_verify_eligible].
        """
        return await self._interaction._post_tokens_verify_eligible(False, body=body)

    async def post_tokens_verify(self, body: PostTokensVerifyBody) -> PostTokensVerifyResponse:
        """
        Call the Rugcheck's POST **[Post Tokens Verify](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_tokens_verify`][cyhole.rugcheck.interaction.Rugcheck._post_tokens_verify].
        """
        return await self._interaction._post_tokens_verify(False, body=body)

    async def post_tokens_verify_transaction(self, body: PostTokensVerifyTransactionBody) -> PostTokensVerifyTransactionResponse:
        """
        Call the Rugcheck's POST **[Post Tokens Verify Transaction](https://api.rugcheck.xyz/swagger/index.html)** API endpoint for asynchronous logic.
        All the API endpoint details are available on [`Rugcheck._post_tokens_verify_transaction`][cyhole.rugcheck.interaction.Rugcheck._post_tokens_verify_transaction].
        """
        return await self._interaction._post_tokens_verify_transaction(False, body=body)
