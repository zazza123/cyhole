import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from cyhole.rugcheck import Rugcheck
from cyhole.rugcheck.param import RugcheckAnalyticsWindow
from cyhole.rugcheck.schema import (
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

from .config import load_config, MockerManager

config = load_config()

mock_path = Path(config.mock_folder) / config.rugcheck.mock_folder
mock_path.mkdir(parents=True, exist_ok=True)

BONK_MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
TEST_WALLET = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
TEST_DOMAIN = "ageur.token"


class TestRugcheck:
    """Class grouping all unit tests for Rugcheck interaction."""

    rugcheck = Rugcheck()
    mocker = MockerManager(mock_path)

    # -------------------------------------------------------------------------
    # Ping
    # -------------------------------------------------------------------------

    def test_get_ping_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Ping" — synchronous logic.

        Mock Response File: getPing_default.json
        """
        mock_file_name = "getPing_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPingResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_ping()
        assert isinstance(response, GetPingResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_ping_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Ping" — asynchronous logic.

        Mock Response File: getPing_default.json
        """
        mock_file_name = "getPing_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetPingResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_ping()
        assert isinstance(response, GetPingResponse)

    # -------------------------------------------------------------------------
    # Maintenance
    # -------------------------------------------------------------------------

    def test_get_maintenance_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Maintenance" — synchronous logic.

        Mock Response File: getMaintenance_default.json
        """
        mock_file_name = "getMaintenance_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetMaintenanceResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_maintenance()
        assert isinstance(response, GetMaintenanceResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_maintenance_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Maintenance" — asynchronous logic.

        Mock Response File: getMaintenance_default.json
        """
        mock_file_name = "getMaintenance_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetMaintenanceResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_maintenance()
        assert isinstance(response, GetMaintenanceResponse)

    # -------------------------------------------------------------------------
    # Leaderboard
    # -------------------------------------------------------------------------

    def test_get_leaderboard_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Leaderboard" — synchronous logic.

        Mock Response File: getLeaderboard_default.json
        """
        mock_file_name = "getLeaderboard_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLeaderboardResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_leaderboard(page=0, limit=2)
        assert isinstance(response, GetLeaderboardResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_leaderboard_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Leaderboard" — asynchronous logic.

        Mock Response File: getLeaderboard_default.json
        """
        mock_file_name = "getLeaderboard_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetLeaderboardResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_leaderboard(page=0, limit=2)
        assert isinstance(response, GetLeaderboardResponse)

    # -------------------------------------------------------------------------
    # Token report
    # -------------------------------------------------------------------------

    def test_get_token_report_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Report" — synchronous logic.

        Mock Response File: getTokenReport_default.json
        """
        mock_file_name = "getTokenReport_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenReportResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_report(BONK_MINT)
        assert isinstance(response, GetTokenReportResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_report_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Report" — asynchronous logic.

        Mock Response File: getTokenReport_default.json
        """
        mock_file_name = "getTokenReport_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenReportResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_report(BONK_MINT)
        assert isinstance(response, GetTokenReportResponse)

    # -------------------------------------------------------------------------
    # Token report summary
    # -------------------------------------------------------------------------

    def test_get_token_report_summary_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Report Summary" — synchronous logic.

        Mock Response File: getTokenReportSummary_default.json
        """
        mock_file_name = "getTokenReportSummary_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenReportSummaryResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_report_summary(BONK_MINT)
        assert isinstance(response, GetTokenReportSummaryResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_report_summary_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Report Summary" — asynchronous logic.

        Mock Response File: getTokenReportSummary_default.json
        """
        mock_file_name = "getTokenReportSummary_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenReportSummaryResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_report_summary(BONK_MINT)
        assert isinstance(response, GetTokenReportSummaryResponse)

    # -------------------------------------------------------------------------
    # Token metadata
    # -------------------------------------------------------------------------

    def test_get_token_metadata_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Metadata" — synchronous logic.

        Mock Response File: getTokenMetadata_default.json
        """
        mock_file_name = "getTokenMetadata_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMetadataResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_metadata(BONK_MINT)
        assert isinstance(response, GetTokenMetadataResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_metadata_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Metadata" — asynchronous logic.

        Mock Response File: getTokenMetadata_default.json
        """
        mock_file_name = "getTokenMetadata_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenMetadataResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_metadata(BONK_MINT)
        assert isinstance(response, GetTokenMetadataResponse)

    # -------------------------------------------------------------------------
    # Token votes
    # -------------------------------------------------------------------------

    def test_get_token_votes_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Votes" — synchronous logic.

        Mock Response File: getTokenVotes_default.json
        """
        mock_file_name = "getTokenVotes_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenVotesResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_votes(BONK_MINT)
        assert isinstance(response, GetTokenVotesResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_votes_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Votes" — asynchronous logic.

        Mock Response File: getTokenVotes_default.json
        """
        mock_file_name = "getTokenVotes_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenVotesResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_votes(BONK_MINT)
        assert isinstance(response, GetTokenVotesResponse)

    # -------------------------------------------------------------------------
    # Token insiders graph
    # -------------------------------------------------------------------------

    def test_get_token_insiders_graph_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Insiders Graph" — synchronous logic.

        Mock Response File: getTokenInsidersGraph_default.json
        """
        mock_file_name = "getTokenInsidersGraph_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInsidersGraphResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_insiders_graph(BONK_MINT)
        assert isinstance(response, GetTokenInsidersGraphResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_insiders_graph_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Insiders Graph" — asynchronous logic.

        Mock Response File: getTokenInsidersGraph_default.json
        """
        mock_file_name = "getTokenInsidersGraph_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInsidersGraphResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_insiders_graph(BONK_MINT)
        assert isinstance(response, GetTokenInsidersGraphResponse)

    # -------------------------------------------------------------------------
    # Token insiders networks
    # -------------------------------------------------------------------------

    def test_get_token_insiders_networks_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Insiders Networks" — synchronous logic.

        Mock Response File: getTokenInsidersNetworks_default.json
        """
        mock_file_name = "getTokenInsidersNetworks_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInsidersNetworksResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_insiders_networks(BONK_MINT)
        assert isinstance(response, GetTokenInsidersNetworksResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_token_insiders_networks_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Insiders Networks" — asynchronous logic.

        Mock Response File: getTokenInsidersNetworks_default.json
        """
        mock_file_name = "getTokenInsidersNetworks_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenInsidersNetworksResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_insiders_networks(BONK_MINT)
        assert isinstance(response, GetTokenInsidersNetworksResponse)

    # -------------------------------------------------------------------------
    # Stats: new tokens
    # -------------------------------------------------------------------------

    def test_get_stats_new_tokens_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats New Tokens" — synchronous logic.

        Mock Response File: getStatsNewTokens_default.json
        """
        mock_file_name = "getStatsNewTokens_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsNewTokensResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_stats_new_tokens()
        assert isinstance(response, GetStatsNewTokensResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_stats_new_tokens_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats New Tokens" — asynchronous logic.

        Mock Response File: getStatsNewTokens_default.json
        """
        mock_file_name = "getStatsNewTokens_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsNewTokensResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_stats_new_tokens()
        assert isinstance(response, GetStatsNewTokensResponse)

    # -------------------------------------------------------------------------
    # Stats: recent
    # -------------------------------------------------------------------------

    def test_get_stats_recent_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Recent" — synchronous logic.

        Mock Response File: getStatsRecent_default.json
        """
        mock_file_name = "getStatsRecent_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsRecentResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_stats_recent()
        assert isinstance(response, GetStatsRecentResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_stats_recent_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Recent" — asynchronous logic.

        Mock Response File: getStatsRecent_default.json
        """
        mock_file_name = "getStatsRecent_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsRecentResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_stats_recent()
        assert isinstance(response, GetStatsRecentResponse)

    # -------------------------------------------------------------------------
    # Stats: trending
    # -------------------------------------------------------------------------

    def test_get_stats_trending_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Trending" — synchronous logic.

        Mock Response File: getStatsTrending_default.json
        """
        mock_file_name = "getStatsTrending_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsTrendingResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_stats_trending()
        assert isinstance(response, GetStatsTrendingResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_stats_trending_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Trending" — asynchronous logic.

        Mock Response File: getStatsTrending_default.json
        """
        mock_file_name = "getStatsTrending_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsTrendingResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_stats_trending()
        assert isinstance(response, GetStatsTrendingResponse)

    # -------------------------------------------------------------------------
    # Stats: verified
    # -------------------------------------------------------------------------

    def test_get_stats_verified_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Verified" — synchronous logic.

        Mock Response File: getStatsVerified_default.json
        """
        mock_file_name = "getStatsVerified_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsVerifiedResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_stats_verified()
        assert isinstance(response, GetStatsVerifiedResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_stats_verified_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Verified" — asynchronous logic.

        Mock Response File: getStatsVerified_default.json
        """
        mock_file_name = "getStatsVerified_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsVerifiedResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_stats_verified()
        assert isinstance(response, GetStatsVerifiedResponse)

    # -------------------------------------------------------------------------
    # Stats: analytics
    # -------------------------------------------------------------------------

    def test_get_stats_analytics_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Analytics" — synchronous logic.

        Mock Response File: getStatsAnalytics_default.json
        """
        mock_file_name = "getStatsAnalytics_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsAnalyticsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_stats_analytics(RugcheckAnalyticsWindow.D7)
        assert isinstance(response, GetStatsAnalyticsResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_stats_analytics_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Analytics" — asynchronous logic.

        Mock Response File: getStatsAnalytics_default.json
        """
        mock_file_name = "getStatsAnalytics_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsAnalyticsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_stats_analytics(RugcheckAnalyticsWindow.D7)
        assert isinstance(response, GetStatsAnalyticsResponse)

    # -------------------------------------------------------------------------
    # Stats: rugs ticker
    # -------------------------------------------------------------------------

    def test_get_stats_rugs_ticker_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Rugs Ticker" — synchronous logic.

        Mock Response File: getStatsRugsTicker_default.json
        """
        mock_file_name = "getStatsRugsTicker_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsRugsTickerResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_stats_rugs_ticker(limit=5)
        assert isinstance(response, GetStatsRugsTickerResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_stats_rugs_ticker_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Stats Rugs Ticker" — asynchronous logic.

        Mock Response File: getStatsRugsTicker_default.json
        """
        mock_file_name = "getStatsRugsTicker_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetStatsRugsTickerResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_stats_rugs_ticker(limit=5)
        assert isinstance(response, GetStatsRugsTickerResponse)

    # -------------------------------------------------------------------------
    # Creator
    # -------------------------------------------------------------------------

    def test_get_creator_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Creator" — synchronous logic.

        Mock Response File: getCreator_default.json
        """
        mock_file_name = "getCreator_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetCreatorResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_creator(TEST_WALLET)
        assert isinstance(response, GetCreatorResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_creator_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Creator" — asynchronous logic.

        Mock Response File: getCreator_default.json
        """
        mock_file_name = "getCreator_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetCreatorResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_creator(TEST_WALLET)
        assert isinstance(response, GetCreatorResponse)

    # -------------------------------------------------------------------------
    # Domains
    # -------------------------------------------------------------------------

    def test_get_domains_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Domains" — synchronous logic.

        Mock Response File: getDomains_default.json
        """
        mock_file_name = "getDomains_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetDomainsResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_domains(limit=2)
        assert isinstance(response, GetDomainsResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_domains_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Domains" — asynchronous logic.

        Mock Response File: getDomains_default.json
        """
        mock_file_name = "getDomains_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetDomainsResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_domains(limit=2)
        assert isinstance(response, GetDomainsResponse)

    # -------------------------------------------------------------------------
    # Domain lookup
    # -------------------------------------------------------------------------

    def test_get_domain_lookup_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Domain Lookup" — synchronous logic.

        Mock Response File: getDomainLookup_default.json
        """
        mock_file_name = "getDomainLookup_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetDomainLookupResponse)
            mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_domain_lookup(TEST_DOMAIN)
        assert isinstance(response, GetDomainLookupResponse)

        if config.mock_file_overwrite and not config.rugcheck.mock_response:
            self.mocker.store_mock_model(mock_file_name, response)

    @pytest.mark.asyncio
    async def test_get_domain_lookup_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Domain Lookup" — asynchronous logic.

        Mock Response File: getDomainLookup_default.json
        """
        mock_file_name = "getDomainLookup_default"
        if config.mock_response or config.rugcheck.mock_response:
            mock_response = self.mocker.load_mock_response(mock_file_name, GetDomainLookupResponse)
            mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_domain_lookup(TEST_DOMAIN)
        assert isinstance(response, GetDomainLookupResponse)

    # -------------------------------------------------------------------------
    # Post token report (auth required)
    # -------------------------------------------------------------------------

    def test_post_token_report_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Token Report" — synchronous logic.

        Mock Response File: postTokenReport_default.json
        """
        mock_file_name = "postTokenReport_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenReportResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.post_token_report(BONK_MINT)
        assert isinstance(response, PostTokenReportResponse)

    @pytest.mark.asyncio
    async def test_post_token_report_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Token Report" — asynchronous logic.

        Mock Response File: postTokenReport_default.json
        """
        mock_file_name = "postTokenReport_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenReportResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.post_token_report(BONK_MINT)
        assert isinstance(response, PostTokenReportResponse)

    # -------------------------------------------------------------------------
    # Post token vote (auth required)
    # -------------------------------------------------------------------------

    def test_post_token_vote_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Token Vote" — synchronous logic.

        Mock Response File: postTokenVote_default.json
        """
        mock_file_name = "postTokenVote_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenVoteResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        body = PostTokenVoteBody(mint=BONK_MINT, side=True)
        response = self.rugcheck.client.post_token_vote(body)
        assert isinstance(response, PostTokenVoteResponse)

    @pytest.mark.asyncio
    async def test_post_token_vote_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Token Vote" — asynchronous logic.

        Mock Response File: postTokenVote_default.json
        """
        mock_file_name = "postTokenVote_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokenVoteResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        body = PostTokenVoteBody(mint=BONK_MINT, side=True)
        async with self.rugcheck.async_client as client:
            response = await client.post_token_vote(body)
        assert isinstance(response, PostTokenVoteResponse)

    # -------------------------------------------------------------------------
    # Get token lockers (auth required)
    # -------------------------------------------------------------------------

    def test_get_token_lockers_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Lockers" — synchronous logic.

        Mock Response File: getTokenLockers_default.json
        """
        mock_file_name = "getTokenLockers_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenLockersResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_lockers(BONK_MINT)
        assert isinstance(response, GetTokenLockersResponse)

    @pytest.mark.asyncio
    async def test_get_token_lockers_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Lockers" — asynchronous logic.

        Mock Response File: getTokenLockers_default.json
        """
        mock_file_name = "getTokenLockers_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenLockersResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_lockers(BONK_MINT)
        assert isinstance(response, GetTokenLockersResponse)

    # -------------------------------------------------------------------------
    # Get token lockers flux (auth required)
    # -------------------------------------------------------------------------

    def test_get_token_lockers_flux_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Lockers Flux" — synchronous logic.

        Mock Response File: getTokenLockersFlux_default.json
        """
        mock_file_name = "getTokenLockersFlux_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenLockersFluxResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        response = self.rugcheck.client.get_token_lockers_flux(BONK_MINT)
        assert isinstance(response, GetTokenLockersFluxResponse)

    @pytest.mark.asyncio
    async def test_get_token_lockers_flux_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Get Token Lockers Flux" — asynchronous logic.

        Mock Response File: getTokenLockersFlux_default.json
        """
        mock_file_name = "getTokenLockersFlux_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, GetTokenLockersFluxResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        async with self.rugcheck.async_client as client:
            response = await client.get_token_lockers_flux(BONK_MINT)
        assert isinstance(response, GetTokenLockersFluxResponse)

    # -------------------------------------------------------------------------
    # Post bulk tokens report (auth required)
    # -------------------------------------------------------------------------

    def test_post_bulk_tokens_report_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Bulk Tokens Report" — synchronous logic.

        Mock Response File: postBulkTokensReport_default.json
        """
        mock_file_name = "postBulkTokensReport_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostBulkTokensReportResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        body = PostBulkTokensBody(tokens=[BONK_MINT], **{"cacheOnly": False})
        response = self.rugcheck.client.post_bulk_tokens_report(body)
        assert isinstance(response, PostBulkTokensReportResponse)

    @pytest.mark.asyncio
    async def test_post_bulk_tokens_report_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Bulk Tokens Report" — asynchronous logic.

        Mock Response File: postBulkTokensReport_default.json
        """
        mock_file_name = "postBulkTokensReport_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostBulkTokensReportResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        body = PostBulkTokensBody(tokens=[BONK_MINT], **{"cacheOnly": False})
        async with self.rugcheck.async_client as client:
            response = await client.post_bulk_tokens_report(body)
        assert isinstance(response, PostBulkTokensReportResponse)

    # -------------------------------------------------------------------------
    # Post bulk tokens summary (auth required)
    # -------------------------------------------------------------------------

    def test_post_bulk_tokens_summary_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Bulk Tokens Summary" — synchronous logic.

        Mock Response File: postBulkTokensSummary_default.json
        """
        mock_file_name = "postBulkTokensSummary_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostBulkTokensSummaryResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        body = PostBulkTokensBody(tokens=[BONK_MINT], **{"cacheOnly": False})
        response = self.rugcheck.client.post_bulk_tokens_summary(body)
        assert isinstance(response, PostBulkTokensSummaryResponse)

    @pytest.mark.asyncio
    async def test_post_bulk_tokens_summary_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Bulk Tokens Summary" — asynchronous logic.

        Mock Response File: postBulkTokensSummary_default.json
        """
        mock_file_name = "postBulkTokensSummary_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostBulkTokensSummaryResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        body = PostBulkTokensBody(tokens=[BONK_MINT], **{"cacheOnly": False})
        async with self.rugcheck.async_client as client:
            response = await client.post_bulk_tokens_summary(body)
        assert isinstance(response, PostBulkTokensSummaryResponse)

    # -------------------------------------------------------------------------
    # Post tokens verify eligible (auth required)
    # -------------------------------------------------------------------------

    def test_post_tokens_verify_eligible_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Tokens Verify Eligible" — synchronous logic.

        Mock Response File: postTokensVerifyEligible_default.json
        """
        mock_file_name = "postTokensVerifyEligible_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokensVerifyEligibleResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        body = PostTokensVerifyEligibleBody(mint=BONK_MINT)
        response = self.rugcheck.client.post_tokens_verify_eligible(body)
        assert isinstance(response, PostTokensVerifyEligibleResponse)

    @pytest.mark.asyncio
    async def test_post_tokens_verify_eligible_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Tokens Verify Eligible" — asynchronous logic.

        Mock Response File: postTokensVerifyEligible_default.json
        """
        mock_file_name = "postTokensVerifyEligible_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokensVerifyEligibleResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        body = PostTokensVerifyEligibleBody(mint=BONK_MINT)
        async with self.rugcheck.async_client as client:
            response = await client.post_tokens_verify_eligible(body)
        assert isinstance(response, PostTokensVerifyEligibleResponse)

    # -------------------------------------------------------------------------
    # Post tokens verify (auth required)
    # -------------------------------------------------------------------------

    def test_post_tokens_verify_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Tokens Verify" — synchronous logic.

        Mock Response File: postTokensVerify_default.json
        """
        mock_file_name = "postTokensVerify_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokensVerifyResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        from cyhole.rugcheck.schema import RugcheckVerifyData
        body = PostTokensVerifyBody(
            mint=BONK_MINT,
            payer=TEST_WALLET,
            signature="sig123",
            data=RugcheckVerifyData(**{
                "solDomain": "bonk.token",
                "description": "Bonk token",
                "termsAccepted": True,
                "dataIntegrityAccepted": True,
                "links": {}
            })
        )
        response = self.rugcheck.client.post_tokens_verify(body)
        assert isinstance(response, PostTokensVerifyResponse)

    @pytest.mark.asyncio
    async def test_post_tokens_verify_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Tokens Verify" — asynchronous logic.

        Mock Response File: postTokensVerify_default.json
        """
        mock_file_name = "postTokensVerify_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokensVerifyResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        from cyhole.rugcheck.schema import RugcheckVerifyData
        body = PostTokensVerifyBody(
            mint=BONK_MINT,
            payer=TEST_WALLET,
            signature="sig123",
            data=RugcheckVerifyData(**{
                "solDomain": "bonk.token",
                "description": "Bonk token",
                "termsAccepted": True,
                "dataIntegrityAccepted": True,
                "links": {}
            })
        )
        async with self.rugcheck.async_client as client:
            response = await client.post_tokens_verify(body)
        assert isinstance(response, PostTokensVerifyResponse)

    # -------------------------------------------------------------------------
    # Post tokens verify transaction (auth required)
    # -------------------------------------------------------------------------

    def test_post_tokens_verify_transaction_sync(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Tokens Verify Transaction" — synchronous logic.

        Mock Response File: postTokensVerifyTransaction_default.json
        """
        mock_file_name = "postTokensVerifyTransaction_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokensVerifyTransactionResponse)
        mocker.patch("cyhole.core.client.APIClient.api", return_value=mock_response)

        body = PostTokensVerifyTransactionBody(
            mint=BONK_MINT,
            payer=TEST_WALLET,
            data={},
            priority_fee=1000
        )
        response = self.rugcheck.client.post_tokens_verify_transaction(body)
        assert isinstance(response, PostTokensVerifyTransactionResponse)

    @pytest.mark.asyncio
    async def test_post_tokens_verify_transaction_async(self, mocker: MockerFixture) -> None:
        """
        Unit Test for endpoint "Post Tokens Verify Transaction" — asynchronous logic.

        Mock Response File: postTokensVerifyTransaction_default.json
        """
        mock_file_name = "postTokensVerifyTransaction_default"
        mock_response = self.mocker.load_mock_response(mock_file_name, PostTokensVerifyTransactionResponse)
        mocker.patch("cyhole.core.client.AsyncAPIClient.api", return_value=mock_response)

        body = PostTokensVerifyTransactionBody(
            mint=BONK_MINT,
            payer=TEST_WALLET,
            data={},
            priority_fee=1000
        )
        async with self.rugcheck.async_client as client:
            response = await client.post_tokens_verify_transaction(body)
        assert isinstance(response, PostTokensVerifyTransactionResponse)
